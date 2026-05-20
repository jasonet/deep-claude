"""Local admin UI routes and APIs."""

from __future__ import annotations

import inspect
import ipaddress
import json
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import httpx
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from config.deepseek_pricing import estimate_cost_cny
from config.settings import Settings
from config.settings import get_settings as get_cached_settings
from core.usage_tracker import aggregate as aggregate_usage
from providers.registry import ProviderRegistry

from .admin_config import (
    FIELD_BY_KEY,
    load_config_response,
    provider_config_status,
    validate_updates,
    write_managed_env,
)
from .admin_urls import local_admin_url

router = APIRouter()

STATIC_DIR = Path(__file__).resolve().parent / "admin_static"
LOCAL_PROVIDER_PATHS = {
    "lmstudio": "/models",
    "llamacpp": "/models",
    "ollama": "/api/tags",
}
DEEPSEEK_BALANCE_URL = "https://api.deepseek.com/user/balance"


def _deepseek_balance_cache_path() -> Path:
    override = os.environ.get("DCC_DEEPSEEK_BALANCE_CACHE")
    if override:
        return Path(override)
    return Path.home() / ".config" / "deep-claude" / "deepseek_balance.json"


def _read_balance_cache() -> dict[str, Any] | None:
    path = _deepseek_balance_cache_path()
    if not path.is_file():
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except OSError, ValueError:
        return None


def _write_balance_cache(payload: dict[str, Any]) -> None:
    path = _deepseek_balance_cache_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False)
    except OSError:
        pass


def _deepseek_balance_history_path() -> Path:
    override = os.environ.get("DCC_DEEPSEEK_BALANCE_HISTORY")
    if override:
        return Path(override)
    return Path.home() / ".config" / "deep-claude" / "deepseek_balance_history.jsonl"


def _append_balance_history(balance_data: dict[str, Any], ts: str) -> None:
    path = _deepseek_balance_history_path()
    row = {"ts": ts, "balance_infos": balance_data.get("balance_infos", [])}
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _read_balance_history() -> list[dict[str, Any]]:
    path = _deepseek_balance_history_path()
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        return []
    return rows


