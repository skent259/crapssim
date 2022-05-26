import pytest
import crapssim
import numpy as np

from crapssim.bet import Bet, PassLine, Come, DontCome, Odds4, Odds6, CAndE
from crapssim.table import Table


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
    t.point.number = 8  # for place bets to pay properly
    outcomes = []
    t.players[0].add_bet(bet)
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            t.dice.fixed_roll([d1, d2])
            status, win_amt, remove = bet.get_status(t), bet.get_win_amount(t), bet.should_remove(t)

            outcomes.append(win_amt if status == "win" else -1 if status == "lose" else 0)

    assert round(np.mean(outcomes), 4) == ev


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


def test_passline_is_irremovable_table_point_off():
    bet = PassLine(5)
    table = Table()
    table.add_player()
    table.point.number = 6
    assert bet.is_removable(table.players[0]) is False


def test_come_is_removable_without_point():
    bet = Come(5)
    table = Table()
    table.add_player()
    table.point.number = 6
    assert bet.is_removable(table.players[0]) is True


def test_come_is_irremovable_with_point():
    bet = Come(5)
    bet.point = 10
    table = Table()
    table.add_player()
    table.point.number = 6
    assert bet.is_removable(table.players[0]) is False


def test_pass_line_odds_allowed():
    table = Table()
    table.add_player()
    table.players[0].bets_on_table = [PassLine(5)]
    table.point.number = 6
    bet = Odds6(25)
    assert bet.allowed(table.players[0])


def test_pass_line_odds_too_high():
    table = Table()
    table.add_player()
    table.players[0].bets_on_table = [PassLine(5)]
    table.point.number = 4
    bet = Odds4(25)
    assert bet.allowed(table.players[0]) is False


def test_come_odds_allowed():
    table = Table()
    table.add_player()
    come_bet = Come(5)
    come_bet.point = 6
    table.players[0].bets_on_table = [come_bet]
    bet = Odds6(25)
    assert bet.allowed(table.players[0])


def test_come_odds_not_allowed():
    table = Table()
    table.add_player()
    come_bet = Come(5)
    come_bet.point = 6
    table.players[0].bets_on_table = [come_bet]
    bet = Odds6(9000)
    assert bet.allowed(table.players[0]) is False
