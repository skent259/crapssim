# crapssim

Simulator for craps with various betting strategies

## About

crapssim is a python package to run all of the necessary elements of a Craps table.  The package is designed to follow some natural logic: 

- a `CrapsTable` has `Player`(s) and `Dice` on it
- the `Player`(s) have `Bet`(s) on the `CrapsTable` as perscribed by their strategies.  

With these building blocks, crapssim supports 

- running one craps session with a single player strategy to see the results of each dice roll,
- simulating one strategy many times to understand how it performs in the long term,
- simulating multiple strategies against each other on the same table to see how they compare,
- and many more scenarios.

These powerful options can lead to unique analysis of the game of craps, such as the following figure comparing 4 strategies with a budget of $200:

![best-budget-strategies](https://user-images.githubusercontent.com/41379385/109597132-404bc280-7add-11eb-848c-1981d57d100a.png)

## Results

I will post results from this simulator on my personal site: http://pages.stat.wisc.edu/~kent/.  

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

To see how a single session might play out for you using a pass line bet with double odds, over 20 rolls, one might run

```python
import crapssim as cs

table = cs.CrapsTable()
your_strat = cs.strategy.passline_odds2
you = cs.Player(bankroll=200, bet_strategy=your_strat)
table._add_player(you)
table.run(max_rolls=20)
```
