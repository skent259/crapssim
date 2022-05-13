from crapssim import Table, Dice
from crapssim.bet import PassLine
from crapssim.player import Player
from crapssim.strategy import BetPassLine


def test_default_strategy():
    player = Player(100)
    assert player.bet_strategy.__class__ == BetPassLine


def test_irremovable_bet():
    bet = PassLine(50)
    table = Table()
    table.fixed_roll([2, 2])
    bet.update(table)
    assert bet.removable is False


def test_existing_bet():
    player = Player(100)
    table = Table()
    table.add_player(player)
    bet_one = PassLine(50)
    player.place_bet(bet_one, table)
    bet_two = PassLine(50)
    player.place_bet(bet_two, table)

    bet_count = len(player.bets_on_table)
    bet_amount = player.bets_on_table[0].bet_amount
    bankroll = player.bankroll
    total_bet_amount = player.total_bet_amount

    assert (bet_count, bet_amount, bankroll, total_bet_amount) == (1, 100, 0, 100)
