"""CCXT wallet utilities for order execution."""

import os
from typing import Any, Dict

import ccxt.async_support as ccxt


class CCXTWallet:
    """Thin async wrapper around ccxt exchanges."""

    def __init__(self, exchange: str = "binance") -> None:
        key = os.getenv("CCXT_API_KEY")
        secret = os.getenv("CCXT_API_SECRET")
        self.client = getattr(ccxt, exchange)({
            "apiKey": key,
            "secret": secret,
            "enableRateLimit": True,
        })

    async def fetch_balance(self) -> Dict[str, Any]:
        """Fetch account balances."""
        try:
            return await self.client.fetch_balance()
        except ccxt.BaseError as exc:  # pragma: no cover - network errors
            raise RuntimeError("Balance fetch failed") from exc

    async def create_order(
        self, symbol: str, side: str, amount: float, price: float | None = None
    ) -> Dict[str, Any]:
        """Create an order with basic rate-limit handling."""
        order_type = "limit" if price is not None else "market"
        try:
            return await self.client.create_order(symbol, order_type, side, amount, price)
        except ccxt.RateLimitExceeded as exc:  # pragma: no cover - depends on exchange load
            raise RuntimeError("Rate limit exceeded") from exc
        except ccxt.BaseError as exc:  # pragma: no cover
            raise RuntimeError("Order failed") from exc

    async def close(self) -> None:
        """Close underlying exchange client."""
        await self.client.close()
