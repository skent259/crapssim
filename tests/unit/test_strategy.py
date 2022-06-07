from unittest.mock import MagicMock, call

import pytest

from crapssim import Player, Table
from crapssim.bet import Bet, PassLine, Come, HardWay, Odds, DontCome, Place
from crapssim.strategy import Strategy, AggregateStrategy, BetIfTrue, RemoveIfTrue, IfBetNotExist, \
    BetPointOff, BetPointOn, CountStrategy, BetPlace
from crapssim.strategy.core import ReplaceIfTrue, RemoveByType
from crapssim.strategy.examples import TwoCome, Pass2Come
from crapssim.strategy.odds import OddsAmountStrategy, OddsMultiplierStrategy
from crapssim.strategy.simple_bet import BaseSimpleBet, SimpleStrategyMode


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
    bet1 = MagicMock()
    bet2 = MagicMock()
    player.bets_on_table = [bet1, bet2]
    remove_if_true.update_bets(player)
    remove_if_true.key.assert_has_calls([call(bet1, player),
                                         call(bet2, player)])


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



def test_remove_if_true_calls_remove_bet(player):
    bet1, bet2, bet3 = MagicMock(), MagicMock(), MagicMock()
    player.bets_on_table = [bet1, bet2, bet3]
    player.remove_bet = MagicMock()

    def key(bet, player):
        return bet == bet1 or bet == bet3

    strategy = RemoveIfTrue(key=key)
    strategy.update_bets(player)
    player.remove_bet.assert_has_calls([call(bet1), call(bet3)])


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
    strategy = CountStrategy((HardWay,), 0, PassLine(5))
    assert strategy.get_bets_of_type_count(player) == 1


def test_count_strategy_less_than_count_bets_of_type(player):
    bet1, bet2, bet3 = PassLine(1), Come(1), HardWay(4, 1)
    player.bets_on_table = [bet1, bet2, bet3]
    strategy = CountStrategy((HardWay,), 2, PassLine(5))
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
    assert repr(strategy) == f'CountStrategy(bet_type=({PassLine},' \
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


def test_remove_by_type_remove_bet_called(player):
    strategy = RemoveByType(PassLine)
    player.remove_bet = MagicMock()
    bet = MagicMock(PassLine)
    player.bets_on_table = [bet]
    strategy.update_bets(player)
    player.remove_bet.assert_called_once_with(bet)


def test_remove_by_type_remove_bet_not_called(player):
    strategy = RemoveByType(PassLine)
    player.remove_bet = MagicMock()
    bet1 = MagicMock(Come)
    bet2 = MagicMock(HardWay)
    player.bets_on_table = [bet1, bet2]
    strategy.update_bets(player)
    player.remove_bet.assert_not_called()


def test_odds_amount_strategy_add_bet_called_pass_line(player):
    strategy = OddsAmountStrategy(PassLine, {4: 5, 5: 5})
    player.bets_on_table = [PassLine(5)]
    player.add_bet = MagicMock()
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Odds(PassLine, 4, 5))


def test_odds_amount_strategy_add_bet_not_called_pass_line(player):
    strategy = OddsAmountStrategy(PassLine, {4: 5, 5: 5})
    player.bets_on_table = [PassLine(5)]
    player.add_bet = MagicMock()
    player.table.point.number = 6
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_odds_amount_strategy_add_bet_called_come(player):
    strategy = OddsAmountStrategy(Come, {4: 5, 5: 5})
    player.bets_on_table = [Come(5, 4)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Odds(Come, 4, 5))


