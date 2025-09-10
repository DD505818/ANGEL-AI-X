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
