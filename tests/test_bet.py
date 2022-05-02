import pytest
import crapssim
import numpy as np

from crapssim.bet import AllSmall, AllTall, AllOrNothingAtAll
from crapssim.dice import Dice
from crapssim.table import Table, Point


# Check EV of bets on a "per-roll" basis

@pytest.mark.parametrize("bet, ev", [
    (crapssim.bet.Place4(1), -0.0167),
    (crapssim.bet.Place5(1), -0.0111),
    (crapssim.bet.Place6(1), -0.0046),
    (crapssim.bet.Place8(1), -0.0046),
    (crapssim.bet.Place9(1), -0.0111),
    (crapssim.bet.Place10(1), -0.0167),
    (crapssim.bet.Field(1), -0.0556),
    (crapssim.bet.Any7(1), -0.1667),
    (crapssim.bet.Two(1), -0.1389),
    (crapssim.bet.Three(1), -0.1111),
    (crapssim.bet.Yo(1), -0.1111),
    (crapssim.bet.Boxcars(1), -0.1389),
    (crapssim.bet.AnyCraps(1), -0.1111),
    (crapssim.bet.CAndE(1), -0.1111),
    (crapssim.bet.Hard4(1), -0.0278),
    (crapssim.bet.Hard6(1), -0.0278),
    (crapssim.bet.Hard8(1), -0.0278),
    (crapssim.bet.Hard10(1), -0.0278),
])
def test_ev_oneroll(bet, ev):
    d = Dice()
    t = Table()
    t.point.status = "On"  # for place bets to pay properly

    outcomes = []
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            d.fixed_roll([d1, d2])
            status, win_amt = bet._update_bet(t, d)

            outcomes.append(win_amt if status == "win" else -1 if status == "lose" else 0)

    assert round(np.mean(outcomes), 4) == ev


@pytest.mark.parametrize('rolls, correct_status, correct_win_amount', [
    ([(2, 2)], None, 0.0),
    ([(1, 1), (1, 2), (2, 2), (2, 3), (3, 3)], 'win', 34),
    ([(1, 1), (1, 2), (2, 2), (2, 3), (3, 4)], 'lose', 0.0)
])
def test_all_small(rolls: list[tuple[int]], correct_status: str | None, correct_win_amount: float):
    table = Table()
    dice = Dice()
    bet = AllSmall(1)

    status, win_amt = None, None
    for roll in rolls:
        dice.fixed_roll(roll)
        status, win_amt = bet._update_bet(table, dice)
    assert (status, win_amt) == (correct_status, correct_win_amount)


@pytest.mark.parametrize('rolls, correct_status, correct_win_amount', [
    ([(2, 2)], None, 0.0),
    ([(10, 1), (10, 2), (7, 2), (5, 5), (2, 6)], 'win', 34),
    ([(1, 1), (1, 2), (2, 2), (2, 3), (3, 4)], 'lose', 0.0)
])
def test_all_tall(rolls: list[tuple[int]], correct_status: str | None, correct_win_amount: float):
    table = Table()
    dice = Dice()
    bet = AllTall(1)

    status, win_amt = None, None
    for roll in rolls:
        dice.fixed_roll(roll)
        status, win_amt = bet._update_bet(table, dice)
    assert (status, win_amt) == (correct_status, correct_win_amount)


@pytest.mark.parametrize('rolls, correct_status, correct_win_amount', [
    ([(2, 2)], None, 0.0),
    ([(10, 1), (10, 2), (7, 2), (5, 5), (2, 6),
      (1, 1), (1, 2), (2, 2), (2, 3), (3, 3)], 'win', 175),
    ([(1, 1), (1, 2), (2, 2), (2, 3), (3, 4)], 'lose', 0.0)
])
def test_all_or_nothing_at_all(rolls: list[tuple[int]],
                               correct_status: str | None,
                               correct_win_amount: float):
    table = Table()
    dice = Dice()
    bet = AllOrNothingAtAll(1)

    status, win_amt = None, None
    for roll in rolls:
        dice.fixed_roll(roll)
        status, win_amt = bet._update_bet(table, dice)
    assert (status, win_amt) == (correct_status, correct_win_amount)

