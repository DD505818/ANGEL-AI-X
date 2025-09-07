"""Tests for evaluation selector."""

from __future__ import annotations

from evaluation.selector import choose_config


def test_choose_config_picks_highest_pnl_lowest_dd() -> None:
    results = {
        "a": {"pnl": 0.5, "max_dd": 0.1},
        "b": {"pnl": 0.6, "max_dd": 0.2},
        "c": {"pnl": 0.6, "max_dd": 0.15},
    }
    assert choose_config(results) == "c"
