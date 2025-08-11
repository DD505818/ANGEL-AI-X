"""Risk management utilities for ANGEL.AI.

This module implements classic risk metrics and dynamic sizing helpers.
"""
from __future__ import annotations

from typing import Iterable


def kelly_fraction(win_rate: float, win_loss_ratio: float) -> float:
    """Return Kelly optimal fraction.

    Raises ValueError if inputs are out of bounds.
    """
    if not 0 < win_rate < 1:
        raise ValueError("win_rate must be between 0 and 1")
    if win_loss_ratio <= 0:
        raise ValueError("win_loss_ratio must be positive")
    return win_rate - (1 - win_rate) / win_loss_ratio


def max_drawdown(equity_curve: Iterable[float]) -> float:
    """Compute maximum drawdown of an equity curve."""
    peak = float("-inf")
    max_dd = 0.0
    for equity in equity_curve:
        peak = max(peak, equity)
        drawdown = (peak - equity) / peak if peak else 0.0
        max_dd = max(max_dd, drawdown)
    return max_dd


def value_at_risk(returns: Iterable[float], confidence: float = 0.95) -> float:
    """Return historical Value-at-Risk."""
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    data = sorted(returns)
    index = int((1 - confidence) * len(data))
    return abs(data[index])


def dynamic_position_size(balance: float, risk_fraction: float) -> float:
    """Return position size based on account balance and risk fraction."""
    if balance <= 0 or not 0 < risk_fraction <= 1:
        raise ValueError("invalid balance or risk_fraction")
    return balance * risk_fraction
