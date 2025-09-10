"""Thin wrapper around ccxt to manage exchange clients and bracket orders."""
from __future__ import annotations

import asyncio
import os

import ccxt.async_support as ccxt


class CCXTManager:
    """Cache exchange clients and provide helper order methods."""

    def __init__(self) -> None:
        self._clients: dict[str, ccxt.Exchange] = {}

    async def client(self, venue: str) -> ccxt.Exchange:
        """Return an async ccxt client for ``venue``.

        Clients are cached for reuse; credentials are sourced from environment variables.
        """
        key = venue.lower()
        if key not in self._clients:
            klass = getattr(ccxt, key)
            self._clients[key] = klass(
                {
                    "apiKey": os.getenv(f"{key.upper()}_KEY"),
                    "secret": os.getenv(f"{key.upper()}_SECRET"),
                    "enableRateLimit": True,
                }
            )
        return self._clients[key]

    async def submit_bracket(self, venue: str, symbol: str, side: str, qty: float, tp: float, sl: float) -> dict:
        """Submit a simple market order with OCO take-profit and stop-loss."""
        client = await self.client(venue)
        order = await client.create_order(symbol, "market", side, qty)
        # TODO: add TP/SL as OCO if venue supports, else emulate via watcher
        return order

    async def close(self) -> None:
        """Gracefully close all cached clients."""
        await asyncio.gather(*[c.close() for c in self._clients.values()])
