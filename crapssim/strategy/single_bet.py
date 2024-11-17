"""Strategies that place a given bet if that bet of that type isn't currently placed and the bet
is allowed."""

import enum
import typing

from crapssim.bet import (
    Any7,
    Bet,
    Boxcars,
    DontCome,
    DontPass,
    Field,
    Fire,
    HardWay,
    PassLine,
    Place,
    Three,
    Two,
    Yo,
)
from crapssim.strategy import BetIfTrue
from crapssim.strategy.core import Player, Strategy
from crapssim.strategy.odds import OddsAmountStrategy


class SimpleStrategyMode(enum.Enum):
    ADD_IF_NON_EXISTENT = enum.auto()
    ADD_OR_INCREASE = enum.auto()
    REPLACE = enum.auto()


class BaseSingleBet(Strategy):
    def __init__(
        self,
        bet: Bet,
        mode: SimpleStrategyMode = SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__()
        self.bet = bet
        self.mode = mode

    def completed(self, player: Player) -> bool:
        return player.bankroll < self.bet.amount and len(player.bets) == 0

    def update_bets(self, player: Player) -> None:
        if not self.bet.is_allowed(player):
            return

        if self.mode == SimpleStrategyMode.ADD_IF_NON_EXISTENT:
            BetIfTrue(self.bet, lambda p: self.bet not in p.bets).update_bets(player)
        elif self.mode == SimpleStrategyMode.ADD_OR_INCREASE:
            player.add_bet(self.bet)
        elif self.mode == SimpleStrategyMode.REPLACE:
            existing_bets = player.already_placed_bets(self.bet)
            for bet in existing_bets:
                player.remove_bet(bet)
            player.add_bet(self.bet)


class PassLineAmount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(PassLine(bet_amount), mode=mode)


class PassLineOddsAmount(OddsAmountStrategy):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        numbers: tuple[int] = (4, 5, 6, 8, 9, 10),
    ):
        super().__init__(PassLine, {x: bet_amount for x in numbers})


class DontPassAmount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(DontPass(bet_amount), mode=mode)


class DontPassOddsAmount(OddsAmountStrategy):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        numbers: tuple[int] = (4, 5, 6, 8, 9, 10),
    ):
        super().__init__(DontPass, {x: bet_amount for x in numbers})


class ComeAmount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(DontCome(bet_amount), mode=mode)


class ComeOddsAmount(OddsAmountStrategy):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        numbers: tuple[int] = (4, 5, 6, 8, 9, 10),
    ):
        super().__init__(DontPass, {x: bet_amount for x in numbers})


class DontComeAmount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(DontCome(bet_amount), mode=mode)


class DontComeOddsAmount(OddsAmountStrategy):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        numbers: tuple[int] = (4, 5, 6, 8, 9, 10),
    ):
        super().__init__(DontCome, {x: bet_amount for x in numbers})


class Place4Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Place(4, bet_amount), mode=mode)


class Place5Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Place(5, bet_amount), mode=mode)


class Place6Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Place(6, bet_amount), mode=mode)


class Place8Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Place(8, bet_amount), mode=mode)


class Place9Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Place(9, bet_amount), mode=mode)


class Place10Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Place(10, bet_amount), mode=mode)


class Hard4Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(HardWay(4, bet_amount), mode=mode)


class Hard5Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(HardWay(5, bet_amount), mode=mode)


class Hard6Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(HardWay(6, bet_amount), mode=mode)


class Hard8Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(HardWay(8, bet_amount), mode=mode)


class Hard9Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(HardWay(9, bet_amount), mode=mode)


class Hard10Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(HardWay(10, bet_amount), mode=mode)


class FieldAmount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Field(bet_amount), mode=mode)


class Any7Amount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Any7(bet_amount), mode=mode)


class TwoAmount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Two(bet_amount), mode=mode)


class ThreeAmount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Three(bet_amount), mode=mode)


class YoAmount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Yo(bet_amount), mode=mode)


class BoxcarsAmount(BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT,
    ):
        super().__init__(Boxcars(bet_amount), mode=mode)


class FireAmount(BaseSingleBet):
    def __init__(self, bet_amount: float, mode=SimpleStrategyMode.ADD_IF_NON_EXISTENT):
        super().__init__(Fire(bet_amount), mode=mode)
