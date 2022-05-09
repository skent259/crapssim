from crapssim import Table, Dice
from crapssim.bet import PassLine
from crapssim.player import Player
from crapssim.strategy import passline


def test_default_strategy():
    player = Player(100)
    assert player.bet_strategy == passline


def test_irremovable_bet():
    player = Player(100)
    bet = PassLine(50)
    table = Table()
    table.add_player(player)
    player.bet(bet)
    table = Table()
    dice = Dice()
    dice.fixed_roll([2, 2])
    player.get_bet(PassLine)._update_bet(table)
    player.remove_if_present(PassLine)
    assert len(player.bets_on_table) == 1


def test_existing_bet():
    player = Player(100)
    table = Table()
    table.add_player(player)
    bet_one = PassLine(50)
    player.bet(bet_one)
    bet_two = PassLine(50)
    player.bet(bet_two)

    bet_count = len(player.bets_on_table)
    bet_amount = player.bets_on_table[0].bet_amount
    bankroll = player.bankroll
    total_bet_amount = player.total_bet_amount

    assert (bet_count, bet_amount, bankroll, total_bet_amount) == (1, 100, 0, 100)
