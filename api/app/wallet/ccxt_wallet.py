"""CCXT-powered wallet utilities with basic rate-limit handling."""
from __future__ import annotations

import os
from typing import Any, Dict

import ccxt.async_support as ccxt


class CCXTWallet:
    """Interact with an exchange wallet using CCXT."""

    def __init__(self) -> None:
        exchange_id = os.getenv("CCXT_EXCHANGE", "binance")
        api_key = os.getenv("CCXT_API_KEY")
        api_secret = os.getenv("CCXT_API_SECRET")
        if not api_key or not api_secret:
            raise RuntimeError("CCXT API credentials not configured")
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class({
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
        })

    async def balance(self) -> Dict[str, Any]:
        """Return current wallet balances."""

        return await self.exchange.fetch_balance()

    async def close(self) -> None:
        """Close underlying connections if any."""

        await self.exchange.close()
