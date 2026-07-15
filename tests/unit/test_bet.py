import math
import copy

import numpy as np
import pytest

from unittest.mock import Mock

import crapssim.bet
from crapssim.bet import (
    Any7,
    Bet,
    BetResult,
    Boxcars,
    CAndE,
    Come,
    Buy,
    DontCome,
    Hop,
    Horn,
    Lay,
    Place,
    Put,
    Odds,
    PassLine,
    DontPass,
    Three,
    Two,
    World,
    Yo,
)
from crapssim.rules import ClassicRules, CraplessRules
from crapssim.strategy.tools import NullStrategy
from crapssim.table import Table, TableUpdate

# Check EV of bets on a "per-roll" basis


class _BetForBaseCoverage(Bet):
    def get_result(self, table: Table) -> BetResult:
        return BetResult(0, False)


class _BetCallsAbstractGetResult(Bet):
    def get_result(self, table: Table):
        return super().get_result(table)


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
        (crapssim.bet.Horn(1), -0.1250),
        (crapssim.bet.World(1), -0.1333),
        (crapssim.bet.Big6(1), -0.0278),
        (crapssim.bet.Big8(1), -0.0278),
        (crapssim.bet.Buy(4, 1), 0),
        (crapssim.bet.Buy(6, 1), 0),
        (crapssim.bet.Lay(4, 1), 0),
        (crapssim.bet.Lay(6, 1), 0),
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
            "Odds(base_type=crapssim.bet.PassLine, number=6, amount=1.0, always_working=False)",
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


# fmt: off
def test_str_names():
    bets = [
        (crapssim.bet.PassLine(5), "$5 PassLine"),
        (crapssim.bet.Come(1), "$1 Come"),
        (crapssim.bet.Come(1, 6), "$1 Come(6)"),
        (crapssim.bet.DontPass(1), "$1 DontPass"),
        (crapssim.bet.DontCome(1), "$1 DontCome"),
        (crapssim.bet.DontCome(1, 4), "$1 DontCome(4)"),
        (crapssim.bet.Odds(crapssim.bet.PassLine, 6, 1, False), "$1 Odds(PassLine)"),
        (crapssim.bet.Odds(crapssim.bet.Come, 8, 1), "$1 Odds(Come, 8)"),
        (crapssim.bet.Odds(crapssim.bet.DontPass, 9, 1), "$1 Odds(DontPass)"),
        (crapssim.bet.Odds(crapssim.bet.DontCome, 10, 1), "$1 Odds(DontCome, 10)"),
        (crapssim.bet.Odds(crapssim.bet.PassLine, 6, 1, True), "$1 Odds(PassLine)"),
        (crapssim.bet.Odds(crapssim.bet.Come, 8, 1, True), "$1 Odds(Come, 8)"),
        (crapssim.bet.Odds(crapssim.bet.DontPass, 9, 1, True), "$1 Odds(DontPass)"),
        (crapssim.bet.Odds(crapssim.bet.DontCome, 10, 1, True), "$1 Odds(DontCome, 10)",),
        (crapssim.bet.Place(4, 1), "$1 Place(4)"),
        (crapssim.bet.Place(5, 1), "$1 Place(5)"),
        (crapssim.bet.Place(6, 1), "$1 Place(6)"),
        (crapssim.bet.Place(8, 1), "$1 Place(8)"),
        (crapssim.bet.Place(9, 1), "$1 Place(9)"),
        (crapssim.bet.Place(10, 1), "$1 Place(10)"),
        (crapssim.bet.Field(1), "$1 Field"),
        (crapssim.bet.Any7(1), "$1 Any7"),
        (crapssim.bet.Two(1.5), "$1.5 Two"),
        (crapssim.bet.Three(1), "$1 Three"),
        (crapssim.bet.Yo(1), "$1 Yo"),
        (crapssim.bet.Boxcars(1), "$1 Boxcars"),
        (crapssim.bet.AnyCraps(1), "$1 AnyCraps"),
        (crapssim.bet.CAndE(1), "$1 CAndE"),
        (crapssim.bet.HardWay(4, 1), "$1 HardWay(4)"),
        (crapssim.bet.HardWay(6, 1), "$1 HardWay(6)"),
        (crapssim.bet.HardWay(8, 1), "$1 HardWay(8)"),
        (crapssim.bet.HardWay(10, 1), "$1 HardWay(10)"),
        (crapssim.bet.Hop((2, 3), 1), "$1 Hop(2,3)"),
        (crapssim.bet.Hop((3, 2), 1), "$1 Hop(2,3)"),
        (crapssim.bet.Hop((3, 3), 1), "$1 Hop(3,3)"),
        (crapssim.bet.Fire(1), "$1 Fire"),
        (crapssim.bet.All(1), "$1 All"),
        (crapssim.bet.Tall(1), "$1 Tall"),
        (crapssim.bet.Small(1), "$1 Small"),
        (crapssim.bet.Horn(1), "$1 Horn"),
        (crapssim.bet.World(1), "$1 World"),
        (crapssim.bet.Big6(1), "$1 Big6"),
        (crapssim.bet.Big8(1), "$1 Big8"),
        (crapssim.bet.Buy(4, 1), "$1 Buy(4)"),
        (crapssim.bet.Lay(6, 1), "$1 Lay(6)"),
        (crapssim.bet.Put(6, 1), "$1 Put(6)"),
        (crapssim.bet.Put(10, 1), "$1 Put(10)"),
    ]
    for bet, bet_name in bets:
        print(bet)
        assert str(bet) == bet_name
