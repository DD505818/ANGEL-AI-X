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
