import pytest

from api.app.wallet.ccxt_wallet import CCXTWallet


@pytest.mark.asyncio
async def test_wallet_requires_credentials(monkeypatch):
    monkeypatch.delenv("CCXT_API_KEY", raising=False)
    monkeypatch.delenv("CCXT_API_SECRET", raising=False)
    with pytest.raises(RuntimeError):
        CCXTWallet()


@pytest.mark.asyncio
async def test_wallet_init(monkeypatch):
    monkeypatch.setenv("CCXT_API_KEY", "k")
    monkeypatch.setenv("CCXT_API_SECRET", "s")
    wallet = CCXTWallet()
    assert wallet.exchange.apiKey == "k"
    await wallet.close()
