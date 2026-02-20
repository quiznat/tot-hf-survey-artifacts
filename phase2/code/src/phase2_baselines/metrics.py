"""Metrics and token-cost helpers."""

from __future__ import annotations

from .models import PricingConfig


def estimate_tokens(text: str) -> int:
    """Approximate token count using whitespace segmentation.

    This is a placeholder estimator until provider-native token accounting
    is wired into the run harness.
    """
    stripped = text.strip()
    if not stripped:
        return 0
    return len(stripped.split())


def estimate_cost_usd(tokens_in: int, tokens_out: int, pricing: PricingConfig) -> float:
    """Estimate USD cost based on per-1k token rates."""
    input_cost = (tokens_in / 1000.0) * pricing.input_per_1k
    output_cost = (tokens_out / 1000.0) * pricing.output_per_1k
    return round(input_cost + output_cost, 8)
