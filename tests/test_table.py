from crapssim import Table, Player
from crapssim.bet import Come, PassLine
from crapssim.strategy import passline


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