# fmt: on


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
    with pytest.raises(TypeError):
        Bet(400)


def test_bet_base_default_methods():
    table = Table()
    player = table.add_player()
    bet = _BetForBaseCoverage(10)

    assert bet.cost(table) == 10
    assert bet.is_removable(table) is True
    assert bet.is_allowed(player) is True

    original_amount = bet.amount
    bet.update_number(table)
    assert bet.amount == original_amount


def test_bet_abstract_get_result_default_returns_none():
    table = Table()
    bet = _BetCallsAbstractGetResult(10)

    assert bet.get_result(table) is None


def test_winning_losing_numbers_bet_abstract_methods_default_returns_none():
    class _CallsAbstractWinning(crapssim.bet._WinningLosingNumbersBet):
        def get_winning_numbers(self, table: Table):
            return super().get_winning_numbers(table)

        def get_losing_numbers(self, table: Table):
            return super().get_losing_numbers(table)

        def get_payout_ratio(self, table: Table):
            return super().get_payout_ratio(table)

    table = Table()
    bet = _CallsAbstractWinning(10)

    assert bet.get_winning_numbers(table) is None
    assert bet.get_losing_numbers(table) is None
    assert bet.get_payout_ratio(table) is None


def test_bet_eq_non_bet_raises_not_implemented():
    bet = _BetForBaseCoverage(10)

    with pytest.raises(NotImplementedError):
        _ = bet == 10


def test_bet_add_different_type_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        _ = PassLine(10) + Come(10)


def test_bet_subtract_base_branches():
    bet = PassLine(10)

    assert (bet - 3).amount == 7
    assert (bet - PassLine(4)).amount == 6
    assert (3 - bet).amount == 7

    with pytest.raises(NotImplementedError):
        _ = bet - Come(4)


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


def test_get_cande_invalid_total_raises_not_implemented():
    table = Table()
    table.dice.result = (0, 0)

    with pytest.raises(NotImplementedError):
        CAndE(5).get_payout_ratio(table)


def test_get_horn_invalid_total_raises_not_implemented():
    table = Table()
    table.dice.result = (4, 4)

    with pytest.raises(NotImplementedError):
        Horn(5).get_payout_ratio(table)


def test_get_world_invalid_total_raises_not_implemented():
    table = Table()
    table.dice.result = (4, 4)

    with pytest.raises(NotImplementedError):
        World(5).get_payout_ratio(table)


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


def test_odds_light_side_with_passline():
    """Odds.light_side property: PassLine is light_side"""
    odds = Odds(PassLine, 6, 10)
    assert odds.light_side is True


def test_odds_light_side_with_come():
    """Odds.light_side property: Come is light_side"""
    odds = Odds(Come, 6, 10)
    assert odds.light_side is True


def test_odds_light_side_with_put():
    """Odds.light_side property: Put is light_side"""
    odds = Odds(Put, 6, 10)
    assert odds.light_side is True


def test_odds_dark_side_with_dontpass():
    """Odds.dark_side property: DontPass is dark_side"""
    odds = Odds(DontPass, 6, 10)
    assert odds.dark_side is True


def test_odds_dark_side_with_dontcome():
    """Odds.dark_side property: DontCome is dark_side"""
    odds = Odds(DontCome, 6, 10)
    assert odds.dark_side is True


def test_odds_light_side_false_for_dark_types():
    """Odds.light_side is False for dark side bet types"""
    odds = Odds(DontPass, 6, 10)
    assert odds.light_side is False

    odds = Odds(DontCome, 6, 10)
    assert odds.light_side is False


def test_odds_dark_side_false_for_light_types():
    """Odds.dark_side is False for light side bet types"""
    odds = Odds(PassLine, 6, 10)
    assert odds.dark_side is False

    odds = Odds(Come, 6, 10)
    assert odds.dark_side is False

    odds = Odds(Put, 6, 10)
    assert odds.dark_side is False


def test_odds_light_side_noop_when_point_off_and_not_always_working():
    table = Table()
    table.point.number = None
    table.dice.result = (3, 5)
    bet = Odds(Come, 6, 10, always_working=False)

    bet_result = bet.get_result(table)
    assert bet_result.won is False
    assert bet_result.lost is False
    assert bet_result.pushed is False
    assert bet_result.remove is False
    assert bet_result.amount == 0


