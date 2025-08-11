"""Time-of-day volume analysis."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Dict, Iterable, Tuple


def time_of_day_volume(samples: Iterable[Tuple[datetime, float]]) -> Dict[int, float]:
    """Compute average traded volume per hour of day.

    Args:
        samples: Iterable of (timestamp, volume) pairs.

    Returns:
        Mapping from hour (0-23) to average volume.
    """

    totals: Dict[int, float] = defaultdict(float)
    counts: Dict[int, int] = defaultdict(int)
    for ts, volume in samples:
        if volume < 0:
            raise ValueError("volume must be non-negative")
        hour = ts.hour
        totals[hour] += volume
        counts[hour] += 1
    return {h: totals[h] / counts[h] for h in totals}
