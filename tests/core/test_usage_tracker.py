from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from core.usage_tracker import aggregate, record_usage


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


@pytest.fixture
def usage_log(tmp_path, monkeypatch) -> Path:
    path = tmp_path / "usage.jsonl"
    monkeypatch.setenv("DCC_USAGE_LOG", str(path))
    return path


def test_record_usage_writes_jsonl_row(usage_log: Path):
    asyncio.run(
        record_usage(
            provider="DEEPSEEK",
            model="deepseek-v4-flash",
            input_tokens=100,
            output_tokens=200,
            cache_read_input_tokens=10,
            cache_creation_input_tokens=5,
        )
    )
    lines = usage_log.read_text("utf-8").splitlines()
    assert len(lines) == 1
    row = json.loads(lines[0])
    assert row["provider"] == "DEEPSEEK"
    assert row["model"] == "deepseek-v4-flash"
    assert row["input_tokens"] == 100
    assert row["output_tokens"] == 200
    assert row["cache_read_input_tokens"] == 10
    assert row["cache_creation_input_tokens"] == 5


def test_record_usage_skips_zero_rows(usage_log: Path):
    asyncio.run(
        record_usage(provider="DEEPSEEK", model="x", input_tokens=0, output_tokens=0)
    )
    assert not usage_log.exists() or usage_log.read_text("utf-8") == ""


def test_aggregate_today_filters_by_date(usage_log: Path):
    now = datetime.now(UTC)
    yesterday = now - timedelta(days=1)
    rows = [
        {
            "ts": yesterday.isoformat(),
            "provider": "DEEPSEEK",
            "model": "deepseek-v4-flash",
            "input_tokens": 500,
            "output_tokens": 100,
            "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 0,
        },
        {
            "ts": now.isoformat(),
            "provider": "DEEPSEEK",
            "model": "deepseek-v4-flash",
            "input_tokens": 1000,
            "output_tokens": 200,
            "cache_read_input_tokens": 50,
            "cache_creation_input_tokens": 0,
        },
        {
            "ts": now.isoformat(),
            "provider": "DEEPSEEK",
            "model": "deepseek-v4-pro",
            "input_tokens": 2000,
            "output_tokens": 400,
            "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 0,
        },
        {
            "ts": now.isoformat(),
            "provider": "OTHER",
            "model": "irrelevant",
            "input_tokens": 9999,
            "output_tokens": 9999,
            "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 0,
        },
    ]
    usage_log.parent.mkdir(parents=True, exist_ok=True)
    usage_log.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8"
    )

    result = aggregate(provider="DEEPSEEK", period="today")

    assert result["totals"]["calls"] == 2
    assert result["totals"]["input_tokens"] == 3000
    assert result["totals"]["output_tokens"] == 600
    models = {row["model"]: row for row in result["by_model"]}
    assert models["deepseek-v4-flash"]["calls"] == 1
    assert models["deepseek-v4-pro"]["calls"] == 1


def test_aggregate_handles_malformed_lines(usage_log: Path):
    usage_log.parent.mkdir(parents=True, exist_ok=True)
    usage_log.write_text("not-json\n\n", encoding="utf-8")

    result = aggregate(provider="DEEPSEEK", period="today")

    assert result["totals"]["calls"] == 0
    assert result["by_model"] == []


def test_aggregate_rejects_bad_period(usage_log: Path):
    with pytest.raises(ValueError):
        aggregate(provider="DEEPSEEK", period="year")
