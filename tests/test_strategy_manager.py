import pytest

from datetime import datetime

from app.agents.admin import AdminAgent
from app.agents.base import AgentKPI, Signal, TradingAgent
from app.agents.strategy_manager import StrategyManager


class DummyAgent(TradingAgent):
    async def generate_signal(self) -> Signal:
        return Signal(
            schema_version=1,
            timestamp=datetime.utcnow(),
            symbol="BTC/USDT",
            action="BUY",
            confidence=0.9,
            size=1.0,
        )

    async def update_state(self, market_data):  # pragma: no cover - not used
        self._state.update(market_data)


@pytest.mark.asyncio
async def test_manager_aggregates():
    admin = AdminAgent()
    agent = DummyAgent("a", admin, kpi=AgentKPI(1.0, 0.5, 0.1))
    mgr = StrategyManager()
    mgr.register(agent)
    signals = await mgr.generate()
    assert signals["BTC/USDT"].action == "BUY"
