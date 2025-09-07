"""Risk safety gate enforcing portfolio-level guardrails."""
from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class RiskConfig:
    portfolio_notional_cap: float        # e.g., 0.12  (12% NAV)
    daily_loss_cap: float                # e.g., 0.02  (2% NAV)
    mdd_brake: float                     # e.g., 0.07  (7% peak-to-trough)
    per_trade_risk_max: float            # e.g., 0.005 (0.5% NAV)
    max_clock_skew_ms: int               # e.g., 100

def safety_gate(decision, portfolio, risk: RiskConfig, now_ms: Optional[int]=None):
    """
    Applies cross-agent, cross-venue safety checks BEFORE OMS commit.
    decision: enriched decision object with fields .risk_size_nav, .clock_skew_ms
    portfolio: exposes .nav, .open_notional, .day_pnl_nav, .drawdown_nav
    """
    now_ms = now_ms or int(time.time()*1000)

    # 1) Per-trade risk clamp
    if decision.risk_size_nav > risk.per_trade_risk_max:
        return decision.veto("PerTradeRiskExceeded")

    # 2) Aggregate exposure after this decision
    future_notional = portfolio.open_notional + decision.notional_estimate
    if future_notional > risk.portfolio_notional_cap * portfolio.nav:
        return decision.veto("PortfolioNotionalCap")

    # 3) Daily loss cap & cooldown
    if portfolio.day_pnl_nav <= -risk.daily_loss_cap:
        return decision.veto("DailyLossCap")

    # 4) Max drawdown brake
    if portfolio.drawdown_nav >= risk.mdd_brake:
        return decision.veto("MDDBrake")

    # 5) Clock skew guard
    if abs(decision.clock_skew_ms) > risk.max_clock_skew_ms:
        return decision.veto("ClockSkew")

    decision.annotate({"safety_gate_ts": now_ms})
    return decision

