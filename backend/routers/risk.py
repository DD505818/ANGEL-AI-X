"""Risk analytics endpoints."""
from typing import List

from fastapi import APIRouter

from backend.services import risk as risk_svc

router = APIRouter(tags=["risk"])


@router.post("/kelly")
async def kelly(edge: float, variance: float, prev_risk: float) -> dict[str, float]:
    """Calculate adjusted Kelly fraction."""
    frac = risk_svc.kelly_two_thirds(edge, variance, prev_risk)
    return {"fraction": frac}


@router.post("/esd")
async def esd(spreads: List[float]) -> dict[str, bool]:
    """Detect extreme studentized deviation on the last spread value."""
    return {"flag": risk_svc.esd_last_z(spreads)}
