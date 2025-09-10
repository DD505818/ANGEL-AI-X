from fastapi import APIRouter, HTTPException, Header
from redis import Redis
from app.services.idempotency import IdemStore
from app.services.risk import RiskState, pretrade_gate
from .schemas import KillReq, OrderReq, Portfolio

router = APIRouter()
risk_state = RiskState()
r = Redis.from_url("redis://redis:6379/0")
idem = IdemStore(r)

@router.get("/healthz")
async def health(): return {"ok": True}

@router.get("/v1/portfolio", response_model=Portfolio)
async def portfolio():
    return {"equity": 1_000_000.0, "positions": []}

@router.post("/v1/risk/kill")
async def kill(req: KillReq):
    risk_state.kill = bool(req.enabled); return {"enabled": risk_state.kill}

@router.post("/v1/order")
async def order(req: OrderReq, x_idempotency_key: str = Header(...)):
    if idem.seen(x_idempotency_key): raise HTTPException(status_code=409, detail="DUPLICATE")
    try:
        pretrade_gate(risk_state)
    except RuntimeError as e:
        raise HTTPException(status_code=403, detail=str(e))
    # Execution stub; integrate venue routing here
    return {"accepted": True, "client_order_id": req.client_order_id}
