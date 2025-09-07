"""Select the best configuration based on backtest metrics."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

RESULT_FILE = Path("out/eval_results.json")


def choose_config(results: Dict[str, Dict[str, float]]) -> str:
    """Return path of config with highest PnL and lowest drawdown."""
    if not results:
        raise ValueError("no results to choose from")
    return min(results, key=lambda p: (-results[p]["pnl"], results[p]["max_dd"]))


def main() -> None:
    data = json.loads(RESULT_FILE.read_text())
    best_path = choose_config(data)
    best = data[best_path]
    report_lines = ["Config evaluation results:"]
    for path, stats in data.items():
        report_lines.append(
            f"- {stats['name']}: pnl={stats['pnl']:.4f}, max_dd={stats['max_dd']:.4f}"
        )
    report_lines.append(
        f"\nChosen config: {best['name']} ({best_path}) based on highest pnl and lowest drawdown."
    )
    print("\n".join(report_lines))


if __name__ == "__main__":
    main()
