import numpy as np

from app.models.drift_detection import ks_drift_detect


def test_ks_drift_detect():
    base = np.random.default_rng(0).normal(0, 1, 100)
    new = np.random.default_rng(1).normal(1, 1, 100)
    assert ks_drift_detect(base, new, alpha=0.05)
