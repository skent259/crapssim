import typing

from crapssim.bet import Bet, Come, DontCome, DontPass, Odds, PassLine, Put
from crapssim.strategy.tools import Player, Strategy, Table


def _expand_multiplier_dict(multiplier):
    """Helper function to expand a multiplier dictionary to include all
    possible point numbers (4, 5, 6, 8, 9, 10) if not already present.

    Args:
        multiplier: A dictionary of point numbers and their associated
            multipliers or a float to be applied to all point numbers.
    """
    if isinstance(multiplier, typing.SupportsFloat):
        return {x: multiplier for x in (4, 5, 6, 8, 9, 10)}
    else:
        return multiplier


def _condense_multiplier_dict(
    multiplier: dict[int, typing.SupportsFloat],
) -> typing.SupportsFloat | dict[int, typing.SupportsFloat]:
    """Helper function to condense a multiplier dictionary to a single
    float if all the multipliers are the same for all point numbers.
    Args:
        multiplier: A dictionary of point numbers and their associated
            multipliers.
    """
    all_mult_same = len(set(multiplier.values())) == 1
    mult_has_all_numbers = set(multiplier.keys()) == {4, 5, 6, 8, 9, 10}
    if all_mult_same and mult_has_all_numbers:
        return list(multiplier.values())[0]
    else:
        return multiplier


