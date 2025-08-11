"""Monte Carlo stress testing utilities."""

from __future__ import annotations

from typing import Iterable, Optional

import numpy as np


def monte_carlo_var(
    returns: Iterable[float],
    horizon: int,
    iterations: int = 1000,
    alpha: float = 0.95,
    rng: Optional[np.random.Generator] = None,
) -> float:
    """Estimate value-at-risk using Monte Carlo simulation.

    Args:
        returns: Historical returns sample.
        horizon: Number of periods to simulate.
        iterations: Number of simulation runs.
        alpha: Confidence level.

    Returns:
        Estimated VaR as a positive float.
    """

    if horizon <= 0 or iterations <= 0:
        raise ValueError("horizon and iterations must be positive")
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie in (0, 1)")
    data = np.asarray(list(returns), dtype=float)
    if data.size == 0:
        raise ValueError("returns must not be empty")

    mean = np.mean(data)
    std = np.std(data, ddof=1)
    generator = rng or np.random.default_rng()
    simulations = generator.normal(mean, std, size=(iterations, horizon))
    pnl = simulations.sum(axis=1)
    var_index = int((1 - alpha) * iterations)
    return float(-np.sort(pnl)[var_index])


def kelly_fraction(mean: float, variance: float) -> float:
    """Compute Kelly optimal fraction for a given return distribution."""
    if variance <= 0:
        raise ValueError("variance must be positive")
    return mean / variance
