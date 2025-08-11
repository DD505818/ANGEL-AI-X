"""GARCH(1,1) volatility forecasting."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def garch_forecast(returns: Iterable[float], omega: float, alpha: float, beta: float) -> float:
    """Forecast next-period variance using GARCH(1,1).

    Args:
        returns: Iterable of historical returns.
        omega: Constant term of the model.
        alpha: Reaction coefficient for last period's squared return.
        beta: Persistence coefficient for last period's variance.

    Returns:
        Forecasted variance for the next period.
    """

    if omega < 0 or alpha < 0 or beta < 0:
        raise ValueError("omega, alpha, and beta must be non-negative")
    if alpha + beta >= 1:
        raise ValueError("alpha + beta must be < 1 for stationarity")

    data = np.asarray(list(returns), dtype=float)
    if data.size == 0:
        raise ValueError("returns must not be empty")

    # Initialize variance with sample variance
    var = np.var(data, ddof=1)
    for r in data:
        var = omega + alpha * r ** 2 + beta * var
    return float(var)
