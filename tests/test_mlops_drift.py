import numpy as np
from backend.services.mlops.drift import psi, drift_action


def test_psi_and_action():
    expected = np.zeros(100)
    actual = np.ones(100)
    v = psi(expected, actual)
    assert v > 0
    assert drift_action(v) in {"ok", "ok_warn", "halve_size"}
