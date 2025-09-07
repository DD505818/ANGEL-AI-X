"""Idempotency utilities for ensuring exactly-once order submits."""
import uuid

IDEMP_PREFIX = "ANGEL"

def make_client_key(symbol: str, side: str, qty: float, px: float, intent_ts_ms: int) -> str:
    """
    Deterministic client idempotency key for exactly-once submit attempts.
    """
    base = f"{IDEMP_PREFIX}:{symbol}:{side}:{qty:.8f}:{px:.8f}:{intent_ts_ms}"
    return base

def new_uuid_key() -> str:
    return f"{IDEMP_PREFIX}:{uuid.uuid4()}"

