"""Unit tests for fee shadow veto logic."""
from backend.services.risk import veto_poor_edge


def test_fee_shadow_veto() -> None:
    assert veto_poor_edge(expected_r=0.0009, fee=0.0006, slip=0.0002) is True
    assert veto_poor_edge(expected_r=0.005, fee=0.0006, slip=0.0002) is False
