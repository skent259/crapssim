import typing

from crapssim.bet import PassLine, DontPass, Come, DontCome, Odds, Bet
from crapssim.strategy import Strategy, IfBetNotExist, AggregateStrategy

if typing.TYPE_CHECKING:
    from crapssim import Player, Table


class OddsAmountStrategy(Strategy):
    """Strategy that takes places odds on a given number for a given bet type."""

    def __init__(self, base_type: typing.Type[PassLine | DontPass | Come | DontCome],
                 odds_amounts: dict[int, typing.SupportsFloat]):
        self.base_type = base_type
        self.odds_amounts = odds_amounts

    def completed(self, player: 'Player') -> bool:
        """Return True if there are no bets of base_type on the table.

        Parameters
        ----------
        player
            The player whose bets to check for.

        Returns
        -------
        True if there are no base type bets on the table, otherwise False.
        """
        return len([x for x in player.bets_on_table if isinstance(x, self.base_type)]) == 0


    def update_bets(self, player: 'Player') -> None:
        for number, amount in self.odds_amounts.items():
            bet = Odds(self.base_type, number, float(amount))
            if bet.allowed(player) and not bet.already_placed(player):
                player.add_bet(bet)


class LightSideOddsAmount(AggregateStrategy):
    def __init__(self, odds_amounts: dict[int, typing.SupportsFloat]):
        super().__init__(OddsAmountStrategy(PassLine, odds_amounts),
                         OddsAmountStrategy(Come, odds_amounts))


class DarkSideOddsAmount(AggregateStrategy):
    def __init__(self, odds_amounts: dict[int, typing.SupportsFloat]):
        super().__init__(OddsAmountStrategy(DontPass, odds_amounts),
                         OddsAmountStrategy(DontCome, odds_amounts))


class OddsMultiplierStrategy(Strategy):
    """Strategy that takes an AllowsOdds object and places Odds on it given either a multiplier,
    or a dictionary of points and multipliers."""

    def __init__(self, base_type: typing.Type[PassLine | DontPass | Come | DontCome],
                 odds_multiplier: dict[int, int] | int):
        """Takes an AllowsOdds item (ex. PassLine, Come, DontPass) and adds a BaseOdds bet
        (either Odds or LayOdds) based on the odds_multiplier given.

        Parameters
        ----------
        base_type
            The bet that odds will be added to.
        odds_multiplier
            If odds_multiplier is an integer adds multiplier * base_bets amount to the odds.
            If the odds multiplier is a dictionary of Integers looks at the dictionary to
            determine what odds multiplier to use depending on the given point.
        """
        self.base_type = base_type

        if isinstance(odds_multiplier, int):
            self.odds_multiplier = {x: odds_multiplier for x in (4, 5, 6, 8, 9, 10)}
        else:
            self.odds_multiplier = odds_multiplier

    @staticmethod
    def get_point_number(bet: Bet, table: 'Table'):
        if isinstance(bet, (PassLine, DontPass)):
            return table.point.number
        elif isinstance(bet, (Come, DontCome)):
            return bet.point.number
        else:
            raise NotImplementedError

    def update_bets(self, player: 'Player') -> None:
        """Add an Odds bet to the given base_types in the amount determined by the odds_multiplier.

        Parameters
        ----------
        player
            The player to add the odds bet to.
        """
        for bet in [x for x in player.bets_on_table if isinstance(x, self.base_type)]:
            point = self.get_point_number(bet, player.table)

            if point in self.odds_multiplier:
                multiplier = self.odds_multiplier[point]
            else:
                return

            amount = bet.amount * multiplier
            OddsAmountStrategy(self.base_type, {point: amount}).update_bets(player)

    def completed(self, player: 'Player') -> bool:
        """Return True if there are no bets of base_type on the table.

        Parameters
        ----------
        player
            The player whose bets to check for.

        Returns
        -------
        True if there are no base type bets on the table, otherwise False.
        """
        return len([x for x in player.bets_on_table if isinstance(x, self.base_type)]) == 0

    def get_odds_multiplier_repr(self) -> int | dict[int, int]:
        """If the odds_multiplier has multiple values return a dictionary with the values,
        if all the multipliers are the same return an integer of the multiplier."""
        if all([x == self.odds_multiplier[4] for x in self.odds_multiplier.values()]):
            odds_multiplier: int | dict[int, int] = self.odds_multiplier[4]
        else:
            odds_multiplier = self.odds_multiplier
        return odds_multiplier

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(base_type={self.base_type}, ' \
               f'odds_multiplier={self.get_odds_multiplier_repr()})'


class LightSideOddsMultiplier(AggregateStrategy):
    def __init__(self, odds_multiplier: dict[int, int] | int):
        super().__init__(OddsMultiplierStrategy(PassLine, odds_multiplier),
                         OddsMultiplierStrategy(Come, odds_multiplier))


class DarkSideOddsMultiplier(AggregateStrategy):
    def __init__(self, odds_multiplier: dict[int, int] | int):
        super().__init__(OddsMultiplierStrategy(DontPass, odds_multiplier),
                         OddsMultiplierStrategy(DontCome, odds_multiplier))
