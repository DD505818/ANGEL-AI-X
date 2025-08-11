"""Volatility calculations and risk metrics."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def realized_volatility(returns: Iterable[float]) -> float:
    """Compute annualized realized volatility from returns.

    Args:
        returns: Iterable of periodic returns as floats.

    Returns:
        Annualized volatility assuming 252 trading days.
    """

    data = np.asarray(list(returns), dtype=float)
    if data.size == 0:
        raise ValueError("returns must not be empty")
    return float(np.std(data, ddof=1) * np.sqrt(252))


def value_at_risk(returns: Iterable[float], alpha: float) -> float:
    """Compute historical value-at-risk at level ``alpha``.

    Args:
        returns: Iterable of periodic returns.
        alpha: Confidence level between 0 and 1.

    Returns:
        VaR expressed as a positive float.
    """

    if not 0 < alpha < 1:
        raise ValueError("alpha must lie in (0, 1)")
    data = np.sort(np.asarray(list(returns), dtype=float))
    index = int((1 - alpha) * len(data))
    return float(-data[index])
