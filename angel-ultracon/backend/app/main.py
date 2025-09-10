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
