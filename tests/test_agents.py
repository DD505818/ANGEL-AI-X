"""Tests for trading agents and governance components."""

import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.agents import (
    AdminAgent,
    AgentKPI,
    MeanReversionAgent,
    MetaGovernor,
    MomentumAgent,
)


@pytest.mark.asyncio
async def test_meta_governor_allocation() -> None:
    admin = AdminAgent()
    kpi_mom = AgentKPI(sharpe_ratio=1.0, win_rate=0.6, max_drawdown=0.1)
    kpi_mean = AgentKPI(sharpe_ratio=1.5, win_rate=0.65, max_drawdown=0.05)
    mom = MomentumAgent("mom", admin, kpi=kpi_mom)
    mean = MeanReversionAgent("mean", admin, kpi=kpi_mean)
    for price in range(1, 12):
        data = {"symbol": "XYZ", "price": float(price)}
        await mom.update_state(data)
        await mean.update_state(data)
    health = admin.check_health()
    assert all(health.values())
    admin.evaluate_promotions(threshold=1.0)
    assert admin.is_promoted("mean")
    governor = MetaGovernor(admin, total_capital=100_000)
    signal, allocations = await governor.vote_and_allocate()
    assert signal.action in {"BUY", "SELL", "HOLD"}
    assert pytest.approx(sum(allocations.values()), rel=1e-6) == 100_000
    assert allocations["mean"] > allocations["mom"]
