def score(latency_ms: float, spread_bps: float, fee_bps: float, slip_bps: float, queue_pos: float=0.0) -> float:
    # Lower is better
    return fee_bps + slip_bps + 0.5*latency_ms + 0.1*spread_bps + 0.2*queue_pos
