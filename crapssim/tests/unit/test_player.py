from crapssim import Table
from crapssim.bet import PassLine
from crapssim.strategy import BetPassLine


def test_default_strategy():
    table = Table()
    table.add_player()
    assert table.players[0].strategy == BetPassLine(5)


def test_irremovable_bet():
    bet = PassLine(50)
    table = Table()
    table.add_player(500)
    table.fixed_run([(2, 2)])
    assert bet.is_removable(table) is False


def test_existing_bet():
    table = Table()
    table.add_player()
    bet_one = PassLine(50)
    table.players[0].add_bet(bet_one)
    bet_two = PassLine(50)
    table.players[0].add_bet(bet_two)

    bet_count = len(table.players[0].bets)
    bet_amount = table.players[0].bets[0].amount
    bankroll = table.players[0].bankroll
    total_bet_amount = table.players[0].total_bet_amount

    assert (bet_count, bet_amount, bankroll, total_bet_amount) == (1, 100, 0, 100)
