from crapssim import Table
from crapssim.strategy import passline


def test_ensure_one_player():
    table = Table()
    count_zero = len(table.players)
    table.ensure_one_player()
    count_one = len(table.players)
    bankroll = table.players[0].bankroll
    strategy = table.players[0].bet_strategy
    assert (count_zero, count_one, bankroll, strategy) == (0, 1, 500, passline)
