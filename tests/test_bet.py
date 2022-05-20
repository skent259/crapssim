import pytest
import crapssim
import numpy as np

from crapssim import Player
from crapssim.bet import Fire, Bet, PassLine, Come, Odds, DontPass, DontCome, Field, Odds4, Odds5, Odds6, Odds8, Odds9, \
    Odds10, Place4, Place5, Place6, Place8, Place9, Place10, LayOdds4, LayOdds5, LayOdds6, LayOdds8, LayOdds9, \
    LayOdds10, Any7, Two, Three, Yo, Boxcars, AnyCraps, CAndE, Hard4, Hard6, Hard8, Hard10
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
    t.add_player()
    t.point.status = "On"  # for place bets to pay properly
    outcomes = []
    t.players[0].add_bet(bet)
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
    table.add_player()
    bet = Fire(1)
    table.players[0].add_bet(bet)

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
    table.add_player()
    dice = Dice()
    dice.total = point_number

    point = Point()
    point.update(dice)

    table.point = point

    assert bet.allowed(player=table.players[0]) == allowed


@pytest.mark.parametrize('bet, new_shooter, allowed', [
    (Field(5), True, True),
    (Field(5), False, True),
    (Fire(5), True, True),
    (Fire(5), False, False)
])
def test_bet_allowed_new_shooter(bet, new_shooter, allowed):
    table = Table()
    table.add_player()

    if new_shooter is False:
        table.fixed_roll((3, 4))

    assert bet.allowed(player=table.players[0]) == allowed


@pytest.mark.parametrize('bet_one, bet_two', [
    (PassLine(5), PassLine(5)),
    (Come(5), Come(5)),
    (Odds4(5), Odds4(5)),
    (Odds5(5), Odds5(5)),
    (Odds6(5), Odds6(5)),
    (Odds8(5), Odds8(5)),
    (Odds9(5), Odds9(5)),
    (Odds10(5), Odds10(5)),
    (Place4(5), Place4(5)),
    (Place5(5), Place5(5)),
    (Place6(5), Place6(5)),
    (Place8(5), Place8(5)),
    (Place9(5), Place9(5)),
    (Place10(5), Place10(5)),
    (Field(5), Field(5)),
    (DontPass(5), DontPass(5)),
    (DontCome(5), DontCome(5)),
    (LayOdds4(5), LayOdds4(5)),
    (LayOdds5(5), LayOdds5(5)),
    (LayOdds6(5), LayOdds6(5)),
    (LayOdds8(5), LayOdds8(5)),
    (LayOdds9(5), LayOdds9(5)),
    (LayOdds10(5), LayOdds10(5)),
    (Any7(5), Any7(5)),
    (Two(5), Two(5)),
    (Three(5), Three(5)),
    (Yo(5), Yo(5)),
    (Boxcars(5), Boxcars(5)),
    (AnyCraps(5), AnyCraps(5)),
    (CAndE(5), CAndE(5)),
    (Hard4(5), Hard4(5)),
    (Hard6(5), Hard6(5)),
    (Hard8(5), Hard8(5)),
    (Hard10(5), Hard10(5)),
    (Fire(5), Fire(5))
])
def test_bet_equality(bet_one, bet_two):
    assert bet_one == bet_two


