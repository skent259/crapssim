import pytest
import crapssim as craps


def test_first_chunk():
    table = craps.Table()
    your_strat = craps.strategy.passline_odds2
    you = craps.Player(bankroll=200, bet_strategy=your_strat)

    table.add_player(you)
    table.run(max_rolls=20, verbose=False)


# def test_second_chunk():
#     n_sim = 10
#     bankroll = 300
#     strategies = {
#         "place68": craps.strategy.place68,
#         "ironcross": craps.strategy.ironcross
#     }
#
#     for i in range(n_sim):
#         table = craps.Table()
#         for s in strategies:
#             table.add_player(craps.Player(bankroll, strategies[s], s))
#
#         table.run(max_rolls=float("inf"), max_shooter=10, verbose=False)
#         for s in strategies:
#             print(f"{i}, {s}, {table.get_player(s).bankroll}, {bankroll}, {table.dice.n_rolls}")
