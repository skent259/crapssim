# Supported Bets

The crapssim package includes all of the common bets for a craps table in the {mod}`crapssim.bet` module:

* PassLine, Come
* DontPass, DontCome
* Place, Buy, Lay, and Put on 4/5/6/8/9/10
* Field
* Prop bets: 
  * Any 7
  * Any Craps
  * Two, Three, Yo (11), Boxcars (12)
  * CAndE (craps and 11), Horn, World
  * Hardways
  * Hop bets
* Big 6/8
* Side features: Fire, All/Tall/Small (ATS)

## Overview

Most bets take an `amount` (typically the cost of the bet) argument (e.g. 
`PassLine(5)` is a \$5 PassLine bet). Place bets, along with Buy, Lay, and 
Put bets, also need a `number` to be bet on (e.g. `Place(8, 12)` is a \$12 
Place bet on the 8). 

Some bets have options that can be specified in the {py:class}`~crapssim.table.TableSettings`, which is unique to each Table. 


### Odds bets

Odds bets need the `bet_type` in addition to the `amount` and `number`.
For example, `Odds(PassLine, 4, 10)` is a \$10 odds bet on the pass line, 
where the point is 4. 

The maximum odds allowable is defined by the `"max_odds"` and `"max_dont_odds"` option in TableSettings. The default is `{4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}` 
for `"max_odds"` on light-side bets (3-4-5x odds), and `{4: 6, 5: 6, 6: 6, 8: 6, 9: 6, 10: 6}` for `"max_dont_odds"` on dark-side bets (6x odds, which win 3-4-5x).
If you wanted 100x odds, you could use `{x: 100 for x in (4, 5, 6, 8, 9, 10)}`.


### Field bets

The field bet wins if 2/3/4/9/10/11/12 are rolled, but casinos have some variation 
in the payout. Commonly, the field pays 2x on 2/12 and 1x on everything else (5.56\% house edge). Sometimes, either the 2 or 12 will pay 3x instead (reduces the house edge to 2.78\%). 

This can be specified with the `"field_payouts"` option of the TableSettings, which expects a dictionary with all of the numbers and the payout ratio. The default is 
`{2: 2, 3: 1, 4: 1, 9: 1, 10: 1, 11: 1, 12: 2}`, which pays 2x on 2/12. For example, to have a 3x payout on the 2 instead, use `{2: 3, 3: 1, 4: 1, 9: 1, 10: 1, 11: 1, 12: 2}`.

### Buy/Lay bets and the vig (commission)

This simulator uses a fixed 5% commission for applicable bets (e.g., Buy/Lay). This is 5% of the **bet amount** for Buy bets, and 5% of the potential **win amount** for Lay bets, as per common practice. For example, a \$20 Buy bet on the 4 and a \$40 Lay bet on the 4 (which wins \$20) both have a \$1 vig. 

The `vig` is added to the bet `amount` to equal the bet's `cost`. 

**Buy/Lay commission policy in {py:class}`~crapssim.table.TableSettings`:**
- `vig_rounding` (`"none"`, `"ceil_dollar"`, `"nearest_dollar"` default)
- `vig_floor` (float dollars, default `0.0`)
- `vig_paid_on_win` (bool, default `False`)

**Rounding semantics in `vig_floor`**
- `"none"` will do no rounding, mimicking a bubble craps style. 
- `"ceil_dollar"` always rounds up to the next whole dollar (e.g. 1.25 rounds to 2).
- `"nearest_dollar"` rounds to the nearest dollar, and rounds up when the decimal is 0.5 (e.g. 2.5 rounds to 3).

The `vig_floor` setting is the minimum vig that will be charged, for example in a high-roller table with the lowest demonination of \$5, one could set the minimum vig to be $5. 

The `vig_paid_on_win` setting will determine whether to charge the vig after the bet wins (if `True`) or up-front when the bet is placed (if `False`). For example, if there is a \$20 buy bet on the 4, up-front cost is \$21 (\$1 vig) and a win will give the player \$60 = \$40 win + $20 bet cost. If the vig is paid on win, the up-front cost is \$20 and a win will give the player $59 = \$40 win + $20 bet cost - \$1 vig. 

## What if I want to change things?

### Calling a bet by a different name

If, for example, you love to call the prop bet on 12 as "Midnight" instead of "Boxcars", and you want to do this in your code as well, you can either import the bet under an alias, or define your own subclass.

```python
"""Import under an alias"""
from crapssim.bet import Boxcars as Midnight

my_bet = Midnight(1) # $1 bet on 12 in the next roll
# Note, bet will still print out as `Boxcars(amount=1.0)`
```

```python
"""Define custom subclass"""
from crapssim.bet import Boxcars

class Midnight(Boxcars):
    pass

my_bet = Midnight(1) # $1 bet on 12 in the next roll
# Prints out as `Mignight(amount=1.0)`
```

### Changing payouts when things are hardcoded

While the {py:class}`~crapssim.table.TableSettings` covers a lot of common options, 
it might not cover every option in a casino, especially for bet payouts. 

For example, the Yo (11) bet in crapssim has a fixed payout of 15 **to** 1, 
so winning a \$1 bet will give the player \$15 in winnings plus the \$1 
bet back. If your local casino pays 15 **for** 1 instead, i.e. \$15 in winnings
but not returning your bet back, for net \$14 payout ratio, you can modify 
bet into your own class and over-ride the attribute. Then you can define a 
corresponding single-bet strategy, like in {doc}`crapssim.strategy.single_bet`.

```python
from crapssim.bet import Yo 

class MyYo(Yo):
    payout_ratio: int = 14 # vs 15 in Yo

my_bet = MyYo(1)

class BetMyYo(BetSingle):
    """Place a Yo bet if none currently placed."""

    bet_type = MyYo

my_strategy = BetMyYo()
```



