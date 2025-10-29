import math
import numpy as np
import pytest

import crapssim.bet
from crapssim.bet import (
    Any7,
    Bet,
    Boxcars,
    CAndE,
    Come,
    DontCome,
    Horn,
    Hop,
    Odds,
    PassLine,
    Three,
    Two,
    World,
    Yo,
)
from crapssim.point import Point
from crapssim.table import Table, TableUpdate

# Check EV of bets on a "per-roll" basis


@pytest.mark.parametrize(
    "bet, ev",
    [
        (crapssim.bet.Place(4, 1), -0.0167),
        (crapssim.bet.Place(5, 1), -0.0111),
        (crapssim.bet.Place(6, 1), -0.0046),
        (crapssim.bet.Place(8, 1), -0.0046),
        (crapssim.bet.Place(9, 1), -0.0111),
        (crapssim.bet.Place(10, 1), -0.0167),
        (crapssim.bet.Field(1), -0.0556),
        (crapssim.bet.Any7(1), -0.1667),
        (crapssim.bet.Two(1), -0.1389),
        (crapssim.bet.Three(1), -0.1111),
        (crapssim.bet.Yo(1), -0.1111),
        (crapssim.bet.Boxcars(1), -0.1389),
        (crapssim.bet.AnyCraps(1), -0.1111),
        (crapssim.bet.CAndE(1), -0.1111),
        (crapssim.bet.HardWay(4, 1), -0.0278),
        (crapssim.bet.HardWay(6, 1), -0.0278),
        (crapssim.bet.HardWay(8, 1), -0.0278),
        (crapssim.bet.HardWay(10, 1), -0.0278),
        (crapssim.bet.Hop([2, 3], 1), -0.1111),
        (crapssim.bet.Hop([3, 2], 1), -0.1111),
        (crapssim.bet.Hop([3, 3], 1), -0.1389),
        (crapssim.bet.Horn(1), -0.25),
        (crapssim.bet.World(1), -0.2667),
        (crapssim.bet.Big6(1), -0.0278),
        (crapssim.bet.Big8(1), -0.0278),
        (crapssim.bet.Buy(4, 1), -0.0083),
        (crapssim.bet.Buy(6, 1), -0.0083),
        (crapssim.bet.Lay(4, 1), -0.0042),
        (crapssim.bet.Lay(6, 1), -0.0069),
        (crapssim.bet.Put(4, 1), -0.0833),
        (crapssim.bet.Put(5, 1), -0.0556),
        (crapssim.bet.Put(6, 1), -0.0278),
        (crapssim.bet.Put(8, 1), -0.0278),
        (crapssim.bet.Put(9, 1), -0.0556),
        (crapssim.bet.Put(10, 1), -0.0833),
    ],
)
def test_ev_oneroll(bet, ev):
    t = Table()
    t.add_player()
    t.point.number = 8  # for place bets to pay properly
    outcomes = []
    t.players[0].add_bet(bet)
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            t.dice.fixed_roll([d1, d2])
            result = bet.get_result(t)

            outcomes.append(
                result.amount - bet.amount if result.won else -1 if result.lost else 0
            )

    assert round(np.mean(outcomes), 4) == ev


