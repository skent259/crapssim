"""
Strategies to be assigned to players on the Craps table. The strategy determines what bets the
player should make, remove, or change. Strategies are applied for the player to change the bets
after the previous bets and table have been updated.
"""

from crapssim.strategy.odds import (
    ComeOddsMultiplier,
    DontComeOddsMultiplier,
    DontPassOddsMultiplier,
    OddsAmount,
    OddsMultiplier,
    PassLineOddsMultiplier,
)
from crapssim.strategy.single_bet import BetDontPass, BetPassLine, BetPlace
from crapssim.strategy.tools import (
    AddIfNewShooter,
    AddIfNotBet,
    AddIfPointOff,
    AddIfPointOn,
    AddIfTrue,
    AggregateStrategy,
    CountStrategy,
    RemoveIfPointOff,
    RemoveIfTrue,
    Strategy,
)

from . import examples, odds
