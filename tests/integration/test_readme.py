import crapssim as craps
import crapssim.strategy.examples
import crapssim.strategy.odds
import crapssim.strategy.simple_bet


def test_first_chunk():
    table = craps.Table()
    your_strat = crapssim.strategy.examples.BetPassLine(5) + \
                 crapssim.strategy.odds.PassLineOddsMultiplier(2)

    table.add_player(strategy=your_strat)
    table.run(max_rolls=20, verbose=False)


def test_second_chunk():
    n_sim = 10
    bankroll = 300
    strategies = {
        "place68": crapssim.strategy.examples.PassLinePlace68(5),
        # "ironcross": craps.strategy.ironcross
    }

    for i in range(n_sim):
        table = craps.Table()
        for s in strategies:
            table.add_player(strategy=strategies[s], name=s)

        table.run(max_rolls=float("inf"), max_shooter=10, verbose=False)
        for p in table.players:
            print(f"{i}, {p.strategy}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")
