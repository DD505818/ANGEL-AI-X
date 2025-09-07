from backend.risk.safety_gate import safety_gate, RiskConfig


class DummyDecision:
    def __init__(self, risk_size_nav=0.0, notional_estimate=0.0, clock_skew_ms=0):
        self.risk_size_nav = risk_size_nav
        self.notional_estimate = notional_estimate
        self.clock_skew_ms = clock_skew_ms
        self.is_veto = False
        self.annotations = {}

    def veto(self, reason: str):
        self.is_veto = True
        self.reason = reason
        return self

    def annotate(self, data):
        self.annotations.update(data)


class DummyPortfolio:
    nav = 100.0
    open_notional = 0.0
    day_pnl_nav = 0.0
    drawdown_nav = 0.0


def test_per_trade_risk_veto():
    risk = RiskConfig(0.5, 0.1, 0.2, 0.01, 100)
    decision = DummyDecision(risk_size_nav=0.02)
    result = safety_gate(decision, DummyPortfolio(), risk)
    assert result.is_veto and result.reason == "PerTradeRiskExceeded"


def test_safe_decision_passes():
    risk = RiskConfig(0.5, 0.1, 0.2, 0.05, 100)
    decision = DummyDecision(risk_size_nav=0.01)
    result = safety_gate(decision, DummyPortfolio(), risk)
    assert not result.is_veto and "safety_gate_ts" in result.annotations
