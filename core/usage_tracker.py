"""Append-only JSONL usage recorder + period aggregation for provider stats."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from loguru import logger

_WRITE_LOCK = asyncio.Lock()


def usage_log_path() -> Path:
    """Return the JSONL path; honor DCC_USAGE_LOG when set."""
    override = os.environ.get("DCC_USAGE_LOG")
    if override:
        return Path(override)
    return Path.home() / ".config" / "deep-claude" / "usage.jsonl"


@dataclass(frozen=True, slots=True)
class UsageRow:
    ts: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    cache_read_input_tokens: int
    cache_creation_input_tokens: int


async def record_usage(
    *,
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_read_input_tokens: int = 0,
    cache_creation_input_tokens: int = 0,
    ts: datetime | None = None,
) -> None:
    """Append one row to the usage JSONL. Never raises into caller."""
    if not provider or not model:
        return
    if input_tokens <= 0 and output_tokens <= 0:
        return
    row = {
        "ts": (ts or datetime.now(UTC)).isoformat(),
        "provider": provider,
        "model": model,
        "input_tokens": int(input_tokens),
        "output_tokens": int(output_tokens),
        "cache_read_input_tokens": int(cache_read_input_tokens),
        "cache_creation_input_tokens": int(cache_creation_input_tokens),
    }
    path = usage_log_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        async with _WRITE_LOCK:
            await asyncio.to_thread(
                _append_line, path, json.dumps(row, ensure_ascii=False)
            )
    except Exception as exc:
        logger.warning("usage_tracker.record_failed: {}", type(exc).__name__)


def _append_line(path: Path, line: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def _period_start(period: str, now: datetime) -> datetime:
    local = now.astimezone()
    midnight = local.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "today":
        return midnight
    if period == "week":
        return midnight - timedelta(days=midnight.weekday())
    if period == "month":
        return midnight.replace(day=1)
    raise ValueError(f"unknown period: {period!r}")


def _read_rows(path: Path) -> Iterable[dict[str, Any]]:
    if not path.is_file():
        return
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def _parse_ts(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def aggregate(
    *,
    provider: str,
    period: str,
    now: datetime | None = None,
    path: Path | None = None,
) -> dict[str, Any]:
    """Aggregate rows for ``provider`` in ``period`` (today/week/month) by model."""
    current = now or datetime.now(UTC)
    start = _period_start(period, current)
    log_path = path or usage_log_path()

    by_model: dict[str, dict[str, int]] = {}
    for row in _read_rows(log_path):
        if row.get("provider") != provider:
            continue
        ts = _parse_ts(row.get("ts"))
        if ts is None:
            continue
        if ts.astimezone() < start:
            continue
        model = str(row.get("model") or "")
        bucket = by_model.setdefault(
            model,
            {
                "calls": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "cache_read_input_tokens": 0,
                "cache_creation_input_tokens": 0,
            },
        )
        bucket["calls"] += 1
        bucket["input_tokens"] += int(row.get("input_tokens", 0) or 0)
        bucket["output_tokens"] += int(row.get("output_tokens", 0) or 0)
        bucket["cache_read_input_tokens"] += int(
            row.get("cache_read_input_tokens", 0) or 0
        )
        bucket["cache_creation_input_tokens"] += int(
            row.get("cache_creation_input_tokens", 0) or 0
        )

    totals = {
        "calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
    }
    for bucket in by_model.values():
        for key in totals:
            totals[key] += bucket[key]

    return {
        "period": period,
        "period_start": start.isoformat(),
        "provider": provider,
        "totals": totals,
        "by_model": [
            {"model": model, **bucket} for model, bucket in sorted(by_model.items())
        ],
    }
