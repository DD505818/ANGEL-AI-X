from dataclasses import dataclass
@dataclass
class RiskState:
    kill: bool = False
    max_dd: float = 0.008
    dd: float = 0.0
def pretrade_gate(state: RiskState) -> None:
    if state.kill: raise RuntimeError("RISK_HALT")
    if state.dd > state.max_dd: raise RuntimeError("MAX_DD_BREACH")