@pytest.mark.parametrize('bet_one, bet_two', [
    (PassLine(5), Come(5)),
    (PassLine(5), Odds4(5)),
    (PassLine(5), Odds5(5)),
    (PassLine(5), Odds6(5)),
    (PassLine(5), Odds8(5)),
    (PassLine(5), Odds9(5)),
    (PassLine(5), Odds10(5)),
    (PassLine(5), Place4(5)),
    (PassLine(5), Place5(5)),
    (PassLine(5), Place6(5)),
    (PassLine(5), Place8(5)),
    (PassLine(5), Place9(5)),
    (PassLine(5), Place10(5)),
    (PassLine(5), Field(5)),
    (PassLine(5), DontPass(5)),
    (PassLine(5), DontCome(5)),
    (PassLine(5), LayOdds4(5)),
    (PassLine(5), LayOdds5(5)),
    (PassLine(5), LayOdds6(5)),
    (PassLine(5), LayOdds8(5)),
    (PassLine(5), LayOdds9(5)),
    (PassLine(5), LayOdds10(5)),
    (PassLine(5), Any7(5)),
    (PassLine(5), Two(5)),
    (PassLine(5), Three(5)),
    (PassLine(5), Yo(5)),
    (PassLine(5), Boxcars(5)),
    (PassLine(5), AnyCraps(5)),
    (PassLine(5), CAndE(5)),
    (PassLine(5), Hard4(5)),
    (PassLine(5), Hard6(5)),
    (PassLine(5), Hard8(5)),
    (PassLine(5), Hard10(5)),
    (PassLine(5), Fire(5)),
    (Come(5), Odds4(5)),
    (Come(5), Odds5(5)),
    (Come(5), Odds6(5)),
    (Come(5), Odds8(5)),
    (Come(5), Odds9(5)),
    (Come(5), Odds10(5)),
    (Come(5), Place4(5)),
    (Come(5), Place5(5)),
    (Come(5), Place6(5)),
    (Come(5), Place8(5)),
    (Come(5), Place9(5)),
    (Come(5), Place10(5)),
    (Come(5), Field(5)),
    (Come(5), DontPass(5)),
    (Come(5), DontCome(5)),
    (Come(5), LayOdds4(5)),
    (Come(5), LayOdds5(5)),
    (Come(5), LayOdds6(5)),
    (Come(5), LayOdds8(5)),
    (Come(5), LayOdds9(5)),
    (Come(5), LayOdds10(5)),
    (Come(5), Any7(5)),
    (Come(5), Two(5)),
    (Come(5), Three(5)),
    (Come(5), Yo(5)),
    (Come(5), Boxcars(5)),
    (Come(5), AnyCraps(5)),
    (Come(5), CAndE(5)),
    (Come(5), Hard4(5)),
    (Come(5), Hard6(5)),
    (Come(5), Hard8(5)),
    (Come(5), Hard10(5)),
    (Come(5), Fire(5)),
    (Odds4(5), Odds5(5)),
    (Odds4(5), Odds6(5)),
    (Odds4(5), Odds8(5)),
    (Odds4(5), Odds9(5)),
    (Odds4(5), Odds10(5)),
    (Odds4(5), Place4(5)),
    (Odds4(5), Place5(5)),
    (Odds4(5), Place6(5)),
    (Odds4(5), Place8(5)),
    (Odds4(5), Place9(5)),
    (Odds4(5), Place10(5)),
    (Odds4(5), Field(5)),
    (Odds4(5), DontPass(5)),
    (Odds4(5), DontCome(5)),
    (Odds4(5), LayOdds4(5)),
    (Odds4(5), LayOdds5(5)),
    (Odds4(5), LayOdds6(5)),
    (Odds4(5), LayOdds8(5)),
    (Odds4(5), LayOdds9(5)),
    (Odds4(5), LayOdds10(5)),
    (Odds4(5), Any7(5)),
    (Odds4(5), Two(5)),
    (Odds4(5), Three(5)),
    (Odds4(5), Yo(5)),
    (Odds4(5), Boxcars(5)),
    (Odds4(5), AnyCraps(5)),
    (Odds4(5), CAndE(5)),
    (Odds4(5), Hard4(5)),
    (Odds4(5), Hard6(5)),
    (Odds4(5), Hard8(5)),
    (Odds4(5), Hard10(5)),
    (Odds4(5), Fire(5)),
    (Odds5(5), Odds6(5)),
    (Odds5(5), Odds8(5)),
    (Odds5(5), Odds9(5)),
    (Odds5(5), Odds10(5)),
    (Odds5(5), Place4(5)),
    (Odds5(5), Place5(5)),
    (Odds5(5), Place6(5)),
    (Odds5(5), Place8(5)),
    (Odds5(5), Place9(5)),
    (Odds5(5), Place10(5)),
    (Odds5(5), Field(5)),
    (Odds5(5), DontPass(5)),
    (Odds5(5), DontCome(5)),
    (Odds5(5), LayOdds4(5)),
    (Odds5(5), LayOdds5(5)),
    (Odds5(5), LayOdds6(5)),
    (Odds5(5), LayOdds8(5)),
    (Odds5(5), LayOdds9(5)),
    (Odds5(5), LayOdds10(5)),
    (Odds5(5), Any7(5)),
    (Odds5(5), Two(5)),
    (Odds5(5), Three(5)),
    (Odds5(5), Yo(5)),
    (Odds5(5), Boxcars(5)),
    (Odds5(5), AnyCraps(5)),
    (Odds5(5), CAndE(5)),
    (Odds5(5), Hard4(5)),
    (Odds5(5), Hard6(5)),
    (Odds5(5), Hard8(5)),
    (Odds5(5), Hard10(5)),
    (Odds5(5), Fire(5)),
    (Odds6(5), Odds8(5)),
    (Odds6(5), Odds9(5)),
    (Odds6(5), Odds10(5)),
    (Odds6(5), Place4(5)),
    (Odds6(5), Place5(5)),
    (Odds6(5), Place6(5)),
    (Odds6(5), Place8(5)),
    (Odds6(5), Place9(5)),
    (Odds6(5), Place10(5)),
    (Odds6(5), Field(5)),
    (Odds6(5), DontPass(5)),
    (Odds6(5), DontCome(5)),
    (Odds6(5), LayOdds4(5)),
    (Odds6(5), LayOdds5(5)),
    (Odds6(5), LayOdds6(5)),
    (Odds6(5), LayOdds8(5)),
    (Odds6(5), LayOdds9(5)),
    (Odds6(5), LayOdds10(5)),
    (Odds6(5), Any7(5)),
    (Odds6(5), Two(5)),
    (Odds6(5), Three(5)),
    (Odds6(5), Yo(5)),
    (Odds6(5), Boxcars(5)),
    (Odds6(5), AnyCraps(5)),
    (Odds6(5), CAndE(5)),
    (Odds6(5), Hard4(5)),
    (Odds6(5), Hard6(5)),
    (Odds6(5), Hard8(5)),
    (Odds6(5), Hard10(5)),
    (Odds6(5), Fire(5)),
    (Odds8(5), Odds9(5)),
    (Odds8(5), Odds10(5)),
    (Odds8(5), Place4(5)),
    (Odds8(5), Place5(5)),
    (Odds8(5), Place6(5)),
    (Odds8(5), Place8(5)),
    (Odds8(5), Place9(5)),
    (Odds8(5), Place10(5)),
    (Odds8(5), Field(5)),
    (Odds8(5), DontPass(5)),
    (Odds8(5), DontCome(5)),
    (Odds8(5), LayOdds4(5)),
    (Odds8(5), LayOdds5(5)),
    (Odds8(5), LayOdds6(5)),
    (Odds8(5), LayOdds8(5)),
    (Odds8(5), LayOdds9(5)),
    (Odds8(5), LayOdds10(5)),
    (Odds8(5), Any7(5)),
    (Odds8(5), Two(5)),
    (Odds8(5), Three(5)),
    (Odds8(5), Yo(5)),
    (Odds8(5), Boxcars(5)),
    (Odds8(5), AnyCraps(5)),
    (Odds8(5), CAndE(5)),
    (Odds8(5), Hard4(5)),
    (Odds8(5), Hard6(5)),
    (Odds8(5), Hard8(5)),
    (Odds8(5), Hard10(5)),
    (Odds8(5), Fire(5)),
    (Odds9(5), Odds10(5)),
    (Odds9(5), Place4(5)),
    (Odds9(5), Place5(5)),
    (Odds9(5), Place6(5)),
    (Odds9(5), Place8(5)),
    (Odds9(5), Place9(5)),
    (Odds9(5), Place10(5)),
    (Odds9(5), Field(5)),
    (Odds9(5), DontPass(5)),
    (Odds9(5), DontCome(5)),
    (Odds9(5), LayOdds4(5)),
    (Odds9(5), LayOdds5(5)),
    (Odds9(5), LayOdds6(5)),
    (Odds9(5), LayOdds8(5)),
    (Odds9(5), LayOdds9(5)),
    (Odds9(5), LayOdds10(5)),
    (Odds9(5), Any7(5)),
    (Odds9(5), Two(5)),
    (Odds9(5), Three(5)),
    (Odds9(5), Yo(5)),
    (Odds9(5), Boxcars(5)),
    (Odds9(5), AnyCraps(5)),
    (Odds9(5), CAndE(5)),
    (Odds9(5), Hard4(5)),
    (Odds9(5), Hard6(5)),
    (Odds9(5), Hard8(5)),
    (Odds9(5), Hard10(5)),
    (Odds9(5), Fire(5)),
    (Odds10(5), Place4(5)),
    (Odds10(5), Place5(5)),
    (Odds10(5), Place6(5)),
    (Odds10(5), Place8(5)),
    (Odds10(5), Place9(5)),
    (Odds10(5), Place10(5)),
    (Odds10(5), Field(5)),
    (Odds10(5), DontPass(5)),
    (Odds10(5), DontCome(5)),
    (Odds10(5), LayOdds4(5)),
    (Odds10(5), LayOdds5(5)),
    (Odds10(5), LayOdds6(5)),
    (Odds10(5), LayOdds8(5)),
    (Odds10(5), LayOdds9(5)),
    (Odds10(5), LayOdds10(5)),
    (Odds10(5), Any7(5)),
    (Odds10(5), Two(5)),
    (Odds10(5), Three(5)),
    (Odds10(5), Yo(5)),
    (Odds10(5), Boxcars(5)),
    (Odds10(5), AnyCraps(5)),
    (Odds10(5), CAndE(5)),
    (Odds10(5), Hard4(5)),
    (Odds10(5), Hard6(5)),
    (Odds10(5), Hard8(5)),
    (Odds10(5), Hard10(5)),
    (Odds10(5), Fire(5)),
    (Place4(5), Place5(5)),
    (Place4(5), Place6(5)),
    (Place4(5), Place8(5)),
    (Place4(5), Place9(5)),
    (Place4(5), Place10(5)),
    (Place4(5), Field(5)),
    (Place4(5), DontPass(5)),
    (Place4(5), DontCome(5)),
    (Place4(5), LayOdds4(5)),
    (Place4(5), LayOdds5(5)),
    (Place4(5), LayOdds6(5)),
    (Place4(5), LayOdds8(5)),
    (Place4(5), LayOdds9(5)),
    (Place4(5), LayOdds10(5)),
    (Place4(5), Any7(5)),
    (Place4(5), Two(5)),
    (Place4(5), Three(5)),
    (Place4(5), Yo(5)),
    (Place4(5), Boxcars(5)),
    (Place4(5), AnyCraps(5)),
    (Place4(5), CAndE(5)),
    (Place4(5), Hard4(5)),
    (Place4(5), Hard6(5)),
    (Place4(5), Hard8(5)),
    (Place4(5), Hard10(5)),
    (Place4(5), Fire(5)),
    (Place5(5), Place6(5)),
    (Place5(5), Place8(5)),
    (Place5(5), Place9(5)),
    (Place5(5), Place10(5)),
    (Place5(5), Field(5)),
    (Place5(5), DontPass(5)),
    (Place5(5), DontCome(5)),
    (Place5(5), LayOdds4(5)),
    (Place5(5), LayOdds5(5)),
    (Place5(5), LayOdds6(5)),
    (Place5(5), LayOdds8(5)),
    (Place5(5), LayOdds9(5)),
    (Place5(5), LayOdds10(5)),
    (Place5(5), Any7(5)),
    (Place5(5), Two(5)),
    (Place5(5), Three(5)),
    (Place5(5), Yo(5)),
    (Place5(5), Boxcars(5)),
    (Place5(5), AnyCraps(5)),
    (Place5(5), CAndE(5)),
    (Place5(5), Hard4(5)),
    (Place5(5), Hard6(5)),
    (Place5(5), Hard8(5)),
    (Place5(5), Hard10(5)),
    (Place5(5), Fire(5)),
    (Place6(5), Place8(5)),
    (Place6(5), Place9(5)),
    (Place6(5), Place10(5)),
    (Place6(5), Field(5)),
    (Place6(5), DontPass(5)),
    (Place6(5), DontCome(5)),
    (Place6(5), LayOdds4(5)),
    (Place6(5), LayOdds5(5)),
    (Place6(5), LayOdds6(5)),
    (Place6(5), LayOdds8(5)),
    (Place6(5), LayOdds9(5)),
    (Place6(5), LayOdds10(5)),
    (Place6(5), Any7(5)),
    (Place6(5), Two(5)),
    (Place6(5), Three(5)),
    (Place6(5), Yo(5)),
    (Place6(5), Boxcars(5)),
    (Place6(5), AnyCraps(5)),
    (Place6(5), CAndE(5)),
    (Place6(5), Hard4(5)),
    (Place6(5), Hard6(5)),
    (Place6(5), Hard8(5)),
    (Place6(5), Hard10(5)),
    (Place6(5), Fire(5)),
    (Place8(5), Place9(5)),
    (Place8(5), Place10(5)),
    (Place8(5), Field(5)),
    (Place8(5), DontPass(5)),
    (Place8(5), DontCome(5)),
    (Place8(5), LayOdds4(5)),
    (Place8(5), LayOdds5(5)),
    (Place8(5), LayOdds6(5)),
    (Place8(5), LayOdds8(5)),
    (Place8(5), LayOdds9(5)),
    (Place8(5), LayOdds10(5)),
    (Place8(5), Any7(5)),
    (Place8(5), Two(5)),
    (Place8(5), Three(5)),
    (Place8(5), Yo(5)),
    (Place8(5), Boxcars(5)),
    (Place8(5), AnyCraps(5)),
    (Place8(5), CAndE(5)),
    (Place8(5), Hard4(5)),
    (Place8(5), Hard6(5)),
    (Place8(5), Hard8(5)),
    (Place8(5), Hard10(5)),
    (Place8(5), Fire(5)),
    (Place9(5), Place10(5)),
    (Place9(5), Field(5)),
    (Place9(5), DontPass(5)),
    (Place9(5), DontCome(5)),
    (Place9(5), LayOdds4(5)),
    (Place9(5), LayOdds5(5)),
    (Place9(5), LayOdds6(5)),
    (Place9(5), LayOdds8(5)),
    (Place9(5), LayOdds9(5)),
    (Place9(5), LayOdds10(5)),
    (Place9(5), Any7(5)),
    (Place9(5), Two(5)),
    (Place9(5), Three(5)),
    (Place9(5), Yo(5)),
    (Place9(5), Boxcars(5)),
    (Place9(5), AnyCraps(5)),
    (Place9(5), CAndE(5)),
    (Place9(5), Hard4(5)),
    (Place9(5), Hard6(5)),
    (Place9(5), Hard8(5)),
    (Place9(5), Hard10(5)),
    (Place9(5), Fire(5)),
    (Place10(5), Field(5)),
    (Place10(5), DontPass(5)),
    (Place10(5), DontCome(5)),
    (Place10(5), LayOdds4(5)),
    (Place10(5), LayOdds5(5)),
    (Place10(5), LayOdds6(5)),
    (Place10(5), LayOdds8(5)),
    (Place10(5), LayOdds9(5)),
    (Place10(5), LayOdds10(5)),
    (Place10(5), Any7(5)),
    (Place10(5), Two(5)),
    (Place10(5), Three(5)),
    (Place10(5), Yo(5)),
    (Place10(5), Boxcars(5)),
    (Place10(5), AnyCraps(5)),
    (Place10(5), CAndE(5)),
    (Place10(5), Hard4(5)),
    (Place10(5), Hard6(5)),
    (Place10(5), Hard8(5)),
    (Place10(5), Hard10(5)),
    (Place10(5), Fire(5)),
    (Field(5), DontPass(5)),
    (Field(5), DontCome(5)),
    (Field(5), LayOdds4(5)),
    (Field(5), LayOdds5(5)),
    (Field(5), LayOdds6(5)),
    (Field(5), LayOdds8(5)),
    (Field(5), LayOdds9(5)),
    (Field(5), LayOdds10(5)),
    (Field(5), Any7(5)),
    (Field(5), Two(5)),
    (Field(5), Three(5)),
    (Field(5), Yo(5)),
    (Field(5), Boxcars(5)),
    (Field(5), AnyCraps(5)),
    (Field(5), CAndE(5)),
    (Field(5), Hard4(5)),
    (Field(5), Hard6(5)),
    (Field(5), Hard8(5)),
    (Field(5), Hard10(5)),
    (Field(5), Fire(5)),
    (DontPass(5), DontCome(5)),
    (DontPass(5), LayOdds4(5)),
    (DontPass(5), LayOdds5(5)),
    (DontPass(5), LayOdds6(5)),
    (DontPass(5), LayOdds8(5)),
    (DontPass(5), LayOdds9(5)),
    (DontPass(5), LayOdds10(5)),
    (DontPass(5), Any7(5)),
    (DontPass(5), Two(5)),
    (DontPass(5), Three(5)),
    (DontPass(5), Yo(5)),
    (DontPass(5), Boxcars(5)),
    (DontPass(5), AnyCraps(5)),
    (DontPass(5), CAndE(5)),
    (DontPass(5), Hard4(5)),
    (DontPass(5), Hard6(5)),
    (DontPass(5), Hard8(5)),
    (DontPass(5), Hard10(5)),
    (DontPass(5), Fire(5)),
    (DontCome(5), LayOdds4(5)),
    (DontCome(5), LayOdds5(5)),
    (DontCome(5), LayOdds6(5)),
    (DontCome(5), LayOdds8(5)),
    (DontCome(5), LayOdds9(5)),
    (DontCome(5), LayOdds10(5)),
    (DontCome(5), Any7(5)),
    (DontCome(5), Two(5)),
    (DontCome(5), Three(5)),
    (DontCome(5), Yo(5)),
    (DontCome(5), Boxcars(5)),
    (DontCome(5), AnyCraps(5)),
    (DontCome(5), CAndE(5)),
    (DontCome(5), Hard4(5)),
    (DontCome(5), Hard6(5)),
    (DontCome(5), Hard8(5)),
    (DontCome(5), Hard10(5)),
    (DontCome(5), Fire(5)),
    (LayOdds4(5), LayOdds5(5)),
    (LayOdds4(5), LayOdds6(5)),
    (LayOdds4(5), LayOdds8(5)),
    (LayOdds4(5), LayOdds9(5)),
    (LayOdds4(5), LayOdds10(5)),
    (LayOdds4(5), Any7(5)),
    (LayOdds4(5), Two(5)),
    (LayOdds4(5), Three(5)),
    (LayOdds4(5), Yo(5)),
    (LayOdds4(5), Boxcars(5)),
    (LayOdds4(5), AnyCraps(5)),
    (LayOdds4(5), CAndE(5)),
    (LayOdds4(5), Hard4(5)),
    (LayOdds4(5), Hard6(5)),
    (LayOdds4(5), Hard8(5)),
    (LayOdds4(5), Hard10(5)),
    (LayOdds4(5), Fire(5)),
    (LayOdds5(5), LayOdds6(5)),
    (LayOdds5(5), LayOdds8(5)),
    (LayOdds5(5), LayOdds9(5)),
    (LayOdds5(5), LayOdds10(5)),
    (LayOdds5(5), Any7(5)),
    (LayOdds5(5), Two(5)),
    (LayOdds5(5), Three(5)),
    (LayOdds5(5), Yo(5)),
    (LayOdds5(5), Boxcars(5)),
    (LayOdds5(5), AnyCraps(5)),
    (LayOdds5(5), CAndE(5)),
    (LayOdds5(5), Hard4(5)),
    (LayOdds5(5), Hard6(5)),
    (LayOdds5(5), Hard8(5)),
    (LayOdds5(5), Hard10(5)),
    (LayOdds5(5), Fire(5)),
    (LayOdds6(5), LayOdds8(5)),
    (LayOdds6(5), LayOdds9(5)),
    (LayOdds6(5), LayOdds10(5)),
    (LayOdds6(5), Any7(5)),
    (LayOdds6(5), Two(5)),
    (LayOdds6(5), Three(5)),
    (LayOdds6(5), Yo(5)),
    (LayOdds6(5), Boxcars(5)),
    (LayOdds6(5), AnyCraps(5)),
    (LayOdds6(5), CAndE(5)),
    (LayOdds6(5), Hard4(5)),
    (LayOdds6(5), Hard6(5)),
    (LayOdds6(5), Hard8(5)),
    (LayOdds6(5), Hard10(5)),
    (LayOdds6(5), Fire(5)),
    (LayOdds8(5), LayOdds9(5)),
    (LayOdds8(5), LayOdds10(5)),
    (LayOdds8(5), Any7(5)),
    (LayOdds8(5), Two(5)),
    (LayOdds8(5), Three(5)),
    (LayOdds8(5), Yo(5)),
    (LayOdds8(5), Boxcars(5)),
    (LayOdds8(5), AnyCraps(5)),
    (LayOdds8(5), CAndE(5)),
    (LayOdds8(5), Hard4(5)),
    (LayOdds8(5), Hard6(5)),
    (LayOdds8(5), Hard8(5)),
    (LayOdds8(5), Hard10(5)),
    (LayOdds8(5), Fire(5)),
    (LayOdds9(5), LayOdds10(5)),
    (LayOdds9(5), Any7(5)),
    (LayOdds9(5), Two(5)),
    (LayOdds9(5), Three(5)),
    (LayOdds9(5), Yo(5)),
    (LayOdds9(5), Boxcars(5)),
    (LayOdds9(5), AnyCraps(5)),
    (LayOdds9(5), CAndE(5)),
    (LayOdds9(5), Hard4(5)),
    (LayOdds9(5), Hard6(5)),
    (LayOdds9(5), Hard8(5)),
    (LayOdds9(5), Hard10(5)),
    (LayOdds9(5), Fire(5)),
    (LayOdds10(5), Any7(5)),
    (LayOdds10(5), Two(5)),
    (LayOdds10(5), Three(5)),
    (LayOdds10(5), Yo(5)),
    (LayOdds10(5), Boxcars(5)),
    (LayOdds10(5), AnyCraps(5)),
    (LayOdds10(5), CAndE(5)),
    (LayOdds10(5), Hard4(5)),
    (LayOdds10(5), Hard6(5)),
    (LayOdds10(5), Hard8(5)),
    (LayOdds10(5), Hard10(5)),
    (LayOdds10(5), Fire(5)),
    (Any7(5), Two(5)),
    (Any7(5), Three(5)),
    (Any7(5), Yo(5)),
    (Any7(5), Boxcars(5)),
    (Any7(5), AnyCraps(5)),
    (Any7(5), CAndE(5)),
    (Any7(5), Hard4(5)),
    (Any7(5), Hard6(5)),
    (Any7(5), Hard8(5)),
    (Any7(5), Hard10(5)),
    (Any7(5), Fire(5)),
    (Two(5), Three(5)),
    (Two(5), Yo(5)),
    (Two(5), Boxcars(5)),
    (Two(5), AnyCraps(5)),
    (Two(5), CAndE(5)),
    (Two(5), Hard4(5)),
    (Two(5), Hard6(5)),
    (Two(5), Hard8(5)),
    (Two(5), Hard10(5)),
    (Two(5), Fire(5)),
    (Three(5), Yo(5)),
    (Three(5), Boxcars(5)),
    (Three(5), AnyCraps(5)),
    (Three(5), CAndE(5)),
    (Three(5), Hard4(5)),
    (Three(5), Hard6(5)),
    (Three(5), Hard8(5)),
    (Three(5), Hard10(5)),
    (Three(5), Fire(5)),
    (Yo(5), Boxcars(5)),
    (Yo(5), AnyCraps(5)),
    (Yo(5), CAndE(5)),
    (Yo(5), Hard4(5)),
    (Yo(5), Hard6(5)),
    (Yo(5), Hard8(5)),
    (Yo(5), Hard10(5)),
    (Yo(5), Fire(5)),
    (Boxcars(5), AnyCraps(5)),
    (Boxcars(5), CAndE(5)),
    (Boxcars(5), Hard4(5)),
    (Boxcars(5), Hard6(5)),
    (Boxcars(5), Hard8(5)),
    (Boxcars(5), Hard10(5)),
    (Boxcars(5), Fire(5)),
    (AnyCraps(5), CAndE(5)),
    (AnyCraps(5), Hard4(5)),
    (AnyCraps(5), Hard6(5)),
    (AnyCraps(5), Hard8(5)),
    (AnyCraps(5), Hard10(5)),
    (AnyCraps(5), Fire(5)),
    (CAndE(5), Hard4(5)),
    (CAndE(5), Hard6(5)),
    (CAndE(5), Hard8(5)),
    (CAndE(5), Hard10(5)),
    (CAndE(5), Fire(5)),
    (Hard4(5), Hard6(5)),
    (Hard4(5), Hard8(5)),
    (Hard4(5), Hard10(5)),
    (Hard4(5), Fire(5)),
    (Hard6(5), Hard8(5)),
    (Hard6(5), Hard10(5)),
    (Hard6(5), Fire(5)),
    (Hard8(5), Hard10(5)),
    (Hard8(5), Fire(5)),
    (Hard10(5), Fire(5))
])
def test_bet_type_inequality(bet_one, bet_two):
    assert bet_one != bet_two


