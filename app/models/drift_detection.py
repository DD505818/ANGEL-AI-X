"""Data drift detection routines."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def ks_drift_detect(base: Iterable[float], new: Iterable[float], alpha: float = 0.05) -> bool:
    """Detect distribution drift using a two-sample KS test.

    Args:
        base: Baseline sample.
        new: New sample to compare.
        alpha: Significance level.

    Returns:
        ``True`` if drift is detected.
    """

    if not 0 < alpha < 1:
        raise ValueError("alpha must lie in (0, 1)")
    base_arr = np.sort(np.asarray(list(base), dtype=float))
    new_arr = np.sort(np.asarray(list(new), dtype=float))
    if base_arr.size == 0 or new_arr.size == 0:
        raise ValueError("samples must not be empty")

    cdf1 = np.searchsorted(base_arr, base_arr, side="right") / base_arr.size
    cdf2 = np.searchsorted(base_arr, new_arr, side="right") / base_arr.size
    cdf3 = np.searchsorted(new_arr, base_arr, side="right") / new_arr.size
    cdf4 = np.searchsorted(new_arr, new_arr, side="right") / new_arr.size
    d1 = np.max(np.abs(cdf1 - cdf2))
    d2 = np.max(np.abs(cdf3 - cdf4))
    d = max(d1, d2)
    n1, n2 = base_arr.size, new_arr.size
    critical = np.sqrt(-0.5 * np.log(alpha / 2)) * np.sqrt((n1 + n2) / (n1 * n2))
    return d > critical