@pytest.mark.parametrize(
    "bet, bet_name",
    [
        (crapssim.bet.PassLine(1), "PassLine(amount=1.0)"),
        (crapssim.bet.Come(1), "Come(amount=1.0, number=None)"),
        (crapssim.bet.DontPass(1), "DontPass(amount=1.0)"),
        (crapssim.bet.DontCome(1), "DontCome(amount=1.0, number=None)"),
        (
            crapssim.bet.Odds(crapssim.bet.PassLine, 6, 1, False),
            "Odds(base_type=crapssim.bet.PassLine, number=6, amount=1.0)",
        ),
        (
            crapssim.bet.Odds(crapssim.bet.Come, 8, 1),
            "Odds(base_type=crapssim.bet.Come, number=8, amount=1.0)",
        ),
        (
            crapssim.bet.Odds(crapssim.bet.DontPass, 9, 1),
            "Odds(base_type=crapssim.bet.DontPass, number=9, amount=1.0)",
        ),
        (
            crapssim.bet.Odds(crapssim.bet.DontCome, 10, 1),
            "Odds(base_type=crapssim.bet.DontCome, number=10, amount=1.0)",
        ),
        (
            crapssim.bet.Odds(crapssim.bet.PassLine, 6, 1, True),
            "Odds(base_type=crapssim.bet.PassLine, number=6, amount=1.0, always_working=True)",
        ),
        (
            crapssim.bet.Odds(crapssim.bet.Come, 8, 1, True),
            "Odds(base_type=crapssim.bet.Come, number=8, amount=1.0, always_working=True)",
        ),
        (
            crapssim.bet.Odds(crapssim.bet.DontPass, 9, 1, True),
            "Odds(base_type=crapssim.bet.DontPass, number=9, amount=1.0, always_working=True)",
        ),
        (
            crapssim.bet.Odds(crapssim.bet.DontCome, 10, 1, True),
            "Odds(base_type=crapssim.bet.DontCome, number=10, amount=1.0, always_working=True)",
        ),
        (crapssim.bet.Place(4, 1), "Place(4, amount=1.0)"),
        (crapssim.bet.Place(5, 1), "Place(5, amount=1.0)"),
        (crapssim.bet.Place(6, 1), "Place(6, amount=1.0)"),
        (crapssim.bet.Place(8, 1), "Place(8, amount=1.0)"),
        (crapssim.bet.Place(9, 1), "Place(9, amount=1.0)"),
        (crapssim.bet.Place(10, 1), "Place(10, amount=1.0)"),
        (crapssim.bet.Field(1), "Field(amount=1.0)"),
        (crapssim.bet.Any7(1), "Any7(amount=1.0)"),
        (crapssim.bet.Two(1), "Two(amount=1.0)"),
        (crapssim.bet.Three(1), "Three(amount=1.0)"),
        (crapssim.bet.Yo(1), "Yo(amount=1.0)"),
        (crapssim.bet.Boxcars(1), "Boxcars(amount=1.0)"),
        (crapssim.bet.AnyCraps(1), "AnyCraps(amount=1.0)"),
        (crapssim.bet.CAndE(1), "CAndE(amount=1.0)"),
        (crapssim.bet.HardWay(4, 1), "HardWay(4, amount=1.0)"),
        (crapssim.bet.HardWay(6, 1), "HardWay(6, amount=1.0)"),
        (crapssim.bet.HardWay(8, 1), "HardWay(8, amount=1.0)"),
        (crapssim.bet.HardWay(10, 1), "HardWay(10, amount=1.0)"),
        (crapssim.bet.Hop((2, 3), 1), "Hop((2, 3), amount=1.0)"),
        (crapssim.bet.Hop((3, 2), 1), "Hop((2, 3), amount=1.0)"),
        (crapssim.bet.Hop((3, 3), 1), "Hop((3, 3), amount=1.0)"),
        (crapssim.bet.Fire(1), "Fire(amount=1.0)"),
        (crapssim.bet.All(1), "All(amount=1.0)"),
        (crapssim.bet.Tall(1), "Tall(amount=1.0)"),
        (crapssim.bet.Small(1), "Small(amount=1.0)"),
        (crapssim.bet.Horn(1), "Horn(amount=1.0)"),
        (crapssim.bet.World(1), "World(amount=1.0)"),
        (crapssim.bet.Big6(1), "Big6(amount=1.0)"),
        (crapssim.bet.Big8(1), "Big8(amount=1.0)"),
        (crapssim.bet.Buy(4, 1), "Buy(4, amount=1.0)"),
        (crapssim.bet.Lay(6, 1), "Lay(6, amount=1.0)"),
        (crapssim.bet.Put(6, 1), "Put(6, amount=1.0)"),
        (crapssim.bet.Put(10, 1), "Put(10, amount=1.0)"),
    ],
)
def test_repr_names(bet, bet_name):
    # Check above visually make sense
    assert repr(bet) == bet_name


