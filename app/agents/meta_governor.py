"""Meta governor aggregating agent signals and allocating capital."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Dict, Tuple

from .admin import AdminAgent
from .base import SCHEMA_VERSION, Signal


class MetaGovernor:
    """Aggregates signals via weighted voting and decides capital allocation."""

    def __init__(self, admin: AdminAgent, total_capital: float = 100_000) -> None:
        self._admin = admin
        self._capital = total_capital

    async def vote_and_allocate(self) -> Tuple[Signal, Dict[str, float]]:
        """Compute a weighted vote and capital allocation across agents."""
        agents = list(self._admin.agents.values())
        if not agents:
            raise ValueError("No agents registered for voting")
        signals = await asyncio.gather(*(agent.generate_signal() for agent in agents))
        symbols = {s.symbol for s in signals}
        if len(symbols) != 1:
            raise ValueError("Signals reference multiple symbols")
        weights = [agent.kpi.weight() for agent in agents]
        total_weight = sum(weights) or 1.0
        decision_score = 0.0
        allocations: Dict[str, float] = {}
        for agent, signal, weight in zip(agents, signals, weights):
            direction = {"BUY": 1, "SELL": -1, "HOLD": 0}[signal.action]
            decision_score += direction * weight * signal.confidence
            allocations[agent.agent_id] = self._capital * (weight / total_weight)
        final_action = "BUY" if decision_score > 0 else "SELL" if decision_score < 0 else "HOLD"
        confidence = min(abs(decision_score) / (total_weight or 1.0), 1.0)
        final_signal = Signal(
            schema_version=SCHEMA_VERSION,
            timestamp=datetime.now(UTC),
            symbol=next(iter(symbols)),
            action=final_action,
            confidence=confidence,
            size=self._capital * confidence,
        )
        return final_signal, allocations
