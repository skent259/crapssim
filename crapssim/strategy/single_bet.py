"""Strategies that place a given bet if that bet of that type isn't currently placed and the bet
is allowed."""

import enum
import typing

from crapssim.bet import (
    Any7,
    Bet,
    Boxcars,
    Come,
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
from crapssim.strategy.tools import (
    AddIfNewShooter,
    AddIfNotBet,
    AddIfPointOff,
    AddIfPointOn,
    AddIfTrue,
    Player,
    RemoveIfPointOff,
    RemoveIfTrue,
    Strategy,
)


class StrategyMode(enum.Enum):
    ADD_IF_NOT_BET = enum.auto()
    ADD_IF_POINT_OFF = enum.auto()
    ADD_IF_POINT_ON = enum.auto()
    ADD_IF_NEW_SHOOTER = enum.auto()
    ADD_OR_INCREASE = enum.auto()
    BET_IF_POINT_ON = enum.auto()
    REPLACE = enum.auto()


class _BaseSingleBet(Strategy):
    def __init__(
        self,
        bet: Bet,
        mode: StrategyMode = StrategyMode.ADD_IF_NOT_BET,
    ):
        super().__init__()
        self.bet = bet
        self.mode = mode

    def completed(self, player: Player) -> bool:
        return player.bankroll < self.bet.amount and len(player.bets) == 0

    def update_bets(self, player: Player) -> None:
        if not self.bet.is_allowed(player):
            return

        match self.mode:
            case StrategyMode.ADD_IF_NOT_BET:
                AddIfNotBet(self.bet).update_bets(player)
            case StrategyMode.ADD_IF_POINT_ON:
                AddIfPointOn(self.bet).update_bets(player)
            case StrategyMode.ADD_IF_POINT_OFF:
                AddIfPointOff(self.bet).update_bets(player)
            case StrategyMode.ADD_IF_NEW_SHOOTER:
                AddIfNewShooter(self.bet).update_bets(player)
            case StrategyMode.ADD_OR_INCREASE:
                player.add_bet(self.bet)
            case StrategyMode.BET_IF_POINT_ON:
                AddIfPointOn(self.bet).update_bets(player)
                # If only betting when point on, also need to turn off when point off
                RemoveIfPointOff(self.bet).update_bets(player)
            case StrategyMode.REPLACE:
                existing_bets = player.already_placed_bets(self.bet)
                for bet in existing_bets:
                    player.remove_bet(bet)
                player.add_bet(self.bet)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(bet_amount={self.bet.amount},"
            f" mode={self.mode})"
        )


class BetPlace(Strategy):
    """Strategy that makes multiple Place bets of given amounts. It can also skip making the bet
    if the point is the same as the given bet number."""

    def __init__(
        self,
        place_bet_amounts: dict[int, float],
        mode: StrategyMode = StrategyMode.BET_IF_POINT_ON,
        skip_point: bool = True,
        skip_come: bool = False,
    ):
        """Strategy for making multiple place bets.

        Parameters
        ----------
        place_bet_amounts
            Dictionary of the point to make the Place bet on and the amount of the
            place bet to make.
        skip_point
            If True don't make the bet on the given Place if that's the number the tables Point
            is on.
        skip_come
            If True don't make the bet on the given Place if there is a Come bet with that Point
            already on that number.
        """
        super().__init__()
        self.place_bet_amounts = place_bet_amounts
        self.mode = mode
        self.skip_point = skip_point
        self.skip_come = skip_come

    def completed(self, player: Player) -> bool:
        """The strategy is completed if the player can no longer make any of the place bets in the
        place_bet_amounts dictionary and there are no Place bets on the table.

        Parameters
        ----------
        player
            The player to check the bankroll for

        Returns
        -------
        True if there are no Place bets on the table and the player can't make any more Place bets
        because their bankroll is too low.
        """
        return (
            player.bankroll < min(x for x in self.place_bet_amounts.values())
            and len([x for x in player.bets if isinstance(x, Place)]) == 0
        )

    def update_bets(self, player: Player) -> None:
        """Add the place bets on the numbers and amounts defined by place_bet_amounts.

        Parameters
        ----------
        player
            The player to add the place bets to.
        """
        if self.skip_point:
            self.remove_point_bet(player)

        for number, amount in self.place_bet_amounts.items():
            if self.skip_point and number == player.table.point.number:
                continue
            if self.skip_come:
                come_numbers = [
                    x.point.number for x in player.bets if isinstance(x, Come)
                ]
                if number in come_numbers:
                    continue
            _BaseSingleBet(Place(number, amount), mode=self.mode).update_bets(player)

    @staticmethod
    def remove_point_bet(player: Player) -> None:
        """If skip_point is true and the player has a place bet for the table point number,
        remove the Place bet.

        Parameters
        ----------
        player
            The player to check and see if they have the given bet.
        """
        point = player.table.point.number
        RemoveIfTrue(
            lambda b, p: isinstance(b, Place) and b.number == point
        ).update_bets(player)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(place_bet_amounts={self.place_bet_amounts},"
            f" mode={self.mode},"
            f" skip_point={self.skip_point}, skip_come={self.skip_come})"
        )


class BetPassLine(_BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_POINT_OFF,
    ):
        super().__init__(PassLine(bet_amount), mode=mode)


class BetDontPass(_BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_POINT_OFF,
    ):
        super().__init__(DontPass(bet_amount), mode=mode)


class BetCome(_BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_POINT_ON,
    ):
        super().__init__(Come(bet_amount), mode=mode)


class BetDontCome(_BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_POINT_ON,
    ):
        super().__init__(DontCome(bet_amount), mode=mode)


class BetHardWay(_BaseSingleBet):
    def __init__(
        self,
        number: tuple[int],
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_NOT_BET,
    ):
        if number not in [4, 6, 8, 10]:
            raise NotImplementedError
        self.number = number
        super().__init__(HardWay(number, bet_amount), mode=mode)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.number}, bet_amount={self.bet.amount},"
            f" mode={self.mode})"
        )


class BetField(_BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_NOT_BET,
    ):
        super().__init__(Field(bet_amount), mode=mode)


class BetAny7(_BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_NOT_BET,
    ):
        super().__init__(Any7(bet_amount), mode=mode)


class BetTwo(_BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_NOT_BET,
    ):
        super().__init__(Two(bet_amount), mode=mode)


class BetThree(_BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_NOT_BET,
    ):
        super().__init__(Three(bet_amount), mode=mode)


class BetYo(_BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_NOT_BET,
    ):
        super().__init__(Yo(bet_amount), mode=mode)


class BetBoxcars(_BaseSingleBet):
    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        mode=StrategyMode.ADD_IF_NOT_BET,
    ):
        super().__init__(Boxcars(bet_amount), mode=mode)


class BetFire(_BaseSingleBet):
    def __init__(self, bet_amount: float, mode=StrategyMode.ADD_IF_NOT_BET):
        super().__init__(Fire(bet_amount), mode=mode)
