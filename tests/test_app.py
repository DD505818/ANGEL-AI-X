from __future__ import annotations

import os
import asyncio
import sys
from pathlib import Path

import pytest

# ensure local app package is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient

os.environ["POSTGRES_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["JWT_SECRET"] = "testsecret"

from app.auth import get_password_hash
from app.db import session_scope, init_db
from app.models import User
from main import app


@pytest.fixture(autouse=True)
def no_redis(monkeypatch):
    async def dummy_publish(*args, **kwargs):
        return None

    monkeypatch.setattr("app.redis_streams.publish", dummy_publish);
    monkeypatch.setattr("main.publish", dummy_publish)


@pytest.fixture(scope="module")
def client() -> TestClient:
    asyncio.get_event_loop().run_until_complete(init_db())

    async def create_user() -> None:
        async with session_scope() as session:
            user = User(username="alice", hashed_password=get_password_hash("wonder"), role="trader")
            session.add(user)
            await session.commit()

    asyncio.get_event_loop().run_until_complete(create_user())
    with TestClient(app) as c:
        yield c


def test_health(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_auth_and_order_flow(client: TestClient) -> None:
    token_resp = client.post("/auth/token", data={"username": "alice", "password": "wonder"})
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]
    order_resp = client.post(
        "/orders",
        json={
            "symbol": "AAPL",
            "price": 100.0,
            "capital": 1000.0,
            "win_prob": 0.6,
            "win_loss_ratio": 1.5,
            "var_limit": 0.5,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert order_resp.status_code == 200
    assert "quantity" in order_resp.json()
