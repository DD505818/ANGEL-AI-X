import logging
import os
from typing import AsyncIterator, Callable

import redis.asyncio as aioredis
import asyncpg
from redis.asyncio import Redis
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest
from starlette.requests import Request
from starlette.responses import Response
import jwt

logger = logging.getLogger(__name__)

app = FastAPI(title="ANGEL.AI Backend", version="0.1.0")

JWT_SECRET = os.getenv("JWT_SECRET", "")
ALLOWLIST = {ip.strip() for ip in os.getenv("IP_ALLOWLIST", "").split(",") if ip.strip()}

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


@app.middleware("http")
async def security_mw(request: Request, call_next: Callable) -> Response:
    """Enforce IP allowlist and JWT auth."""
    client_ip = request.client.host
    if ALLOWLIST and client_ip not in ALLOWLIST:
        return JSONResponse({"detail": "IP not allowed"}, status_code=status.HTTP_403_FORBIDDEN)
    if request.url.path not in {"/health", "/metrics"}:
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JSONResponse({"detail": "Missing token"}, status_code=status.HTTP_401_UNAUTHORIZED)
        token = auth.split(" ", 1)[1]
        try:
            jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.PyJWTError:
            return JSONResponse({"detail": "Invalid token"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return await call_next(request)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> Response:
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type="text/plain")


@app.get("/secure-ping")
async def secure_ping() -> dict[str, str]:
    """Endpoint that requires authentication."""
    return {"status": "secure"}
