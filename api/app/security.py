"""Authentication and network security utilities."""
from __future__ import annotations

import os
from ipaddress import ip_address, ip_network
from typing import List

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class JWTBearer(HTTPBearer):
    """Dependency that validates JWT bearer tokens."""

    def __init__(self) -> None:  # noqa: D401 - short and clear
        super().__init__()

    async def __call__(self, request: Request) -> str:
        creds: HTTPAuthorizationCredentials | None = await super().__call__(request)
        if creds is None:
            raise HTTPException(status_code=403, detail="Missing authorization")
        try:
            secret = get_jwt_secret()
            jwt.decode(creds.credentials, secret, algorithms=["HS256"])
        except jwt.PyJWTError as exc:  # pragma: no cover - decode raises subclasses
            raise HTTPException(status_code=403, detail="Invalid token") from exc
        return creds.credentials


def get_jwt_secret() -> str:
    """Return the JWT secret from the environment."""

    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET not configured")
    return secret


def ip_allowlist() -> List[ip_network]:
    """Parse the IP_ALLOWLIST env var into networks."""

    raw = os.getenv("IP_ALLOWLIST", "")
    nets: List[ip_network] = []
    for item in [x.strip() for x in raw.split(",") if x.strip()]:
        nets.append(ip_network(item, strict=False))
    return nets


async def allowlist_middleware(request: Request, call_next):
    """Middleware enforcing IP allowlist."""

    client_ip = ip_address(request.client.host)
    networks = ip_allowlist()
    if networks and not any(client_ip in net for net in networks):
        raise HTTPException(status_code=403, detail="IP not allowed")
    return await call_next(request)


def create_jwt(payload: dict) -> str:
    """Create a signed JWT using the configured secret."""

    return jwt.encode(payload, get_jwt_secret(), algorithm="HS256")
