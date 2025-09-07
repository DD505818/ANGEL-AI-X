"""Webhook dispatch utilities."""
from __future__ import annotations

import os
from typing import Any, Dict

import httpx


async def post_webhook(payload: Dict[str, Any]) -> None:
    """Send payload to configured webhook URL."""

    url = os.getenv("WEBHOOK_URL")
    if not url:
        raise RuntimeError("WEBHOOK_URL not configured")
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
