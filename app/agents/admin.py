"""Administrative agent supervising strategy health and promotions."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Dict, Set

from .base import TradingAgent


class AdminAgent:
    """Tracks agent health and manages promotions based on KPIs."""

    def __init__(self, health_window: int = 60) -> None:
        self._agents: Dict[str, TradingAgent] = {}
        self._last_update: Dict[str, datetime] = {}
        self._promoted: Set[str] = set()
        self._health_window = timedelta(seconds=health_window)

    def register(self, agent: TradingAgent) -> None:
        if agent.agent_id in self._agents:
            raise ValueError(f"Agent {agent.agent_id} already registered")
        self._agents[agent.agent_id] = agent
        self._last_update[agent.agent_id] = datetime.now(UTC)

    def mark_updated(self, agent_id: str) -> None:
        self._last_update[agent_id] = datetime.now(UTC)

    def check_health(self) -> Dict[str, bool]:
        now = datetime.now(UTC)
        return {
            agent_id: now - self._last_update.get(agent_id, datetime.min.replace(tzinfo=UTC)) < self._health_window
            for agent_id in self._agents
        }

    def evaluate_promotions(self, threshold: float) -> None:
        for agent_id, agent in self._agents.items():
            if agent.kpi.weight() >= threshold:
                self._promoted.add(agent_id)

    def is_promoted(self, agent_id: str) -> bool:
        return agent_id in self._promoted

    @property
    def agents(self) -> Dict[str, TradingAgent]:
        return dict(self._agents)
