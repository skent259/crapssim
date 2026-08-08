
# crapssim
![PyPI](https://img.shields.io/pypi/v/crapssim)
![GitHub Repo stars](https://img.shields.io/github/stars/skent259/crapssim?style=social)

When playing craps in a casino, there are unlimited combinations of ways that that players can place their bets. But, with this freedom comes complexity, and players deserve to know how a strategy could perform in each session. The 'crapssim' package is designed answer these tough questions: What's a fun strategy involving multiple numbers where the house edge doesn't increase too much? What's the best amount of passline or don't pass odds for my bankroll? Does hedging my bet improve my net winnings? 

Crapssim is a python package which runs all of the necessary elements of a Craps table.  The package follows some natural logic: 

- a `Table` has `Player`(s) and `Dice` on it
- the `Player`(s) have `Bet`(s) on the `Table` 
- each `Player`'s `Strategy` can automatically set up `Bet`(s)

With these building blocks, crapssim supports 

- running **1 session** with **1 player/strategy** to test a realistic day at the craps table,
- running **many sessions** with **1 player/strategy** to understand how a strategy performs in the long term, or
- running **many sessions** with **many players/strategies** to simulate how they compare to each other

These powerful options can lead to some unique analysis of the game of craps, such as the following figure comparing 4 strategies with a budget of $200:

![best-budget-strategies](https://user-images.githubusercontent.com/41379385/109597132-404bc280-7add-11eb-848c-1981d57d100a.png)

## It's easy to get started

To see how a single session might play out for you using a pass line bet with double odds, over 20 rolls, one might run:

```python
import crapssim as craps
from crapssim.strategy import BetPassLine, PassLineOddsMultiplier

table = craps.Table()
your_strat = BetPassLine(5) + PassLineOddsMultiplier(2)

table.add_player(strategy=your_strat)
table.run(max_rolls=20, verbose=True)
```

To evaluate a couple of strategies across many table sessions, you can run:

```python
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
```

For more advanced strategies, you can either write your own custom `Strategy` class or add strategy components together.  Some building blocks and examples can be found in the [strategy](https://github.com/skent259/crapssim/tree/main/crapssim/strategy) module. We plan to have a more detailed tutorial and more strategy examples available soon.

## Installation

For a normal user, it is recommended to install the official release. You will 
need an installation of python version 3.10 or newer.  Then, run the following 
code in your terminal: 

```python
pip install crapssim
```

Development installation instructions are [also available](installation.md).


```{toctree}
:caption: Examples and Tutorials
:maxdepth: 2
:hidden:

Strategy Tutorial 1: Starting off <tutorial-strategy-01>
Sandbox <crapssim_sandbox>
```

```{toctree}
:caption: Documentation
:maxdepth: 2
:hidden:

Installation <installation>
Contributing <contributing>
Change Log <changelog>
Supported Bets <supported-bets>
```



## Indices and tables

```{eval-rst}
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```