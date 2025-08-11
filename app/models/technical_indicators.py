"""Technical indicator calculations."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def _validate_window(window: int) -> None:
    if window <= 0:
        raise ValueError("window must be positive")


def sma(prices: Iterable[float], window: int) -> np.ndarray:
    """Return the simple moving average of ``prices`` over ``window``.

    Args:
        prices: Iterable of price floats.
        window: Number of periods for the average.

    Returns:
        NumPy array of SMA values with length ``len(prices) - window + 1``.
    """

    _validate_window(window)
    data = np.asarray(list(prices), dtype=float)
    if data.size < window:
        raise ValueError("prices length must be at least as large as window")
    weights = np.ones(window) / window
    return np.convolve(data, weights, mode="valid")


def ema(prices: Iterable[float], window: int) -> np.ndarray:
    """Return the exponential moving average of ``prices`` over ``window``.

    Args:
        prices: Iterable of price floats.
        window: Number of periods for the average.

    Returns:
        NumPy array of EMA values with length equal to ``len(prices)``.
    """

    _validate_window(window)
    data = np.asarray(list(prices), dtype=float)
    if data.size < window:
        raise ValueError("prices length must be at least as large as window")
    ema_values = np.empty_like(data)
    alpha = 2 / (window + 1)
    ema_values[0] = data[0]
    for i in range(1, len(data)):
        ema_values[i] = alpha * data[i] + (1 - alpha) * ema_values[i - 1]
    return ema_values