@pytest.mark.parametrize('bet_one, bet_two', [
    (PassLine(10), PassLine(15)),
    (Come(25), Come(10)),
    (Odds4(5), Odds4(20)),
    (Odds5(10), Odds5(25)),
    (Odds6(25), Odds6(10)),
    (Odds8(20), Odds8(30)),
    (Odds9(15), Odds9(5)),
    (Odds10(20), Odds10(5)),
    (Place4(10), Place4(30)),
    (Place5(30), Place5(10)),
    (Place6(25), Place6(20)),
    (Place8(30), Place8(15)),
    (Place9(15), Place9(25)),
    (Place10(5), Place10(10)),
    (Field(30), Field(5)),
    (DontPass(20), DontPass(5)),
    (DontCome(15), DontCome(25)),
    (LayOdds4(10), LayOdds4(25)),
    (LayOdds5(10), LayOdds5(15)),
    (LayOdds6(30), LayOdds6(5)),
    (LayOdds8(30), LayOdds8(10)),
    (LayOdds9(5), LayOdds9(10)),
    (LayOdds10(10), LayOdds10(30)),
    (Any7(30), Any7(25)),
    (Two(20), Two(25)),
    (Three(10), Three(25)),
    (Yo(30), Yo(10)),
    (Boxcars(30), Boxcars(10)),
    (AnyCraps(25), AnyCraps(15)),
    (CAndE(5), CAndE(25)),
    (Hard4(25), Hard4(10)),
    (Hard6(15), Hard6(25)),
    (Hard8(15), Hard8(5)),
    (Hard10(20), Hard10(5)),
    (Fire(20), Fire(30))
])
def test_bet_amount_inequality(bet_one, bet_two):
    assert bet_one != bet_two