def test_odds_amount_strategy_add_bet_not_called_come_wrong_numbers(player):
    strategy = OddsAmountStrategy(Come, {4: 5, 5: 5})
    player.bets_on_table = [Come(5, 8)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_odds_amount_strategy_add_bet_not_called_come_bet_wrong_type(player):
    strategy = OddsAmountStrategy(Come, {4: 5, 5: 5})
    player.bets_on_table = [PassLine(5)]
    player.add_bet = MagicMock()
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_odds_amount_strategy_add_bet_not_called_amount_too_high(player):
    strategy = OddsAmountStrategy(Come, {4: 9999, 5: 5})
    player.bets_on_table = [Come(5, 4)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_odds_amount_strategy_add_bet_not_called_already_placed(player):
    strategy = OddsAmountStrategy(Come, {4: 5, 5: 5})
    player.bets_on_table = [Come(5, 4), Odds(Come, 4, 5)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_odds_multiplier_pass_line_point_number():
    table = Table()
    table.point.number = 4
    assert OddsMultiplierStrategy.get_point_number(PassLine(5), table) == 4


def test_odds_multiplier_come_point_number():
    table = Table()
    table.point.number = 4
    assert OddsMultiplierStrategy.get_point_number(Come(5, 9), table) == 9


def test_odds_multiplier_dont_come_bet_placed(player):
    strategy = OddsMultiplierStrategy(DontCome, {6: 6})
    player.bets_on_table = [DontCome(5, 6)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Odds(DontCome, 6, 30))


def test_base_simple_bet_add_if_non_existent_add(player):
    strategy = BaseSimpleBet(PassLine(5))
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(PassLine(5))


def test_base_simple_bet_add_if_non_existent_dont_add(player):
    strategy = BaseSimpleBet(PassLine(5))
    player.add_bet = MagicMock()
    player.bets_on_table = [PassLine(5)]
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_base_simple_bet_not_allowed(player):
    bet = MagicMock(PassLine)
    bet.allowed = MagicMock(return_value=False)
    strategy = BaseSimpleBet(bet)
    strategy.update_bets(player)
    player.add_bet = MagicMock()
    player.add_bet.assert_not_called()


def test_base_simple_bet_add_or_increase(player):
    strategy = BaseSimpleBet(PassLine(5), SimpleStrategyMode.ADD_OR_INCREASE)
    player.bets_on_table = [PassLine(5)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(PassLine(5))


def test_base_simple_bet_replace(player):
    strategy = BaseSimpleBet(PassLine(5), SimpleStrategyMode.REPLACE)
    player.bets_on_table = [PassLine(5)]
    player.add_bet = MagicMock()
    player.remove_bet = MagicMock()
    strategy.update_bets(player)
    player.remove_bet.assert_called_once_with(PassLine(5))
    player.add_bet.assert_called_once_with(PassLine(5))


def test_bet_place_remove_point_bet(player):
    strategy = BetPlace({5: 5})
    player.bets_on_table = [Place(5, 5)]
    player.table.point.number = 5
    player.remove_bet = MagicMock()
    strategy.remove_point_bet(player)
    player.remove_bet.assert_called_once_with(Place(5, 5))


def test_bet_place_skip_point(player):
    strategy = BetPlace({5: 5})
    player.table.point.number = 5
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_bet_place_dont_add_point_off(player):
    strategy = BetPlace({5: 5})
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_bet_place_add_bet(player):
    strategy = BetPlace({5: 5})
    player.add_bet = MagicMock()
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(Place(5, 5))


def test_bet_place_add_bet_not_skip_point(player):
    strategy = BetPlace({5: 5}, skip_point=False)
    player.add_bet = MagicMock()
    player.table.point.number = 5
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(Place(5, 5))


def test_two_come_no_existing_come_bets(player):
    strategy = TwoCome(5)
    player.add_bet = MagicMock()
    player.table.point.number = 5
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(Come(5))


def test_two_come_one_existing_come_bets(player):
    strategy = TwoCome(5)
    player.add_bet = MagicMock()
    player.bets_on_table = [Come(5, 6)]
    player.table.point.number = 5
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(Come(5))


def test_two_come_two_existing_come_bets(player):
    strategy = TwoCome(5)
    player.add_bet = MagicMock()
    player.bets_on_table = [Come(5, 6), Come(5, 10)]
    player.table.point.number = 5
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_pass_2_come_point_off_passline(player):
    strategy = Pass2Come(5)
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(PassLine(5))


def test_pass_2_come_point_on_come(player):
    strategy = Pass2Come(5)
    player.add_bet = MagicMock()
    player.bets_on_table = [PassLine(5)]
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Come(5))


def test_pass_2_come_point_on_come_2(player):
    strategy = Pass2Come(5)
    player.add_bet = MagicMock()
    player.bets_on_table = [PassLine(5), Come(5, 6)]
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Come(5))


def test_pass_2_come_point_off_come_2_dont_add(player):
    strategy = Pass2Come(5)
    player.add_bet = MagicMock()
    player.bets_on_table = [PassLine(5), Come(5, 6), Come(5, 10)]
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_not_called()
