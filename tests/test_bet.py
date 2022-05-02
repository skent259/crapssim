import pytest
import crapssim
import numpy as np

from crapssim import Player
from crapssim.bet import Fire, Bet, PassLine, Come, Odds, DontPass, DontCome, Field

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
            status, win_amt, remove = bet._update_bet(t, d)

            outcomes.append(win_amt if status == "win" else -1 if status == "lose" else 0)

    assert round(np.mean(outcomes), 4) == ev


@pytest.mark.parametrize('rolls, correct_status, correct_win_amt, correct_remove', [
    ([(6, 1)], None, 0.0, False),
    ([(2, 2), (3, 1), (4, 3), (6, 6)], None, 0.0, False),
    ([(2, 2), (4, 3)], 'lose', 0.0, True),
    ([(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), (5, 5)], 'win', 24, False),
    ([(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), (5, 5), (5, 5), (5, 5)], None, 0.0, False),
    ([(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), (5, 5), (5, 5), (3, 4)], 'lose', 0.0, True),
    ([(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), (5, 5), (2, 3), (2, 3)], 'win', 249, False),
    ([(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), (5, 5), (2, 3), (2, 3), (4, 5), (4, 5)],
     'win', 999, True)
])
def test_fire(rolls, correct_status, correct_win_amt, correct_remove):
    table = Table()
    dice = Dice()
    bet = Fire(1)

    status, win_amt, remove = None, None, None
    for roll in rolls:
        dice.fixed_roll(roll)
        status, win_amt, remove = bet._update_bet(table, dice)

    assert (status, win_amt, remove) == (correct_status, correct_win_amt, correct_remove)


@pytest.mark.parametrize('bet, point_number, allowed', [
    (PassLine(5), None, True),
    (PassLine(5), 6, False),
    (Come(5), None, False),
    (Come(5), 6, True),
    (DontPass(5), None, True),
    (DontPass(5), 4, False),
    (DontCome(5), None, False),
    (DontCome(5), 8, True),
    (Field(5), None, True),
    (Field(5), 4, True)
])
def test_bet_allowed_point(bet, point_number, allowed):
    table = Table()
    dice = Dice()
    dice.total = point_number

    point = Point()
    point.update(dice)

    table.point = point

    assert bet.allowed(table) == allowed


@pytest.mark.parametrize('bet, new_shooter, allowed', [
    (Field(5), True, True),
    (Field(5), False, True),
    (Fire(5), True, True),
    (Fire(5), False, False)
])
def test_bet_allowed_new_shooter(bet, new_shooter, allowed):
    table = Table()

    if new_shooter is False:
        table.fixed_roll((3, 4))

    assert bet.allowed(table) == allowed


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

