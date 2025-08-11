"""WebSocket endpoints streaming Redis events to clients."""
from __future__ import annotations


from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .redis_streams import StreamChannel, subscribe

router = APIRouter()


@router.websocket("/ws/{stream}")
async def websocket_endpoint(websocket: WebSocket, stream: StreamChannel) -> None:
    """Stream updates from Redis to the WebSocket client."""
    await websocket.accept()
    subscriber = subscribe(stream)
    try:
        async for message in subscriber:
            await websocket.send_json(message)
    except WebSocketDisconnect:
        pass
    finally:
        await websocket.close()
