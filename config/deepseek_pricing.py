"""DeepSeek pricing table in CNY per 1M tokens.

Source: https://api-docs.deepseek.com/zh-cn/quick_start/pricing
Rates are hardcoded — update manually when DeepSeek changes prices.
"""

from __future__ import annotations

from dataclasses import dataclass

PRICE_UNIT_TOKENS = 1_000_000


@dataclass(frozen=True, slots=True)
class ModelPricing:
    """CNY per 1M tokens."""

    cache_hit_input: float
    cache_miss_input: float
    output: float


PRICING: dict[str, ModelPricing] = {
    "deepseek-v4-flash": ModelPricing(
        cache_hit_input=0.02, cache_miss_input=1.0, output=2.0
    ),
    "deepseek-v4-pro": ModelPricing(
        cache_hit_input=0.025, cache_miss_input=3.0, output=6.0
    ),
}

_ALIASES = {
    "deepseek-chat": "deepseek-v4-flash",
    "deepseek-reasoner": "deepseek-v4-pro",
}


def lookup_pricing(model: str) -> ModelPricing | None:
    """Return pricing for a DeepSeek model id (with alias fallback)."""
    key = model.strip().lower()
    if not key:
        return None
    if key in PRICING:
        return PRICING[key]
    alias = _ALIASES.get(key)
    if alias and alias in PRICING:
        return PRICING[alias]
    return None


def estimate_cost_cny(
    *,
    model: str,
    cache_hit_input_tokens: int,
    cache_miss_input_tokens: int,
    output_tokens: int,
) -> float | None:
    """Estimate cost in CNY; return None when model pricing is unknown."""
    rates = lookup_pricing(model)
    if rates is None:
        return None
    cost = (
        cache_hit_input_tokens * rates.cache_hit_input
        + cache_miss_input_tokens * rates.cache_miss_input
        + output_tokens * rates.output
    ) / PRICE_UNIT_TOKENS
    return round(cost, 4)
