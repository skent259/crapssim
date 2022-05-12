import pytest
import crapssim
import numpy as np

from crapssim import Player
from crapssim.bet import Fire, Bet, PassLine, Come, Odds, DontPass, DontCome, Field
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
    t = Table()
    p = Player(100)
    p.sit_at_table(t)
    t.point.status = "On"  # for place bets to pay properly
    outcomes = []
    bet.player = p
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            t.dice.fixed_roll([d1, d2])
            status, win_amt, remove = bet.get_status(t), bet.get_win_amount(t), bet.should_remove(t)

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
    player = Player(100)
    bet = Fire(1)
    player.sit_at_table(table)
    player.add_bet(bet, table)

    # table.fixed_run(rolls)
    for roll in rolls:
        table.fixed_roll_and_update(roll)

    status, win_amt, remove = bet.get_status(table), bet.get_win_amount(table), bet.should_remove(table)

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
    player = Player(100)
    player.sit_at_table(table)
    dice = Dice()
    dice.total = point_number

    point = Point()
    point.update(dice)

    table.point = point

    assert bet.allowed(table=table, player=player) == allowed


@pytest.mark.parametrize('bet, new_shooter, allowed', [
    (Field(5), True, True),
    (Field(5), False, True),
    (Fire(5), True, True),
    (Fire(5), False, False)
])
def test_bet_allowed_new_shooter(bet, new_shooter, allowed):
    table = Table()
    player = Player(100)
    player.sit_at_table(table)

    if new_shooter is False:
        table.fixed_roll((3, 4))

    assert bet.allowed(table=table, player=player) == allowed
