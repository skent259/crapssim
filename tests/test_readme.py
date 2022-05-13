import pytest
import crapssim as craps


def test_first_chunk():
    table = craps.Table()
    your_strat = craps.strategy.PassLineOdds(2)

    table.add_player(strategy=your_strat)
    table.run(max_rolls=20, verbose=False)


def test_second_chunk():
    n_sim = 10
    bankroll = 300
    strategies = {
        "place68": craps.strategy.PassLinePlace68(5),
        # "ironcross": craps.strategy.ironcross
    }

    for i in range(n_sim):
        table = craps.Table()
        for s in strategies:
            table.add_player(name=s, strategy=strategies[s])

        table.run(max_rolls=float("inf"), max_shooter=10, verbose=False)
        for s in strategies:
            print(f"{i}, {s}, {table.get_player(s).bankroll}, {bankroll}, {table.dice.n_rolls}")
