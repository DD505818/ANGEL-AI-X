"""Model drift detection utilities."""
import numpy as np

def psi(expected: np.ndarray, actual: np.ndarray, bins: int=10) -> float:
    """
    Population Stability Index (simple implementation).
    """
    e_hist, edges = np.histogram(expected, bins=bins)
    a_hist, _     = np.histogram(actual, bins=edges)
    e_pct = np.clip(e_hist / max(e_hist.sum(), 1), 1e-6, 1)
    a_pct = np.clip(a_hist / max(a_hist.sum(), 1), 1e-6, 1)
    return float(((a_pct - e_pct) * np.log(a_pct / e_pct)).sum())

def drift_action(psi_value: float, warn: float=0.1, de_risk: float=0.2):
    """
    Returns policy: 'ok' | 'halve_size' | 'veto'
    """
    if psi_value >= de_risk:
        return "halve_size"
    if psi_value >= warn:
        return "ok_warn"
    return "ok"

