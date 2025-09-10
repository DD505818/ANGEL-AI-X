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
