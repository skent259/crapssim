import pytest

from crapssim import Table
from crapssim.bet import (
    All,
    Any7,
    Bet,
    Boxcars,
    Come,
    Fire,
    HardWay,
    Hop,
    Place,
    Small,
    Tall,
    Three,
    Two,
    Yo,
)
from crapssim.strategy.single_bet import (
    BetAll,
    BetAny7,
    BetBuy,
    BetBoxcars,
    BetCome,
    BetDontCome,
    BetFire,
    BetHardWay,
    BetHop,
    BetLay,
    BetPlace,
    BetSmall,
    BetTall,
    BetThree,
    BetTwo,
    BetYo,
    StrategyMode,
)
from crapssim.strategy.tools import NullStrategy
from crapssim.table import TableUpdate


@pytest.mark.parametrize(
    ["strategy", "rolls", "correct_bets"],
    [
        (BetHardWay(4, bet_amount=5), [], [HardWay(4, amount=5.0)]),
        (BetHardWay(6, bet_amount=5), [], [HardWay(6, amount=5.0)]),
        (BetHardWay(8, bet_amount=5), [], [HardWay(8, amount=5.0)]),
        (BetHardWay(10, bet_amount=5), [], [HardWay(10, amount=5.0)]),
        (BetHop((2, 3), bet_amount=1), [], [Hop((2, 3), amount=1.0)]),
        (BetHop((3, 2), bet_amount=1), [], [Hop((3, 2), amount=1.0)]),
        (BetHop((2, 2), bet_amount=1), [], [Hop((2, 2), amount=1.0)]),
        (BetAny7(bet_amount=5), [], [Any7(amount=5.0)]),
        (BetTwo(bet_amount=5), [], [Two(amount=5.0)]),
        (BetThree(bet_amount=5), [], [Three(amount=5.0)]),
        (BetYo(bet_amount=5), [], [Yo(amount=5.0)]),
        (BetBoxcars(bet_amount=5), [], [Boxcars(amount=5.0)]),
        (BetFire(bet_amount=5), [], [Fire(amount=5.0)]),
        (BetAll(bet_amount=5), [], [All(amount=5.0)]),
        (BetTall(bet_amount=5), [], [Tall(amount=5.0)]),
        (BetSmall(bet_amount=5), [], [Small(amount=5.0)]),
    ],
)
def test_strategies_compare_bets(
    strategy, rolls: list[tuple[int, int]], correct_bets: {(str, str, float)}
):
    table = Table()
    table.add_player(strategy=strategy)
    table.fixed_run(rolls, verbose=False)
    TableUpdate().run_strategies(table)

    bets = table.players[0].bets

    assert set(bets) == set(correct_bets)


@pytest.mark.parametrize(
    ["strategy", "rolls", "correct_bets"],
    [
        (
            BetHardWay(4, 1, mode=StrategyMode.BET_IF_POINT_ON) + BetHardWay(8, 1),
            [(3, 3), (6, 1)],
            [HardWay(8, 1)],
        ),
        (
            BetHardWay(4, 1, mode=StrategyMode.BET_IF_POINT_ON) + BetHardWay(8, 1),
            [(3, 3), (6, 1), (4, 4)],
            [HardWay(4, 1), HardWay(8, 1)],
        ),
        (
            BetHop((2, 3), 1, mode=StrategyMode.BET_IF_POINT_ON) + BetHop((5, 4), 1),
            [(3, 3), (6, 1)],
            [Hop((4, 5), 1)],
        ),
        (
            BetHop((2, 3), 1, mode=StrategyMode.BET_IF_POINT_ON) + BetHop((5, 4), 1),
            [(3, 3), (6, 1), (4, 4)],
            [Hop((2, 3), 1), Hop((4, 5), 1)],
        ),
    ],
)
def test_bet_point_on_special_cases(
    strategy, rolls: list[tuple[int, int]], correct_bets: list[Bet]
):

    table = Table()
    table.add_player(strategy=strategy)
    table.fixed_run(rolls, verbose=False)
    TableUpdate().run_strategies(table)

    bets = table.players[0].bets

    assert set(bets) == set(correct_bets)


def test_betplace_always_working_passthrough_controls_comeout_resolution():
    table_push = Table()
    table_push.settings["come_out_working_policy"] = "real_casino"
    table_push.add_player(
        strategy=BetPlace(
            {6: 6},
            mode=StrategyMode.ADD_IF_NOT_BET,
            always_working=False,
        )
    )
    table_push.fixed_run([(3, 3)], verbose=False)

    assert table_push.players[0].bankroll == pytest.approx(94)
    assert len(table_push.players[0].bets) == 1

    table_working = Table()
    table_working.settings["come_out_working_policy"] = "real_casino"
    table_working.add_player(
        strategy=BetPlace(
            {6: 6},
            mode=StrategyMode.ADD_IF_NOT_BET,
            always_working=True,
        )
    )
    table_working.fixed_run([(3, 3)], verbose=False)

    assert table_working.players[0].bankroll == pytest.approx(101)
    assert len(table_working.players[0].bets) == 1


def test_betplace_skip_come_skips_matching_number_only():
    table = Table()
    strategy = BetPlace(
        {5: 10, 6: 12},
        mode=StrategyMode.ADD_IF_NOT_BET,
        skip_point=False,
        skip_come=True,
    )
    player = table.add_player(strategy=strategy)

    # Simulate an established Come bet on 5 so skip_come excludes only that number.
    player.bets.append(Come(10, number=5))

    TableUpdate().run_strategies(table)

    assert not any(isinstance(bet, Place) and bet.number == 5 for bet in player.bets)
    assert any(
        isinstance(bet, Place) and bet.number == 6 and bet.amount == 12
        for bet in player.bets
    )


@pytest.mark.parametrize(
    "strategy, expected_bankroll",
    [
        (BetBuy(4, 10, always_working=False), 90),
        (BetLay(5, 10, always_working=False), 90),
    ],
)
def test_betbuy_betlay_always_working_false_stays_inactive_on_comeout(
    strategy, expected_bankroll
):
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    table.settings["vig_paid_on_win"] = True
    table.add_player(strategy=strategy)
    table.fixed_run([(4, 3)], verbose=False)

    assert table.players[0].bankroll == pytest.approx(expected_bankroll)
    assert len(table.players[0].bets) == 1


def test_betcome_contract_bet_stays_working_on_comeout():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    table.add_player(strategy=BetCome(10))
    player = table.players[0]

    # Start with point on so BetCome strategy can place the bet.
    table.point.number = 4
    table.fixed_run([(3, 3)], verbose=False)  # travel Come to 6
    player.strategy = NullStrategy()
    table.fixed_run([(2, 2), (3, 3)], verbose=False)  # point hit, then come-out 6

    assert player.bankroll == pytest.approx(110)
    assert len(player.bets) == 0


def test_betdontcome_contract_bet_stays_working_on_comeout():
    table = Table()
    table.settings["come_out_working_policy"] = "real_casino"
    table.add_player(strategy=BetDontCome(10))
    player = table.players[0]

    # Start with point on so BetDontCome strategy can place the bet.
    table.point.number = 4
    table.fixed_run([(2, 3)], verbose=False)  # travel Don't Come to 5
    player.strategy = NullStrategy()
    table.fixed_run([(2, 2), (3, 4)], verbose=False)  # point hit, then come-out 7

    assert player.bankroll == pytest.approx(110)
    assert len(player.bets) == 0