def test_come_equality():
    come_one = Come(5)
    come_one.point = 5
    come_one.new_point = True

    come_two = Come(5)
    come_two.point = 5
    come_two.new_point = True

    assert come_one == come_two


def test_come_point_inequality():
    come_one = Come(5)
    come_one.point = 5
    come_one.new_point = True

    come_two = Come(5)
    come_two.point = 6
    come_two.new_point = True

    assert come_one != come_two


def test_dont_come_equality():
    dont_come_one = DontCome(5)
    dont_come_one.point = 5
    dont_come_one.new_point = True

    dont_come_two = DontCome(5)
    dont_come_two.point = 5
    dont_come_two.new_point = True

    assert dont_come_one == dont_come_two


def test_dont_come_point_inequality():
    dont_come_one = DontCome(5)
    dont_come_one.point = 5
    dont_come_one.new_point = True

    dont_come_two = Come(5)
    dont_come_two.point = 8
    dont_come_two.new_point = True

    assert dont_come_one != dont_come_two


def test_cant_instantiate_bet_object():
    with pytest.raises(TypeError) as e_info:
        Bet(400)


@pytest.mark.parametrize('bet, ratio', [
    (PassLine, 1),
    (Come, 1),
    (DontPass, 1),
    (DontCome, 1),
    (Odds4, 2 / 1),
    (Odds5, 3 / 2),
    (Odds6, 6 / 5),
    (Odds8, 6 / 5),
    (Odds9, 3 / 2),
    (Odds10, 2 / 1),
    (Place4, 9 / 5),
    (Place5, 7 / 5),
    (Place6, 7 / 6),
    (Place8, 7 / 6),
    (Place9, 7 / 5),
    (Place10, 9 / 5),
    (LayOdds4, 1 / 2),
    (LayOdds5, 2 / 3),
    (LayOdds6, 5 / 6),
    (LayOdds8, 5 / 6),
    (LayOdds9, 2 / 3),
    (LayOdds10, 1 / 2),
    (Any7, 4),
    (Two, 30),
    (Three, 15),
    (Yo, 15),
    (Boxcars, 30),
    (AnyCraps, 7),
    (Hard4, 7),
    (Hard6, 9),
    (Hard8, 9),
    (Hard10, 7)
])
def test_get_static_payout_ratio(bet, ratio):
    assert bet.payout_ratio == ratio


