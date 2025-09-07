import httpx
import pytest

from api.app.webhooks import post_webhook


@pytest.mark.asyncio
async def test_post_webhook(monkeypatch):
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.content == b'{"a": 1}'
        return httpx.Response(200)

    transport = httpx.MockTransport(handler)
    client = httpx.AsyncClient(transport=transport)

    monkeypatch.setenv("WEBHOOK_URL", "http://test")
    monkeypatch.setattr("api.app.webhooks.httpx.AsyncClient", lambda **_: client)

    await post_webhook({"a": 1})
    await client.aclose()
