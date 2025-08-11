"""Async market data feed with reconnection and throttling."""
from __future__ import annotations

import asyncio
import json
from typing import Awaitable, Callable

import websockets


async def stream_quotes(
    url: str,
    handler: Callable[[dict], Awaitable[None]],
    throttle: float = 0.1,
) -> None:
    """Stream JSON quotes from ``url`` and pass to ``handler``.

    Reconnects on failure with exponential backoff.
    """
    delay = 1.0
    while True:
        try:
            async with websockets.connect(url) as ws:
                delay = 1.0
                async for msg in ws:
                    await handler(json.loads(msg))
                    await asyncio.sleep(throttle)
        except Exception:
            await asyncio.sleep(delay)
            delay = min(delay * 2, 60.0)
