import time
from backend.common.timeguard import validate_event_clock, reject_if_stale


def test_validate_event_clock_within_skew():
    now = time.time()
    assert validate_event_clock(now - 0.05, now, 100)  # 50ms skew


def test_reject_if_stale():
    now = time.time()
    assert reject_if_stale(now - 1.0, now, 500)  # 1s age > 500ms
