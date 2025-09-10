set -euo pipefail

APP=angel-ultracon
mkdir -p $APP && cd $APP

cat > .env <<'ENV'
NATS_URL=nats://nats:4222
REDIS_URL=redis://redis:6379/0
# Base64-encoded Ed25519 public key (see keygen below)
ED25519_PUBKEY=
JWT_SECRET=change-me
ALLOW_ORIGINS=http://localhost:3000
ENV

cat > docker-compose.yml <<'YML'
version: "3.9"
services:
  nats:
    image: nats:2.10
    command: ["-js","-sd","/data"]
    ports: ["4222:4222"]
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
  backend:
    build: ./backend
    env_file: .env
    depends_on: [nats, redis]
    ports: ["8000:8000"]
    security_opt: ["no-new-privileges:true"]
    read_only: true
    tmpfs: ["/tmp"]
  web:
    build: ./web
    env_file: .env
    depends_on: [backend]
    ports: ["3000:3000"]
YML

mkdir -p backend/app/{api,services,transport,tests} web/app web/lib web/components

# ================= BACKEND =================
cat > backend/requirements.txt <<'REQ'
fastapi==0.111.0
uvicorn[standard]==0.30.0
pydantic==2.7.4
redis==5.0.4
nats-py==2.6.0
PyNaCl==1.5.0
orjson==3.10.3
jsonschema==4.23.0
REQ

cat > backend/Dockerfile <<'DF'
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
ENV PORT=8000
USER nobody
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--proxy-headers"]
DF

cat > backend/app/config.py <<'PY'
from pydantic import BaseModel
import os
class Settings(BaseModel):
    nats_url: str = os.getenv("NATS_URL","nats://localhost:4222")
    redis_url: str = os.getenv("REDIS_URL","redis://localhost:6379/0")
    ed25519_pubkey: str = os.getenv("ED25519_PUBKEY","")
    jwt_secret: str = os.getenv("JWT_SECRET","dev")
    allow_origins: list[str] = os.getenv("ALLOW_ORIGINS","http://localhost:3000").split(",")
settings = Settings()
PY

cat > backend/app/services/idempotency.py <<'PY'
import time
from redis import Redis
class IdemStore:
    def __init__(self, r: Redis, ttl_s: int = 86400):
        self.r = r; self.ttl_s = ttl_s
    def seen(self, key: str) -> bool:
        # SETNX; if set, it's new. Expire for 1d.
        is_new = self.r.setnx(f"idem:{key}", int(time.time()))
        if is_new: self.r.expire(f"idem:{key}", self.ttl_s)
        return not is_new
PY

cat > backend/app/services/risk.py <<'PY'
from dataclasses import dataclass
@dataclass
class RiskState:
    kill: bool = False
    max_dd: float = 0.008
    dd: float = 0.0
def pretrade_gate(state: RiskState) -> None:
    if state.kill: raise RuntimeError("RISK_HALT")
    if state.dd > state.max_dd: raise RuntimeError("MAX_DD_BREACH")
PY

cat > backend/app/services/router.py <<'PY'
def score(latency_ms: float, spread_bps: float, fee_bps: float, slip_bps: float, queue_pos: float=0.0) -> float:
    # Lower is better
    return fee_bps + slip_bps + 0.5*latency_ms + 0.1*spread_bps + 0.2*queue_pos
PY

cat > backend/app/transport/schemas.py <<'PY'
envelope_schema = {
  "type": "object",
  "required": ["msg_id","ts","issuer","type","scope","targets","ttl_ms","hysteresis_s","options","sig"],
  "properties": {
    "msg_id": {"type":"string"},
    "ts": {"type":"integer"},
    "issuer": {"type":"string"},
    "type": {"type":"string", "enum":["halt","resume","cancel_all","gear_set","gear_restore"]},
    "scope": {"type":"string"},
    "targets": {"type":"array","items":{"type":"string"}},
    "ttl_ms": {"type":"integer","minimum":1},
    "hysteresis_s": {"type":"integer","minimum":0},
    "options": {"type":"object"},
    "sig": {"type":"string"}
  },
  "additionalProperties": False
}
PY

