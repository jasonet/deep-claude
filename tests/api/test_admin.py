from __future__ import annotations

from datetime import UTC
from pathlib import Path
from unittest.mock import patch

import httpx
import pytest
from fastapi.testclient import TestClient

from api.admin_config import MASKED_SECRET
from api.admin_urls import local_admin_url
from api.app import create_app
from config.settings import Settings, get_settings


def _local_client(app):
    return TestClient(app, client=("127.0.0.1", 50000))


def _set_home(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.chdir(tmp_path)


def _clear_process_config(monkeypatch) -> None:
    for key in (
        "MODEL",
        "NVIDIA_NIM_API_KEY",
        "OPENROUTER_API_KEY",
        "ANTHROPIC_AUTH_TOKEN",
        "DCC_ENV_FILE",
        "HOST",
        "PORT",
        "LOG_FILE",
    ):
        monkeypatch.delenv(key, raising=False)


def test_admin_page_is_loopback_only(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    app = create_app(lifespan_enabled=False)

    assert _local_client(app).get("/admin").status_code == 200
    remote_client = TestClient(app, client=("203.0.113.10", 50000))
    assert remote_client.get("/admin").status_code == 403


def test_admin_config_masks_secrets_and_exposes_manifest(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)

    response = _local_client(app).get("/admin/api/config")

    assert response.status_code == 200
    body = response.json()
    keys = {field["key"] for field in body["fields"]}
    assert "ANTHROPIC_AUTH_TOKEN" in keys
    assert "OPENROUTER_API_KEY" in keys
    auth_field = next(
        field for field in body["fields"] if field["key"] == "ANTHROPIC_AUTH_TOKEN"
    )
    assert auth_field["secret"] is True
    assert auth_field["value"] == MASKED_SECRET
    assert auth_field["source"] == "template"


def test_admin_validate_rejects_bad_model_shape(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)

    response = _local_client(app).post(
        "/admin/api/config/validate",
        json={"values": {"MODEL": "missing-provider-prefix"}},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is False
    assert any("provider type" in error for error in body["errors"])
    assert isinstance(body.get("errors_detailed"), list)
    model_err = next(
        (row for row in body["errors_detailed"] if row["key"] == "MODEL"), None
    )
    assert model_err is not None
    assert model_err["label"] == "Default Model"
    assert "provider type" in model_err["message"]
    assert model_err["default"] == "nvidia_nim/z-ai/glm4.7"
    assert model_err["suggestion"].startswith("Reset to default:")
    assert "managed_env_path" in body


def test_admin_apply_writes_complete_managed_env_and_masks_preview(
    monkeypatch, tmp_path
):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)

    response = _local_client(app).post(
        "/admin/api/config/apply",
        json={
            "values": {
                "MODEL": "open_router/test-model",
                "OPENROUTER_API_KEY": "router-secret",
            }
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["applied"] is True
    assert "OPENROUTER_API_KEY=********" in body["env_preview"]
    env_file = tmp_path / ".config" / "deep-claude" / ".env"
    text = env_file.read_text("utf-8")
    assert "MODEL=open_router/test-model" in text
    assert "OPENROUTER_API_KEY=router-secret" in text
    assert "ANTHROPIC_AUTH_TOKEN=" in text
    assert body["restart"] == {
        "required": False,
        "automatic": False,
        "admin_url": None,
        "fields": [],
    }


def test_admin_apply_restart_required_reports_automatic_restart(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)
    callbacks: list[str] = []

    async def restart_callback() -> None:
        callbacks.append("restart")

    app.state.admin_restart_callback = restart_callback

    response = _local_client(app).post(
        "/admin/api/config/apply",
        json={"values": {"PORT": "9090"}},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["applied"] is True
    assert body["pending_fields"] == ["PORT"]
    assert body["restart"] == {
        "required": True,
        "automatic": True,
        "admin_url": "http://127.0.0.1:9090/admin",
        "fields": ["PORT"],
    }
    assert callbacks == ["restart"]


def test_admin_apply_restart_required_reports_manual_fallback(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)

    response = _local_client(app).post(
        "/admin/api/config/apply",
        json={"values": {"PORT": "9091"}},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["applied"] is True
    assert body["pending_fields"] == ["PORT"]
    assert body["restart"] == {
        "required": True,
        "automatic": False,
        "admin_url": None,
        "fields": ["PORT"],
    }


def test_admin_process_env_values_are_locked_and_not_written(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    monkeypatch.setenv("MODEL", "open_router/process-model")
    app = create_app(lifespan_enabled=False)

    config = _local_client(app).get("/admin/api/config").json()
    model_field = next(field for field in config["fields"] if field["key"] == "MODEL")
    assert model_field["locked"] is True
    assert model_field["source"] == "process"

    response = _local_client(app).post(
        "/admin/api/config/apply",
        json={"values": {"MODEL": "deepseek/managed-model"}},
    )

    assert response.status_code == 200
    env_file = tmp_path / ".config" / "deep-claude" / ".env"
    assert "deepseek/managed-model" not in env_file.read_text("utf-8")


def test_admin_first_apply_migrates_repo_env(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text(
        "MODEL=deepseek/deepseek-chat\nDEEPSEEK_API_KEY=deepseek-secret\n",
        encoding="utf-8",
    )
    app = create_app(lifespan_enabled=False)

    config = _local_client(app).get("/admin/api/config").json()
    model_field = next(field for field in config["fields"] if field["key"] == "MODEL")
    assert model_field["value"] == "deepseek/deepseek-chat"
    assert model_field["source"] == "repo_env"

    response = _local_client(app).post(
        "/admin/api/config/apply",
        json={"values": {}},
    )

    assert response.status_code == 200
    managed_text = (tmp_path / ".config" / "deep-claude" / ".env").read_text("utf-8")
    assert "MODEL=deepseek/deepseek-chat" in managed_text
    assert "DEEPSEEK_API_KEY=deepseek-secret" in managed_text


def test_admin_local_provider_status_reports_reachable(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def get(self, url: str):
            return httpx.Response(200, json={"data": []})

    with patch("api.admin_routes.httpx.AsyncClient", FakeAsyncClient):
        response = _local_client(app).get("/admin/api/providers/local-status")

    assert response.status_code == 200
    providers = response.json()["providers"]
    assert {provider["status"] for provider in providers} == {"reachable"}


def test_admin_launch_url_uses_loopback_for_wildcard_host():
    settings = Settings.model_construct(host="0.0.0.0", port=8082)

    assert local_admin_url(settings) == "http://127.0.0.1:8082/admin"


class _BalanceFakeClient:
    """Stub httpx.AsyncClient that returns a preset response or raises."""

    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None


def _balance_client_factory(
    response: httpx.Response | None, exc: Exception | None = None
):
    captured: dict[str, object] = {}

    class _Client(_BalanceFakeClient):
        async def get(self, url, headers=None):
            captured["url"] = url
            captured["headers"] = headers or {}
            if exc is not None:
                raise exc
            assert response is not None
            return response

    return _Client, captured


def test_admin_deepseek_balance_requires_loopback(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)

    remote = TestClient(app, client=("203.0.113.10", 50000))
    assert remote.get("/admin/api/providers/deepseek/balance").status_code == 403


def test_admin_deepseek_balance_default_returns_no_cache(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_CACHE", str(tmp_path / "balance.json"))
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_HISTORY", str(tmp_path / "history.jsonl"))
    app = create_app(lifespan_enabled=False)

    response = _local_client(app).get("/admin/api/providers/deepseek/balance")

    assert response.status_code == 200
    body = response.json()
    assert body == {"ok": False, "error": "no_cache", "cached": True}


def test_admin_deepseek_balance_missing_key(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_CACHE", str(tmp_path / "balance.json"))
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_HISTORY", str(tmp_path / "history.jsonl"))
    get_settings.cache_clear()
    app = create_app(lifespan_enabled=False)

    response = _local_client(app).get(
        "/admin/api/providers/deepseek/balance?refresh=true"
    )

    assert response.status_code == 200
    assert response.json() == {
        "ok": False,
        "error": "missing_key",
        "cached": False,
    }


def test_admin_deepseek_balance_refresh_caches_and_default_reads_cache(
    monkeypatch, tmp_path
):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    cache_path = tmp_path / "balance.json"
    history_path = tmp_path / "history.jsonl"
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_CACHE", str(cache_path))
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_HISTORY", str(history_path))
    monkeypatch.setenv("DEEPSEEK_API_KEY", "ds-secret")
    get_settings.cache_clear()
    app = create_app(lifespan_enabled=False)

    payload = {
        "is_available": True,
        "balance_infos": [
            {
                "currency": "CNY",
                "total_balance": "110.00",
                "granted_balance": "10.00",
                "topped_up_balance": "100.00",
            }
        ],
    }
    client_cls, captured = _balance_client_factory(httpx.Response(200, json=payload))

    with patch("api.admin_routes.httpx.AsyncClient", client_cls):
        response = _local_client(app).get(
            "/admin/api/providers/deepseek/balance?refresh=true"
        )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["balance"] == payload
    assert body["cached"] is False
    assert "fetched_at" in body
    assert body["trend"]["by_currency"][0]["currency"] == "CNY"
    assert body["trend"]["by_currency"][0]["current_total"] == 110.0
    assert body["trend"]["by_currency"][0]["today_drop"] is None
    assert body["trend"]["by_currency"][0]["week_drop"] is None
    assert captured["url"] == "https://api.deepseek.com/user/balance"
    assert captured["headers"]["Authorization"] == "Bearer ds-secret"
    assert cache_path.is_file()
    assert history_path.is_file()

    default_response = _local_client(app).get("/admin/api/providers/deepseek/balance")
    assert default_response.status_code == 200
    default_body = default_response.json()
    assert default_body["ok"] is True
    assert default_body["balance"] == payload
    assert default_body["cached"] is True
    assert "trend" in default_body


def test_admin_deepseek_balance_upstream_error(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "ds-secret")
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_CACHE", str(tmp_path / "balance.json"))
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_HISTORY", str(tmp_path / "history.jsonl"))
    get_settings.cache_clear()
    app = create_app(lifespan_enabled=False)

    client_cls, _ = _balance_client_factory(httpx.Response(401, text="Unauthorized"))

    with patch("api.admin_routes.httpx.AsyncClient", client_cls):
        response = _local_client(app).get(
            "/admin/api/providers/deepseek/balance?refresh=true"
        )

    assert response.status_code == 200
    assert response.json() == {
        "ok": False,
        "error": "upstream_error",
        "status_code": 401,
        "cached": False,
    }


def test_admin_deepseek_usage_empty(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    monkeypatch.setenv("DCC_USAGE_LOG", str(tmp_path / "usage.jsonl"))
    app = create_app(lifespan_enabled=False)

    response = _local_client(app).get("/admin/api/providers/deepseek/usage")

    assert response.status_code == 200
    body = response.json()
    assert body["totals"]["calls"] == 0
    assert body["totals"]["estimated_cost_cny"] is None
    assert body["by_model"] == []


def test_admin_deepseek_usage_aggregates_and_costs(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    usage_path = tmp_path / "usage.jsonl"
    monkeypatch.setenv("DCC_USAGE_LOG", str(usage_path))
    app = create_app(lifespan_enabled=False)

    import json as _json
    from datetime import datetime as _dt

    now = _dt.now(UTC).isoformat()
    rows = [
        {
            "ts": now,
            "provider": "DEEPSEEK",
            "model": "deepseek-v4-flash",
            "input_tokens": 1000,
            "output_tokens": 500,
            "cache_read_input_tokens": 100,
            "cache_creation_input_tokens": 0,
        },
    ]
    usage_path.write_text(_json.dumps(rows[0]) + "\n", encoding="utf-8")

    response = _local_client(app).get(
        "/admin/api/providers/deepseek/usage?period=today"
    )

    assert response.status_code == 200
    body = response.json()
    assert body["totals"]["calls"] == 1
    assert body["totals"]["input_tokens"] == 1000
    assert body["totals"]["output_tokens"] == 500
    cost = body["totals"]["estimated_cost_cny"]
    assert cost is not None
    assert cost > 0


def test_admin_deepseek_usage_rejects_bad_period(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)

    response = _local_client(app).get("/admin/api/providers/deepseek/usage?period=year")

    assert response.status_code == 400


def test_admin_deepseek_usage_requires_loopback(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)

    remote = TestClient(app, client=("203.0.113.10", 50000))
    assert remote.get("/admin/api/providers/deepseek/usage").status_code == 403


def test_admin_deepseek_balance_request_failure(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "ds-secret")
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_CACHE", str(tmp_path / "balance.json"))
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_HISTORY", str(tmp_path / "history.jsonl"))
    get_settings.cache_clear()
    app = create_app(lifespan_enabled=False)

    client_cls, _ = _balance_client_factory(None, exc=httpx.ConnectError("boom"))

    with patch("api.admin_routes.httpx.AsyncClient", client_cls):
        response = _local_client(app).get(
            "/admin/api/providers/deepseek/balance?refresh=true"
        )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["error"] == "request_failed"
    assert body["error_type"] == "ConnectError"
    assert body["cached"] is False


def test_admin_server_stop_invokes_callback(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)
    calls: list[str] = []

    def stop_cb() -> None:
        calls.append("stop")

    app.state.admin_stop_callback = stop_cb

    response = _local_client(app).post("/admin/api/server/stop")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "action": "stopping"}
    assert calls == ["stop"]


def test_admin_server_stop_returns_501_when_unsupported(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)

    response = _local_client(app).post("/admin/api/server/stop")

    assert response.status_code == 501


def test_admin_server_restart_invokes_callback(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)
    calls: list[str] = []

    def restart_cb() -> None:
        calls.append("restart")

    app.state.admin_restart_callback = restart_cb

    response = _local_client(app).post("/admin/api/server/restart")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "action": "restarting"}
    assert calls == ["restart"]


def test_admin_server_stop_requires_loopback(monkeypatch, tmp_path):
    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    app = create_app(lifespan_enabled=False)

    remote = TestClient(app, client=("203.0.113.10", 50000))
    assert remote.post("/admin/api/server/stop").status_code == 403
    assert remote.post("/admin/api/server/restart").status_code == 403


def test_admin_deepseek_balance_trend_computes_today_drop(monkeypatch, tmp_path):
    import json as _json
    from datetime import datetime as _dt
    from datetime import timedelta as _td

    _set_home(monkeypatch, tmp_path)
    _clear_process_config(monkeypatch)
    cache_path = tmp_path / "balance.json"
    history_path = tmp_path / "history.jsonl"
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_CACHE", str(cache_path))
    monkeypatch.setenv("DCC_DEEPSEEK_BALANCE_HISTORY", str(history_path))
    monkeypatch.setenv("DEEPSEEK_API_KEY", "ds-secret")
    get_settings.cache_clear()

    old_baseline = _dt.now().astimezone() - _td(days=8)
    history_path.write_text(
        _json.dumps(
            {
                "ts": old_baseline.isoformat(),
                "balance_infos": [
                    {"currency": "CNY", "total_balance": "120.00"},
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    app = create_app(lifespan_enabled=False)
    payload = {
        "is_available": True,
        "balance_infos": [
            {
                "currency": "CNY",
                "total_balance": "108.30",
                "granted_balance": "0",
                "topped_up_balance": "108.30",
            }
        ],
    }
    client_cls, _ = _balance_client_factory(httpx.Response(200, json=payload))

    with patch("api.admin_routes.httpx.AsyncClient", client_cls):
        response = _local_client(app).get(
            "/admin/api/providers/deepseek/balance?refresh=true"
        )

    body = response.json()
    by_currency = body["trend"]["by_currency"]
    assert len(by_currency) == 1
    row = by_currency[0]
    assert row["currency"] == "CNY"
    assert row["current_total"] == 108.3
    assert row["today_drop"] == pytest.approx(11.7, abs=0.01)
    assert row["week_drop"] == pytest.approx(11.7, abs=0.01)
