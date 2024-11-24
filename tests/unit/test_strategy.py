from unittest.mock import MagicMock, call

import pytest

import crapssim.strategy
import crapssim.strategy.examples
import crapssim.strategy.single_bet
from crapssim import Player, Table
from crapssim.bet import (
    Bet,
    BetResult,
    Come,
    DontCome,
    DontPass,
    Field,
    HardWay,
    Odds,
    PassLine,
    Place,
)
from crapssim.strategy import (
    AggregateStrategy,
    BetIfTrue,
    BetNewShooter,
    BetPlace,
    BetPointOff,
    BetPointOn,
    CountStrategy,
    IfBetNotExist,
    RemoveIfTrue,
    Strategy,
)
from crapssim.strategy.examples import (
    DiceDoctor,
    HammerLock,
    Pass2Come,
    PassLinePlace68,
    Place68Move59,
    Place68PR,
    Place682Come,
    PlaceInside,
    Risk12,
)
from crapssim.strategy.odds import OddsAmount, OddsMultiplier
from crapssim.strategy.single_bet import StrategyMode, _BaseSingleBet
from crapssim.strategy.tools import RemoveByType, ReplaceIfTrue


@pytest.fixture
def base_strategy():
    class TestStrategy(Strategy):
        def update_bets(self, player: Player) -> None:
            pass

        def completed(self, player: Player) -> bool:
            return False

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
        def update_bets(self, player: Player) -> None:
            pass

        def completed(self, player: Player) -> bool:
            return False

    assert base_strategy + AddedStrategy() == AggregateStrategy(
        base_strategy, AddedStrategy()
    )


def test_strategy_equality(base_strategy):
    assert base_strategy == base_strategy


def test_strategy_inequality(base_strategy):
    class TestStrategy2(Strategy):
        def update_bets(self, player: Player) -> None:
            pass

        def completed(self, player: Player) -> bool:
            return False

    assert base_strategy != TestStrategy2()


def test_strategy_repr(base_strategy):
    assert repr(base_strategy) == "TestStrategy()"


@pytest.fixture
def aggregate_strategy() -> AggregateStrategy:
    class TestStrategy1(Strategy):
        def update_bets(self, player: Player) -> None:
            pass

        def completed(self, player: Player) -> bool:
            return False

    class TestStrategy2(Strategy):
        def update_bets(self, player: Player) -> None:
            pass

        def completed(self, player: Player) -> bool:
            return False

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
    assert repr(aggregate_strategy) == "TestStrategy1() + TestStrategy2()"


@pytest.fixture
def example_bet():
    class ExampleBet(Bet):
        def get_payout_ratio(self, table: "Table") -> float:
            return 1.0

        def get_result(self, table: "Table") -> BetResult:
            return BetResult(0, False)

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
    bet_if_true.key = MagicMock(return_value=False, name="key")
    bet_if_true.update_bets(player)
    player.add_bet.assert_not_called()


def test_bet_if_true_repr(bet_if_true):
    assert (
        repr(bet_if_true) == f"BetIfTrue(bet={bet_if_true.bet}, key={bet_if_true.key})"
    )


def test_remove_if_true_key_called_for_each_bet(player):
    key = MagicMock(return_value=True)
    remove_if_true = RemoveIfTrue(key=key)
    remove_if_true.key = MagicMock(return_value=True)
    bet1 = MagicMock()
    bet2 = MagicMock()
    player.bets = [bet1, bet2]
    remove_if_true.update_bets(player)
    remove_if_true.key.assert_has_calls([call(bet1, player), call(bet2, player)])


def test_remove_if_true_no_bets_removed(player):
    key = MagicMock(return_value=False)
    remove_if_true = RemoveIfTrue(key=key)
    bet1, bet2, bet3 = MagicMock(), MagicMock(), MagicMock()
    player.bets = [bet1, bet2, bet3]
    remove_if_true.update_bets(player)
    assert player.bets == [bet1, bet2, bet3]


def test_remove_if_true_one_bet_removed(player):
    bet1, bet2, bet3 = MagicMock(), MagicMock(), MagicMock()
    player.bets = [bet1, bet2, bet3]

    def key(bet, player):
        return bet == bet2

    strategy = RemoveIfTrue(key=key)
    strategy.update_bets(player)
    assert player.bets == [bet1, bet3]


