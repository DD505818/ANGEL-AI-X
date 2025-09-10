"""Strategy configuration endpoints."""
from typing import Dict

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["strategy"])


class StrategyParams(BaseModel):
    """Payload containing strategy parameter overrides."""

    params: Dict[str, float]


_STRATS: Dict[str, Dict[str, object]] = {
    "MOM": {"enabled": True, "params": {"ema_fast": 12, "ema_slow": 48, "rsi_low": 42, "rsi_high": 74}},
    "VWAP": {"enabled": True, "params": {"z_entry": -2.1, "rsi_max": 38}},
    "SCALP": {"enabled": True, "params": {"imb": 0.58, "qpos": 0.62, "dspread_bps": -0.4}},
    "ARB": {"enabled": True, "params": {"min_bps": 12}},
    "VOL": {"enabled": True, "params": {"rv_gate": 0.82}},
}


@router.get("/list")
async def list_strategies() -> Dict[str, Dict[str, object]]:
    """Return configured strategies and their current state."""
    return _STRATS


@router.post("/{sid}/enable")
async def enable(sid: str) -> dict[str, bool]:
    """Enable the strategy identified by ``sid``."""
    _STRATS[sid]["enabled"] = True
    return {"ok": True}


@router.post("/{sid}/disable")
async def disable(sid: str) -> dict[str, bool]:
    """Disable the strategy identified by ``sid``."""
    _STRATS[sid]["enabled"] = False
    return {"ok": True}


@router.post("/{sid}/params")
async def set_params(sid: str, payload: StrategyParams) -> dict[str, object]:
    """Update runtime parameters for strategy ``sid``."""
    _STRATS[sid]["params"].update(payload.params or {})
    # TODO: publish hot-reload event to agents via Redis/NATS
    return {"ok": True, "params": _STRATS[sid]["params"]}
