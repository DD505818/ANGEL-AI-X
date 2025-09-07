"""Coordinator for multiple trading agents."""
from __future__ import annotations

import asyncio
from typing import Dict

from .base import Signal, TradingAgent


class StrategyManager:
    """Manage a collection of trading agents and aggregate their signals."""

    def __init__(self) -> None:
        self._agents: Dict[str, TradingAgent] = {}

    def register(self, agent: TradingAgent) -> None:
        """Register an agent for participation."""

        self._agents[agent.agent_id] = agent

    def unregister(self, agent_id: str) -> None:
        """Remove an agent by identifier."""

        self._agents.pop(agent_id, None)

    async def generate(self) -> Dict[str, Signal]:
        """Gather signals from all agents concurrently."""

        tasks = [agent.generate_signal() for agent in self._agents.values()]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return {sig.symbol: sig for sig in results}
