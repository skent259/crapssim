"""Strategies that place a given bet if that bet of that type isn't currently placed and the bet
is allowed."""
import typing

from crapssim.bet import PassLine, DontPass, Place
from crapssim.strategy import BetPointOff, Strategy, IfBetNotExist, OddsStrategy

if typing.TYPE_CHECKING:
    from crapssim.table import Player


class BetPassLine(BetPointOff):
    """Strategy that adds a PassLine bet if the point is Off and the player doesn't have a PassLine
    bet already on the table. Equivalent to BetPointOff(PassLine(bet_amount))."""
    def __init__(self, bet_amount: typing.SupportsFloat):
        """Adds a PassLine bet for the given bet_amount if the point is Off and the player doesn't
        have a PassLine bet for that amount already on the table.

        Parameters
        ----------
        bet_amount
            The amount of the PassLine bet.
        """
        self.bet_amount: float = float(bet_amount)
        super().__init__(PassLine(bet_amount))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount})'


class PassLineOdds(OddsStrategy):
    """Strategy that adds an Odds bet to the PassLine bet. Equivalent to
    OddsStrategy(PassLine, odds)."""
    def __init__(self, odds_multiplier: dict[int, int] | int | None = None):
        """Add odds to PassLine bets with the multiplier specified by the odds_multiplier variable.

        Parameters
        ----------
        odds_multiplier
            If odds_multiplier is an integer the bet amount is the PassLine bet amount *
            odds_multiplier.  If it's a dictionary it uses the PassLine bet's point to determine
            the multiplier. Defaults to {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3} which are 345x odds.
            """
        if odds_multiplier is None:
            odds_multiplier = {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
        super().__init__(PassLine, odds_multiplier)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(odds_multiplier={self.get_odds_multiplier_repr()})'


class BetDontPass(BetPointOff):
    """Strategy that adds a DontPass bet if the point is off and the player doesn't have a DontPass
    bet of the given amount already on the table.
    Equivalent to BetPointOff(DontPass(bet_amount))."""
    def __init__(self, bet_amount: float):
        """If the point is off and the player doesn't have a DontPass(bet_amount) bet on the table
        place a DontPass(bet_amount) bet.

        Parameters
        ----------
        bet_amount
            The amount of the DontPass bet to place.
        """
        self.bet_amount = bet_amount
        super().__init__(DontPass(bet_amount))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount})'


class BetDontPassOdds(OddsStrategy):
    """Strategy that adds a LayOdds bet to the DontPass bet. Equivalent to
    OddsStrategy(DontPass, odds)"""
    def __init__(self, odds_multiplier: dict[int, int] | int | None = None):
        """Add odds to DontPass bets with the multiplier specified by odds.

        Parameters
        ----------
        odds_multiplier
            If odds_multiplier is an integer the bet amount is the PassLine bet amount *
            odds_multiplier. If it's a dictionary it uses the PassLine bet's point to determine the
            multiplier. Defaults to 6.
        """
        if odds_multiplier is None:
            odds_multiplier = 6
        super().__init__(DontPass, odds_multiplier)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(odds_multiplier={self.get_odds_multiplier_repr()})'


class BetPlace(Strategy):
    """Strategy that makes multiple Place bets of given amounts. It can also skip making the bet
    if the point is the same as the given bet number."""
    def __init__(self, place_bet_amounts: dict[int, float], skip_point: bool = True):
        """Strategy for making multiple place bets.

        Parameters
        ----------
        place_bet_amounts
            Dictionary of the point to make the Place bet on and the amount of the
            place bet to make.
        skip_point
            If True don't make the bet on the given Place if that's the number the tables Point
            is on.
        """
        super().__init__()
        self.place_bet_amounts = place_bet_amounts
        self.skip_point = skip_point

    def update_bets(self, player: 'Player') -> None:
        """Add the place bets on the numbers and amounts defined by place_bet_amounts.

        Parameters
        ----------
        player
            The player to add the place bet to.
        """
        for number, amount in self.place_bet_amounts.items():
            if self.skip_point and number == player.table.point.number:
                continue
            if player.table.point.status == 'Off':
                continue
            IfBetNotExist(Place(number, amount)).update_bets(player)
        self.remove_point_bet(player)

    def remove_point_bet(self, player: "Player") -> None:
        """If skip_point is true and the player has a place bet for the table point number,
        remove the Place bet.

        Parameters
        ----------
        player
            The player to check and see if they have the given bet.
        """
        if self.skip_point and player.table.point.number in self.place_bet_amounts:
            bet_amount = self.place_bet_amounts[player.table.point.number]
            bet = Place(player.table.point.number, bet_amount)

            if bet in player.bets_on_table:
                player.remove_bet(bet)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(place_bet_amounts={self.place_bet_amounts},' \
               f' skip_point={self.skip_point})'