def test_get_cande_dice_2_payout_ratio():
    table = Table()
    table.dice.fixed_roll((1, 1))
    assert CAndE(5).get_payout_ratio(table) == 3


def test_get_cande_dice_3_payout_ratio():
    table = Table()
    table.dice.fixed_roll((1, 2))
    assert CAndE(5).get_payout_ratio(table) == 3


def test_get_cande_dice_11_payout_ratio():
    table = Table()
    table.dice.fixed_roll((6, 5))
    assert CAndE(5).get_payout_ratio(table) == 7


def test_get_cande_dice_12_payout_ratio():
    table = Table()
    table.dice.fixed_roll((6, 6))
    assert CAndE(5).get_payout_ratio(table) == 3


@pytest.mark.parametrize('dice1, dice2, correct_ratio', [
    (1, 1, 2),
    (1, 2, 1),
    (2, 2, 1),
    (5, 4, 1),
    (5, 5, 1),
    (6, 5, 1),
    (6, 6, 2)
])
def test_get_field_default_table_payout_ratio(dice1, dice2, correct_ratio):
    table = Table()
    table.dice.fixed_roll((dice1, dice2))
    assert Field(5).get_payout_ratio(table) == correct_ratio


@pytest.mark.parametrize('dice1, dice2, correct_ratio', [
    (1, 1, 2),
    (1, 2, 14),
    (2, 2, 14000),
    (5, 4, 1),
    (5, 5, 1),
    (6, 5, 1),
    (6, 6, 3)
])
def test_get_field_non_default_table_payout_ratio(dice1, dice2, correct_ratio):
    table = Table()
    table.settings['field_payouts'].update({3: 14, 12: 3, 4: 14000})
    table.dice.fixed_roll((dice1, dice2))
    assert Field(5).get_payout_ratio(table) == correct_ratio


