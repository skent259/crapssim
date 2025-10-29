# :game_die::chart_with_upwards_trend: crapssim
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

For more advanced strategies, you can either write your own custom `Strategy` class or add strategy components together. To see the many possibilities, start with the tutorials on documentation site: 

* [Tutorial 1: Starting off with strategies](https://skent259.github.io/crapssim/tutorial-strategy-01.html). 

## Installation

For a normal user, it is recommended to install the official release. You will 
need an installation of python version 3.10 or newer.  Then, run the following 
code in your terminal: 

```python
pip install crapssim
```

Development installation instructions are [also available](./docs/installation.md).

## Results

Some results from this simulator have been posted to http://pages.stat.wisc.edu/~kent/blog:
- [One Surprising Feature of Dark Side Betting](https://pages.stat.wisc.edu/~kent/blog/2021.10.24/dark-side-surprises.html)
- [5 Systems to Try at the Craps Table](http://pages.stat.wisc.edu/~kent/blog/2021.02.22/five_craps_systems.html)
- [Craps: Best Strategies on a Budget](http://pages.stat.wisc.edu/~kent/blog/2019.07.31_Craps_Budget/craps_best-strategies-on-a-budget.html)
- [All Bets Are Off: Re-learning the Pass Line Bet in Craps](http://pages.stat.wisc.edu/~kent/blog/2019.02.28_Craps_Passline/passline-and-odds.html)


## Supported Bets (high level)

- Line & numbers: Pass Line, Come, **Put**, Place (4/5/6/8/9/10), Odds (PL/Come/**Put**)

- Dark side: Don’t Pass, Don’t Come, Odds (DP/DC), **Lay** (4/5/6/8/9/10)
- Field & props: Field, **Horn**, **World (Whirl)**, Any 7, Any Craps, 2/3/11/12, Hardways, Hop
- Side features: Fire, All/Tall/Small (ATS), **Big 6**, **Big 8**

### Commission

This simulator uses a fixed 5% commission for applicable bets (e.g., Buy/Lay) to match common table practice. The rate is not configurable.

Commission is applied by the bet implementation (current default: applied to the potential win).

**Horn / World modeling:**  
These are implemented as *net single-wager equivalents* of equal-split sub-bets (Horn across 2/3/11/12; World adds Any 7 break-even). This keeps payouts explicit and avoids sub-bet bookkeeping.

**Buy/Lay commission policy (optional keys):**
- `commission_mode` (`"on_win"` default, or `"on_bet"`)
- `commission_rounding` (`"none"` default, `"ceil_dollar"`, `"nearest_dollar"`)
- `commission_floor` (float dollars, default `0.0`)

**Rounding semantics**
- `nearest_dollar` uses Python’s standard rounding (`round`) which is banker's rounding.
  Ties (e.g., 2.5) round to the nearest even integer.
- `ceil_dollar` always rounds up to the next whole dollar.

| Scenario                         | Settings                                                                  | Effect (conceptual)                            |
|----------------------------------|---------------------------------------------------------------------------|-----------------------------------------------|
| Default explicit mode            | `commission_mode="on_win"`, `commission_rounding="none"` | Commission = 5% of gross win                  |
| On-bet with rounding + floor     | `commission_mode="on_bet"`, `commission_rounding="ceil_dollar"`, `commission_floor=25.0` | Fee is 5% of bet, rounded up, waived < $25 |

### Examples

See `crapssim/strategy/examples.py` for:
- QuickProps (World + Big6/Big8)
- BuySampler (Buy 4/10)
- LaySampler (Lay 5/9)
- PutWithOdds (Put on 6 with odds)
- HornShowcase (Horn + World)

### Running examples
A deterministic demo script is provided:

```bash
python -m examples.run_examples
```

This script exercises the new bets (Horn, World, Big6/Big8, Buy/Lay, Put with odds)
over a fixed roll sequence for reproducible behavior.


## Contributing

If you discover something interesting using this simulator, please let me know so that I can highlight those results here.  You can find me at skent259@gmail.com.

Those looking to contribute to this project are welcome to do so.  Currently, the top priority is to improve

- Supported bets (see [bet.py](https://github.com/skent259/crapssim/blob/main/crapssim/bet.py))
- Supported strategies (see [strategy](https://github.com/skent259/crapssim/tree/main/crapssim/strategy))
- Documentation




### Developer Documentation
See [`docs/VXP_METHODLOGY.md`](docs/VXP_METHODLOGY.md) for a full record of the Vanilla Expansion Project,
including design choices, validation methods, and audit results.


## Stress tests (optional)

A randomized torture test for new bets lives under `tests/stress/`.

- Quick smoke runs by default with `pytest -q`.
- Heavy stress is opt-in:

```bash
pytest -q -m stress
```
