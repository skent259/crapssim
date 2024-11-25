import pytest

from crapssim import Table
from crapssim.bet import (
    Any7,
    Boxcars,
    Come,
    DontCome,
    DontPass,
    Field,
    Fire,
    HardWay,
    Odds,
    PassLine,
    Place,
    Three,
    Two,
    Yo,
)
from crapssim.strategy.single_bet import (
    BetAny7,
    BetBoxcars,
    BetFire,
    BetHardWay,
    BetThree,
    BetTwo,
    BetYo,
)
from crapssim.table import TableUpdate


@pytest.mark.parametrize(
    ["strategy", "rolls", "correct_bets"],
    [
        (BetHardWay(4, bet_amount=5), [], [HardWay(4, amount=5.0)]),
        (BetHardWay(6, bet_amount=5), [], [HardWay(6, amount=5.0)]),
        (BetHardWay(8, bet_amount=5), [], [HardWay(8, amount=5.0)]),
        (BetHardWay(10, bet_amount=5), [], [HardWay(10, amount=5.0)]),
        (BetAny7(bet_amount=5), [], [Any7(amount=5.0)]),
        (BetTwo(bet_amount=5), [], [Two(amount=5.0)]),
        (BetThree(bet_amount=5), [], [Three(amount=5.0)]),
        (BetYo(bet_amount=5), [], [Yo(amount=5.0)]),
        (BetBoxcars(bet_amount=5), [], [Boxcars(amount=5.0)]),
        (BetFire(bet_amount=5), [], [Fire(amount=5.0)]),
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
