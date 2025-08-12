import pytest

from crapssim import Table
from crapssim.bet import (
    All,
    Any7,
    Bet,
    Boxcars,
    Come,
    DontCome,
    DontPass,
    Field,
    Fire,
    HardWay,
    Hop,
    Odds,
    PassLine,
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
    BetBoxcars,
    BetFire,
    BetHardWay,
    BetHop,
    BetSmall,
    BetTall,
    BetThree,
    BetTwo,
    BetYo,
    StrategyMode,
)
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
