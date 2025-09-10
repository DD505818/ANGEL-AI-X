"""Wallet related API endpoints."""
from typing import Any
import os

import ccxt.async_support as ccxt
from fastapi import APIRouter

router = APIRouter(tags=["wallet"])


@router.get("/balances")
async def balances() -> list[dict[str, Any]]:
    """Return balances from supported exchanges in USD terms."""
    venues = ["binance", "kraken", "bybit", "okx"]
    output: list[dict[str, Any]] = []
    for venue in venues:
        klass = getattr(ccxt, venue)
        client = klass(
            {
                "apiKey": os.getenv(f"{venue.upper()}_KEY"),
                "secret": os.getenv(f"{venue.upper()}_SECRET"),
                "enableRateLimit": True,
            }
        )
        try:
            balance = await client.fetch_balance()
            total_usd = 0.0
            for asset, amount in (balance.get("total") or {}).items():
                if asset in {"USD", "USDT", "USDC"}:
                    total_usd += float(amount or 0.0)
            output.append({"venue": venue.upper(), "total_usd": total_usd, "details": balance})
        finally:
            await client.close()
    return output