@pytest.mark.parametrize('points_made, correct_ratio', [
    ([4, 5, 6, 9], 24),
    ([4, 5, 6, 9, 10], 249),
    ([4, 5, 6, 8, 9, 10], 999)
])
def test_get_fire_default_table_payout_ratio(points_made, correct_ratio):
    table = Table()
    bet = Fire(5)
    bet.points_made = points_made
    assert bet.get_payout_ratio(table) == correct_ratio


@pytest.mark.parametrize('points_made, correct_ratio', [
    ([4, 5, 6], 6),
    ([4, 5, 6, 9], 9),
    ([4, 5, 6, 9, 10], 69),
    ([4, 5, 6, 8, 9, 10], 420)
])
def test_get_fire_non_default_table_payout_ratio(points_made, correct_ratio):
    table = Table()
    table.settings['fire_points'] = {3: 6, 4: 9, 5: 69, 6: 420}
    bet = Fire(5)
    bet.points_made = points_made
    assert bet.get_payout_ratio(table) == correct_ratio


@pytest.mark.parametrize('bet', [
    PassLine(5),
    Odds4(5),
    Odds5(5),
    Odds6(5),
    Odds8(5),
    Odds9(5),
    Odds10(5),
    Place4(5),
    Place5(5),
    Place6(6),
    Place8(8),
    Place9(9),
    Place10(10),
    LayOdds4(5),
    LayOdds5(5),
    LayOdds6(5),
    LayOdds8(5),
    LayOdds9(5),
    LayOdds10(5),
    Field(5),
    DontPass(5),
    DontCome(5),
    Any7(5),
    Two(5),
    Three(5),
    Yo(5),
    Boxcars(5),
    AnyCraps(5),
    Hard4(5),
    Hard6(5),
    Hard8(5),
    Hard10(5)
])
def test_is_removable_table_point_off(bet):
    table = Table()
    table.add_player()
    assert bet.is_removable(table.players[0]) is True