def test_remove_if_true_two_bets_removed(player):
    bet1, bet2, bet3 = MagicMock(), MagicMock(), MagicMock()
    player.bets = [bet1, bet2, bet3]

    def key(bet, player):
        return bet == bet1 or bet == bet3

    strategy = RemoveIfTrue(key=key)
    strategy.update_bets(player)
    assert player.bets == [bet2]


def test_remove_if_true_calls_remove_bet(player):
    bet1, bet2, bet3 = MagicMock(), MagicMock(), MagicMock()
    player.bets = [bet1, bet2, bet3]
    player.remove_bet = MagicMock()

    def key(bet, player):
        return bet == bet1 or bet == bet3

    strategy = RemoveIfTrue(key=key)
    strategy.update_bets(player)
    player.remove_bet.assert_has_calls([call(bet1), call(bet3)])


def test_remove_if_true_repr():
    key = MagicMock()
    strategy = RemoveIfTrue(key)
    assert repr(strategy) == f"RemoveIfTrue(key={key})"


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
    player.bets = [bet1]
    player.add_bet = MagicMock()
    player.remove_bet = MagicMock()
    strategy = ReplaceIfTrue(bet2, key)
    strategy.update_bets(player)
    player.remove_bet.assert_called_once_with(bet1)


def test_replace_if_true_key_true_has_replacement_bet_added(player):
    bet1 = MagicMock()
    bet2 = MagicMock()
    key = MagicMock(return_value=True)
    player.bets = [bet1]
    player.add_bet = MagicMock()
    player.remove_bet = MagicMock()
    strategy = ReplaceIfTrue(bet2, key)
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(bet2)


def test_if_bet_not_exists_bet_doesnt_exist_add_bet(player):
    bet1 = MagicMock()
    bet2 = MagicMock()
    player.bets = [bet1]
    player.add_bet = MagicMock()
    strategy = IfBetNotExist(bet2)
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(bet2)


def test_if_bet_exists_dont_add_bet(player):
    bet1 = MagicMock()
    bet2 = MagicMock()
    player.bets = [bet1, bet2]
    player.add_bet = MagicMock()
    strategy = IfBetNotExist(bet2)
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_if_bet_not_exist_repr(player):
    bet = MagicMock()
    strategy = IfBetNotExist(bet)
    assert repr(strategy) == f"IfBetNotExist(bet={bet})"


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


def test_bet_new_shooter_add_bet(player):
    player.table.new_shooter = True
    player.add_bet = MagicMock()
    bet = MagicMock()
    strategy = BetNewShooter(bet)
    strategy.update_bets(player)
    player.add_bet.assert_called_with(bet)


def test_bet_new_shooter_dont_add_bet(player):
    player.table.new_shooter = False
    player.add_bet = MagicMock()
    bet = MagicMock()
    strategy = BetNewShooter(bet)
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_count_strategy_when_more(player):
    player.bets = [PassLine(1), Come(1), HardWay(4, 1)]
    strategy = CountStrategy((HardWay,), 0, PassLine(5))
    assert not strategy.key(player)


def test_count_strategy_when_more_two_bets(player):
    player.bets = [PassLine(1), Come(1), HardWay(4, 1), HardWay(6, 1)]
    strategy = CountStrategy((PassLine, Come), 2, PassLine(5))
    assert not strategy.key(player)


def test_count_strategy_when_more_three_bets(player):
    player.bets = [PassLine(1), Come(1), HardWay(4, 1), HardWay(6, 1), HardWay(8, 1)]
    strategy = CountStrategy((PassLine, Come), 2, PassLine(5))
    assert not strategy.key(player)


def test_count_strategy_when_less(player):
    bet1, bet2, bet3 = PassLine(1), Come(1), HardWay(4, 1)
    player.bets = [bet1, bet2, bet3]
    strategy = CountStrategy((HardWay,), 2, PassLine(5))
    assert strategy.key(player)


def test_count_strategy_repr():
    strategy = CountStrategy((PassLine, Come), 2, PassLine(1))
    assert (
        repr(strategy) == f"CountStrategy(bet_type=({PassLine},"
        f" {Come}), count=2, bet={PassLine(1)})"
    )


def test_count_strategy_key_passes(player):
    strategy = CountStrategy((PassLine, Come), 2, PassLine(1))
    player.bets = [Come(1)]
    assert strategy.key(player)


