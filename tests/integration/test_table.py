import os
from unittest.mock import MagicMock, call

import pytest

from crapssim import Table
from crapssim.strategy.odds import PassLineOddsMultiplier
from crapssim.strategy.single_bet import BetCome, BetPassLine, BetPlace


def test_table_print_output(capsys):

    output_file = os.path.join(".", "tests", "integration", "verified_table_output.txt")

    table = Table(seed=8)
    table.add_player(bankroll=100, strategy=BetPassLine(5) + PassLineOddsMultiplier(2))
    table.add_player(bankroll=1000, strategy=BetPlace({5: 10, 6: 12, 8: 12, 4: 10}))
    table.run(max_rolls=20, verbose=True)

    # Capture and check output
    captured = capsys.readouterr()

    # # Do this once if the output changes
    # with open(output_file, "w") as f:
    #     f.write(captured.out)

    with open(output_file, "r") as f:
        output_content = f.read().strip()

    assert captured.out.rstrip() == output_content


@pytest.mark.parametrize(
    "strategy", [BetPassLine(10) + BetCome(10), BetPlace({6: 12, 9: 10})]
)
def test_table_runout_comebets(strategy):
    table = Table(seed=9)
    table.add_player(bankroll=200, strategy=strategy)

    # Get some bets active
    table.run(max_rolls=4, runout=False)
    table.players[0].strategy.update_bets = MagicMock()
    # Only run strategy once
    table.run(max_rolls=1, runout=True)

    n_strategy_updates = table.players[0].strategy.update_bets.call_count
    assert (
        n_strategy_updates == 1
    ), "The strategy called `update_bets` more than one with 1 additional roll"
    assert table.dice.n_rolls > 5


@pytest.mark.parametrize(
    "strategy", [BetPassLine(10) + BetCome(10), BetPlace({6: 12, 9: 10})]
)
def test_table_without_runout_comebets(strategy):
    table = Table(seed=9)
    table.add_player(bankroll=200, strategy=strategy)

    table.run(max_rolls=5, runout=False)

    assert (
        table.dice.n_rolls == 5
    ), "Run stopped later than max_rolls even though runout=False"
