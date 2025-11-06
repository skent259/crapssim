import pytest

from crapssim.bet import _compute_commission


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
    result = _compute_commission(
        bet,
        rounding=rounding,
        floor=floor,
        mode=mode,
    )

    assert abs(result - expected) < 1e-9


@pytest.mark.parametrize(
    ("rounding", "floor", "bet"),
    [
        ("ceil_dollar", 0.0, 20.0),
        ("nearest_dollar", 1.0, 20.0),
        ("nearest_dollar", 1.0, 25.0),
        ("nearest_dollar", 1.0, 5.0),
        ("none", 0.0, 20.0),
    ],
)
def test_commission_mode_parity(rounding, floor, bet):
    on_bet = _compute_commission(
        bet,
        rounding=rounding,
        floor=floor,
        mode="on_bet",
    )
    on_win = _compute_commission(
        bet,
        rounding=rounding,
        floor=floor,
        mode="on_win",
    )

    assert abs(on_bet - on_win) < 1e-9
