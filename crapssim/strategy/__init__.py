"""
Strategies to be assigned to players on the Craps table. The strategy determines what bets the
player should make, remove, or change. Strategies are applied for the player to change the bets
after the previous bets and table have been updated.
"""

from crapssim.strategy.core import (
    AggregateStrategy,
    BetIfTrue,
    BetPointOff,
    BetPointOn,
    CountStrategy,
    IfBetNotExist,
    RemoveIfTrue,
    Strategy,
)
from crapssim.strategy.odds import (
    DontPassOddsMultiplier,
    OddsMultiplierStrategy,
    PassLineOddsMultiplier,
)
from crapssim.strategy.single_bet import BetDontPass, BetPassLine, BetPlace
