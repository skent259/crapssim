import os

import pytest

from crapssim import Table
from crapssim.strategy.odds import PassLineOddsMultiplier
from crapssim.strategy.single_bet import BetPassLine, BetPlace


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
