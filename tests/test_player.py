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
    player.bet(bet)
    table = Table()
    dice = Dice()
    dice.fixed_roll([2, 2])
    player.get_bet('PassLine')._update_bet(table, dice)
    player.remove_if_present('PassLine')
    assert len(player.bets_on_table) == 1
