"""Position sizing helper."""

from __future__ import annotations

def adaptive_position_size(
    nav: float,
    atr: float,
    sigma: float,
    kelly: float,
    dd_frac: float,
    trend_conf: float,
    regime: bool,
) -> float:
    """Calculate position size with volatility and drawdown adjustments."""
    if nav <= 0 or atr <= 0:
        raise ValueError("nav and atr must be positive")
    vol_penalty = 1.0 / (1.0 + 2.0 * sigma)
    trend_boost = 1.0 + 0.5 * max(0.0, trend_conf - 0.6)
    dd_penalty = 1.0 - min(0.8, dd_frac * 2.0)
    raw = nav * kelly * vol_penalty * trend_boost * dd_penalty
    return raw if regime else 0.0
