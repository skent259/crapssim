# :game_die::chart_with_upwards_trend: crapssim

A python package to run all of the necessary elements of a Craps table.  The package follows some natural logic: 

- a `CrapsTable` has `Player`(s) and `Dice` on it
- the `Player`(s) have `Bet`(s) on the `CrapsTable` as prescribed by their strategies.  

With these building blocks, crapssim supports 

- running **1 session** with **1 player/strategy** to test a realistic day at the craps table,
- running **many sessions** with **1 player/strategy** to understand how a strategy performs in the long term, or
- running **many sessions** with **many players/strategies** to simulate how they compare to each other

These powerful options can lead to some unique analysis of the game of craps, such as the following figure comparing 4 strategies with a budget of $200:

![best-budget-strategies](https://user-images.githubusercontent.com/41379385/109597132-404bc280-7add-11eb-848c-1981d57d100a.png)

## Results

I will post results from this simulator on my site: http://pages.stat.wisc.edu/~kent/blog.  

Current blog posts include:
- [5 Systems to Try at the Craps Table](http://pages.stat.wisc.edu/~kent/blog/2021.02.22/five_craps_systems.html)
- [Craps: Best Strategies on a Budget](http://pages.stat.wisc.edu/~kent/blog/2019.07.31_Craps_Budget/craps_best-strategies-on-a-budget.html)
- [All Bets Are Off: Re-learning the Pass Line Bet in Craps](http://pages.stat.wisc.edu/~kent/blog/2019.02.28_Craps_Passline/passline-and-odds.html)

## Installation

You can install crapssim with

```python
pip install crapssim
```

This requires Python >=3.6 and pip to be installed on your computer.

## Getting Started

To see how a single session might play out for you using a pass line bet with double odds, over 20 rolls, one might run:

```python
import crapssim as craps

table = craps.Table()
your_strat = craps.strategy.passline_odds2
you = craps.Player(bankroll=200, bet_strategy=your_strat)

table.add_player(you)
table.run(max_rolls=20)
```

To evaluate a couple of strategies across many table sessions, you can run:

```python
import crapssim as craps

n_sim = 20
bankroll = 300
strategies = {
    "place68": craps.strategy.place68,
    "ironcross": craps.strategy.ironcross
}

for i in range(n_sim):
    table = craps.Table()
    for s in strategies:
        table.add_player(craps.Player(bankroll, strategies[s], s))

    table.run(max_rolls=float("inf"), max_shooter=10, verbose=False)
    for s in strategies:
        print(f"{i}, {s}, {table.get_player(s).bankroll}, {bankroll}, {table.dice.n_rolls}")
```

For more advanced strategies, you need to write a custom function that can perform the strategy.  Some building blocks and examples can be found in [strategy.py](./crapssim/strategy.py)

## Contributing 

If you discover something interesting using this simulator, please let me know so that I can highlight those results here.  You can find me at skent259@gmail.com.

Those looking to contribute to this project are welcome to do so.  Currently, the top priority is to improve

- Supported bets (see [bet.py](./crapssim/bet.py))
- Supported strategies (see [strategy.py](./crapssim/strategy.py))
- Documentation



