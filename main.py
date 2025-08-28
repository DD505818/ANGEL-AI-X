import logging
import os
from typing import AsyncIterator, Callable

import aioredis
import asyncpg
from aioredis import Redis
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

app = FastAPI(title="ANGEL.AI Backend", version="0.1.0")

REQUEST_TIME = Histogram("http_request_duration_seconds", "Request latency")
HITS = Counter("http_request_total", "Total HTTP hits")


@app.on_event("startup")
async def startup() -> None:
    """Initialize shared connection pools."""
    pg_url = os.getenv("POSTGRES_URL")
    redis_url = os.getenv("REDIS_URL")
    try:
        app.state.pg_pool = await asyncpg.create_pool(dsn=pg_url, min_size=1, max_size=10)
        app.state.redis = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    except Exception:
        logger.exception("Failed to initialize dependencies")
        raise


@app.on_event("shutdown")
async def shutdown() -> None:
    """Close connection pools on shutdown."""
    await app.state.pg_pool.close()
    await app.state.redis.close()


async def get_pg() -> AsyncIterator[asyncpg.Connection]:
    """Yield a PostgreSQL connection from the pool."""
    try:
        async with app.state.pg_pool.acquire() as conn:
            yield conn
    except Exception:
        logger.exception("PostgreSQL operation failed")
        raise


async def get_redis() -> AsyncIterator[Redis]:
    """Yield the Redis client instance."""
    try:
        yield app.state.redis
    except Exception:
        logger.exception("Redis operation failed")
        raise


@app.middleware("http")
async def metrics_mw(request: Request, call_next: Callable) -> Response:
    """Record metrics for each HTTP request."""
    HITS.inc()
    with REQUEST_TIME.time():
        return await call_next(request)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> Response:
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type="text/plain")
