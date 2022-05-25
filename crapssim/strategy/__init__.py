"""
Strategies to be assigned to players on the Craps table. The strategy determines what bets the
player should make, remove, or change. Strategies are applied for the player to change the bets
after the previous bets and table have been updated.
"""

from crapssim.strategy.core import Strategy, AggregateStrategy, BetIfTrue, RemoveIfTrue, \
    IfBetNotExist, BetPointOff, BetPointOn, CountStrategy, PlaceBetAndMove

from crapssim.strategy.defaults import BetPassLine, OddsStrategy, PassLineOdds, \
    TwoCome, Pass2Come, BetPlace, PassLinePlace68, BetDontPass, BetLayOdds, Place68Move59, \
    PassLinePlace68Move59, Place682Come, IronCross, HammerLock, Risk12, Knockout, \
    FieldWinProgression, DiceDoctor, Place68CPR, Place68DontCome2Odds