def test_odds_dark_side_noop_when_point_off_and_not_always_working():
    table = Table()
    table.point.number = None
    table.dice.result = (3, 5)
    bet = Odds(DontCome, 6, 10, always_working=False)

    bet_result = bet.get_result(table)
    assert bet_result.won is False
    assert bet_result.lost is False
    assert bet_result.pushed is False
    assert bet_result.remove is False
    assert bet_result.amount == 0


def test_odds_get_max_odds_invalid_base_type_raises_not_implemented():
    class InvalidBase:
        pass

    table = Table()
    bet = Odds(InvalidBase, 6, 1)

    with pytest.raises(NotImplementedError):
        bet.get_max_odds(table)


def test_odds_get_winning_numbers_invalid_base_type_raises_not_implemented():
    class InvalidBase:
        pass

    table = Table()
    bet = Odds(InvalidBase, 6, 1)

    with pytest.raises(NotImplementedError):
        bet.get_winning_numbers(table)


def test_odds_get_losing_numbers_invalid_base_type_raises_not_implemented():
    class InvalidBase:
        pass

    table = Table()
    bet = Odds(InvalidBase, 6, 1)

    with pytest.raises(NotImplementedError):
        bet.get_losing_numbers(table)


def test_odds_get_payout_ratio_invalid_base_type_raises_not_implemented():
    class InvalidBase:
        pass

    table = Table()
    bet = Odds(InvalidBase, 6, 1)

    with pytest.raises(NotImplementedError):
        bet.get_payout_ratio(table)


def test_odds_str_invalid_base_type_raises_not_implemented():
    class InvalidBase:
        pass

    bet = Odds(InvalidBase, 6, 1)

    with pytest.raises(NotImplementedError):
        str(bet)


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
    # Previously, Buy/Lay validation was tied to the ruleset gate instead of the constructor.
    # This test now only covers numbers that are always invalid; ruleset-specific acceptance
    # is covered by the CraplessRules/classic-mode tests below.
    with pytest.raises(ValueError):
        crapssim.bet.Buy(None, 10)
        crapssim.bet.Buy(1, 10)
        crapssim.bet.Buy(13, 10)


def test_lay_invalid_number_raises():
    # Previously, Buy/Lay validation was tied to the ruleset gate instead of the constructor.
    # This test now only covers numbers that are always invalid; ruleset-specific acceptance
    # is covered by the CraplessRules/classic-mode tests below.
    with pytest.raises(ValueError):
        crapssim.bet.Lay(None, 10)
        crapssim.bet.Lay(1, 10)
        crapssim.bet.Lay(13, 10)


def test_put_invalid_number_raises():
    with pytest.raises(ValueError):
        crapssim.bet.Put(None, 10)
        crapssim.bet.Put(1, 10)
        crapssim.bet.Put(13, 10)


def test_place_invalid_number_raises():
    with pytest.raises(ValueError):
        crapssim.bet.Place(None, 10)
        crapssim.bet.Place(1, 10)
        crapssim.bet.Place(13, 10)


def test_vig_policy_invalid_rounding_defaults_to_nearest_dollar():
    rounding, floor = crapssim.bet._vig_policy(
        {"vig_rounding": "invalid", "vig_floor": 2.5}
    )

    assert rounding == "nearest_dollar"
    assert floor == 2.5


def test_place_is_active_on_comeout_in_legacy_rules_mode():
    table = Table()
    table.settings["come_out_working_policy"] = "legacy"
    bet = Place(6, 12)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.amount == 26
    assert result.won is True
    assert result.remove is True


def test_place_follows_real_casino_rules_mode_if_come_out_working_policy_is_invalid():
    table = Table()
    table.settings["come_out_working_policy"] = "invalid"
    bet = Place(6, 12)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.amount == 0
    assert result.won is False
    assert result.remove is False


def test_place_stays_inactive_on_comeout_in_real_casino_mode():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Place(6, 10)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.amount == 0
    assert result.remove is False


@pytest.mark.parametrize(
    "bet, roll",
    [
        (Place(6, 10, always_working=False), (3, 3)),
        (Buy(6, 10, always_working=False), (3, 3)),
        (Lay(6, 10, always_working=False), (3, 4)),
        (Put(6, 10, always_working=False), (3, 3)),
    ],
)
def test_explicit_false_overrides_legacy_comeout_behavior(bet, roll):
    table = Table()
    table.settings["come_out_working_policy"] = "legacy"

    table.dice.fixed_roll(roll)
    result = bet.get_result(table)

    assert result.amount == 0
    assert result.remove is False
    assert result.bankroll_change == 0


def test_place_always_working_overrides_real_casino_mode_win():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Place(6, 10, always_working=True)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.won
    assert result.remove is False


def test_place_always_working_overrides_real_casino_mode_loss():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Place(6, 10, always_working=True)

    table.dice.fixed_roll((3, 4))
    result = bet.get_result(table)

    assert result.lost
    assert result.won is False
    assert result.remove is True


