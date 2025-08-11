"""Redis Stream publishers and subscribers."""
from __future__ import annotations

from enum import Enum
from typing import AsyncGenerator, Dict

import redis.asyncio as aioredis

from .config import settings


class StreamChannel(str, Enum):
    SIGNAL = "signals"
    ORDER = "orders"
    FILL = "fills"
    RISK = "risk"
    SENTIMENT = "sentiment"


async def get_redis() -> aioredis.Redis:
    """Create a Redis connection."""
    return await aioredis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)


async def publish(stream: StreamChannel, message: Dict[str, str]) -> None:
    """Publish a message to a Redis stream."""
    redis = await get_redis()
    try:
        await redis.xadd(stream.value, message)
    finally:
        await redis.close()


async def subscribe(stream: StreamChannel, last_id: str = "$") -> AsyncGenerator[Dict[str, str], None]:
    """Subscribe to a Redis stream yielding new messages."""
    redis = await get_redis()
    try:
        while True:
            response = await redis.xread({stream.value: last_id}, block=1000, count=10)
            if response:
                for _, messages in response:
                    for msg_id, data in messages:
                        last_id = msg_id
                        yield data
    finally:
        await redis.close()