def test_count_strategy_key_fails_bet_on_table(player):
    strategy = CountStrategy((PassLine, Come), 2, PassLine(1))
    player.bets = [PassLine(1)]
    assert not strategy.key(player)


def test_count_strategy_key_fails_too_many_bets(player):
    strategy = CountStrategy((PassLine, Come), 2, PassLine(1))
    player.bets = [Come(1), Come(1)]
    assert not strategy.key(player)


def test_remove_by_type_remove_bet_called(player):
    strategy = RemoveByType(PassLine)
    player.remove_bet = MagicMock()
    bet = MagicMock(PassLine)
    player.bets = [bet]
    strategy.update_bets(player)
    player.remove_bet.assert_called_once_with(bet)


def test_remove_by_type_remove_bet_not_called(player):
    strategy = RemoveByType(PassLine)
    player.remove_bet = MagicMock()
    bet1 = MagicMock(Come)
    bet2 = MagicMock(HardWay)
    player.bets = [bet1, bet2]
    strategy.update_bets(player)
    player.remove_bet.assert_not_called()


def test_odds_amount_strategy_add_bet_called_pass_line(player):
    strategy = OddsAmount(PassLine, {4: 5, 5: 5})
    player.bets = [PassLine(5)]
    player.add_bet = MagicMock()
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Odds(PassLine, 4, 5))


def test_odds_amount_strategy_add_bet_not_called_pass_line(player):
    strategy = OddsAmount(PassLine, {4: 5, 5: 5})
    player.bets = [PassLine(5)]
    player.add_bet = MagicMock()
    player.table.point.number = 6
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_odds_amount_strategy_add_bet_called_come(player):
    strategy = OddsAmount(Come, {4: 5, 5: 5})
    player.bets = [Come(5, 4)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Odds(Come, 4, 5))