cat > backend/app/transport/nats_bus.py <<'PY'
import json, nacl.signing, nacl.encoding
from jsonschema import validate
from nats.aio.client import Client as NATS
from app.config import settings
from .schemas import envelope_schema

SUBJ_BASE='angel.trading'

def verify_signature(env: dict) -> bool:
    if not settings.ed25519_pubkey: return False
    try:
        vk = nacl.signing.VerifyKey(settings.ed25519_pubkey, encoder=nacl.encoding.Base64Encoder)
        sig = nacl.encoding.Base64Encoder.decode(env['sig'])
        payload = {k: env[k] for k in env if k!='sig'}
        msg = json.dumps(payload, separators=(',',':'), sort_keys=True).encode()
        vk.verify(msg, sig); return True
    except Exception:
        return False

async def connect():
    nc = NATS()
    await nc.connect(servers=[settings.nats_url])
    return nc

async def subscribe_control(nc, handler):
    async def cb(msg):
        env = json.loads(msg.data)
        validate(instance=env, schema=envelope_schema)
        if not verify_signature(env): return
        await handler(env)
    for c in ("halt","resume","cancel_all","gear_set","gear_restore"):
        await nc.subscribe(f"{SUBJ_BASE}.{c}.v1", cb=cb)
PY

cat > backend/app/transport/redis_bus.py <<'PY'
import json
import redis
from app.config import settings
r = redis.Redis.from_url(settings.redis_url, decode_responses=True)
def publish_cmd(env: dict): r.xadd("angel:trading:commands", {"env": json.dumps(env, separators=(',',':'))})
def ack_cmd(id: str, status: str): r.xadd("angel:trading:acks", {"id": id, "status": status})
def last_offset(stream: str)->str|None:
    return r.get(f"offset:{stream}")
def set_offset(stream: str, off: str):
    r.set(f"offset:{stream}", off)
PY

cat > backend/app/api/schemas.py <<'PY'
from pydantic import BaseModel, Field
class KillReq(BaseModel): enabled: bool
class OrderReq(BaseModel):
    client_order_id: str = Field(min_length=8)
    symbol: str
    side: str  # BUY/SELL
    qty: float
    price: float|None = None
class Portfolio(BaseModel):
    equity: float
    positions: list[dict]
PY

cat > backend/app/api/routes.py <<'PY'
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
PY

cat > backend/app/main.py <<'PY'
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import router
from app.transport.nats_bus import connect, subscribe_control
from app.transport.redis_bus import publish_cmd, ack_cmd

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=settings.allow_origins,
                   allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(router)

@app.on_event("startup")
async def start():
    app.state.nc = await connect()
    async def handler(env: dict):
        publish_cmd(env); ack_cmd(env["msg_id"], "OK")
    await subscribe_control(app.state.nc, handler)

@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    await ws.send_json({"type":"welcome"})
PY

# ================= FRONTEND =================
cat > web/Dockerfile <<'DF'
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund
FROM node:20-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules node_modules
COPY . .
RUN npm run build
FROM node:20-alpine
WORKDIR /app
ENV HOST=0.0.0.0 PORT=3000
COPY --from=build /app ./
EXPOSE 3000
CMD ["npm","start"]
DF

cat > web/package.json <<'PKG'
{
  "name": "angel-web",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start -p 3000",
    "lint": "eslint ."
  },
  "dependencies": {
    "next": "14.2.4",
    "react": "18.3.1",
    "react-dom": "18.3.1"
  }
}
PKG

cat > web/next.config.js <<'JS'
module.exports = { reactStrictMode: true };
JS

cat > web/app/page.tsx <<'TS'
"use client";
import { useEffect, useRef, useState } from "react";

