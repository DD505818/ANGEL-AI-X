"""ANGEL.AI Backend application."""
from __future__ import annotations

import logging
from typing import Dict

from fastapi import Depends, FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.auth import login, require_role
from app.db import get_session, init_db
from app.models import Fill, Order, RiskMetric, Sentiment, Signal
from app.redis_streams import StreamChannel, publish
from app.scheduler import start_scheduler
from app.schemas import FillIn, OrderIn, RiskMetricIn, SentimentIn, SignalIn
from app.websocket import router as ws_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ANGEL.AI Backend", version="0.2.0")

REQUEST_TIME = Histogram("http_request_duration_seconds", "Request latency")
HITS = Counter("http_request_total", "Total HTTP hits")


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
    start_scheduler()


@app.middleware("http")
async def metrics_mw(request, call_next):
    HITS.inc()
    with REQUEST_TIME.time():
        return await call_next(request)


@app.post("/auth/token")
async def auth_token(token=Depends(login)):
    return token


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> Response:
    return Response(generate_latest(), media_type="text/plain")


@app.post("/signals", dependencies=[Depends(require_role("analyst"))])
async def create_signal(payload: SignalIn, session: AsyncSession = Depends(get_session)) -> Dict[str, int]:
    """Store and publish trading signals."""
    signal = Signal(**payload.dict())
    session.add(signal)
    await session.flush()
    await publish(StreamChannel.SIGNAL, {"id": str(signal.id), **payload.dict()})
    return {"id": signal.id}


@app.post("/orders", dependencies=[Depends(require_role("trader"))])
async def create_order(payload: OrderIn, session: AsyncSession = Depends(get_session)) -> Dict[str, float]:
    """Risk-managed order creation with Kelly sizing."""
    kelly_fraction = payload.win_prob - (1 - payload.win_prob) / payload.win_loss_ratio
    quantity = (payload.capital * kelly_fraction) / payload.price
    max_risk = payload.capital * payload.var_limit
    if quantity * payload.price > max_risk:
        raise HTTPException(status_code=400, detail="Risk limit exceeded")
    order = Order(symbol=payload.symbol, quantity=quantity, price=payload.price, status="NEW")
    session.add(order)
    await session.flush()
    await publish(StreamChannel.ORDER, {"id": str(order.id), "symbol": payload.symbol, "quantity": f"{quantity}", "price": f"{payload.price}"})
    return {"id": order.id, "quantity": quantity}


@app.post("/fills", dependencies=[Depends(require_role("trader"))])
async def create_fill(payload: FillIn, session: AsyncSession = Depends(get_session)) -> Dict[str, int]:
    """Record fill events and publish to subscribers."""
    fill = Fill(**payload.dict())
    session.add(fill)
    await session.flush()
    await publish(StreamChannel.FILL, {"id": str(fill.id), **payload.dict()})
    return {"id": fill.id}


@app.post("/risk", dependencies=[Depends(require_role("risk"))])
async def create_risk(payload: RiskMetricIn, session: AsyncSession = Depends(get_session)) -> Dict[str, int]:
    """Persist risk metrics and publish them."""
    metric = RiskMetric(**payload.dict())
    session.add(metric)
    await session.flush()
    await publish(StreamChannel.RISK, {"id": str(metric.id), **payload.dict()})
    return {"id": metric.id}


@app.post("/sentiment", dependencies=[Depends(require_role("analyst"))])
async def create_sentiment(payload: SentimentIn, session: AsyncSession = Depends(get_session)) -> Dict[str, int]:
    """Store sentiment data and publish it."""
    sentiment = Sentiment(**payload.dict())
    session.add(sentiment)
    await session.flush()
    await publish(StreamChannel.SENTIMENT, {"id": str(sentiment.id), **payload.dict()})
    return {"id": sentiment.id}


app.include_router(ws_router)
