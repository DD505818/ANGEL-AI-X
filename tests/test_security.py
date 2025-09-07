import pytest
from fastapi import Request, HTTPException

from api.app.security import (
    JWTBearer,
    allowlist_middleware,
    create_jwt,
    ip_allowlist,
)


@pytest.mark.asyncio
async def test_jwt_bearer_valid(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "secret")
    token = create_jwt({"sub": "abc"})
    bearer = JWTBearer()
    scope = {
        "type": "http",
        "headers": [(b"authorization", f"Bearer {token}".encode())],
        "client": ("127.0.0.1", 1234),
    }
    request = Request(scope)
    assert await bearer(request) == token


def test_ip_allowlist(monkeypatch):
    monkeypatch.setenv("IP_ALLOWLIST", "127.0.0.1,10.0.0.0/24")
    nets = ip_allowlist()
    assert len(nets) == 2


@pytest.mark.asyncio
async def test_allowlist_blocks(monkeypatch):
    monkeypatch.setenv("IP_ALLOWLIST", "10.0.0.0/24")
    scope = {
        "type": "http",
        "client": ("11.1.1.1", 80),
        "headers": [],
    }
    request = Request(scope)
    with pytest.raises(HTTPException):
        await allowlist_middleware(request, lambda r: r)