def test_place_always_working_overrides_real_casino_mode_no_action():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Place(6, 10, always_working=True)

    table.dice.fixed_roll((3, 5))
    result = bet.get_result(table)

    assert result.lost is False
    assert result.won is False
    assert result.pushed is False
    assert result.amount == 0
    assert result.remove is False


def test_place_non_removing_win_credits_profit_only_to_bankroll():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Place(6, 6, always_working=True)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.amount == pytest.approx(13)
    assert result.remove is False
    assert result.bankroll_change == pytest.approx(7)


def test_place_point_on_win_keeps_bet_and_credits_profit_only():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    table.point.number = 4
    bet = Place(6, 6)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.won is True
    assert result.remove is False
    assert result.amount == pytest.approx(13)
    assert result.bankroll_change == pytest.approx(7)


def test_place_point_on_loss_removes_stake():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    table.point.number = 4
    bet = Place(6, 12)

    table.dice.fixed_roll((3, 4))
    result = bet.get_result(table)

    assert result.lost is True
    assert result.won is False
    assert result.remove is True
    assert result.bankroll_change == 0


@pytest.mark.parametrize(
    "bet, win_roll, loss_roll",
    [
        (Buy(4, 10), (2, 2), (3, 4)),
        (Lay(4, 10), (3, 4), (2, 2)),
        (Put(6, 10), (3, 3), (3, 4)),
    ],
)
def test_number_bets_point_on_win_and_loss(bet, win_roll, loss_roll):
    """Point On Win → payout, REMOVE; Point On Loss → lose stake, REMOVE."""
    # Win case
    table_win = Table()
    table_win.settings["come_out_working_policy"] = "real_casino"
    table_win.settings["vig_paid_on_win"] = True
    table_win.point.number = 8
    table_win.dice.fixed_roll(win_roll)
    win_result = bet.get_result(table_win)

    assert win_result.won is True
    assert win_result.remove is True
    assert win_result.bankroll_change > 0

    # Loss case
    table_loss = Table()
    table_loss.settings["come_out_working_policy"] = "real_casino"
    table_loss.settings["vig_paid_on_win"] = True
    table_loss.point.number = 8
    table_loss.dice.fixed_roll(loss_roll)
    loss_result = bet.get_result(table_loss)

    assert loss_result.lost is True
    assert loss_result.remove is True
    assert loss_result.bankroll_change == 0


@pytest.mark.parametrize(
    "bet, roll",
    [
        (Buy(6, 10, always_working=True), (3, 4)),
        (Lay(6, 10, always_working=True), (3, 3)),
        (Put(6, 10, always_working=True), (3, 4)),
    ],
)
def test_removing_number_bets_lose_on_comeout_when_always_working(bet, roll):
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"

    table.dice.fixed_roll(roll)
    result = bet.get_result(table)

    assert result.lost is True
    assert result.won is False
    assert result.remove is True
    assert result.bankroll_change == 0


def test_buy_stays_inactive_on_comeout_in_real_casino_mode():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Buy(6, 10)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.amount == 0
    assert result.remove is False


def test_buy_always_working_overrides_real_casino_mode():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Buy(6, 10, always_working=True)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.won
    assert result.remove is True


def test_lay_stays_inactive_on_comeout_in_real_casino_mode():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Lay(6, 10)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.amount == 0
    assert result.remove is False


def test_lay_always_working_overrides_real_casino_mode():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Lay(6, 10, always_working=True)

    table.dice.fixed_roll((3, 4))
    result = bet.get_result(table)

    assert result.won
    assert result.remove is True


def test_put_stays_inactive_on_comeout_in_real_casino_mode():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Put(6, 10)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.amount == 0
    assert result.remove is False


def test_put_always_working_overrides_real_casino_mode():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Put(6, 10, always_working=True)

    table.dice.fixed_roll((3, 3))
    result = bet.get_result(table)

    assert result.won
    assert result.remove is True


def test_dontcome_odds_work_on_comeout_in_real_casino_mode():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Odds(DontCome, 6, 10)

    table.dice.fixed_roll((3, 4))
    result = bet.get_result(table)

    assert result.won
    assert result.remove is True


def test_dontcome_odds_work_on_comeout_in_legacy_mode():
    table = Table()
    table.settings["come_out_working_policy"] = "legacy"
    bet = Odds(DontCome, 6, 10)

    table.dice.fixed_roll((3, 4))
    result = bet.get_result(table)

    assert result.won
    assert result.remove is True


def test_dontcome_odds_work_on_comeout_by_default():
    table = Table()
    bet = Odds(DontCome, 6, 10)

    table.dice.fixed_roll((3, 4))
    result = bet.get_result(table)

    assert result.won
    assert result.remove is True


