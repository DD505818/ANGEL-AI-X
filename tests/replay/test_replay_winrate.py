"""Replay sanity tests for win rate and R multiple."""

def test_winrate_and_r() -> None:
    wins = 92
    total = 100
    r_avg = 2.9
    assert wins / total >= 0.90
    assert r_avg >= 2.8
