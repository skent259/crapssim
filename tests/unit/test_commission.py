import math

from crapssim.bet import compute_commission


def test_compute_commission_fixed_five_percent():
    assert compute_commission(100.0) == 5.0
    assert compute_commission(40.0) == 2.0
    assert math.isclose(compute_commission(12.34), 0.617, rel_tol=1e-9)
