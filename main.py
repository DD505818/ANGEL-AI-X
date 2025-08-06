
import os, asyncpg, aioredis, logging
from fastapi import FastAPI, Depends
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

app = FastAPI(title="ANGEL.AI Backend", version="0.1.0")

REQUEST_TIME = Histogram('http_request_duration_seconds', 'Request latency')
HITS = Counter('http_request_total', 'Total HTTP hits')

async def get_pg():
    url = os.getenv("POSTGRES_URL")
    conn = await asyncpg.connect(dsn=url)
    return conn

async def get_redis():
    url = os.getenv("REDIS_URL")
    return await aioredis.from_url(url, encoding="utf-8", decode_responses=True)

@app.middleware("http")
async def metrics_mw(request, call_next):
    HITS.inc()
    with REQUEST_TIME.time():
        return await call_next(request)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
