"""Risk management utilities."""
from __future__ import annotations

import math
from typing import List

import numpy as np


def veto_poor_edge(expected_r: float, fee: float, slip: float, min_rcost: float = 1.8) -> bool:
    """Return ``True`` when risk-adjusted return is below ``min_rcost``."""
    rcost = expected_r / max(1e-9, fee + slip)
    return rcost < min_rcost


def kelly_two_thirds(edge: float, variance: float, prev_risk: float, cap: float = 0.25, bump: float = 0.005, floor: float = 0.005) -> float:
    """Adapted Kelly sizing with two-thirds scaling and smooth bumps."""
    base = 0.66 * edge / max(1e-9, variance)
    next_risk = min(prev_risk + bump, base, cap)
    return max(next_risk, floor, 0.0)


def esd_last_z(spreads: List[float], z: float = 2.0) -> bool:
    """Flag extreme studentized deviation on ``spreads``."""
    if len(spreads) < 30:
        return False
    arr = np.array(spreads[-400:]) if len(spreads) > 400 else np.array(spreads)
    mean = float(arr.mean())
    std = float(arr.std() or 1e-9)
    return abs((arr[-1] - mean) / std) > z