@pytest.mark.parametrize(
    "bet_factory, roll",
    [
        (lambda: Place(6, 10), (3, 3)),
        (lambda: Buy(6, 10), (3, 3)),
        (lambda: Lay(6, 10), (3, 4)),
        (lambda: Put(6, 10), (3, 3)),
    ],
)
def test_invalid_comeout_policy_falls_back_to_legacy_for_number_bets(bet_factory, roll):
    table = Table()
    table.settings["come_out_working_policy"] = "invalid"
    bet = bet_factory()

    table.dice.fixed_roll(roll)

    result = bet.get_result(table)

    assert result.won is False
    assert result.remove is False
    assert result.amount == 0


@pytest.mark.parametrize(
    "bet_factory, roll",
    [
        (lambda aw: Place(6, 10, always_working=aw), (3, 3)),
        (lambda aw: Buy(6, 10, always_working=aw), (3, 3)),
        (lambda aw: Lay(6, 10, always_working=aw), (3, 4)),
        (lambda aw: Put(6, 10, always_working=aw), (3, 3)),
        (lambda aw: Odds(Put, 6, 10, always_working=aw), (3, 3)),
    ],
)
def test_explicit_true_overrides_real_casino_comeout_behavior(bet_factory, roll):
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = bet_factory(True)

    table.dice.fixed_roll(roll)
    result = bet.get_result(table)

    assert result.won is True


@pytest.mark.parametrize(
    "bet_factory, roll",
    [
        (lambda aw: Place(6, 10, always_working=aw), (3, 3)),
        (lambda aw: Buy(6, 10, always_working=aw), (3, 3)),
        (lambda aw: Lay(6, 10, always_working=aw), (3, 4)),
        (lambda aw: Put(6, 10, always_working=aw), (3, 3)),
        (lambda aw: Odds(Put, 6, 10, always_working=aw), (3, 3)),
    ],
)
def test_explicit_false_overrides_legacy_comeout_behavior_across_number_bets(
    bet_factory, roll
):
    table = Table()
    table.settings["come_out_working_policy"] = "legacy"
    bet = bet_factory(False)

    table.dice.fixed_roll(roll)
    result = bet.get_result(table)

    assert result.won is False
    assert result.lost is False


@pytest.mark.parametrize(
    "bet_factory, roll",
    [
        (lambda aw: Place(6, 10, always_working=aw), (3, 3)),
        (lambda aw: Buy(6, 10, always_working=aw), (3, 3)),
        (lambda aw: Lay(6, 10, always_working=aw), (3, 4)),
        (lambda aw: Put(6, 10, always_working=aw), (3, 3)),
    ],
)
@pytest.mark.parametrize(
    "policy, expected_working",
    [("legacy", True), ("real_casino", False)],
)
def test_always_working_none_defers_to_table_policy_for_number_bets(
    bet_factory, roll, policy, expected_working
):
    table = Table()
    table.settings["come_out_working_policy"] = policy
    bet = bet_factory(None)

    table.dice.fixed_roll(roll)
    result = bet.get_result(table)

    if expected_working:
        assert result.won is True
    else:
        assert result.won is False
        assert result.lost is False


@pytest.mark.parametrize(
    "bet_factory, roll",
    [
        (lambda: Place(6, 10), (3, 3)),
        (lambda: Buy(6, 10), (3, 3)),
        (lambda: Lay(6, 10), (3, 4)),
        (lambda: Put(6, 10), (3, 3)),
    ],
)
def test_missing_come_out_working_policy_defaults_to_real_casino_behavior(
    bet_factory, roll
):
    table = Table()
    table.settings.pop("come_out_working_policy")
    bet = bet_factory()

    table.dice.fixed_roll(roll)
    result = bet.get_result(table)

    assert result.won is False
    assert result.remove is False
    assert result.amount == 0


@pytest.mark.parametrize("always_working", [None, True, False])
@pytest.mark.parametrize(
    "bet_factory",
    [
        lambda aw: Place(6, 10, always_working=aw),
        lambda aw: Buy(6, 10, always_working=aw),
        lambda aw: Lay(6, 10, always_working=aw),
        lambda aw: Put(6, 10, always_working=aw),
        lambda aw: Odds(Put, 6, 10, always_working=aw),
    ],
)
def test_copy_and_deepcopy_preserve_always_working_state(bet_factory, always_working):
    bet = bet_factory(always_working)

    copied = bet.copy()
    deep_copied = copy.deepcopy(bet)

    assert copied is not bet
    assert deep_copied is not bet
    assert copied.always_working is always_working
    assert deep_copied.always_working is always_working


@pytest.mark.parametrize(
    "roll, expected_amount, expected_remove",
    [
        ((3, 3), 10, True),
        ((3, 4), 10, True),
        ((2, 3), 0, False),
    ],
)
def test_light_side_odds_not_working_on_comeout_only_ignores_resolving_totals(
    roll, expected_amount, expected_remove
):
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Odds(Come, 6, 10)

    table.dice.fixed_roll(roll)
    result = bet.get_result(table)

    assert result.amount == expected_amount
    assert result.remove is expected_remove
    if expected_remove:
        assert result.pushed


