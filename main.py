import logging
import os
from typing import AsyncGenerator, Awaitable, Callable

import aioredis
import asyncpg
from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI(title="ANGEL.AI Backend", version="0.1.0")

logger = logging.getLogger(__name__)

REQUEST_TIME = Histogram("http_request_duration_seconds", "Request latency")
HITS = Counter("http_request_total", "Total HTTP hits")


@app.on_event("startup")
async def startup() -> None:
    """Initialize resource pools for database and cache."""
    pg_url = os.getenv("POSTGRES_URL")
    redis_url = os.getenv("REDIS_URL")

    try:
        app.state.pg_pool = await asyncpg.create_pool(dsn=pg_url)
    except Exception as exc:  # pragma: no cover - connection may fail in CI
        logger.error("Postgres connection failed", exc_info=exc)
        raise

    try:
        app.state.redis = aioredis.from_url(
            redis_url, encoding="utf-8", decode_responses=True
        )
    except Exception as exc:  # pragma: no cover - connection may fail in CI
        logger.error("Redis connection failed", exc_info=exc)
        raise


@app.on_event("shutdown")
async def shutdown() -> None:
    """Gracefully close resource pools."""
    await app.state.pg_pool.close()
    await app.state.redis.close()


async def get_pg() -> AsyncGenerator[asyncpg.Connection, None]:
    """Yield a Postgres connection from the pool."""
    async with app.state.pg_pool.acquire() as conn:
        yield conn


async def get_redis() -> aioredis.Redis:
    """Return the Redis client instance."""
    return app.state.redis


@app.middleware("http")
async def metrics_mw(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Collect request metrics for Prometheus."""
    HITS.inc()
    with REQUEST_TIME.time():
        return await call_next(request)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> Response:
    """Expose Prometheus metrics."""
    return Response(generate_latest(), media_type="text/plain")
