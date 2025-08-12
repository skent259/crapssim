def test_first_chunk():
    import crapssim as craps
    from crapssim.strategy import BetPassLine, PassLineOddsMultiplier

    table = craps.Table()
    your_strat = BetPassLine(5) + PassLineOddsMultiplier(2)

    table.add_player(strategy=your_strat)
    table.run(max_rolls=20, verbose=True)


def test_second_chunk():
    import crapssim as craps

    n_sim = 20
    bankroll = 300
    strategies = {
        "place68": craps.strategy.examples.PassLinePlace68(5),
        "ironcross": craps.strategy.examples.IronCross(5),
    }

    for i in range(n_sim):
        table = craps.Table()
        for s in strategies:
            table.add_player(bankroll, strategy=strategies[s], name=s)

        table.run(max_rolls=float("inf"), max_shooter=10, verbose=False)

        for p in table.players:
            print(f"{i}, {p.name}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")
