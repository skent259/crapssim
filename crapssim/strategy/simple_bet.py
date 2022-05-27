"""Strategies that place a given bet if that bet of that type isn't currently placed and the bet
is allowed."""
import typing

from crapssim.strategy.core import OddsAmountStrategy

if typing.TYPE_CHECKING:
    pass

from crapssim.bet import PassLine, DontPass, Bet, DontCome, Place, HardWay, Field, Three, Two, Any7, \
    Yo, Boxcars, Fire
from crapssim.strategy import BetIfTrue

if typing.TYPE_CHECKING:
    pass


class BaseSimpleBet(BetIfTrue):
    def __init__(self, bet: Bet):
        def key(player):
            return bet.allowed(player) and bet not in player.bets_on_table
        super().__init__(bet, key)


class PassLineAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(PassLine(bet_amount))


class PassLineOddsAmount(OddsAmountStrategy):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 numbers: tuple[int] = (4, 5, 6, 8, 9, 10)):
        super().__init__(PassLine, {x: bet_amount for x in numbers})


class DontPassAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(DontPass(bet_amount))


class DontPassOddsAmount(OddsAmountStrategy):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 numbers: tuple[int] = (4, 5, 6, 8, 9, 10)):
        super().__init__(DontPass(bet_amount), {x: bet_amount for x in numbers})


class ComeAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(DontCome(bet_amount))


class ComeOddsAmount(OddsAmountStrategy):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 numbers: tuple[int] = (4, 5, 6, 8, 9, 10)):
        super().__init__(DontPass, {x: bet_amount for x in numbers})


class DontComeAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(DontCome(bet_amount))


class DontComeOddsAmount(OddsAmountStrategy):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 numbers: tuple[int] = (4, 5, 6, 8, 9, 10)):
        super().__init__(DontCome, {x: bet_amount for x in numbers})


class Place4Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Place(4, bet_amount))


class Place5Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Place(5, bet_amount))


class Place6Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Place(6, bet_amount))


class Place8Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Place(8, bet_amount))


class Place9Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Place(9, bet_amount))


class Place10Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Place(10, bet_amount))


class Hard4Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(HardWay(4, bet_amount))


class Hard5Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(HardWay(5, bet_amount))


class Hard6Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(HardWay(6, bet_amount))


class Hard8Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(HardWay(8, bet_amount))


class Hard9Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(HardWay(9, bet_amount))


class Hard10Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(HardWay(10, bet_amount))


class FieldAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Field(bet_amount))


class Any7Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Any7(bet_amount))


class TwoAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Two(bet_amount))


class ThreeAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Three(bet_amount))


class YoAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Yo(bet_amount))


class BoxcarsAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Boxcars(bet_amount))


class FireAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(Fire(bet_amount))