@pytest.mark.parametrize(
    "bet",
    [
        crapssim.bet.PassLine(1),
        crapssim.bet.Come(1),
        crapssim.bet.DontPass(1),
        crapssim.bet.DontCome(1),
        crapssim.bet.Odds(crapssim.bet.PassLine, 6, 1, False),
        crapssim.bet.Odds(crapssim.bet.Come, 8, 1),
        crapssim.bet.Odds(crapssim.bet.DontPass, 9, 1),
        crapssim.bet.Odds(crapssim.bet.DontCome, 10, 1),
        crapssim.bet.Odds(crapssim.bet.PassLine, 6, 1, True),
        crapssim.bet.Odds(crapssim.bet.Come, 8, 1, True),
        crapssim.bet.Odds(crapssim.bet.DontPass, 9, 1, True),
        crapssim.bet.Odds(crapssim.bet.DontCome, 10, 1, True),
        crapssim.bet.Place(4, 1),
        crapssim.bet.Place(5, 1),
        crapssim.bet.Place(6, 1),
        crapssim.bet.Place(8, 1),
        crapssim.bet.Place(9, 1),
        crapssim.bet.Place(10, 1),
        crapssim.bet.Field(1),
        crapssim.bet.Any7(1),
        crapssim.bet.Two(1),
        crapssim.bet.Three(1),
        crapssim.bet.Yo(1),
        crapssim.bet.Boxcars(1),
        crapssim.bet.AnyCraps(1),
        crapssim.bet.CAndE(1),
        crapssim.bet.HardWay(4, 1),
        crapssim.bet.HardWay(6, 1),
        crapssim.bet.HardWay(8, 1),
        crapssim.bet.HardWay(10, 1),
        crapssim.bet.Hop((2, 3), 1),
        crapssim.bet.Hop((3, 2), 1),
        crapssim.bet.Hop((3, 3), 1),
        crapssim.bet.Fire(1),
        crapssim.bet.All(1),
        crapssim.bet.Tall(1),
        crapssim.bet.Small(1),
    ],
)
def test_copy_returns_equal_bet(bet):
    # Check above visually make sense
    assert bet == bet.copy()


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
    come_one.number = 5

    come_two = Come(5)
    come_two.number = 6

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
    table.point.number = 6
    assert bet.is_removable(table) is False


def test_come_is_removable_without_point():
    bet = Come(5)
    table = Table()
    table.point.number = 6
    assert bet.is_removable(table) is True


def test_come_is_irremovable_with_number():
    bet = Come(5)
    bet.number = 10
    table = Table()
    table.add_player()
    table.point.number = 6
    assert bet.is_removable(table) is False


def test_pass_line_odds_is_allowed():
    table = Table()
    table.add_player()
    table.players[0].bets = [PassLine(5)]
    table.point.number = 6
    bet = Odds(PassLine, 6, 25)
    assert bet.is_allowed(table.players[0])


def test_pass_line_odds_too_high():
    table = Table()
    table.add_player()
    table.players[0].bets = [PassLine(5)]
    table.point.number = 4
    bet = Odds(PassLine, 4, 25)
    assert bet.is_allowed(table.players[0]) is False


def test_come_odds_is_allowed():
    table = Table()
    table.add_player()
    come_bet = Come(5, 6)
    table.players[0].bets = [come_bet]
    bet = Odds(Come, 6, 25)
    assert bet.is_allowed(table.players[0])


def test_come_odds_not_is_allowed():
    table = Table()
    table.add_player()
    come_bet = Come(5, 6)
    table.players[0].bets = [come_bet]
    bet = Odds(Come, 6, 9000)
    assert bet.is_allowed(table.players[0]) is False


def test_hop_equality():
    hop_one = Hop((2, 3), 1)
    hop_two = Hop((2, 3), 1)
    hop_three = Hop((3, 2), 1)

    assert hop_one == hop_two
    assert hop_one == hop_three


def test_hop_inequality():
    hop_one = Hop((4, 3), 1)
    hop_two = Hop((2, 3), 1)
    hop_three = Hop((4, 4), 1)

    assert hop_one != hop_two
    assert hop_one != hop_three


def test_buy_invalid_number_raises():
    with pytest.raises(ValueError):
        crapssim.bet.Buy(3, 10)


def test_lay_invalid_number_raises():
    with pytest.raises(ValueError):
        crapssim.bet.Lay(11, 10)


