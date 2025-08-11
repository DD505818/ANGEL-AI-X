"""Common agent primitives and data models for trading strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Literal


SCHEMA_VERSION = 1


@dataclass(slots=True)
class Signal:
    """Represents a trading signal emitted by an agent."""

    schema_version: int
    timestamp: datetime
    symbol: str
    action: Literal["BUY", "SELL", "HOLD"]
    confidence: float
    size: float


@dataclass(slots=True)
class AgentKPI:
    """Key performance indicators tracked for each agent."""

    sharpe_ratio: float
    win_rate: float
    max_drawdown: float

    def weight(self) -> float:
        """Return a positive weight derived from KPIs for voting and sizing."""
        penalty = max(self.max_drawdown, 1e-6)
        return max(self.sharpe_ratio * self.win_rate / penalty, 0.0)


class TradingAgent(ABC):
    """Abstract base class for trading agents."""

    def __init__(self, agent_id: str, admin: "AdminAgent", *, kpi: AgentKPI) -> None:
        self.agent_id = agent_id
        self._admin = admin
        self.kpi = kpi
        self._state: Dict[str, Any] = {}
        self._admin.register(self)

    @property
    def state(self) -> Dict[str, Any]:
        """Return a shallow copy of the current agent state."""
        return dict(self._state)

    @abstractmethod
    async def generate_signal(self) -> Signal:
        """Produce a trading signal based on the agent's state.

        Implementations must include risk controls and dynamic sizing.
        """

    @abstractmethod
    async def update_state(self, market_data: Dict[str, Any]) -> None:
        """Update internal state from validated market data."""

    async def _kelly_size(self, edge: float, variance: float, capital: float) -> float:
        """Calculate position size using the Kelly criterion."""
        if variance <= 0:
            raise ValueError("Variance must be positive for Kelly sizing")
        fraction = max(min(edge / variance, 1.0), 0.0)
        return capital * fraction
