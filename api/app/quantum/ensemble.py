"""Meta-governor for ensemble weighting."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class PromotionGates:
    """Gate thresholds for promoting strategies."""
    hit_rate: float
    sharpe_10d: float
    max_dd_10d: float
    route_p95_us: float
    slip_error_pct: float
    days: int


@dataclass
class MetaGovernor:
    """Manage strategy weights subject to promotion gates."""
    gates: PromotionGates
    weights: Dict[str, float] = field(
        default_factory=lambda: {"QBX3": 0.25, "SSv2": 0.25, "ATRA": 0.25, "MS7": 0.25}
    )
    min_w: float = 0.05
    max_w: float = 0.60

    def update_weights(self, perf: Dict[str, float]) -> None:
        """Update weights based on performance dictionary."""
        if not perf:
            return
        total = sum(max(0.0, v) for v in perf.values()) or 1.0
        for key, val in perf.items():
            w = max(self.min_w, min(self.max_w, (max(0.0, val) / total)))
            self.weights[key] = w
        s = sum(self.weights.values())
        for k in self.weights:
            self.weights[k] /= s