class OddsAmount(Strategy):
    """Strategy that takes places odds on a given number for a given bet type."""

    def __init__(
        self,
        base_type: typing.Type[PassLine | DontPass | Come | DontCome | Put],
        odds_amounts: dict[int, typing.SupportsFloat],
        always_working: bool = False,
    ):
        self.base_type = base_type
        """The bet that odds will be added to."""
        self.odds_amounts = odds_amounts
        self.always_working = always_working

    def completed(self, player: Player) -> bool:
        """Return True if there are no bets of base_type on the table.

        Parameters
        ----------
        player
            The player whose bets to check for.

        Returns
        -------
        True if there are no base type bets on the table, otherwise False.
        """
        return len([x for x in player.bets if isinstance(x, self.base_type)]) == 0

    def update_bets(self, player: Player) -> None:
        for number, amount in self.odds_amounts.items():
            bet = Odds(self.base_type, number, float(amount), self.always_working)
            if bet.is_allowed(player) and not player.already_placed(bet):
                player.add_bet(bet)

    def _get_always_working_repr(self) -> str:
        """Since the default is false, only need to print when True"""
        return (
            f", always_working={self.always_working})" if self.always_working else f")"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(base_type={self.base_type}, "
            f"odds_amounts={self.odds_amounts}"
            f"{self._get_always_working_repr()}"
        )


class _OddsAmount(OddsAmount):

    bet_type: type[PassLine | DontPass | Come | DontCome | Put]

    def __init__(
        self,
        bet_amount: typing.SupportsFloat,
        numbers: tuple[int] = (4, 5, 6, 8, 9, 10),
        always_working: bool = False,
    ):
        self.bet_amount = float(bet_amount)
        self.numbers = numbers
        super().__init__(
            self.bet_type, {x: bet_amount for x in numbers}, always_working
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(bet_amount={self.bet_amount}, numbers={self.numbers}"
            f"{self._get_always_working_repr()}"
        )


class PassLineOddsAmount(_OddsAmount):
    bet_type = PassLine


class DontPassOddsAmount(_OddsAmount):
    bet_type = DontPass


class ComeOddsAmount(_OddsAmount):
    bet_type = Come


class DontComeOddsAmount(_OddsAmount):
    bet_type = DontCome


class PutOddsAmount(_OddsAmount):
    bet_type = Put


class OddsMultiplier(Strategy):
    """Strategy that takes an AllowsOdds object and places Odds on it given either a multiplier,
    or a dictionary of points and multipliers."""

    def __init__(
        self,
        base_type: typing.Type[PassLine | DontPass | Come | DontCome | Put],
        odds_multiplier: dict[int, typing.SupportsFloat] | typing.SupportsFloat,
        always_working: bool = False,
    ):
        """Takes an AllowsOdds item (ex. PassLine, Come, DontPass) and adds a BaseOdds bet
        (either Odds or LayOdds) based on the odds_multiplier given.

        Parameters
        ----------
        base_type
            The bet that odds will be added to.
        odds_multiplier
            If odds_multiplier is a float, adds multiplier * base_bets amount to the odds.
            If the odds multiplier is a dictionary of floats, looks at the dictionary to
            determine what odds multiplier to use depending on the given point.
        """
        self.base_type = base_type
        self.always_working = always_working
        self.odds_multiplier = _expand_multiplier_dict(odds_multiplier)

    @staticmethod
    def get_point_number(bet: Bet, table: "Table"):
        if isinstance(bet, (PassLine, DontPass)):
            return table.point.number
        elif isinstance(bet, (Come, Put, DontCome)):
            return bet.number
        else:
            raise NotImplementedError

    def update_bets(self, player: Player) -> None:
        """Add an Odds bet to the given base_types in the amount determined by the odds_multiplier.

        Parameters
        ----------
        player
            The player to add the odds bet to.
        """
        for bet in [x for x in player.bets if isinstance(x, self.base_type)]:
            point = self.get_point_number(bet, player.table)

            if point in self.odds_multiplier:
                multiplier = self.odds_multiplier[point]
            else:
                return

            amount = bet.amount * multiplier
            OddsAmount(
                self.base_type, {point: amount}, self.always_working
            ).update_bets(player)

    def completed(self, player: Player) -> bool:
        """Return True if there are no bets of base_type on the table.

        Parameters
        ----------
        player
            The player whose bets to check for.

        Returns
        -------
        True if there are no base type bets on the table, otherwise False.
        """
        return len([x for x in player.bets if isinstance(x, self.base_type)]) == 0

    def _get_always_working_repr(self) -> str:
        """Since the default is false, only need to print when True"""
        return (
            f", always_working={self.always_working})" if self.always_working else f")"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(base_type={self.base_type}, "
            f"odds_multiplier={_condense_multiplier_dict(self.odds_multiplier)}"
            f"{self._get_always_working_repr()}"
        )


class _OddsMultiplier(OddsMultiplier):
    """Helper class which sets the bet_type for the specific odds multiplier strategies.

    Args:
        odds_multiplier: If odds_multiplier is an integer the bet amount is the PassLine bet amount *
            odds_multiplier.  If it's a dictionary it uses the PassLine bet's point to determine
            the multiplier. Defaults to {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3} which are 345x odds.
        always_working (bool): Whether the odds are working when the point is off.
    """

    bet_type: type[PassLine | DontPass | Come | DontCome | Put]
    default_multiplier: dict[int, typing.SupportsFloat] | typing.SupportsFloat

    def __init__(
        self,
        odds_multiplier: (
            dict[int, typing.SupportsFloat] | typing.SupportsFloat | None
        ) = None,
        always_working: bool = False,
    ):

        if odds_multiplier is None:
            odds_multiplier = self.default_multiplier
        super().__init__(self.bet_type, odds_multiplier, always_working)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"odds_multiplier={_condense_multiplier_dict(self.odds_multiplier)}"
            f"{self._get_always_working_repr()}"
        )


class PassLineOddsMultiplier(_OddsMultiplier):
    """Strategy that adds and Odds bet to the PassLine bet based on the
    specified multiplier."""

    bet_type = PassLine
    default_multiplier = {4: 3.0, 5: 4.0, 6: 5.0, 8: 5.0, 9: 4.0, 10: 3.0}


class DontPassOddsMultiplier(_OddsMultiplier):
    """Strategy that adds and Odds bet to the DontPass bet based on the
    specified multiplier."""

    bet_type = DontPass
    default_multiplier = 6.0


class ComeOddsMultiplier(_OddsMultiplier):
    """Strategy that adds and Odds bet to the Come bet based on the
    specified multiplier."""

    bet_type = Come
    default_multiplier = {4: 3.0, 5: 4.0, 6: 5.0, 8: 5.0, 9: 4.0, 10: 3.0}


class DontComeOddsMultiplier(_OddsMultiplier):
    """Strategy that adds and Odds bet to the DontCome bet based on the
    specified multiplier."""

    bet_type = DontCome
    default_multiplier = 6.0


class PutOddsMultiplier(_OddsMultiplier):
    """Strategy that adds and Odds bet to the Put bet based on the
    specified multiplier."""

    bet_type = Put
    default_multiplier = {4: 3.0, 5: 4.0, 6: 5.0, 8: 5.0, 9: 4.0, 10: 3.0}


class WinMultiplier(OddsMultiplier):
    """Strategy that takes an AllowsOdds object and places Odds on it given the
    multiplier that is desired to win (or a dictionary of numbers and win
    multipliers).

    Args:
        base_type: The bet that odds will be added to.
        win_multiplier: If win_multiplier is a float, adds amount so that
            multiplier * base_bets is the win amount for the odds.
            If the odds multiplier is a dictionary of floats, looks at the
            dictionary to determine what win multiplier to use
            depending on the given point.
        always_working (bool): Whether the odds are working when the point is off.
    """

    def __init__(
        self,
        base_type: typing.Type[PassLine | DontPass | Come | DontCome | Put],
        win_multiplier: dict[int, typing.SupportsFloat] | typing.SupportsFloat,
        always_working: bool = False,
    ):
        self.win_multiplier = _expand_multiplier_dict(win_multiplier)
        odds_multiplier = self._convert_win_to_odds_mult(self.win_multiplier, base_type)

        super().__init__(
            base_type=base_type,
            odds_multiplier=odds_multiplier,
            always_working=always_working,
        )

    def _convert_win_to_odds_mult(
        self,
        win_multiplier: dict[int, typing.SupportsFloat],
        base_type: typing.Type[PassLine | DontPass | Come | DontCome | Put],
    ):
        """
        Converts a win multiplier to an odds multiplier

        For example, for the Don't Pass bet with point of 4, if we want to win
        1x the bet, need to bet 2x odds. A win multiplier of 1.0 will return 2.0.
        The conversion is flipped for a lightside bet. For example, for the Pass
        Line, to win 1x the bet, need 0.5x odds only (note: some casinos won't
        let you have less than 1x odds at any point, but this function will not
        restrict things)
        """

        if base_type in (DontPass, DontCome):
            conversion = {4: 2.0, 5: 3 / 2, 6: 6 / 5, 8: 6 / 5, 9: 3 / 2, 10: 2}
        elif base_type in (PassLine, Come, Put):
            conversion = {4: 1 / 2, 5: 2 / 3, 6: 5 / 6, 8: 5 / 6, 9: 2 / 3, 10: 1 / 2}
        else:
            return None

        return {x: conversion[x] * mult for x, mult in win_multiplier.items()}

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(base_type={self.base_type}, "
            f"win_multiplier={_condense_multiplier_dict(self.win_multiplier)}"
            f"{self._get_always_working_repr()}"
        )


class _WinMultiplier(WinMultiplier):
    """Helper class which sets the bet_type for the specific win multiplier strategies.

    Args:
        win_multiplier: If win_multiplier is a float, adds amount so that
            multiplier * base_bets is the win amount for the odds.
            If the odds multiplier is a dictionary of floats, looks at the
            dictionary to determine what win multiplier to use
            depending on the given point.
        always_working (bool): Whether the odds are working when the point is off.
    """

    bet_type: type[PassLine | DontPass | Come | DontCome | Put]
    """The bet that odds will be added to."""
    default_multiplier: dict[int, typing.SupportsFloat] | typing.SupportsFloat
    """Win multiplier to use if none is specified."""

    def __init__(
        self,
        win_multiplier: (
            dict[int, typing.SupportsFloat] | typing.SupportsFloat | None
        ) = None,
        always_working: bool = False,
    ):

        if win_multiplier is None:
            win_multiplier = self.default_multiplier
        super().__init__(self.bet_type, win_multiplier, always_working)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"win_multiplier={_condense_multiplier_dict(self.win_multiplier)}"
            f"{self._get_always_working_repr()}"
        )


class PassLineWinMultiplier(_WinMultiplier):
    """Strategy that adds and Odds bet to the PassLine bet based on the
    specified win multiplier."""

    bet_type = PassLine
    default_multiplier = 6.0


class DontPassWinMultiplier(_WinMultiplier):
    """Strategy that adds and Odds bet to the DontPass bet based on the
    specified win multiplier."""

    bet_type = DontPass
    default_multiplier = {4: 3.0, 5: 4.0, 6: 5.0, 8: 5.0, 9: 4.0, 10: 3.0}


class ComeWinMultiplier(_WinMultiplier):
    """Strategy that adds and Odds bet to the Come bet based on the
    specified win multiplier."""

    bet_type = Come
    default_multiplier = 6.0


class DontComeWinMultiplier(_WinMultiplier):
    """Strategy that adds and Odds bet to the DontCome bet based on the
    specified win multiplier."""

    bet_type = DontCome
    default_multiplier = {4: 3.0, 5: 4.0, 6: 5.0, 8: 5.0, 9: 4.0, 10: 3.0}


class PutWinMultiplier(_WinMultiplier):
    """Strategy that adds and Odds bet to the Put bet based on the
    specified win multiplier."""

    bet_type = Put
    default_multiplier = 6.0