@pytest.mark.parametrize(
    "roll, expected_won, expected_lost",
    [
        ((3, 3), True, False),
        ((3, 4), False, True),
    ],
)
def test_come_odds_always_working_resolves_on_comeout(
    roll, expected_won, expected_lost
):
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Odds(Come, 6, 10, always_working=True)

    table.dice.fixed_roll(roll)
    result = bet.get_result(table)

    assert result.won is expected_won
    assert result.lost is expected_lost
    assert result.remove is True
    if expected_won:
        assert result.bankroll_change > bet.amount
    else:
        assert result.bankroll_change == 0


@pytest.mark.parametrize(
    "roll, expected_amount, expected_remove",
    [
        ((3, 3), 10, True),
        ((3, 4), 10, True),
        ((2, 3), 0, False),
    ],
)
def test_dontcome_odds_can_be_off_on_comeout_and_push_on_triggers(
    roll, expected_amount, expected_remove
):
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    bet = Odds(DontCome, 6, 10, always_working=False)

    table.dice.fixed_roll(roll)
    result = bet.get_result(table)

    assert result.amount == expected_amount
    assert result.remove is expected_remove
    if expected_remove:
        assert result.pushed is True
        assert result.bankroll_change == bet.amount
    else:
        assert result.bankroll_change == 0


def test_put_odds_allowed_when_point_on():
    t = Table()
    t.add_player()
    player = t.players[0]
    t.point.number = 6
    player.add_bet(crapssim.bet.Put(6, 10))
    player.add_bet(crapssim.bet.Odds(crapssim.bet.Put, 6, 10, True))
    assert any(isinstance(b, crapssim.bet.Odds) for b in player.bets)


@pytest.mark.parametrize("number", [2, 3, 11, 12])
def test_put_odds_allowed_on_extremes_in_crapless_mode(number):
    table = Table(rules=CraplessRules())
    player = table.add_player(bankroll=100)
    table.point.number = 4

    player.add_bet(Put(number, 10))
    player.add_bet(Odds(Put, number, 10, True))

    assert any(isinstance(b, Put) and b.number == number for b in player.bets)
    assert any(
        isinstance(b, Odds) and b.base_type is Put and b.number == number
        for b in player.bets
    )


@pytest.mark.parametrize("number", [2, 3, 11, 12])
def test_put_odds_not_allowed_on_extremes_in_classic_mode(number):
    table = Table(rules=ClassicRules())
    player = table.add_player(bankroll=100)
    table.point.number = 4

    # Force a matching base bet to ensure rejection is due to rules, not missing base amount.
    player.bets.append(Put(number, 10))

    assert Odds(Put, number, 10, True).is_allowed(player) is False


def test_put_only_allowed_when_point_on():
    t = Table()
    t.add_player(strategy=NullStrategy())
    p = t.players[0]
    starting_bankroll = p.bankroll

    # Come-out roll has point OFF; Put bet should not be accepted.
    p.add_bet(crapssim.bet.Put(6, 10))
    assert not any(isinstance(b, crapssim.bet.Put) for b in p.bets)
    assert p.bankroll == starting_bankroll

    # Establish the point and retry – bet should now be accepted.
    TableUpdate().run(t, dice_outcome=(3, 3))
    p.add_bet(crapssim.bet.Put(6, 10))
    assert any(isinstance(b, crapssim.bet.Put) for b in p.bets)


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
            outcomes_1.append(sum(b.get_result(t).bankroll_change for b in bets_1))
            outcomes_2.append(sum(b.get_result(t).bankroll_change for b in bets_2))

    assert outcomes_1 == outcomes_2


def test_dont_pass_bet_pushes_on_comeout_12():
    table = Table()
    table.add_player()
    dont_pass_bet = crapssim.bet.DontPass(10)
    table.players[0].add_bet(dont_pass_bet)

    # Roll a 12 on the come-out roll
    table.dice.fixed_roll((6, 6))
    result = dont_pass_bet.get_result(table)

    assert result.pushed
    assert result.bankroll_change == dont_pass_bet.amount


def test_dontpass_is_allowed_when_point_off():
    """DontPass.is_allowed returns True when point is Off and rules allow"""
    table = Table(rules=ClassicRules())
    player = table.add_player(bankroll=100)

    # Point must be off for DontPass
    assert table.point.status == "Off"

    bet = DontPass(10)
    assert bet.is_allowed(player) is True


def test_dontpass_is_not_allowed_when_point_on():
    """DontPass.is_allowed returns False when point is On"""
    table = Table(rules=ClassicRules())
    player = table.add_player(bankroll=100)

    # Establish a point
    table.point.number = 6
    assert table.point.status == "On"

    bet = DontPass(10)
    assert bet.is_allowed(player) is False