def test_odds_amount_strategy_add_bet_not_called_come_wrong_numbers(player):
    strategy = OddsAmount(Come, {4: 5, 5: 5})
    player.bets = [Come(5, 8)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_odds_amount_strategy_add_bet_not_called_come_bet_wrong_type(player):
    strategy = OddsAmount(Come, {4: 5, 5: 5})
    player.bets = [PassLine(5)]
    player.add_bet = MagicMock()
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_odds_amount_strategy_add_bet_not_called_amount_too_high(player):
    strategy = OddsAmount(Come, {4: 9999, 5: 5})
    player.bets = [Come(5, 4)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_odds_amount_strategy_add_bet_not_called_already_placed(player):
    strategy = OddsAmount(Come, {4: 5, 5: 5})
    player.bets = [Come(5, 4), Odds(Come, 4, 5)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_odds_multiplier_pass_line_point_number():
    table = Table()
    table.point.number = 4
    assert OddsMultiplier.get_point_number(PassLine(5), table) == 4


def test_odds_multiplier_come_point_number():
    table = Table()
    table.point.number = 4
    assert OddsMultiplier.get_point_number(Come(5, 9), table) == 9


def test_odds_multiplier_dont_come_bet_placed(player):
    strategy = OddsMultiplier(DontCome, {6: 6})
    player.bets = [DontCome(5, 6)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Odds(DontCome, 6, 30))


def test_base_single_bet_add_if_non_existent_add(player):
    strategy = _BaseSingleBet(PassLine(5))
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(PassLine(5))


def test_base_single_bet_add_if_non_existent_dont_add(player):
    strategy = _BaseSingleBet(PassLine(5))
    player.add_bet = MagicMock()
    player.bets = [PassLine(5)]
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_base_single_bet_is_not_allowed(player):
    bet = MagicMock(PassLine)
    bet.is_allowed = MagicMock(return_value=False)
    strategy = _BaseSingleBet(bet)
    strategy.update_bets(player)
    player.add_bet = MagicMock()
    player.add_bet.assert_not_called()


def test_base_single_bet_add_or_increase(player):
    strategy = _BaseSingleBet(PassLine(5), StrategyMode.ADD_OR_INCREASE)
    player.bets = [PassLine(5)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(PassLine(5))


def test_base_single_bet_replace(player):
    strategy = _BaseSingleBet(PassLine(5), StrategyMode.REPLACE)
    player.bets = [PassLine(5)]
    player.add_bet = MagicMock()
    player.remove_bet = MagicMock()
    strategy.update_bets(player)
    player.remove_bet.assert_called_once_with(PassLine(5))
    player.add_bet.assert_called_once_with(PassLine(5))


def test_bet_place_remove_point_bet(player):
    strategy = BetPlace({5: 5})
    player.bets = [Place(5, 5)]
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


def test_pass_2_come_point_off_passline(player):
    strategy = Pass2Come(5)
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(PassLine(5))


def test_pass_2_come_point_on_come(player):
    strategy = Pass2Come(5)
    player.add_bet = MagicMock()
    player.bets = [PassLine(5)]
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Come(5))


def test_pass_2_come_point_on_come_2(player):
    strategy = Pass2Come(5)
    player.add_bet = MagicMock()
    player.bets = [PassLine(5), Come(5, 6)]
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Come(5))


def test_pass_2_come_point_off_come_2_dont_add(player):
    strategy = Pass2Come(5)
    player.add_bet = MagicMock()
    player.bets = [PassLine(5), Come(5, 6), Come(5, 10)]
    player.table.point.number = 4
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_pass_line_place_six_eight_pass_line(player):
    strategy = PassLinePlace68()
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(PassLine(5))


def test_pass_line_place_six_eight_place_six_eight(player):
    strategy = PassLinePlace68()
    player.bets = [PassLine(5)]
    player.table.point.number = 5
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_has_calls((call(Place(6, 6)), call(Place(8, 6))))


def test_pass_line_place_six_eight_place_six_eight_skip_point(player):
    strategy = PassLinePlace68()
    player.bets = [PassLine(5)]
    player.table.point.number = 6
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(Place(8, 6))


def test_pass_line_place_six_eight_place_six_eight_not_skip_point(player):
    strategy = PassLinePlace68(skip_point=False)
    player.bets = [PassLine(5)]
    player.table.point.number = 6
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_has_calls((call(Place(6, 6)), call(Place(8, 6))))


def test_pass_line_place_six_eight_place_six_eight_doesnt_place_twice(player):
    strategy = PassLinePlace68()
    player.bets = [PassLine(5), Place(6, 6), Place(8, 6)]
    player.table.point.number = 6
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_place_inside_place_bets_dict(player):
    strategy = PlaceInside({5: 5, 6: 6, 8: 6, 9: 5})
    player.table.point.number = 6
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_has_calls(
        [call(Place(5, 5)), call(Place(6, 6)), call(Place(8, 6)), call(Place(9, 5))]
    )


def test_place_inside_place_bets_int(player):
    strategy = PlaceInside(5)
    player.table.point.number = 6
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_has_calls(
        [call(Place(5, 5)), call(Place(6, 6)), call(Place(8, 6)), call(Place(9, 5))]
    )


def test_place_inside_bets_dont_double(player):
    strategy = PlaceInside(5)
    player.table.point.number = 6
    player.bets = [Place(5, 5), Place(6, 6), Place(8, 6), Place(9, 5)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_place_68_move_59_get_pass_line_come_points(player):
    strategy = Place68Move59()
    player.table.point.number = 8
    player.bets = [PassLine(5), Come(5, None), Come(5, 6)]
    assert strategy.get_pass_line_come_points(player) == [6, 8]


def test_place_68_move_59_do_nothing_point_off(player):
    strategy = Place68Move59()
    player.add_bet = MagicMock()
    player.remove_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()
    player.remove_bet.assert_not_called()


def test_place_68_move_59_remove_matching_place_bet_pass_line(player):
    strategy = Place68Move59()
    player.table.point.number = 6
    player.remove_bet = MagicMock()
    player.bets = [Place(6, 6), PassLine(5)]
    strategy.update_bets(player)
    player.remove_bet.assert_called_once_with(Place(6, 6))


def test_place_68_move_59_remove_matching_place_bet_come(player):
    strategy = Place68Move59()
    player.table.point.number = 4
    player.remove_bet = MagicMock()
    player.bets = [Place(6, 6), Come(5, 6)]
    strategy.update_bets(player)
    player.remove_bet.assert_called_once_with(Place(6, 6))


def test_place_68_move_59_add_six_eight_nothing_on_table(player):
    strategy = Place68Move59()
    player.table.point.number = 6
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_has_calls([call(Place(6, 6)), call(Place(8, 6))])


def test_place_68_move_59_add_six_eight_other_pass_come_on_table(player):
    strategy = Place68Move59()
    player.table.point.number = 5
    player.bets = [PassLine(5), Come(5, 10)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_has_calls([call(Place(6, 6)), call(Place(8, 6))])


def test_place_68_move_59_add_five_eight_six_pass_line(player):
    strategy = Place68Move59()
    player.table.point.number = 6
    player.bets = [PassLine(5)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_has_calls([call(Place(8, 6)), call(Place(5, 5))])


def test_place_68_move_59_no_more_than_2_come_bets(player):
    strategy = Place68Move59()
    player.table.point.number = 6
    player.bets = [PassLine(5), Place(8, 6), Place(5, 5)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_place_68_2_come_pass_line_bet_not_repeated(player):
    strategy = Place682Come()
    player.add_bet = MagicMock()
    player.bets = [PassLine(5)]
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_place_68_2_come_come_bet_not_repeated(player):
    strategy = Place682Come()
    player.table.point.number = 6
    player.add_bet = MagicMock()
    player.bets = [Come(5, None)]
    strategy.update_bets(player)
    player.add_bet.ass()


def test_place_68_2_come_pass_line_added(player):
    strategy = Place682Come()
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(PassLine(5))


def test_place_68_2_come_pass_line_not_added_too_many_come(player):
    strategy = Place682Come()
    player.add_bet = MagicMock()
    player.bets = [Come(5, 6), Come(9, 5)]
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_place_68_2_come_come_added_point_on(player):
    strategy = Place682Come()
    player.add_bet = MagicMock()
    player.table.point.number = 6
    strategy.update_bets(player)
    # strategy.place_pass_line_come(player)
    bets_made = [
        Come(5),
        Place(6, amount=6.0),
        Place(8, amount=6.0),
        Place(5, amount=5.0),
        Place(9, amount=5.0),
    ]
    player.add_bet.assert_has_calls([call(x) for x in bets_made])

    # player.add_bet.assert_called_once_with(Come(5))


def test_place_68_2_come_add_come_and_place(player):
    strategy = Place682Come()
    player.table.point.number = 6
    strategy.update_bets(player)
    assert player.bets == [Come(5), Place(6, 6), Place(8, 6)]


def test_place_68_2_come_dont_add_come(player):
    strategy = Place682Come()
    player.table.point.number = 6
    player.add_bet = MagicMock()
    player.bets = [PassLine(5), Come(5, 8), Place(5, 5), Place(9, 5)]
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_hammerlock_point_start_six_eight_amount(player):
    strategy = HammerLock(5)
    assert strategy.start_six_eight_amount == 12


def test_hammerlock_end_six_eight_amount(player):
    strategy = HammerLock(5)
    assert strategy.end_six_eight_amount == 6


def test_hammerlock_five_nine_amount(player):
    strategy = HammerLock(5)
    assert strategy.five_nine_amount == 5


def test_hammerlock_odds_multiplier(player):
    strategy = HammerLock(5)
    assert strategy.odds_multiplier == 6


def test_hammerlock_1_win_after_roll(player):
    strategy = HammerLock(5)
    bet1 = Place(6, 5)
    bet1.get_result = MagicMock(return_value=BetResult(1, True))
    player.bets = [bet1]
    strategy.after_roll(player)
    assert strategy.place_win_count == 1


def test_hammerlock_2_win_after_roll(player):
    strategy = HammerLock(5)
    bet = Place(6, 5)
    bet.get_result = MagicMock(return_value=BetResult(1, True))
    player.bets = [bet, bet]
    strategy.after_roll(player)
    assert strategy.place_win_count == 2


def test_hammerlock_lose_place_win_count_0(player):
    strategy = HammerLock(5)
    strategy.place_win_count = 2
    player.table.point.number = 6
    player.table.dice.result = (3, 4)
    strategy.after_roll(player)
    assert strategy.place_win_count == 0


def test_hammerlock_point_off_bets(player):
    strategy = HammerLock(5)
    player.add_bet = MagicMock()
    strategy.pass_and_dontpass(player)
    player.add_bet.assert_has_calls([call(PassLine(5)), call(DontPass(5))])


def test_hammerlock_place_68(player):
    strategy = HammerLock(5)
    player.table.point.number = 5
    player.add_bet = MagicMock()
    player.bets = [PassLine(5)]
    strategy.place68(player)
    player.add_bet.assert_has_calls([call(Place(6, 12)), call(Place(8, 12))])


def test_hammerlock_place_5689_removed_bets(player):
    strategy = HammerLock(5)
    player.table.point.number = 4
    player.bets = [Place(6, 12), Place(8, 12)]
    player.remove_bet = MagicMock()
    player.add_bet = MagicMock()
    strategy.place5689(player)
    player.remove_bet.assert_has_calls([call(Place(6, 12)), call(Place(8, 12))])


def test_hammerlock_place_5689_added_bets(player):
    strategy = HammerLock(5)
    player.table.point.number = 4
    player.add_bet = MagicMock()
    strategy.place5689(player)
    player.add_bet.assert_has_calls(
        [call(Place(5, 5)), call(Place(6, 6)), call(Place(8, 6)), call(Place(9, 5))]
    )


@pytest.mark.parametrize("place_win_count", [0, 1, 2])
def test_hammerlock_always_add_dont_odds(player, place_win_count):
    strategy = HammerLock(5)
    strategy.place68 = MagicMock()
    strategy.place5689 = MagicMock()
    player.table.point.number = 4
    player.bets = [DontPass(5)]
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_with(Odds(DontPass, 4, 30))


def test_risk_12_player_won_field_bet(player):
    strategy = Risk12()
    player.bets = [Field(5)]
    player.table.dice.result = (2, 2)
    strategy.after_roll(player)
    assert strategy.pre_point_winnings == 10


def test_risk_12_player_won_double_field_bet(player):
    strategy = Risk12()
    player.bets = [Field(5)]
    player.table.dice.result = (6, 6)
    strategy.after_roll(player)
    assert strategy.pre_point_winnings == 15


def test_risk_12_player_won_pass_line_bet(player):
    strategy = Risk12()
    player.bets = [PassLine(5)]
    player.table.dice.result = (1, 6)
    strategy.after_roll(player)
    assert strategy.pre_point_winnings == 10


def test_risk_12_player_won_pass_line_bet_and_field(player):
    strategy = Risk12()
    player.bets = [PassLine(5), Field(5)]
    player.table.dice.result = (6, 5)
    strategy.after_roll(player)
    assert strategy.pre_point_winnings == 20


def test_risk_12_reset_prepoint_winnings(player):
    strategy = Risk12()
    strategy.pre_point_winnings = 20
    player.table.point.number = 4
    player.bets = [PassLine(5)]
    player.table.dice.result = (2, 5)
    strategy.after_roll(player)
    assert strategy.pre_point_winnings == 0


def test_risk_12_point_off_add_bets(player):
    strategy = Risk12()
    player.add_bet = MagicMock()
    strategy.point_off(player)
    player.add_bet.assert_has_calls([call(PassLine(5)), call(Field(5))])


def test_risk_12_point_on_5_pre_point_winnings(player):
    strategy = Risk12()
    strategy.pre_point_winnings = 5
    player.add_bet = MagicMock()
    player.table.point.number = 5
    strategy.point_on(player)
    player.add_bet.assert_has_calls([call(Place(6, 6))])


def test_risk_12_point_on_10_pre_point_winnings(player):
    strategy = Risk12()
    strategy.pre_point_winnings = 10
    player.add_bet = MagicMock()
    player.table.point.number = 5
    strategy.point_on(player)
    player.add_bet.assert_has_calls([call(Place(6, 6)), call(Place(8, 6))])


def test_dice_doctor_win_increase_progression(player):
    strategy = DiceDoctor()
    bet = Field(5)
    bet.get_status = MagicMock(return_value="win")
    player.table.dice.result = (1, 1)
    player.bets = [bet]
    strategy.after_roll(player)
    assert strategy.current_progression == 1


def test_dice_doctor_lose_progression(player):
    strategy = DiceDoctor()
    strategy.current_progression = 4
    bet = Field(5)
    bet.get_status = MagicMock(return_value="lose")
    player.table.dice.result = (3, 4)
    player.bets = [bet]
    strategy.after_roll(player)
    assert strategy.current_progression == 0


@pytest.mark.parametrize("progression, amount", [(0, 10), (4, 25), (9, 100)])
def test_dice_doctor_bet_amounts(player, progression, amount):
    strategy = DiceDoctor()
    strategy.current_progression = progression
    player.add_bet = MagicMock()
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(Field(amount))


@pytest.mark.parametrize(
    "attribute, amount",
    [
        ("base_amount", 6),
        ("starting_amount", 6),
        ("win_one_amount", 7),
        ("win_two_amount", 14),
    ],
)
def test_place_68_cpr_amounts(attribute, amount):
    strategy = Place68PR()
    assert getattr(strategy, attribute) == amount


def test_place_68_cpr_after_roll_6_winnings_increase(player):
    strategy = Place68PR(6)
    bet6 = Place(6, 6)
    bet8 = Place(8, 6)
    bet6.get_result = MagicMock(return_value=BetResult(13, True))
    bet8.get_result = MagicMock(return_value=BetResult(0, False))
    player.bets = [bet6, bet8]
    player.table.point.number = 6
    strategy.after_roll(player)
    assert strategy.six_winnings == 7


def test_place_68_cpr_after_roll_winnings_dont_change(player):
    strategy = Place68PR(6)
    bet6 = Place(6, 6)
    bet8 = Place(8, 6)
    bet6.get_result = MagicMock(return_value=BetResult(0, False))
    bet8.get_result = MagicMock(return_value=BetResult(0, False))
    player.bets = [bet6, bet8]
    player.table.point.number = 6
    strategy.after_roll(player)
    assert strategy.six_winnings == 0


def test_place_68_cpr_ensure_bets_exist_adds_place_6_place_8(player):
    strategy = Place68PR(6)
    player.add_bet = MagicMock()
    player.table.point.number = 6
    strategy.ensure_bets_exist(player)
    player.add_bet.assert_has_calls([call(Place(6, 6)), call(Place(8, 6))])


def test_place_68_cpr_ensure_bets_exist_doesnt_double_bets(player):
    strategy = Place68PR(6)
    player.add_bet = MagicMock()
    player.bets = [Place(6, 6), Place(8, 6)]
    player.table.point.number = 6
    strategy.ensure_bets_exist(player)
    player.add_bet.assert_not_called()


def test_place_68_cpr_ensure_bets_exist_doesnt_add_to_existing_bets_with_press(player):
    strategy = Place68PR(6)
    player.add_bet = MagicMock()
    player.bets = [Place(6, 12), Place(8, 12)]
    player.table.point.number = 6
    strategy.ensure_bets_exist(player)
    player.add_bet.assert_not_called()


def test_place_68_cpr_press_increases_bet(player):
    strategy = Place68PR(6)
    player.add_bet = MagicMock()
    bet1 = Place(6, 6)
    bet2 = Place(8, 6)
    strategy.six_winnings = 7
    player.bets = [bet1, bet2]
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(Place(6, 6))


def test_place_68_cpr_press_no_increases(player):
    strategy = Place68PR(6)
    player.add_bet = MagicMock()
    bet1 = Place(6, 6)
    bet2 = Place(8, 6)
    player.bets = [bet1, bet2]
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


def test_place_68_cpr_update_bets_initial_bets(player):
    strategy = Place68PR(6)
    player.add_bet = MagicMock()
    player.table.point.number = 6
    strategy.update_bets(player)
    player.add_bet.assert_has_calls([call(Place(6, 6)), call(Place(8, 6))])


def test_place_68_cpr_update_bets_initial_bets_placed_push_6_add_bet(player):
    strategy = Place68PR(6)
    player.add_bet = MagicMock()
    player.table.point.number = 6
    winning_bet = Place(6, 6)
    winning_bet.get_status = MagicMock(return_value="win")
    strategy.six_winnings = 7
    player.bets = [Place(6, 6), Place(8, 6)]
    strategy.update_bets(player)
    player.add_bet.assert_called_once_with(Place(6, 6))


def test_place_68_cpr_update_bets_initial_bets_placed_no_update(player):
    strategy = Place68PR(6)
    player.add_bet = MagicMock()
    player.table.point.number = 6
    player.bets = [Place(6, 6), Place(8, 6)]
    strategy.update_bets(player)
    player.add_bet.assert_not_called()


@pytest.mark.parametrize(
    "strategy, strategy_name",
    [
        # Single bet strategies
        (
            crapssim.strategy.BetPlace({6: 6, 8: 6}),
            "BetPlace(place_bet_amounts={6: 6, 8: 6}, mode=StrategyMode.ADD_IF_POINT_ON, skip_point=True, skip_come=False)",
        ),
        (
            crapssim.strategy.BetPassLine(1),
            "BetPassLine(bet_amount=1.0, mode=StrategyMode.ADD_IF_POINT_OFF)",
        ),
        (
            crapssim.strategy.BetDontPass(1),
            "BetDontPass(bet_amount=1.0, mode=StrategyMode.ADD_IF_POINT_OFF)",
        ),
        (
            crapssim.strategy.single_bet.BetCome(1),
            "BetCome(bet_amount=1.0, mode=StrategyMode.ADD_IF_POINT_ON)",
        ),
        (
            crapssim.strategy.single_bet.BetDontCome(1),
            "BetDontCome(bet_amount=1.0, mode=StrategyMode.ADD_IF_POINT_ON)",
        ),
        (
            crapssim.strategy.single_bet.BetHardWay(4, 1),
            "BetHardWay(4, bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        (
            crapssim.strategy.single_bet.BetHardWay(6, 1),
            "BetHardWay(6, bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        (
            crapssim.strategy.single_bet.BetHardWay(8, 1),
            "BetHardWay(8, bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        (
            crapssim.strategy.single_bet.BetHardWay(10, 1),
            "BetHardWay(10, bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        (
            crapssim.strategy.single_bet.BetField(1),
            "BetField(bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        (
            crapssim.strategy.single_bet.BetAny7(1),
            "BetAny7(bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        (
            crapssim.strategy.single_bet.BetTwo(1),
            "BetTwo(bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        (
            crapssim.strategy.single_bet.BetThree(1),
            "BetThree(bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        (
            crapssim.strategy.single_bet.BetYo(1),
            "BetYo(bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        (
            crapssim.strategy.single_bet.BetBoxcars(1),
            "BetBoxcars(bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        (
            crapssim.strategy.single_bet.BetFire(1),
            "BetFire(bet_amount=1.0, mode=StrategyMode.ADD_IF_NON_EXISTENT)",
        ),
        # Example strategies
        (crapssim.strategy.examples.Pass2Come(1), "Pass2Come(amount=1.0)"),
        (
            crapssim.strategy.examples.PassLinePlace68(5, 6, 6),
            "PassLinePlace68(pass_line_amount=5.0, six_amount=6.0, eight_amount=6.0, skip_point=True)",
        ),
        (crapssim.strategy.examples.PlaceInside(5), "PlaceInside(amount=5.0)"),
        (
            crapssim.strategy.examples.Place68Move59(5, 6, 5),
            "Place68Move59(pass_come_amount=5.0, six_eight_amount=6.0, five_nine_amount=5.0)",
        ),
        (
            crapssim.strategy.examples.PassLinePlace68Move59(5, 6, 5),
            "PassLinePlace68Move59(pass_line_amount=5.0, six_eight_amount=6.0, five_nine_amount=5.0)",
        ),
        (
            crapssim.strategy.examples.Place682Come(5, 6, 5),
            "Place682Come(pass_come_amount=5.0, six_eight_amount=6.0, five_nine_amount=5.0)",
        ),
        (crapssim.strategy.examples.IronCross(10), "IronCross(base_amount=10.0)"),
        (crapssim.strategy.examples.HammerLock(5), "HammerLock(base_amount=5.0)"),
        (crapssim.strategy.examples.Risk12(), "Risk12()"),
        (crapssim.strategy.examples.Knockout(5), "Knockout(base_amount=5.0)"),
        (crapssim.strategy.examples.DiceDoctor(5), "DiceDoctor(base_amount=5.0)"),
        (crapssim.strategy.examples.Place68PR(6), "Place68PR(base_amount=6.0)"),
        (
            crapssim.strategy.examples.Place68DontCome2Odds(6, 5),
            "Place68DontCome2Odds(six_eight_amount=6.0, dont_come_amount=5.0)",
        ),
    ],
)
def test_repr_names(strategy, strategy_name):
    # Check above visually make sense
    assert repr(strategy) == strategy_name
