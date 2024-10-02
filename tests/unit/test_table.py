import pytest

from crapssim import Table
from crapssim.bet import Come
from crapssim.point import Point
from crapssim.strategy import BetPassLine


def test_ensure_one_player():
    table = Table()
    count_zero = len(table.players)
    table.ensure_one_player()
    count_one = len(table.players)
    bankroll = table.players[0].bankroll
    strategy = table.players[0].strategy.__class__
    assert (count_zero, count_one, bankroll, strategy) == (0, 1, 100, BetPassLine)


def test_wrong_point_off():
    table = Table()
    table.add_player(bankroll=500)
    table.players[0].add_bet(Come(100))
    assert (len(table.players[0].bets), table.players[0].bankroll) == (0, 500)


def test_wrong_point_on():
    table = Table()
    table.point.number = 4
    table.add_player(bankroll=500)
    assert (len(table.players[0].bets), table.players[0].bankroll) == (0, 500)


@pytest.mark.parametrize(
    ["status", "number", "comparison"],
    [
        ("Off", None, "Off"),
        ("Off", None, "off"),
        ("On", 6, 6),
        ("On", 6, "6"),
        ("On", 8, "on"),
    ],
)
def test_point_equality(status, number, comparison):
    point = Point()
    point.number = number
    assert point == comparison


@pytest.mark.parametrize(["number", "comparison"], [(8, 6), (8, "6")])
def test_point_greater_than(number, comparison):
    point = Point()
    point.number = number
    assert point > comparison


@pytest.mark.parametrize(["number", "comparison"], [(4, 6), (4, "10")])
def test_point_less_than(number, comparison):
    point = Point()
    point.number = number
    assert point < comparison


@pytest.mark.parametrize("seed", [8, 15, 21234, 0])
def test_table_seed_idential(seed):
    table1 = Table(seed)
    table2 = Table(seed)

    table1.run(max_rolls=100)
    table2.run(max_rolls=100)

    assert (table1.dice.result == table2.dice.result).all()