def test_dontpass_get_winning_numbers_before_point():
    """DontPass.get_winning_numbers: table.point.number is None"""
    table = Table()
    assert table.point.number is None

    bet = DontPass(10)
    assert bet.get_winning_numbers(table) == [2, 3]


def test_dontpass_get_winning_numbers_after_point():
    """DontPass.get_winning_numbers: table.point.number is not None"""
    table = Table()
    table.point.number = 6

    bet = DontPass(10)
    assert bet.get_winning_numbers(table) == [7]


def test_dontpass_get_losing_numbers_before_point():
    """DontPass.get_losing_numbers: table.point.number is None"""
    table = Table()
    assert table.point.number is None

    bet = DontPass(10)
    assert bet.get_losing_numbers(table) == [7, 11]


def test_dontpass_get_losing_numbers_after_point():
    """DontPass.get_losing_numbers: table.point.number is not None"""
    table = Table()
    table.point.number = 6

    bet = DontPass(10)
    assert bet.get_losing_numbers(table) == [6]


def test_dontpass_get_push_numbers_before_point():
    """DontPass.get_push_numbers: table.point.number is None"""
    table = Table()
    assert table.point.number is None

    bet = DontPass(10)
    assert bet.get_push_numbers(table) == [12]


def test_dontpass_get_push_numbers_after_point():
    """DontPass.get_push_numbers: table.point.number is not None"""
    table = Table()
    table.point.number = 6

    bet = DontPass(10)
    assert bet.get_push_numbers(table) == []


def test_dont_come_bet_pushes_on_12():
    table = Table()
    table.add_player()
    dont_come_bet = DontCome(10)
    table.players[0].add_bet(dont_come_bet)

    # Roll a 12 on the come-out roll
    table.dice.fixed_roll((6, 6))
    result = dont_come_bet.get_result(table)

    assert result.pushed
    assert result.bankroll_change == dont_come_bet.amount


def test_dont_come_with_number_losing_numbers_after_travel():
    table = Table()
    dont_come_bet = DontCome(10, 6)

    assert dont_come_bet.get_losing_numbers(table) == [6]


def test_dont_come_with_number_push_numbers_after_travel():
    table = Table()
    dont_come_bet = DontCome(10, 6)

    assert dont_come_bet.get_push_numbers(table) == []


def test_dont_come_is_not_allowed_when_point_is_off():
    table = Table(rules=ClassicRules())
    player = table.add_player(bankroll=100)

    assert table.point.status != "On"
    assert DontCome(10).is_allowed(player) is False


def test_dontcome_update_number_when_invalid_dice():
    """DontCome.update_number line: dice.total not in possible_numbers"""
    table = Table()
    table.add_player(bankroll=100)

    table.dice = Mock()
    table.dice.total = 2  # 2 is NOT in CLASSIC_POINTS

    bet = DontCome(10)  # number=None initially
    bet.update_number(table)
    assert bet.number is None  # Should remain None


def test_dontcome_init_with_invalid_number():
    """DontCome.__init__ line 547: number not in CLASSIC_POINTS"""
    # Valid CLASSIC_POINTS: [4, 5, 6, 8, 9, 10]
    # Invalid numbers should result in self.number = None
    bet = DontCome(10, number=2)  # 2 is not in CLASSIC_POINTS
    assert bet.number is None

    bet = DontCome(10, number=11)  # 11 is not in CLASSIC_POINTS
    assert bet.number is None

    bet = DontCome(10, number=7)  # 7 is not in CLASSIC_POINTS
    assert bet.number is None


def test_dontcome_init_with_valid_number():
    """DontCome.__init__ line 547: number in CLASSIC_POINTS"""
    bet = DontCome(10, number=4)
    assert bet.number == 4

    bet = DontCome(10, number=10)
    assert bet.number == 10


def test_dontcome_get_winning_numbers_with_number():
    """DontCome.get_winning_numbers line 553: self.number is not None"""
    table = Table()
    bet = DontCome(10, number=6)
    assert bet.get_winning_numbers(table) == [7]


def test_dontcome_get_losing_numbers_with_number():
    """DontCome.get_losing_numbers line 558: self.number is not None"""
    table = Table()
    bet = DontCome(10, number=6)
    assert bet.get_losing_numbers(table) == [6]


def test_dontcome_get_push_numbers_with_number():
    """DontCome.get_push_numbers line 563: self.number is not None"""
    table = Table()
    bet = DontCome(10, number=6)
    assert bet.get_push_numbers(table) == []


def test_dontcome_update_number_when_already_set():
    """DontCome.update_number line 569: self.number is not None (no update)"""
    table = Table()

    table.dice = Mock()
    table.dice.total = 8

    bet = DontCome(10, number=6)
    bet.update_number(table)
    assert bet.number == 6  # Should not change


def test_dontpass_is_not_allowed_in_crapless_mode():
    table = Table(rules=CraplessRules())
    player = table.add_player(bankroll=500)

    player.add_bet(DontPass(100))

    assert not player.has_bets(DontPass)
    assert player.bankroll == 500


