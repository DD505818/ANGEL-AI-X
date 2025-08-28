
"""FastAPI application exposing health and metrics endpoints."""

from __future__ import annotations

import logging
import os
from typing import AsyncGenerator

import aioredis
import asyncpg
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

logger = logging.getLogger(__name__)


app = FastAPI(title="ANGEL.AI Backend", version="0.1.0")

REQUEST_TIME = Histogram("http_request_duration_seconds", "Request latency")
HITS = Counter("http_request_total", "Total HTTP hits")


@app.on_event("startup")
async def startup() -> None:
    """Create connection pools for Postgres and Redis."""
    try:
        app.state.pg_pool = await asyncpg.create_pool(dsn=os.environ["POSTGRES_URL"])
    except Exception as exc:  # pragma: no cover - logs for operators
        logger.error("Postgres pool creation failed", exc_info=exc)
        raise

    try:
        app.state.redis = aioredis.from_url(
            os.environ["REDIS_URL"], encoding="utf-8", decode_responses=True
        )
    except Exception as exc:  # pragma: no cover - logs for operators
        logger.error("Redis client creation failed", exc_info=exc)
        raise


@app.on_event("shutdown")
async def shutdown() -> None:
    """Close connection pools on shutdown."""
    await app.state.pg_pool.close()
    await app.state.redis.close()


async def get_pg() -> AsyncGenerator[asyncpg.Connection, None]:
    """Yield a Postgres connection from the pool."""
    async with app.state.pg_pool.acquire() as conn:
        yield conn


async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """Yield the Redis client."""
    yield app.state.redis


@app.middleware("http")
async def metrics_mw(request, call_next):
    """Collect Prometheus metrics for each request."""
    HITS.inc()
    with REQUEST_TIME.time():
        return await call_next(request)


@app.get("/health")
async def health() -> dict[str, str]:
    """Basic liveness probe verifying database connectivity."""
    try:
        async with app.state.pg_pool.acquire() as conn:
            await conn.execute("SELECT 1")
    except Exception as exc:  # pragma: no cover - logs for operators
        logger.exception("Health check failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="database error")
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> Response:
    """Expose Prometheus metrics."""
    return Response(generate_latest(), media_type="text/plain")