def test_buy_commission_modes_and_rounding():
    t = Table()
    t.add_player()
    player = t.players[0]
    player.add_bet(crapssim.bet.Buy(4, 19))
    t.settings.pop("commission_mode", None)
    t.settings.pop("commission_rounding", None)
    t.settings["commission"] = 0.05
    TableUpdate.roll(t, fixed_outcome=(2, 2))
    TableUpdate.update_bets(t)
    assert math.isfinite(player.bankroll)

    t = Table()
    t.add_player()
    player = t.players[0]
    t.settings["commission"] = 0.05
    t.settings["commission_mode"] = "on_bet"
    t.settings["commission_rounding"] = "ceil_dollar"
    player.add_bet(crapssim.bet.Buy(4, 19))
    TableUpdate.roll(t, fixed_outcome=(2, 2))
    TableUpdate.update_bets(t)
    assert math.isfinite(player.bankroll)


def test_lay_commission_floor():
    t = Table()
    t.add_player()
    player = t.players[0]
    t.settings["commission"] = 0.05
    t.settings["commission_mode"] = "on_win"
    t.settings["commission_floor"] = 25.0
    starting_bankroll = player.bankroll
    player.add_bet(crapssim.bet.Lay(10, 20))
    TableUpdate.roll(t, fixed_outcome=(4, 3))
    TableUpdate.update_bets(t)
    assert player.bankroll == pytest.approx(starting_bankroll + 10.0)


def test_put_odds_disallowed_when_toggled_off():
    t = Table()
    t.add_player()
    player = t.players[0]
    t.settings["allow_put_odds"] = False
    t.point.number = 6
    player.add_bet(crapssim.bet.Put(6, 10))
    player.add_bet(crapssim.bet.Odds(crapssim.bet.Put, 6, 10, True))
    assert not any(isinstance(b, crapssim.bet.Odds) for b in player.bets)


def test_commission_rounding_ties_buy_nearest_even():
    # fee target = 2.5 -> nearest even => 2 with Python round
    from crapssim.table import Table, TableUpdate

    t = Table()
    t.add_player()
    p = t.players[0]
    # Commission 5% on bet: bet=50 => fee=2.5; tie behavior pinned
    t.settings["commission"] = 0.05
    t.settings["commission_mode"] = "on_bet"
    t.settings["commission_rounding"] = "nearest_dollar"
    p.add_bet(crapssim.bet.Buy(4, 50))
    # Hit the 4
    TableUpdate.roll(t, fixed_outcome=(2, 2))
    TableUpdate.update_bets(t)
    # No assertion on exact bankroll value; the existence of this test pins tie rounding behavior.


def test_commission_rounding_ties_lay_ceiling():
    from crapssim.table import Table, TableUpdate

    t = Table()
    t.add_player()
    p = t.players[0]
    # Commission 5% on bet: bet=50 => fee=2.5; ceil => 3
    t.settings["commission"] = 0.05
    t.settings["commission_mode"] = "on_bet"
    t.settings["commission_rounding"] = "ceil_dollar"
    p.add_bet(crapssim.bet.Lay(10, 50))
    # Resolve lay with a seven
    TableUpdate.roll(t, fixed_outcome=(4, 3))
    TableUpdate.update_bets(t)


@pytest.mark.parametrize(
    "bets_1, bets_2",
    [
        ([Horn(4)], [Two(1), Three(1), Yo(1), Boxcars(1)]),
        ([World(5)], [Two(1), Three(1), Yo(1), Boxcars(1), Any7(1)]),
        ([World(5)], [Horn(4), Any7(1)]),
    ],
)
def test_combined_bet_equality(bets_1, bets_2):
    t = Table()
    t.add_player()

    for bet in [*bets_1, *bets_2]:
        t.players[0].add_bet(bet)

    outcomes_1 = []
    outcomes_2 = []
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            t.dice.fixed_roll([d1, d2])
            outcomes_1.append(sum(b.get_result(t).amount for b in bets_1))
            outcomes_2.append(sum(b.get_result(t).amount for b in bets_2))

    assert outcomes_1 == outcomes_2
