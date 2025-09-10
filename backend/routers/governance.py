"""Governance control-plane API."""
from __future__ import annotations

import hashlib
import json

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["governance"])


class Control(BaseModel):
    """Signed control command."""

    action: str
    reason: str | None = None
    signature: str
    timestamp: float


def valid_sig(payload: dict[str, object], signature: str, secret: str) -> bool:
    """Check whether ``signature`` matches SHA256 hash of payload and secret."""
    body = json.dumps(payload, sort_keys=True).encode()
    want = hashlib.sha256(secret.encode() + body).hexdigest()
    return want == signature


@router.post("/kill")
async def kill(_: Control) -> dict[str, str]:
    """Halt trading activities."""
    # TODO: verify signature with governance secret and publish halt event
    return {"ok": True, "action": "halted"}


@router.post("/resume")
async def resume(_: Control) -> dict[str, str]:
    """Resume trading activities."""
    # TODO: verify signature with governance secret and publish resume event
    return {"ok": True, "action": "resumed"}
