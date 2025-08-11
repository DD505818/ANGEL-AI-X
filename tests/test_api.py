import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio
async def test_health(monkeypatch):
    # monkeypatch redis ping
    class DummyRedis:
        async def ping(self):
            return True
    app.state.redis = DummyRedis()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
        resp = await ac.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
