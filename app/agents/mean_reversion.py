"""Mean reversion trading agent."""

from __future__ import annotations

from collections import deque
from datetime import UTC, datetime
from typing import Any, Deque, Dict

from .admin import AdminAgent
from .base import SCHEMA_VERSION, AgentKPI, Signal, TradingAgent


class MeanReversionAgent(TradingAgent):
    """Contrarian strategy that bets on prices reverting to their mean."""

    def __init__(
        self,
        agent_id: str,
        admin: AdminAgent,
        *,
        kpi: AgentKPI,
        window: int = 10,
        threshold: float = 0.01,
        capital: float = 10_000,
    ) -> None:
        super().__init__(agent_id, admin, kpi=kpi)
        self._prices: Deque[float] = deque(maxlen=window)
        self._threshold = threshold
        self._capital = capital

    async def update_state(self, market_data: Dict[str, Any]) -> None:
        """Update price window for mean-reversion calculation."""
        price = market_data.get("price")
        symbol = market_data.get("symbol")
        if not isinstance(price, (int, float)) or not isinstance(symbol, str):
            raise ValueError("Invalid market data for MeanReversionAgent")
        self._prices.append(float(price))
        self._state["symbol"] = symbol
        self._admin.mark_updated(self.agent_id)

    async def generate_signal(self) -> Signal:
        """Produce a mean-reversion trading signal."""
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
        deviation = (last - avg) / avg
        variance = max(sum((p - avg) ** 2 for p in self._prices) / len(self._prices), 1e-6)
        edge = -deviation
        size = await self._kelly_size(edge, variance, self._capital)
        if deviation > self._threshold:
            action = "SELL"
        elif deviation < -self._threshold:
            action = "BUY"
        else:
            action = "HOLD"
            size = 0.0
        confidence = min(abs(deviation) * 10, 1.0)
        return Signal(
            schema_version=SCHEMA_VERSION,
            timestamp=datetime.now(UTC),
            symbol=self._state.get("symbol", ""),
            action=action,
            confidence=confidence,
            size=size,
        )
