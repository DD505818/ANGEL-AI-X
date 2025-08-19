"""Momentum-based trading agent."""

from __future__ import annotations

from collections import deque
from datetime import UTC, datetime
from typing import Any, Deque, Dict

from .admin import AdminAgent
from .base import SCHEMA_VERSION, AgentKPI, Signal, TradingAgent


class MomentumAgent(TradingAgent):
    """Simple momentum strategy relying on recent price trends."""

    def __init__(
        self,
        agent_id: str,
        admin: AdminAgent,
        *,
        kpi: AgentKPI,
        lookback: int = 5,
        capital: float = 10_000,
    ) -> None:
        super().__init__(agent_id, admin, kpi=kpi)
        self._prices: Deque[float] = deque(maxlen=lookback)
        self._capital = capital

    async def update_state(self, market_data: Dict[str, Any]) -> None:
        """Ingest latest price for momentum calculation."""
        price = market_data.get("price")
        symbol = market_data.get("symbol")
        if not isinstance(price, (int, float)) or not isinstance(symbol, str):
            raise ValueError("Invalid market data for MomentumAgent")
        self._prices.append(float(price))
        self._state["symbol"] = symbol
        self._admin.mark_updated(self.agent_id)

    async def generate_signal(self) -> Signal:
        """Generate a trading signal based on recent momentum."""
        if len(self._prices) < self._prices.maxlen:
            return Signal(
                schema_version=SCHEMA_VERSION,
                timestamp=datetime.now(UTC),
                symbol=self._state.get("symbol", ""),
                action="HOLD",
                confidence=0.0,
                size=0.0,
            )
        avg = sum(self._prices) / len(self._prices)
        last = self._prices[-1]
        edge = (last - avg) / avg
        variance = max(sum((p - avg) ** 2 for p in self._prices) / len(self._prices), 1e-6)
        size = await self._kelly_size(edge, variance, self._capital)
        action = "BUY" if edge > 0 else "SELL"
        confidence = min(abs(edge) * 10, 1.0)
        return Signal(
            schema_version=SCHEMA_VERSION,
            timestamp=datetime.now(UTC),
            symbol=self._state.get("symbol", ""),
            action=action,
            confidence=confidence,
            size=size,
        )
