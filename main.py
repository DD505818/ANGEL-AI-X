
"""ANGEL.AI FastAPI backend with structured logging and rate limits."""

import contextvars
import logging
import os
import uuid

from redis import asyncio as aioredis
import asyncpg
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Literal
from prometheus_client import Counter, Histogram, generate_latest
from pythonjsonlogger import jsonlogger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import Response

logger = logging.getLogger("angel_ai")
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

rate_limit = os.getenv("RATE_LIMIT_REQUESTS_PER_MIN", "60")
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.getenv("REDIS_URL", "memory://"),
    default_limits=[f"{rate_limit}/minute"],
)

app = FastAPI(title="ANGEL.AI Backend", version="0.1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

REQUEST_TIME = Histogram("http_request_duration_seconds", "Request latency")
HITS = Counter("http_request_total", "Total HTTP hits")

pg_pool: asyncpg.Pool | None = None
redis_pool: aioredis.Redis | None = None
correlation_id_ctx = contextvars.ContextVar("correlation_id", default="")


@app.on_event("startup")
async def startup() -> None:
    """Initialize connection pools on startup."""
    global pg_pool, redis_pool
    pg_dsn = os.getenv("POSTGRES_URL")
    if pg_dsn:
        pg_pool = await asyncpg.create_pool(dsn=pg_dsn, min_size=1, max_size=5)
    redis_dsn = os.getenv("REDIS_URL")
    if redis_dsn and not redis_dsn.startswith("memory://"):
        redis_pool = aioredis.from_url(redis_dsn, encoding="utf-8", decode_responses=True)


@app.on_event("shutdown")
async def shutdown() -> None:
    """Close pools on shutdown."""
    if pg_pool:
        await pg_pool.close()
    if redis_pool:
        await redis_pool.close()


async def get_pg() -> asyncpg.Pool:
    """Return PostgreSQL pool or raise if not configured."""
    if pg_pool is None:
        raise RuntimeError("database not configured")
    return pg_pool


@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    """Attach correlation ID to each request and response."""
    cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    correlation_id_ctx.set(cid)
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = cid
    return response


@app.middleware("http")
async def metrics_mw(request: Request, call_next):
    """Record basic Prometheus metrics."""
    HITS.inc()
    with REQUEST_TIME.time():
        return await call_next(request)


class OrderRequest(BaseModel):
    """Order payload validated by Pydantic."""
    symbol: str
    side: Literal["buy", "sell"]
    qty: float = Field(gt=0)
    price: float | None = Field(default=None, gt=0)


@app.post("/orders")
@limiter.limit("5/minute")
async def create_order(request: Request, order: OrderRequest):
    """Accept an order after validating payload and rate limits."""
    if order.price is None:
        raise HTTPException(status_code=400, detail="limit_price_required")
    logger.info(
        "order_received",
        extra={"cid": correlation_id_ctx.get(), **order.model_dump()},
    )
    return {"status": "accepted", "correlation_id": correlation_id_ctx.get()}


@app.get("/health")
async def health() -> dict[str, str]:
    """Basic health probe."""
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> Response:
    """Expose Prometheus metrics."""
    return Response(generate_latest(), media_type="text/plain")
