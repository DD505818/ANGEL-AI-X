"""Vectorised backtesting engine with adaptive sizing."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Optional

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import optuna
import pandas as pd

from .adaptive import (
    DynamicThresholdsConfig,
    FeesConfig,
    RunConfig,
    SizingParams,
    VenueCosts,
    adaptive_fraction,
)
from .indicators import garch_proxy
from .strategies import (
    ATRTrendArbConfig,
    MomentumStacker7Config,
    QBX3Config,
    SSv2Config,
    atr_trend_arb,
    momentum_stacker_7,
    quantumboost_x3,
    sentimentsurge_v2,
)

matplotlib.use("Agg")


@dataclass
class Result:
    """Outcome of a backtest run."""

    equity_curve: np.ndarray
    drawdown: np.ndarray
    trades: int
    wins: int
    wr: float
    sharpe: float
    max_dd: float
    pnl: float


class BacktestEngine:
    """Orchestrates tuning, simulation and output generation."""

    def __init__(
        self,
        symbol: str,
        csv_ohlcv_path: Optional[str],
        csv_sentiment_path: Optional[str],
        fees: FeesConfig,
        venue_costs: Dict[str, VenueCosts],
        sizing: SizingParams,
        dyn: DynamicThresholdsConfig,
        run: RunConfig,
        seed: int,
        outdir: Path,
    ) -> None:
        self.symbol = symbol
        self.csv = csv_ohlcv_path
        self.csv_sent = csv_sentiment_path
        self.fees = fees
        self.venues = venue_costs
        self.sizing = sizing
        self.dyn = dyn
        self.run = run
        self.seed = seed
        self.outdir = outdir

    def load_data(self) -> pd.DataFrame:
        """Load OHLCV and sentiment data, synthesising if necessary."""
        if self.csv:
            df = pd.read_csv(self.csv)
            df = df.rename(columns={c: c.lower() for c in df.columns})
        else:
            n = 6000
            t = np.arange(n)
            rng = np.random.default_rng(self.seed)
            close = 100 + np.sin(t / 50.0) * 2 + rng.normal(0, 0.5, size=n)
            high = close + 0.5
            low = close - 0.5
            volume = 1e5 + rng.normal(0, 2e4, size=n)
            df = pd.DataFrame(
                {
                    "ts": t,
                    "open": close,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                }
            )
        if self.csv_sent and Path(self.csv_sent).exists():
            s = pd.read_csv(self.csv_sent)
            s = s.rename(columns={c: c.lower() for c in s.columns})
            df["sentiment"] = s.get("sentiment", pd.Series(0.0, index=df.index)).fillna(0.0)
        else:
            df["sentiment"] = 0.6 + 0.1 * np.tanh(np.sin(np.arange(len(df)) / 300.0))
        return df

    def _tx_cost(self, venue: str, taker: bool = True) -> float:
        """Return the transaction cost for a venue."""
        c = self.venues.get(venue, VenueCosts())
        return c.taker_fee if taker else c.maker_fee

    def simulate(self, df: pd.DataFrame, params: Dict[str, Any]) -> Result:
        """Simulate trading given parameterised strategies."""
        px = df["close"].to_numpy()
        hi = df["high"].to_numpy()
        lo = df["low"].to_numpy()
        vol = np.maximum(1.0, df["volume"].to_numpy())
        sent = df["sentiment"].to_numpy()
        ret = np.diff(px, prepend=px[0]) / px
        sigma = garch_proxy(ret, 200)

        e1, x1, tp1, sl1 = quantumboost_x3(px, vol, sent, params["qbx3"])
        e2, x2, tp2, sl2 = sentimentsurge_v2(px, vol, sent, params["ssv2"])
        e3, x3, tp3, sl3 = atr_trend_arb(px, hi, lo, params["atra"])
        e4, x4, tp4, sl4 = momentum_stacker_7(px, params["ms7"])

        entries = {"QBX3": e1, "SSv2": e2, "ATRA": e3, "MS7": e4}
        exits = {"QBX3": x1, "SSv2": x2, "ATRA": x3, "MS7": x4}
        tps = {"QBX3": tp1, "SSv2": tp2, "ATRA": tp3, "MS7": tp4}
        sls = {"QBX3": sl1, "SSv2": sl2, "ATRA": sl3, "MS7": sl4}

        equity = np.ones_like(px)
        peak = 1.0
        dd = 0.0
        trades = 0
        wins = 0
        venue_cycle = ["binance", "bybit", "coinbase", "kraken"]
        venue_idx = 0
        frac = 0.01
        for i in range(1, len(px)):
            frac = adaptive_fraction(ret[:i], dd, self.sizing)
            take = False
            who = None
            for name, mask in entries.items():
                if mask[i]:
                    who = name
                    take = True
                    break
            if take:
                tp = tps[who]
                sl = sls[who]
                r = (px[i] - px[i - 1]) / px[i - 1]
                venue = venue_cycle[venue_idx % len(venue_cycle)]
                venue_idx += 1
                fee = self._tx_cost(venue, taker=True) + self.fees.slippage_bp / 1e4
                pnl = (tp if r > tp else (-sl if r < -sl else r)) - fee
                equity[i] = equity[i - 1] * (1 + frac * pnl)
                trades += 1
                wins += 1 if pnl > 0 else 0
            else:
                equity[i] = equity[i - 1]
            peak = max(peak, equity[i])
            dd = max(dd, (peak - equity[i]) / peak)
        wr = wins / max(1, trades)
        pnl = equity[-1] - 1.0
        sharpe = float(
            np.mean(np.diff(equity)) / (np.std(np.diff(equity)) + 1e-9) * np.sqrt(252 * 24 * 12)
        )
        drawdown = 1 - equity / np.maximum.accumulate(equity)
        return Result(equity, drawdown, trades, wins, wr, sharpe, float(np.max(drawdown)), pnl)

    def _objective(self, trial: optuna.Trial, df: pd.DataFrame) -> float:
        """Optuna objective for hyper-parameter tuning."""
        params = {
            "qbx3": QBX3Config(
                rsi_buy_low=trial.suggest_float("qbx3_rsi_low", 20, 40),
                rsi_sell_high=trial.suggest_float("qbx3_rsi_high", 60, 80),
                sentiment_buy=trial.suggest_float("qbx3_sent", 0.6, 0.85),
                tp_pct=trial.suggest_float("qbx3_tp", 0.01, 0.03),
                sl_pct=trial.suggest_float("qbx3_sl", 0.005, 0.02),
            ),
            "ssv2": SSv2Config(
                sentiment_buy=trial.suggest_float("ssv2_sent", 0.7, 0.9),
                tp_pct=trial.suggest_float("ssv2_tp", 0.01, 0.03),
                sl_pct=trial.suggest_float("ssv2_sl", 0.005, 0.02),
            ),
            "atra": ATRTrendArbConfig(
                bb_n=trial.suggest_int("atra_n", 18, 22),
                bb_k=trial.suggest_float("atra_k", 1.8, 2.2),
                atr_delta=trial.suggest_float("atra_delta", 0.05, 0.2),
                tp_pct=trial.suggest_float("atra_tp", 0.01, 0.03),
                sl_pct=trial.suggest_float("atra_sl", 0.005, 0.02),
            ),
            "ms7": MomentumStacker7Config(
                mom_thresh=trial.suggest_float("ms7_mom", 0.005, 0.02),
                rsi_low=trial.suggest_float("ms7_rsi_low", 35, 45),
                rsi_high=trial.suggest_float("ms7_rsi_high", 55, 65),
                tp_pct=trial.suggest_float("ms7_tp", 0.01, 0.03),
                sl_pct=trial.suggest_float("ms7_sl", 0.005, 0.02),
            ),
        }
        res = self.simulate(df, params)
        return res.equity_curve[-1] - 0.5 * res.max_dd

    def run_full(self) -> Dict[str, Any]:
        """Run tuning then backtest using best parameters."""
        df = self.load_data()
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        study = optuna.create_study(direction="maximize")
        study.optimize(lambda tr: self._objective(tr, df), n_trials=60)
        best = study.best_params
        params = {
            "qbx3": QBX3Config(
                best["qbx3_rsi_low"],
                best["qbx3_rsi_high"],
                best["qbx3_sent"],
                best["qbx3_tp"],
                best["qbx3_sl"],
            ),
            "ssv2": SSv2Config(best["ssv2_sent"], best["ssv2_tp"], best["ssv2_sl"]),
            "atra": ATRTrendArbConfig(
                best["atra_n"],
                best["atra_k"],
                best["atra_delta"],
                best["atra_tp"],
                best["atra_sl"],
            ),
            "ms7": MomentumStacker7Config(
                best["ms7_mom"],
                best["ms7_rsi_low"],
                best["ms7_rsi_high"],
                best["ms7_tp"],
                best["ms7_sl"],
            ),
        }
        res = self.simulate(df, params)
        self._save_outputs(df, res)
        perf_by_strategy = {"QBX3": float(res.pnl)}
        return {
            "summary": {
                "equity": float(res.equity_curve[-1]),
                "max_dd": res.max_dd,
                "wr": res.wr,
                "sharpe": res.sharpe,
            },
            "best_params": best,
            "perf_by_strategy": perf_by_strategy,
        }

    def _save_outputs(self, df: pd.DataFrame, res: Result) -> None:
        """Persist metrics and plots to the output directory."""
        out = self.outdir
        dfm = pd.DataFrame({"equity": res.equity_curve, "drawdown": res.drawdown})
        out.mkdir(parents=True, exist_ok=True)
        dfm.to_csv(out / "metrics.csv", index=False)
        pd.DataFrame({"t": df["ts"], "px": df["close"]}).to_csv(
            out / "trade_log.csv", index=False
        )
        plt.figure(figsize=(10, 4))
        plt.plot(res.equity_curve)
        plt.title("Equity Curve")
        plt.tight_layout()
        plt.savefig(out / "equity_curve.png")
        plt.close()
        plt.figure(figsize=(10, 3))
        plt.plot(res.drawdown)
        plt.title("Drawdown")
        plt.tight_layout()
        plt.savefig(out / "drawdown.png")
        plt.close()
