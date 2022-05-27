"""Strategies that place a given bet if that bet of that type isn't currently placed and the bet
is allowed."""
import enum
import typing

from crapssim.strategy.core import OddsAmountStrategy, Strategy

from crapssim.bet import PassLine, DontPass, Bet, DontCome, Place, HardWay, Field, Three, Two, \
    Any7, Yo, Boxcars, Fire
from crapssim.strategy import BetIfTrue

if typing.TYPE_CHECKING:
    from crapssim.table import Player


class SimpleStrategyMode(enum.Enum):
    ADD_IF_NON_EXISTENT = enum.auto()
    ADD_OR_INCREASE = enum.auto()
    REPLACE = enum.auto()


class BaseSimpleBet(Strategy):
    def __init__(self, bet: Bet, mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__()
        self.bet = bet
        self.mode = mode

    def update_bets(self, player: 'Player') -> None:
        if not self.bet.allowed(player):
            return

        if self.mode == SimpleStrategyMode.ADD_IF_NON_EXISTENT:
            BetIfTrue(self.bet, lambda p: self.bet not in p.bets_on_table).update_bets(player)
        elif self.mode == SimpleStrategyMode.ADD_OR_INCREASE:
            player.add_bet(self.bet)
        elif self.mode == SimpleStrategyMode.REPLACE:
            existing_bets = self.bet.already_placed_bets(player)
            for bet in existing_bets:
                player.bets_on_table.remove(bet)
            player.add_bet(self.bet)


class PassLineAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(PassLine(bet_amount), mode=mode)


class PassLineOddsAmount(OddsAmountStrategy):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 numbers: tuple[int] = (4, 5, 6, 8, 9, 10)):
        super().__init__(PassLine, {x: bet_amount for x in numbers})


class DontPassAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(DontPass(bet_amount), mode=mode)


class DontPassOddsAmount(OddsAmountStrategy):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 numbers: tuple[int] = (4, 5, 6, 8, 9, 10)):
        super().__init__(DontPass(bet_amount), {x: bet_amount for x in numbers})


class ComeAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(DontCome(bet_amount), mode=mode)


class ComeOddsAmount(OddsAmountStrategy):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 numbers: tuple[int] = (4, 5, 6, 8, 9, 10)):
        super().__init__(DontPass, {x: bet_amount for x in numbers})


class DontComeAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(DontCome(bet_amount), mode=mode)


class DontComeOddsAmount(OddsAmountStrategy):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 numbers: tuple[int] = (4, 5, 6, 8, 9, 10)):
        super().__init__(DontCome, {x: bet_amount for x in numbers})


class Place4Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Place(4, bet_amount), mode=mode)


class Place5Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Place(5, bet_amount), mode=mode)


class Place6Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Place(6, bet_amount), mode=mode)


class Place8Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Place(8, bet_amount), mode=mode)


class Place9Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Place(9, bet_amount), mode=mode)


class Place10Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Place(10, bet_amount), mode=mode)


class Hard4Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(HardWay(4, bet_amount), mode=mode)


class Hard5Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(HardWay(5, bet_amount), mode=mode)


class Hard6Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(HardWay(6, bet_amount), mode=mode)


class Hard8Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(HardWay(8, bet_amount), mode=mode)


class Hard9Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(HardWay(9, bet_amount), mode=mode)


class Hard10Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(HardWay(10, bet_amount), mode=mode)


class FieldAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Field(bet_amount), mode=mode)


class Any7Amount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Any7(bet_amount), mode=mode)


class TwoAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Two(bet_amount), mode=mode)


class ThreeAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Three(bet_amount), mode=mode)


class YoAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Yo(bet_amount), mode=mode)


class BoxcarsAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Boxcars(bet_amount), mode=mode)


class FireAmount(BaseSimpleBet):
    def __init__(self, bet_amount: typing.SupportsFloat,
                 mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Fire(bet_amount), mode=mode)
