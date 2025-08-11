import logging
import os
import uuid
from contextvars import ContextVar
from typing import AsyncGenerator, Literal

import asyncpg
import redis.asyncio as aioredis
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

from risk import kelly_fraction

logger = logging.getLogger("angel.backend")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(correlation_id)s %(message)s",
)
class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_ctx.get()
        return True

logger.addFilter(CorrelationIdFilter())

correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id", default="-")

app = FastAPI(title="ANGEL.AI Backend", version="0.2.0")

REQUEST_TIME = Histogram("http_request_duration_seconds", "Request latency")
HITS = Counter("http_request_total", "Total HTTP hits")

auth_scheme = HTTPBearer(auto_error=False)


class TradeRequest(BaseModel):
    symbol: str
    side: Literal["buy", "sell"]
    qty: float
    price: float


class TradeResponse(BaseModel):
    status: str
    executed_qty: float


async def get_secret(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Missing secret: {name}")
    return value


@app.on_event("startup")
async def startup() -> None:
    app.state.pg_pool = await asyncpg.create_pool(os.environ["POSTGRES_URL"])
    app.state.redis = aioredis.from_url(
        os.environ["REDIS_URL"], encoding="utf-8", decode_responses=True
    )


@app.on_event("shutdown")
async def shutdown() -> None:
    await app.state.pg_pool.close()
    await app.state.redis.close()


async def get_pg() -> AsyncGenerator[asyncpg.Connection, None]:
    async with app.state.pg_pool.acquire() as conn:
        yield conn


def get_redis() -> aioredis.Redis:
    return app.state.redis


async def authenticate(
    credentials: HTTPAuthorizationCredentials | None = Depends(auth_scheme),
) -> None:
    token = await get_secret("API_TOKEN")
    if not credentials or credentials.credentials != token:
        raise HTTPException(status_code=401, detail="Invalid token")


async def rate_limit(request: Request, redis: aioredis.Redis = Depends(get_redis)) -> None:
    limit = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
    window = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    key = f"rl:{request.client.host}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, window)
    if count > limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")


@app.middleware("http")
async def metrics_mw(request: Request, call_next):
    HITS.inc()
    cid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    token = correlation_id_ctx.set(cid)
    try:
        with REQUEST_TIME.time():
            response = await call_next(request)
        response.headers["X-Request-ID"] = cid
        return response
    finally:
        correlation_id_ctx.reset(token)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    logger.exception("Unhandled error")
    raise HTTPException(status_code=500, detail="Internal error")


@app.get("/health", response_model=dict)
async def health(redis: aioredis.Redis = Depends(get_redis)) -> dict:
    if not await redis.ping():
        raise HTTPException(status_code=503, detail="Redis unreachable")
    return {"status": "ok"}


@app.post(
    "/trade",
    response_model=TradeResponse,
    dependencies=[Depends(rate_limit), Depends(authenticate)],
)
async def trade(req: TradeRequest) -> TradeResponse:
    fraction = kelly_fraction(0.5, 1)
    executed_qty = req.qty * fraction
    return TradeResponse(status="accepted", executed_qty=executed_qty)


@app.get("/metrics")
async def metrics() -> Response:
    return Response(generate_latest(), media_type="text/plain")
