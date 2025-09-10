"""Simple smart order router scoring logic."""
from dataclasses import dataclass


@dataclass
class Venue:
    """Execution venue attributes relevant for routing."""

    name: str
    taker_fee: float
    maker_rebate: float
    p99_ms: int
    qpos: float


VENUES = [
    Venue("BYBIT", 0.0006, 0.0001, 35, 0.70),
    Venue("KRAKEN", 0.00026, 0.0, 45, 0.55),
    Venue("OKX", 0.0004, 0.00012, 40, 0.65),
]


def score(venue: Venue) -> float:
    """Return a cost score for ``venue`` combining fees, latency and queue position."""
    cost = venue.taker_fee - venue.maker_rebate
    latency_penalty = max(0, (venue.p99_ms - 25) / 1000.0)
    qpos_penalty = (1.0 - venue.qpos) * 0.05
    return cost + latency_penalty + qpos_penalty


def pick_best() -> Venue:
    """Pick the venue with the minimal score that meets latency constraints."""
    candidates = [v for v in VENUES if v.p99_ms <= 50]
    return min(candidates, key=score)
