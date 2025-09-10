"""WebSocket endpoints providing live dashboard tiles."""
from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, WebSocket

router = APIRouter(tags=["ws"])


@router.websocket("/tiles")
async def tiles(ws: WebSocket) -> None:
    """Stream synthetic updates to connected dashboards."""
    await ws.accept()
    try:
        while True:
            payload = {
                "orders": [],
                "fills": [],
                "pnl_tick": {"equity": 101_234.5, "dd": 0.003},
                "agent_status": {"MOM": "live", "VWAP": "live", "SCALP": "live", "ARB": "live", "VOL": "live"},
            }
            await ws.send_text(json.dumps(payload))
            await asyncio.sleep(1.0)
    except Exception:  # noqa: BLE001
        await ws.close()