@pytest.mark.parametrize('bet', [
    Odds4(5),
    Odds5(5),
    Odds6(5),
    Odds8(5),
    Odds9(5),
    Odds10(5),
    Place4(5),
    Place5(5),
    Place6(6),
    Place8(8),
    Place9(9),
    Place10(10),
    LayOdds4(5),
    LayOdds5(5),
    LayOdds6(5),
    LayOdds8(5),
    LayOdds9(5),
    LayOdds10(5),
    Field(5),
    DontPass(5),
    DontCome(5),
    Any7(5),
    Two(5),
    Three(5),
    Yo(5),
    Boxcars(5),
    AnyCraps(5),
    Hard4(5),
    Hard6(5),
    Hard8(5),
    Hard10(5)
])
def test_is_removable_table_point_on(bet):
    table = Table()
    table.add_player()
    table.point.number = 6
    table.point.status = 'On'
    assert bet.is_removable(table.players[0]) is True


def test_passline_is_irremovable_table_point_off():
    bet = PassLine(5)
    table = Table()
    table.add_player()
    table.point.number = 6
    table.point.status = 'On'
    assert bet.is_removable(table.players[0]) is False


def test_come_is_removable_without_point():
    bet = Come(5)
    table = Table()
    table.add_player()
    table.point.number = 6
    table.point.status = 'On'
    assert bet.is_removable(table.players[0]) is True