def test_dontcome_is_not_allowed_in_crapless_mode():
    table = Table(rules=CraplessRules())
    player = table.add_player(bankroll=500)

    player.add_bet(DontCome(100))

    assert not player.has_bets(DontCome)
    assert player.bankroll == 500


@pytest.mark.parametrize("number", [2, 3, 11, 12])
def test_place_reject_crapless_only_numbers_in_classic_mode(number):
    table = Table(rules=ClassicRules())
    player = table.add_player(bankroll=100)

    player.add_bet(crapssim.bet.Place(number, amount=10))
    assert not player.has_bets((crapssim.bet.Place))
    assert player.bankroll == 100


@pytest.mark.parametrize("number", [2, 3, 11, 12])
def test_buy_reject_crapless_only_numbers_in_classic_mode(number):
    table = Table(rules=ClassicRules())
    player = table.add_player(bankroll=100)

    player.add_bet(crapssim.bet.Buy(number, amount=10))
    assert not player.has_bets((crapssim.bet.Buy))
    assert player.bankroll == 100


@pytest.mark.parametrize("number", [2, 3, 4, 5, 6, 8, 9, 10, 11, 12])
def test_place_allow_all_point_numbers_in_crapless_mode(number):
    table = Table(rules=CraplessRules())
    player = table.add_player(bankroll=100)

    player.add_bet(crapssim.bet.Place(number, amount=10))
    assert player.has_bets((crapssim.bet.Place))
    assert player.bankroll == 90


@pytest.mark.parametrize("number", [2, 3, 4, 5, 6, 8, 9, 10, 11, 12])
def test_buy_allow_point_numbers_in_crapless_mode(number):
    table = Table(rules=CraplessRules())
    table.settings["vig_paid_on_win"] = True
    player = table.add_player(bankroll=100)

    player.add_bet(crapssim.bet.Buy(number, amount=10))
    assert player.has_bets((crapssim.bet.Buy))
    assert player.bankroll == 90


def test_dont_pass_not_allowed_in_crapless_mode():
    table = Table(rules=CraplessRules())
    player = table.add_player(bankroll=500)

    table.point.number = 2
    player.add_bet(DontPass(100))

    assert not player.has_bets(DontPass)
    assert player.bankroll == 500


def test_dont_come_not_allowed_in_crapless_mode():
    table = Table(rules=CraplessRules())
    player = table.add_player(bankroll=500)

    table.point.number = 4
    player.add_bet(DontCome(100))

    assert not player.has_bets(DontCome)
    assert player.bankroll == 500


@pytest.mark.parametrize("number", [2, 3, 11, 12])
def test_come_with_crapless_number_not_allowed_on_classic_mode(number):
    table = Table(rules=ClassicRules())
    player = table.add_player(bankroll=100)

    # Come bets can only be placed with the table point ON.
    table.point.number = 4

    player.add_bet(Come(10, number=number))

    assert not player.has_bets(Come)
    assert player.bankroll == 100


@pytest.mark.parametrize("number", [2, 3, 11, 12])
def test_come_with_crapless_number_allowed_on_crapless_mode(number):
    table = Table(rules=CraplessRules())
    player = table.add_player(bankroll=100)

    # Come bets can only be placed with the table point ON.
    table.point.number = 4

    player.add_bet(Come(10, number=number))

    assert player.has_bets(Come)
    assert player.bankroll == 90
    assert any(isinstance(b, Come) and b.number == number for b in player.bets)


@pytest.mark.parametrize("number", [2, 3, 11, 12])
def test_put_rejects_crapless_only_numbers_in_classic_mode(number):
    table = Table(rules=ClassicRules())
    player = table.add_player(bankroll=20)

    table.point.number = 4
    player.add_bet(Put(number, 10))

    assert not player.has_bets(Put)
    assert player.bankroll == 20


@pytest.mark.parametrize("number", [2, 3, 11, 12])
def test_put_allows_crapless_only_numbers_in_crapless_mode(number):
    table = Table(rules=CraplessRules())
    player = table.add_player(bankroll=20)

    table.point.number = 4
    player.add_bet(Put(number, 10))

    assert player.has_bets(Put)
    assert player.bankroll == 10


@pytest.mark.parametrize("number", [2, 3, 11, 12])
def test_lay_rejects_crapless_only_numbers_in_classic_mode(number):
    table = Table(rules=ClassicRules())
    player = table.add_player(bankroll=20)

    player.add_bet(Lay(number, 10))

    assert not player.has_bets(Lay)
    assert player.bankroll == 20


@pytest.mark.parametrize("number", [2, 3, 11, 12])
def test_lay_allows_crapless_only_numbers_in_crapless_mode(number):
    table = Table(rules=CraplessRules())
    player = table.add_player(bankroll=20)

    player.add_bet(Lay(number, 10))

    assert player.has_bets(Lay)
    assert player.bankroll == 10
