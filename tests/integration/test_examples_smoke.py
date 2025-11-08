from crapssim.strategy.examples import (
    BuySampler,
    HornExample,
    LaySampler,
    PutWithOdds,
    QuickProps,
    WorldExample,
)
from crapssim.table import Table, TableUpdate


def _run(strategy, rolls):
    table = Table()
    player = table.add_player()
    player.strategy = strategy
    for die_one, die_two in rolls:
        TableUpdate.roll(table, fixed_outcome=(die_one, die_two))
    assert player.bankroll == player.bankroll  # finite; ensures no NaN/inf


def test_examples_smoke():
    rolls = [(3, 3), (4, 4), (4, 3), (1, 1), (2, 2)]
    _run(QuickProps(5.0, 10.0), rolls)
    _run(BuySampler(25.0), rolls)
    _run(LaySampler(30.0), rolls)
    _run(PutWithOdds(10.0, 2.0, True), rolls)
    _run(HornExample(4.0), rolls)
    _run(WorldExample(5.0), rolls)
