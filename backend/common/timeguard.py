"""Utilities for validating event timestamps and staleness."""

def validate_event_clock(event_ts: float, ingest_ts: float, max_skew_ms: int) -> bool:
    """
    event_ts, ingest_ts in epoch seconds. Returns True if within skew.
    """
    skew_ms = abs((ingest_ts - event_ts) * 1000.0)
    return skew_ms <= max_skew_ms

def reject_if_stale(event_ts: float, now_ts: float, max_age_ms: int) -> bool:
    age_ms = (now_ts - event_ts) * 1000.0
    return age_ms > max_age_ms

