"""FastAPI router exposing the backtest engine."""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

from ..quantum.backtester import BacktestEngine, FeesConfig, RunConfig, SizingParams, VenueCosts
from ..quantum.ensemble import MetaGovernor, PromotionGates
from ..quantum.adaptive import DynamicThresholdsConfig

router = APIRouter()


class BacktestReq(BaseModel):
    """Request schema for a backtest run."""

    symbol: str = "BTC/USDT"
    csv_ohlcv_path: Optional[str] = None
    csv_sentiment_path: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    fees: FeesConfig = FeesConfig()
    venue_costs: Dict[str, VenueCosts] = Field(default_factory=VenueCosts.defaults)
    sizing: SizingParams = SizingParams()
    run: RunConfig = RunConfig()
    dyn: DynamicThresholdsConfig = DynamicThresholdsConfig()
    seed: int = 42


@router.post("/quantum/backtest")
async def run_backtest(req: BacktestReq = Body(...)) -> Dict[str, Any]:
    """Execute a full backtest and return summary results."""
    stamp = time.strftime("%Y%m%d-%H%M%S")
    outdir = Path(f"out/{stamp}-{uuid.uuid4().hex[:6]}")
    outdir.mkdir(parents=True, exist_ok=True)

    engine = BacktestEngine(
        symbol=req.symbol,
        csv_ohlcv_path=req.csv_ohlcv_path,
        csv_sentiment_path=req.csv_sentiment_path,
        fees=req.fees,
        venue_costs=req.venue_costs,
        sizing=req.sizing,
        dyn=req.dyn,
        run=req.run,
        seed=req.seed,
        outdir=outdir,
    )
    report = engine.run_full()

    gates = PromotionGates(
        hit_rate=0.58,
        sharpe_10d=2.2,
        max_dd_10d=0.025,
        route_p95_us=300,
        slip_error_pct=0.10,
        days=10,
    )
    mgov = MetaGovernor(gates=gates)
    mgov.update_weights(report.get("perf_by_strategy", {}))

    payload = {
        "ok": True,
        "outdir": str(outdir),
        "summary": report.get("summary", {}),
        "best_params": report.get("best_params", {}),
        "weights": mgov.weights,
    }
    (outdir / "report.json").write_text(json.dumps(payload, indent=2))
    return payload
