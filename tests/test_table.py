import pytest

from crapssim import Table, Player
from crapssim.bet import Come, PassLine
from crapssim.strategy import passline
from crapssim.table import Point


def test_ensure_one_player():
    table = Table()
    count_zero = len(table.players)
    table.ensure_one_player()
    count_one = len(table.players)
    bankroll = table.players[0].bankroll
    strategy = table.players[0].bet_strategy
    assert (count_zero, count_one, bankroll, strategy) == (0, 1, 500, passline)


def test_wrong_point_off():
    table = Table()
    table.point.status = 'Off'
    player = Player(500)
    player.bet(Come(100), table)
    assert (len(player.bets_on_table), player.bankroll) == (0, 500)


def test_wrong_point_on():
    table = Table()
    table.point.status = 'On'
    table.point.number = 4
    player = Player(500)
    player.bet(PassLine(100), table)
    assert (len(player.bets_on_table), player.bankroll) == (0, 500)


@pytest.mark.parametrize(['status', 'number', 'comparison'], [
    ('Off', None, 'Off'),
    ('Off', None, 'off'),
    ('On', 6, 6),
    ('On', 6, '6'),
    ('On', 8, 'on')
])
def test_point_equality(status, number, comparison):
    point = Point()
    point.status = status
    point.number = number
    assert point == comparison


@pytest.mark.parametrize(['number', 'comparison'], [
    (8, 6),
    (8, '6')
])
def test_point_greater_than(number, comparison):
    point = Point()
    point.status = 'On'
    point.number = number
    assert point > comparison


@pytest.mark.parametrize(['number', 'comparison'], [
    (4, 6),
    (4, '10')
])
def test_point_less_than(number, comparison):
    point = Point()
    point.status = 'On'
    point.number = number
    assert point < comparison


