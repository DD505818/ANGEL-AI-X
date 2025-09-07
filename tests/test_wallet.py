"""CCXT wallet configuration tests."""

import pytest

from api.wallet import CCXTWallet


@pytest.mark.asyncio
async def test_wallet_initializes(monkeypatch) -> None:
    monkeypatch.setenv("CCXT_API_KEY", "k")
    monkeypatch.setenv("CCXT_API_SECRET", "s")
    wallet = CCXTWallet()
    assert wallet.client.apiKey == "k"
    await wallet.close()
