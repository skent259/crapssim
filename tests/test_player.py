from crapssim.player import Player
from crapssim.strategy import passline


def test_default_strategy():
    player = Player(100)
    assert player.bet_strategy == passline
