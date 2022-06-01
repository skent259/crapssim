from crapssim import Player, Table
from crapssim.strategy import Strategy


def test_strategy_completed():
    class TestStrategy(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

        def completed(self, player: 'Player'):
            return player.bankroll == 100

    strategy = TestStrategy()
    table = Table()
    table.add_player(100, strategy=TestStrategy)
    assert strategy.completed(table.players[0]) is True


def test_strategy_default_not_completed():
    class TestStrategy(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

    strategy = TestStrategy()
    table = Table()
    table.add_player(100, strategy=TestStrategy)
    assert strategy.completed(table.players[0]) is False


def test_aggregate_strategy_completed():
    class TestStrategy1(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

        def completed(self, player: 'Player') -> bool:
            return True

    class TestStrategy2(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

        def completed(self, player: 'Player') -> bool:
            return True

    strategy = TestStrategy1() + TestStrategy2()
    table = Table()
    table.add_player(strategy=strategy)
    assert strategy.completed(table.players[0])


def test_aggregate_strategy_incomplete():
    class TestStrategy1(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

        def completed(self, player: 'Player') -> bool:
            return True

    class TestStrategy2(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

        def completed(self, player: 'Player') -> bool:
            return False

    strategy = TestStrategy1() + TestStrategy2()
    table = Table()
    table.add_player(strategy=strategy)
    assert not strategy.completed(table.players[0])