function useWS(url: string) {
  const [open, setOpen] = useState(false);
  const [msg, setMsg] = useState<any>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef(0);
  const hbRef = useRef<any>(null);
  const ping = () => { wsRef.current?.send('{"t":"ping"}'); hbRef.current=setTimeout(reconnect, 4000); };
  const reconnect = () => {
    try { wsRef.current?.close(); } catch {}
    const backoff = Math.min(1000 * (2 ** retryRef.current++), 15000);
    setTimeout(connect, backoff);
  };
  const connect = () => {
    const ws = new WebSocket(url); wsRef.current=ws;
    ws.onopen = () => { retryRef.current=0; setOpen(true); clearTimeout(hbRef.current); ping(); };
    ws.onmessage = (e) => { clearTimeout(hbRef.current); setMsg(e.data); ping(); };
    ws.onclose = () => { setOpen(false); reconnect(); };
    ws.onerror = () => { setOpen(false); reconnect(); };
  };
  useEffect(() => { connect(); return () => { clearTimeout(hbRef.current); wsRef.current?.close(); }; }, [url]);
  return { open, msg };
}

async function post(path: string, body: any, idem: string) {
  const res = await fetch(`http://localhost:8000${path}`, {
    method: "POST",
    headers: { "Content-Type":"application/json", "X-Idempotency-Key": idem },
    body: JSON.stringify(body)
  });
  return res.json();
}

export default function Home() {
  const { open } = useWS("ws://localhost:8000/ws");
  const [halt, setHalt] = useState(false);
  return (
    <main style={{padding:20,fontFamily:"Inter, sans-serif"}}>
      <h1>ANGEL.AI — Ultracon Control</h1>
      <p>WS: {open ? "connected" : "reconnecting..."}</p>
      <button onClick={async ()=>{
        const r = await post("/v1/risk/kill", {enabled: !halt}, crypto.randomUUID());
        setHalt(r.enabled);
      }}>{halt ? "Resume" : "Kill"} Trading</button>
      <button onClick={async ()=>{
        const r = await post("/v1/order", {client_order_id: crypto.randomUUID(), symbol:"BTC-USD", side:"BUY", qty:0.01}, crypto.randomUUID());
        alert(JSON.stringify(r));
      }}>Test Order</button>
    </main>
  );
}
TS

# ================= TESTS =================
cat > backend/app/tests/acceptance.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
curl -s http://localhost:8000/healthz | grep '"ok": true'
# Risk halt authority
curl -s -X POST http://localhost:8000/v1/risk/kill -H 'Content-Type: application/json' -d '{"enabled":true}' | grep '"enabled": true'
# Order blocked under halt
code=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:8000/v1/order \
  -H 'Content-Type: application/json' -H "X-Idempotency-Key: test-1" \
  -d '{"client_order_id":"abc12345","symbol":"BTC-USD","side":"BUY","qty":0.01}')
test "$code" = "403"
# Idempotency duplicate
curl -s -X POST http://localhost:8000/v1/risk/kill -H 'Content-Type: application/json' -d '{"enabled":false}'
curl -s -X POST http://localhost:8000/v1/order -H 'Content-Type: application/json' -H "X-Idempotency-Key: dup-1" \
  -d '{"client_order_id":"abc12346","symbol":"BTC-USD","side":"BUY","qty":0.01}' | grep '"accepted": true'
code=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:8000/v1/order \
  -H 'Content-Type: application/json' -H "X-Idempotency-Key: dup-1" \
  -d '{"client_order_id":"abc12346","symbol":"BTC-USD","side":"BUY","qty":0.01}')
test "$code" = "409"
echo "ACCEPTANCE OK"
SH
chmod +x backend/app/tests/acceptance.sh

# Build & up
docker compose build
docker compose up -d
sleep 5
bash backend/app/tests/acceptance.sh
echo "Running web on http://localhost:3000  | API http://localhost:8000"
