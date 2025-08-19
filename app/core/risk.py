"""Risk management utilities."""

from __future__ import annotations

from typing import Tuple

# Hard-coded risk limits
GROWTH_TARGET_DAILY: float = 0.05
MAX_DD_DAILY: float = 0.02
MAX_DD_INTRADAY: float = 0.015
MAX_LEVERAGE: float = 2.0

def garch_scaled_atr(atr: float, sigma: float) -> float:
    """Scale the ATR by a simple GARCH-like volatility adjustment."""
    if atr <= 0 or sigma < 0:
        raise ValueError("ATR and sigma must be positive")
    return atr * (1.0 + 0.5 * sigma)

def kelly_blend(mu: float, sigma: float, cvar: float, cap: float = 0.25) -> float:
    """Blend Kelly sizing with CVaR to cap excessive bets."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    k_raw = mu / max(1e-9, sigma ** 2)
    k_cvar = 1.0 / (1.0 + 10 * max(cvar, 1e-9))
    return min(max(0.0, k_raw * k_cvar), cap)

def risk_precheck(lev_next: float, dd_today: float) -> Tuple[bool, str]:
    """Basic leverage and drawdown guardrails."""
    if dd_today > MAX_DD_DAILY:
        return False, "daily_dd_limit"
    if lev_next > MAX_LEVERAGE:
        return False, "leverage_cap"
    return True, "ok"
