from __future__ import annotations

import math
from dataclasses import dataclass

import pytest

from crapssim.bet import _compute_commission


@dataclass
class _StubTable:
    settings: dict


@pytest.mark.parametrize(
    ("mode", "rounding", "floor", "bet", "expected"),
    [
        ("on_bet", "ceil_dollar", 0.0, 20.0, 1.0),
        ("on_win", "ceil_dollar", 0.0, 20.0, 1.0),
        ("on_bet", "nearest_dollar", 1.0, 20.0, 1.0),
        ("on_win", "nearest_dollar", 1.0, 25.0, 1.0),
        ("on_bet", "nearest_dollar", 1.0, 5.0, 1.0),
        ("on_bet", "none", 0.0, 20.0, 1.0),
    ],
)
def test_compute_commission_expected_values(mode, rounding, floor, bet, expected):
    table = _StubTable(
        settings={
            "commission_mode": mode,
            "commission_rounding": rounding,
            "commission_floor": floor,
        }
    )

    result = _compute_commission(table, gross_win=bet * 3.5, bet_amount=bet)

    assert math.isclose(result, expected, rel_tol=0.0, abs_tol=1e-9)


@pytest.mark.parametrize(
    ("rounding", "floor", "bet"),
    [
        ("ceil_dollar", 0.0, 20.0),
        ("nearest_dollar", 1.0, 20.0),
        ("nearest_dollar", 1.0, 5.0),
        ("none", 0.0, 12.5),
    ],
)
def test_commission_mode_parity(rounding, floor, bet):
    table_on_bet = _StubTable(
        settings={
            "commission_mode": "on_bet",
            "commission_rounding": rounding,
            "commission_floor": floor,
        }
    )
    table_on_win = _StubTable(
        settings={
            "commission_mode": "on_win",
            "commission_rounding": rounding,
            "commission_floor": floor,
        }
    )

    on_bet = _compute_commission(table_on_bet, gross_win=bet * 20, bet_amount=bet)
    on_win = _compute_commission(table_on_win, gross_win=bet * 0.5, bet_amount=bet)

    assert on_bet == pytest.approx(on_win, abs=1e-9)