def test_come_is_irremovable_with_point():
    bet = Come(5)
    bet.point = 10
    table = Table()
    table.add_player()
    table.point.number = 6
    table.point.status = 'On'
    assert bet.is_removable(table.players[0]) is False


@pytest.mark.parametrize('bet', [
    PassLine(5),
    Place4(5),
    Place5(5),
    Place6(5),
    Place8(5),
    Place9(5),
    Place10(5),
    DontPass(5),
    Field(5),
    Any7(5),
    Two(5),
    Three(5),
    Yo(5),
    Boxcars(5),
    AnyCraps(5),
    Hard4(5),
    Hard6(5),
    Hard8(5),
    Hard10(5)
])
def test_bets_always_allowed_point_off(bet):
    table = Table()
    table.add_player()
    assert bet.allowed(table.players[0])


@pytest.mark.parametrize('bet', [
    Come(5),
    Place4(5),
    Place5(5),
    Place6(5),
    Place8(5),
    Place9(5),
    Place10(5),
    DontCome(5),
    Field(5),
    Any7(5),
    Two(5),
    Three(5),
    Yo(5),
    Boxcars(5),
    AnyCraps(5),
    Hard4(5),
    Hard6(5),
    Hard8(5),
    Hard10(5)
])
def test_bets_always_allowed_point_on(bet):
    table = Table()
    table.point.number = 10
    table.point.status = 'On'
    table.add_player()
    assert bet.allowed(table.players[0])