def _parse_balance_ts(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _balance_total_by_currency(entry: dict[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    infos = entry.get("balance_infos")
    if not isinstance(infos, list):
        return out
    for info in infos:
        if not isinstance(info, dict):
            continue
        currency = info.get("currency")
        total = info.get("total_balance")
        if not isinstance(currency, str) or total is None:
            continue
        try:
            out[currency] = float(total)
        except TypeError, ValueError:
            continue
    return out


def _compute_balance_trend(balance_data: dict[str, Any]) -> dict[str, Any]:
    history = _read_balance_history()
    current = _balance_total_by_currency(balance_data)
    if not current:
        return {"by_currency": []}

    now_local = datetime.now().astimezone()
    today_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())

    by_currency: list[dict[str, Any]] = []
    for currency, current_total in current.items():
        today_baseline = _latest_baseline_before(history, currency, today_start)
        week_baseline = _latest_baseline_before(history, currency, week_start)
        by_currency.append(
            {
                "currency": currency,
                "current_total": round(current_total, 4),
                "today_drop": (
                    round(today_baseline - current_total, 4)
                    if today_baseline is not None
                    else None
                ),
                "week_drop": (
                    round(week_baseline - current_total, 4)
                    if week_baseline is not None
                    else None
                ),
            }
        )
    return {"by_currency": by_currency}


def _latest_baseline_before(
    history: list[dict[str, Any]], currency: str, threshold: datetime
) -> float | None:
    best: tuple[datetime, float] | None = None
    for row in history:
        ts = _parse_balance_ts(row.get("ts"))
        if ts is None:
            continue
        if ts.astimezone() >= threshold:
            continue
        totals = _balance_total_by_currency(row)
        if currency not in totals:
            continue
        if best is None or ts > best[0]:
            best = (ts, totals[currency])
    return best[1] if best is not None else None


class AdminConfigPayload(BaseModel):
    """Partial config update submitted by the admin UI."""

    values: dict[str, Any] = Field(default_factory=dict)


def _is_loopback_host(host: str | None) -> bool:
    if host is None:
        return False
    normalized = host.strip().strip("[]").lower()
    if normalized == "localhost":
        return True
    try:
        return ipaddress.ip_address(normalized).is_loopback
    except ValueError:
        return False


def _origin_is_local(origin: str | None) -> bool:
    if not origin:
        return True
    parsed = urlsplit(origin)
    return _is_loopback_host(parsed.hostname)


def require_loopback_admin(request: Request) -> None:
    """Allow admin access only from the local machine."""

    client_host = request.client.host if request.client else None
    if not _is_loopback_host(client_host):
        raise HTTPException(status_code=403, detail="Admin UI is local-only")

    origin = request.headers.get("origin")
    if not _origin_is_local(origin):
        raise HTTPException(status_code=403, detail="Admin UI is local-only")


def _asset_response(filename: str) -> FileResponse:
    path = STATIC_DIR / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Admin asset not found")
    return FileResponse(path)


@router.get("/admin", include_in_schema=False)
async def admin_page(request: Request):
    require_loopback_admin(request)
    return _asset_response("index.html")


@router.get("/admin/assets/{filename}", include_in_schema=False)
async def admin_asset(filename: str, request: Request):
    require_loopback_admin(request)
    if filename not in {"admin.css", "admin.js"}:
        raise HTTPException(status_code=404, detail="Admin asset not found")
    return _asset_response(filename)


@router.get("/admin/api/config")
async def get_admin_config(request: Request):
    require_loopback_admin(request)
    return load_config_response()


@router.post("/admin/api/config/validate")
async def validate_admin_config(payload: AdminConfigPayload, request: Request):
    require_loopback_admin(request)
    return validate_updates(_filtered_values(payload.values))


@router.post("/admin/api/config/apply")
async def apply_admin_config(
    payload: AdminConfigPayload,
    request: Request,
    background_tasks: BackgroundTasks,
):
    require_loopback_admin(request)
    result = write_managed_env(_filtered_values(payload.values))
    if not result["applied"]:
        return result

    get_cached_settings.cache_clear()
    restart = _restart_metadata(result["pending_fields"], request)
    result["restart"] = restart
    if restart["required"] and restart["automatic"]:
        callback = request.app.state.admin_restart_callback
        background_tasks.add_task(_invoke_admin_restart_callback, callback)
        request.app.state.admin_pending_fields = []
        return result

    old_registry = getattr(request.app.state, "provider_registry", None)
    if isinstance(old_registry, ProviderRegistry):
        await old_registry.cleanup()
    request.app.state.provider_registry = ProviderRegistry()
    request.app.state.admin_pending_fields = result["pending_fields"]
    return result


@router.get("/admin/api/status")
async def admin_status(request: Request):
    require_loopback_admin(request)
    settings = get_cached_settings()
    registry = getattr(request.app.state, "provider_registry", None)
    cached_models: dict[str, list[str]] = {}
    if isinstance(registry, ProviderRegistry):
        cached_models = {
            provider_id: sorted(model_ids)
            for provider_id, model_ids in registry.cached_model_ids().items()
        }
    return {
        "status": "running",
        "host": settings.host,
        "port": settings.port,
        "model": settings.model,
        "provider": settings.provider_type,
        "pending_fields": getattr(request.app.state, "admin_pending_fields", []),
        "provider_status": provider_config_status(),
        "cached_models": cached_models,
    }


@router.get("/admin/api/providers/local-status")
async def local_provider_status(request: Request):
    require_loopback_admin(request)
    config = load_config_response()
    values = {field["key"]: field["value"] for field in config["fields"]}
    checks = []
    for provider_id, path in LOCAL_PROVIDER_PATHS.items():
        base_url = _local_provider_url(provider_id, values)
        checks.append(await _check_local_provider(provider_id, base_url, path))
    return {"providers": checks}


@router.post("/admin/api/providers/{provider_id}/test")
async def test_provider(provider_id: str, request: Request):
    require_loopback_admin(request)
    settings = get_cached_settings()
    registry = getattr(request.app.state, "provider_registry", None)
    if not isinstance(registry, ProviderRegistry):
        registry = ProviderRegistry()
        request.app.state.provider_registry = registry
    try:
        provider = registry.get(provider_id, settings)
        infos = await provider.list_model_infos()
    except Exception as exc:
        return {
            "provider_id": provider_id,
            "ok": False,
            "error_type": type(exc).__name__,
        }
    registry.cache_model_infos(provider_id, infos)
    return {
        "provider_id": provider_id,
        "ok": True,
        "models": sorted(info.model_id for info in infos),
    }


@router.get("/admin/api/providers/deepseek/balance")
async def deepseek_balance(request: Request, refresh: bool = False):
    require_loopback_admin(request)
    if not refresh:
        cached = _read_balance_cache()
        if cached is None:
            return {"ok": False, "error": "no_cache", "cached": True}
        trend = _compute_balance_trend(cached.get("balance") or {})
        return {**cached, "cached": True, "trend": trend}

    settings = get_cached_settings()
    api_key = settings.deepseek_api_key.strip()
    if not api_key:
        return {"ok": False, "error": "missing_key", "cached": False}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                DEEPSEEK_BALANCE_URL,
                headers={"Authorization": f"Bearer {api_key}"},
            )
    except Exception as exc:
        return {
            "ok": False,
            "error": "request_failed",
            "error_type": type(exc).__name__,
            "cached": False,
        }
    if response.status_code != 200:
        return {
            "ok": False,
            "error": "upstream_error",
            "status_code": response.status_code,
            "cached": False,
        }
    try:
        data = response.json()
    except ValueError:
        return {
            "ok": False,
            "error": "invalid_response",
            "status_code": response.status_code,
            "cached": False,
        }
    fetched_at = datetime.now(UTC).isoformat()
    _append_balance_history(data, fetched_at)
    payload = {
        "ok": True,
        "balance": data,
        "fetched_at": fetched_at,
    }
    _write_balance_cache(payload)
    trend = _compute_balance_trend(data)
    return {**payload, "cached": False, "trend": trend}


@router.get("/admin/api/providers/deepseek/usage")
async def deepseek_usage(request: Request, period: str = "today"):
    require_loopback_admin(request)
    if period not in ("today", "week", "month"):
        raise HTTPException(status_code=400, detail="period must be today|week|month")
    summary = aggregate_usage(provider="DEEPSEEK", period=period)
    _annotate_costs(summary)
    return summary


def _annotate_costs(summary: dict[str, Any]) -> None:
    total_cost: float | None = None
    for row in summary["by_model"]:
        cost = estimate_cost_cny(
            model=row["model"],
            cache_hit_input_tokens=row["cache_read_input_tokens"],
            cache_miss_input_tokens=max(
                row["input_tokens"] - row["cache_read_input_tokens"], 0
            ),
            output_tokens=row["output_tokens"],
        )
        row["estimated_cost_cny"] = cost
        if cost is not None:
            total_cost = (total_cost or 0.0) + cost
    summary["totals"]["estimated_cost_cny"] = (
        round(total_cost, 4) if total_cost is not None else None
    )


@router.post("/admin/api/server/stop")
async def stop_server(request: Request, background_tasks: BackgroundTasks):
    require_loopback_admin(request)
    callback = getattr(request.app.state, "admin_stop_callback", None)
    if not callable(callback):
        raise HTTPException(
            status_code=501, detail="stop not supported in this runtime"
        )
    background_tasks.add_task(_invoke_admin_restart_callback, callback)
    return {"ok": True, "action": "stopping"}


@router.post("/admin/api/server/restart")
async def restart_server(request: Request, background_tasks: BackgroundTasks):
    require_loopback_admin(request)
    callback = getattr(request.app.state, "admin_restart_callback", None)
    if not callable(callback):
        raise HTTPException(
            status_code=501, detail="restart not supported in this runtime"
        )
    background_tasks.add_task(_invoke_admin_restart_callback, callback)
    return {"ok": True, "action": "restarting"}


@router.post("/admin/api/models/refresh")
async def refresh_models(request: Request):
    require_loopback_admin(request)
    settings = get_cached_settings()
    registry = getattr(request.app.state, "provider_registry", None)
    if not isinstance(registry, ProviderRegistry):
        registry = ProviderRegistry()
        request.app.state.provider_registry = registry
    await registry.refresh_model_list_cache(settings)
    return {
        "cached_models": {
            provider_id: sorted(model_ids)
            for provider_id, model_ids in registry.cached_model_ids().items()
        }
    }


def _filtered_values(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if key in FIELD_BY_KEY}


async def _invoke_admin_restart_callback(callback: Any) -> None:
    result = callback()
    if inspect.isawaitable(result):
        await result


def _restart_metadata(fields: list[str], request: Request) -> dict[str, Any]:
    callback = getattr(request.app.state, "admin_restart_callback", None)
    automatic = bool(fields and callable(callback))
    return {
        "required": bool(fields),
        "automatic": automatic,
        "admin_url": _next_admin_url() if automatic else None,
        "fields": fields,
    }


def _next_admin_url() -> str:
    fields = {
        field["key"]: field["value"] for field in load_config_response()["fields"]
    }
    settings = Settings.model_construct(
        host=fields.get("HOST") or "0.0.0.0",
        port=int(fields.get("PORT") or 8082),
    )
    return local_admin_url(settings)


def _local_provider_url(provider_id: str, values: dict[str, str]) -> str:
    if provider_id == "lmstudio":
        return values.get("LM_STUDIO_BASE_URL", "")
    if provider_id == "llamacpp":
        return values.get("LLAMACPP_BASE_URL", "")
    if provider_id == "ollama":
        return values.get("OLLAMA_BASE_URL", "")
    return ""


async def _check_local_provider(
    provider_id: str, base_url: str, path: str
) -> dict[str, Any]:
    clean_url = base_url.strip().rstrip("/")
    if not clean_url:
        return {
            "provider_id": provider_id,
            "status": "missing_url",
            "label": "Missing URL",
            "base_url": base_url,
        }

    url = f"{clean_url}{path}"
    try:
        async with httpx.AsyncClient(timeout=1.5) as client:
            response = await client.get(url)
        ok = 200 <= response.status_code < 300
        return {
            "provider_id": provider_id,
            "status": "reachable" if ok else "offline",
            "label": "Reachable" if ok else "Offline",
            "base_url": base_url,
            "status_code": response.status_code,
        }
    except Exception as exc:
        return {
            "provider_id": provider_id,
            "status": "offline",
            "label": "Offline",
            "base_url": base_url,
            "error_type": type(exc).__name__,
        }
