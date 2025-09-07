"""Manage strategy lifecycles and signal aggregation."""
from __future__ import annotations

from typing import Dict, Protocol


class Strategy(Protocol):
    """Protocol for strategies producing a numeric signal."""

    name: str

    async def evaluate(self, market: dict) -> float:
        ...


class StrategyManager:
    """Register and run multiple strategies concurrently."""

    def __init__(self) -> None:
        self._strategies: Dict[str, Strategy] = {}

    def register(self, strategy: Strategy) -> None:
        """Register a strategy instance."""
        self._strategies[strategy.name] = strategy

    async def run(self, market: dict) -> Dict[str, float]:
        """Evaluate all strategies against the provided market snapshot."""
        results: Dict[str, float] = {}
        for name, strat in self._strategies.items():
            results[name] = await strat.evaluate(market)
        return results
