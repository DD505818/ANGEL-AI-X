"""Run backtests for multiple configs with Monte Carlo simulation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import yaml

from api.app.quantum.adaptive import (
    DynamicThresholdsConfig,
    FeesConfig,
    RunConfig,
    SizingParams,
    VenueCosts,
)
from api.app.quantum.backtester import BacktestEngine
from api.app.quantum.strategies import (
    ATRTrendArbConfig,
    MomentumStacker7Config,
    QBX3Config,
    SSv2Config,
)

CONFIG_DIR = Path("config/eval")
OUT_FILE = Path("out/eval_results.json")
MC_RUNS = 10


def _load_config(path: Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    sizing = SizingParams(**data.get("sizing", {}))
    run = RunConfig(**data.get("run", {}))
    fees = FeesConfig(**data.get("fees", {}))
    dyn = DynamicThresholdsConfig(**data.get("dyn", {}))
    return {
        "name": data.get("name", path.stem),
        "sizing": sizing,
        "run": run,
        "fees": fees,
        "dyn": dyn,
    }


def _simulate(cfg: Dict[str, object]) -> Dict[str, float]:
    results: List[Dict[str, float]] = []
    for i in range(MC_RUNS):
        seed = cfg["run"].seed + i
        engine = BacktestEngine(
            symbol="BTC/USDT",
            csv_ohlcv_path=None,
            csv_sentiment_path=None,
            fees=cfg["fees"],
            venue_costs=VenueCosts.defaults(),
            sizing=cfg["sizing"],
            dyn=cfg["dyn"],
            run=RunConfig(seed=seed),
            seed=seed,
            outdir=Path("out") / f"tmp_{seed}",
        )
        df = engine.load_data()
        params = {
            "qbx3": QBX3Config(),
            "ssv2": SSv2Config(),
            "atra": ATRTrendArbConfig(),
            "ms7": MomentumStacker7Config(),
        }
        res = engine.simulate(df, params)
        results.append({"pnl": res.pnl, "max_dd": res.max_dd})
    pnl = float(np.mean([r["pnl"] for r in results]))
    dd = float(np.mean([r["max_dd"] for r in results]))
    return {"pnl": pnl, "max_dd": dd}


def main() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    all_results = {}
    for path in sorted(CONFIG_DIR.glob("*.yaml")):
        cfg = _load_config(path)
        stats = _simulate(cfg)
        all_results[path.as_posix()] = {
            "name": cfg["name"],
            "pnl": stats["pnl"],
            "max_dd": stats["max_dd"],
        }
    OUT_FILE.write_text(json.dumps(all_results, indent=2))
    print(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    main()
