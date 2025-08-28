#!/usr/bin/env python3
"""CLI utility to run the quantum backtester."""

from __future__ import annotations

import argparse
import json
import time
import uuid
from pathlib import Path

from api.app.quantum.adaptive import DynamicThresholdsConfig, SizingParams
from api.app.quantum.backtester import BacktestEngine, FeesConfig, RunConfig, VenueCosts


def main() -> None:
    """Execute the backtester with optional CSV inputs."""
    parser = argparse.ArgumentParser(description="Run ANGEL.AI quantum backtests")
    parser.add_argument("--ohlcv", dest="ohlcv", help="OHLCV CSV path", default=None)
    parser.add_argument("--sentiment", dest="sentiment", help="Sentiment CSV path", default=None)
    args = parser.parse_args()

    stamp = time.strftime("%Y%m%d-%H%M%S")
    outdir = Path(f"out/{stamp}-{uuid.uuid4().hex[:6]}")
    engine = BacktestEngine(
        symbol="BTC/USDT",
        csv_ohlcv_path=args.ohlcv,
        csv_sentiment_path=args.sentiment,
        fees=FeesConfig(),
        venue_costs=VenueCosts.defaults(),
        sizing=SizingParams(),
        dyn=DynamicThresholdsConfig(),
        run=RunConfig(),
        seed=42,
        outdir=outdir,
    )
    report = engine.run_full()
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
