from unittest.mock import MagicMock, Mock, call

import pytest

from crapssim import Player, Table
from crapssim.bet import Bet, PassLine, Come, HardWay
from crapssim.strategy import Strategy, AggregateStrategy, BetIfTrue, RemoveIfTrue, IfBetNotExist, \
    BetPointOff, BetPointOn, CountStrategy, PlaceBetAndMove
from crapssim.strategy.core import ReplaceIfTrue


@pytest.fixture
def base_strategy():
    class TestStrategy(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

    return TestStrategy()


@pytest.fixture
def player():
    table = Table()
    table.add_player()
    return table.players[0]


def test_strategy_completed(base_strategy, player):
    base_strategy.completed = lambda p: p.bankroll == 100
    assert base_strategy.completed(player) is True


def test_strategy_default_not_completed(base_strategy, player):
    assert base_strategy.completed(player) is False


def test_strategy_add(base_strategy):
    class AddedStrategy(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

    assert base_strategy + AddedStrategy() == AggregateStrategy(base_strategy, AddedStrategy())


def test_strategy_equality(base_strategy):
    assert base_strategy == base_strategy


def test_strategy_inequality(base_strategy):
    class TestStrategy2(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

    assert base_strategy != TestStrategy2()


def test_strategy_repr(base_strategy):
    assert repr(base_strategy) == 'TestStrategy()'


@pytest.fixture
def aggregate_strategy() -> AggregateStrategy:
    class TestStrategy1(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

    class TestStrategy2(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass

    return TestStrategy1() + TestStrategy2()


def test_aggregate_strategy_completed(aggregate_strategy, player):
    aggregate_strategy.strategies[0].completed = lambda p: True
    aggregate_strategy.strategies[1].completed = lambda p: True
    assert aggregate_strategy.completed(player)


def test_aggregate_strategy_incomplete(aggregate_strategy, player):
    aggregate_strategy.strategies[0].completed = lambda p: True
    aggregate_strategy.strategies[1].completed = lambda p: False
    assert not aggregate_strategy.completed(player)


def test_aggregate_strategy_calls_all_update_bets(aggregate_strategy, player):
    aggregate_strategy.strategies[0].update_bets = MagicMock()
    aggregate_strategy.strategies[1].update_bets = MagicMock()

    aggregate_strategy.update_bets(player)

    aggregate_strategy.strategies[0].update_bets.assert_called_once_with(player)
    aggregate_strategy.strategies[1].update_bets.assert_called_once_with(player)


def test_aggregate_strategy_update_bets_calls_completed(aggregate_strategy, player):
    aggregate_strategy.strategies[0].completed = MagicMock()
    aggregate_strategy.strategies[1].completed = MagicMock()

    aggregate_strategy.update_bets(player)

    aggregate_strategy.strategies[0].completed.assert_called_once_with(player)
    aggregate_strategy.strategies[1].completed.assert_called_once_with(player)


def test_aggregate_strategy_completed_calls_all_completed(aggregate_strategy, player):
    aggregate_strategy.strategies[0].completed = MagicMock()
    aggregate_strategy.strategies[1].completed = MagicMock()

    aggregate_strategy.completed(player)

    aggregate_strategy.strategies[0].completed.assert_called_once_with(player)
    aggregate_strategy.strategies[1].completed.assert_called_once_with(player)


def test_aggregate_repr(aggregate_strategy):
    assert repr(aggregate_strategy) == 'TestStrategy1() + TestStrategy2()'


@pytest.fixture
def example_bet():
    class ExampleBet(Bet):
        def get_payout_ratio(self, table: "Table") -> float:
            return 1.0

        def get_status(self, table: "Table") -> str | None:
            return None
    return ExampleBet(1)


@pytest.fixture
def bet_if_true(example_bet):
    key = MagicMock(return_value=True)
    return BetIfTrue(example_bet, key)


def test_bet_if_true_key_is_called(bet_if_true, player):
    bet_if_true.update_bets(player)
    bet_if_true.key.assert_called_once_with(player)


def test_player_add_bet_is_called_if_key_is_true(bet_if_true, player):
    player.add_bet = MagicMock()
    bet_if_true.update_bets(player)
    player.add_bet.assert_called_once()


def test_player_add_bet_is_not_called_if_key_is_true(bet_if_true, player):
    player.add_bet = MagicMock()
    bet_if_true.key = MagicMock(return_value=False, name='key')
    bet_if_true.update_bets(player)
    player.add_bet.assert_not_called()


def test_bet_if_true_repr(bet_if_true):
    assert repr(bet_if_true) == f'BetIfTrue(bet={bet_if_true.bet}, key={bet_if_true.key})'


def test_remove_if_true_key_called_for_each_bet(player):
    key = MagicMock(return_value=True)
    remove_if_true = RemoveIfTrue(key=key)
    remove_if_true.key = MagicMock(return_value=True)
    player.bets_on_table = [MagicMock(), MagicMock()]
    before_bets = player.bets_on_table
    remove_if_true.update_bets(player)
    remove_if_true.key.assert_has_calls([call(before_bets[0], player),
                                         call(before_bets[1], player)])


def test_remove_if_true_no_bets_removed(player):
    key = MagicMock(return_value=False)
    remove_if_true = RemoveIfTrue(key=key)
    bet1, bet2, bet3 = MagicMock(), MagicMock(), MagicMock()
    player.bets_on_table = [bet1, bet2, bet3]
    remove_if_true.update_bets(player)
    assert player.bets_on_table == [bet1, bet2, bet3]


def test_remove_if_true_one_bet_removed(player):
    bet1, bet2, bet3 = MagicMock(), MagicMock(), MagicMock()
    player.bets_on_table = [bet1, bet2, bet3]

    def key(bet, player):
        return bet == bet2

    strategy = RemoveIfTrue(key=key)
    strategy.update_bets(player)
    assert player.bets_on_table == [bet1, bet3]


def test_remove_if_true_two_bets_removed(player):
    bet1, bet2, bet3 = MagicMock(), MagicMock(), MagicMock()
    player.bets_on_table = [bet1, bet2, bet3]

    def key(bet, player):
        return bet == bet1 or bet == bet3

    strategy = RemoveIfTrue(key=key)
    strategy.update_bets(player)
    assert player.bets_on_table == [bet2]


def test_remove_if_true_repr():
    key = MagicMock()
    strategy = RemoveIfTrue(key)
    assert repr(strategy) == f'RemoveIfTrue(key={key})'


def test_replace_if_true_no_initial_bets_no_bets_added(player):
    bet = MagicMock()
    key = MagicMock(return_value=True)
    player.add_bet = MagicMock()
    strategy = ReplaceIfTrue(bet, key)
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_replace_if_true_no_initial_bets_no_bets_removed(player):
    bet = MagicMock()
    key = MagicMock(return_value=True)
    player.add_bet = MagicMock()
    player.remove_bet = MagicMock()
    strategy = ReplaceIfTrue(bet, key)
    strategy.update_bets(player)
    player.remove_bet.assert_not_called()


def test_replace_if_true_key_true_has_initial_bets_removed(player):
    bet1 = MagicMock()
    bet2 = MagicMock()
    key = MagicMock(return_value=True)
    player.bets_on_table = [bet1]
    player.add_bet = MagicMock()
    player.remove_bet = MagicMock()
    strategy = ReplaceIfTrue(bet2, key)
    strategy.update_bets(player)
    player.remove_bet.assert_called_once_with(bet1)


def test_replace_if_true_key_true_has_replacement_bet_added(player):
    bet1 = MagicMock()
    bet2 = MagicMock()
    key = MagicMock(return_value=True)
    player.bets_on_table = [bet1]
    player.add_bet = MagicMock()
    player.remove_bet = MagicMock()
    strategy = ReplaceIfTrue(bet2, key)
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(bet2)


def test_if_bet_not_exists_bet_doesnt_exist_add_bet(player):
    bet1 = MagicMock()
    bet2 = MagicMock()
    player.bets_on_table = [bet1]
    player.add_bet = MagicMock()
    strategy = IfBetNotExist(bet2)
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(bet2)


def test_if_bet_exists_dont_add_bet(player):
    bet1 = MagicMock()
    bet2 = MagicMock()
    player.bets_on_table = [bet1, bet2]
    player.add_bet = MagicMock()
    strategy = IfBetNotExist(bet2)
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_if_bet_not_exist_repr(player):
    bet = MagicMock()
    strategy = IfBetNotExist(bet)
    assert repr(strategy) == f'IfBetNotExist(bet={bet})'


def test_bet_point_off_add_bet(player):
    player.table.point.number = None
    player.add_bet = MagicMock()
    bet = MagicMock()
    strategy = BetPointOff(bet)
    strategy.update_bets(player)
    player.add_bet.assert_called_with(bet)


def test_bet_point_off_dont_add_bet(player):
    player.table.point.number = 6
    player.add_bet = MagicMock()
    bet = MagicMock()
    strategy = BetPointOff(bet)
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_bet_point_on_add_bet(player):
    player.table.point.number = 9
    player.add_bet = MagicMock()
    bet = MagicMock()
    strategy = BetPointOn(bet)
    strategy.update_bets(player)
    player.add_bet.assert_called_with(bet)


def test_bet_point_on_dont_add_bet(player):
    player.table.point.number = None
    player.add_bet = MagicMock()
    bet = MagicMock()
    strategy = BetPointOn(bet)
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_count_strategy_get_bets_of_type_count(player):
    bet1, bet2, bet3 = PassLine(1), Come(1), HardWay(4, 1)
    player.bets_on_table = [bet1, bet2, bet3]
    strategy = CountStrategy((HardWay, ), 0, PassLine(5))
    assert strategy.get_bets_of_type_count(player) == 1


def test_count_strategy_less_than_count_bets_of_type(player):
    bet1, bet2, bet3 = PassLine(1), Come(1), HardWay(4, 1)
    player.bets_on_table = [bet1, bet2, bet3]
    strategy = CountStrategy((HardWay, ), 2, PassLine(5))
    assert strategy.less_than_count_bets_of_type(player)


def test_count_strategy_greater_than_count_bets_of_type(player):
    bet1, bet2, bet3 = PassLine(1), Come(1), HardWay(4, 1)
    player.bets_on_table = [bet1, bet2, bet3]
    strategy = CountStrategy((PassLine, Come), 2, PassLine(5))
    assert not strategy.less_than_count_bets_of_type(player)


def test_bet_is_not_on_table(player):
    bet1, bet2 = PassLine(5), Come(1)
    player.bets_on_table = [bet1, bet2]
    strategy = CountStrategy((PassLine, Come), 2, PassLine(1))
    assert strategy.bet_is_not_on_table(player)


def test_bet_is_on_table(player):
    bet1, bet2 = PassLine(1), Come(1)
    player.bets_on_table = [bet1]
    strategy = CountStrategy((PassLine, Come), 2, PassLine(1))
    assert not strategy.bet_is_not_on_table(player)


def test_count_strategy_repr():
    strategy = CountStrategy((PassLine, Come), 2, PassLine(1))
    assert repr(strategy) == f'CountStrategy(bet_types=({PassLine},' \
                             f' {Come}), count=2, bet={PassLine(1)})'


def test_count_strategy_key_passes(player):
    strategy = CountStrategy((PassLine, Come), 2, PassLine(1))
    player.bets_on_table = [Come(1)]
    assert strategy.key(player)


def test_count_strategy_key_fails_bet_on_table(player):
    strategy = CountStrategy((PassLine, Come), 2, PassLine(1))
    player.bets_on_table = [PassLine(1)]
    assert not strategy.key(player)


def test_count_strategy_key_fails_too_many_bets(player):
    strategy = CountStrategy((PassLine, Come), 2, PassLine(1))
    player.bets_on_table = [Come(1), Come(1)]
    assert not strategy.key(player)
