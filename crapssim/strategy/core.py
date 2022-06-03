"""Core strategies are strategies that can be either subclassed, or initialized to create other
strategies with the intended usage. Each of the strategies included in this package are intended
to be used as building blocks when creating strategies."""

import typing
from abc import ABC, abstractmethod

from crapssim.bet import Bet, PassLine, Come
from crapssim.bet.pass_line import DontPass, DontCome, Odds, LayOdds

if typing.TYPE_CHECKING:
    from crapssim.table import Player


class Strategy(ABC):
    """ A Strategy is assigned to a player and determines what bets the player
    is going to make, remove, or change.
    """

    def after_roll(self, player: 'Player') -> None:
        """Method that can update the Strategy from the table/player after the dice are rolled but
        before the bets and the table are updated. For example, if you wanted to know whether the
        point changed from on to off you could do self.point_lost = table.point.status = "On" and
        table.dice.roll.total == 7. You couldn't do this in update_bets since the table has already
        been updated setting the point's status to Off.

        Parameters
        ----------
        player
            The Player to check for bets, etc.
        """

    def completed(self, player: 'Player') -> bool:
        """If True, the Strategy is completed and the Player stops playing. If False, the Player
        keeps playing the Strategy."""
        return False

    @abstractmethod
    def update_bets(self, player: 'Player') -> None:
        """Add, remove, or change the bets on the table.

        This method is applied after the dice are rolled,
        the bets are updated, and the table is updated."""

    def __add__(self, other: 'Strategy') -> "AggregateStrategy":
        return AggregateStrategy(self, other)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Strategy):
            return self.__class__ == other.__class__
        return NotImplemented

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'


class AggregateStrategy(Strategy):
    """A combination of multiple strategies."""

    def __init__(self, *strategies: Strategy):
        """A combination of multiple strategies. Strategies are applied in the order that is given.

        Parameters
        ----------
        strategies
            The strategies to combine to make the new strategy.
        """
        self.strategies = strategies

    def update_bets(self, player: 'Player') -> None:
        """Go through each of the strategies and run its update_bets method if the strategy has
        not been completed.

        Parameters
        ----------
        player
            The player to update the bets for.
        """
        for strategy in self.strategies:
            if not strategy.completed(player):
                strategy.update_bets(player)

    def completed(self, player: 'Player') -> bool:
        """Returns True if all of the strategies in the AggregateStrategy are completed.

        Parameters
        ----------
        player
            The Player to check the strategy for.

        Returns
        -------
        A boolean representing whether the given strategy

        """
        return all(x.completed(player) for x in self.strategies)

    def __repr__(self) -> str:
        repr_strategies = [repr(x) for x in self.strategies]
        return f'{" + ".join(repr_strategies)}'


class BetIfTrue(Strategy):
    """Strategy that places a bet if a given key taking Player as a parameter is True."""

    def __init__(self, bet: Bet, key: typing.Callable[['Player'], bool]):
        """The strategy will place the given bet if the given key is True.

        Parameters
        ----------
        bet
            The Bet to place if key is True.
        key
            Callable with parameters of player and table
            returning a boolean to decide whether to place the bet.
        """

        super().__init__()
        self.bet = bet
        self.key = key

    def update_bets(self, player: 'Player') -> None:
        """If the key is True add the bet to the player and table.

        Parameters
        ----------
        player
            The Player to add the bet for.
        """
        print(player.bets_on_table, self.bet)
        if self.key(player):
            player.add_bet(self.bet)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet={self.bet}, ' \
               f'key={self.key})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Strategy):
            return isinstance(other, type(self)) and self.bet == other.bet
        raise NotImplementedError


class RemoveIfTrue(Strategy):
    """Strategy that removes all bets that are True for a given key. The key takes the Bet and the
     Player as parameters."""
    def __init__(self, key: typing.Callable[['Bet', 'Player'], bool]):
        """The strategy will remove all bets that are true for the given key.

        Parameters
        ----------
        key
            Callable with parameters of bet and player return True if the bet should be removed
            otherwise returning False.
        """
        super().__init__()
        self.key = key

    def update_bets(self, player: 'Player') -> None:
        """For each of the players bets if the key is True remove the bet from the table.

        Parameters
        ----------
        player
            The Player to remove the bets for.
        """
        bets_to_remove = []
        for bet in player.bets_on_table:
            if self.key(bet, player):
                bets_to_remove.append(bet)
        for bet in bets_to_remove:
            player.remove_bet(bet)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(key={self.key})'


class ReplaceIfTrue(Strategy):
    """Strategy that iterates through the bets on the table and if the given key is true, replaces
    the bet with the given bet."""
    def __init__(self, bet: Bet, key: typing.Callable[[Bet, 'Player'], bool]):
        self.key = key
        self.bet = bet

    def update_bets(self, player: 'Player') -> None:
        """Iterate through each bet for the player and if the self.key(bet, player) is True, remove
        the bet and replace it with self.bet.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        for bet in player.bets_on_table:
            if self.key(bet, player):
                player.remove_bet(bet)
                player.add_bet(self.bet)


class IfBetNotExist(BetIfTrue):
    """Strategy that adds a bet if it isn't on the table for that player. Equivalent of
    BetIfTrue(bet, lambda p: bet not in p.bets_on_table)"""

    def __init__(self, bet: Bet):
        """The strategy adds the given bet object to the table if it is not already on the table.

        Parameters
        ----------
        bet
            The bet to add if it isn't already on the table.
        """
        super().__init__(bet, lambda p: bet not in p.bets_on_table)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet={self.bet})'


class BetPointOff(BetIfTrue):
    """Strategy that adds a bet if the table point is Off, and the Player doesn't have a bet on the
    table. Equivalent to BetIfTrue(bet, lambda p: p.table.point.status == "Off"
                                        and bet not in p.bets_on_table)"""
    def __init__(self, bet: Bet):
        """Adds the given bet if the table point is Off and the player doesn't have that bet on the
        table.

        Parameters
        ----------
        bet
            The bet to add if the point is Off.
        """
        super().__init__(bet,
                         lambda p: p.table.point.status == "Off" and bet not in p.bets_on_table)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet={self.bet})'


class BetPointOn(BetIfTrue):
    """Strategy that adds a bet if the table point is On, and the Player doesn't have a bet on the
    table. Equivalent to BetIfTrue(bet, lambda p: p.table.point.status == "On"
                                        and bet not in p.bets_on_table)"""
    def __init__(self, bet: Bet):
        """Add a bet if the point is On.

        Parameters
        ----------
        bet
            The bet to add if the point is On.
        """
        super().__init__(bet, lambda p: p.table.point.status == "On" and bet not in p.bets_on_table)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet={self.bet})'


class CountStrategy(BetIfTrue):
    """Strategy that checks how many bets exist of a certain type. If the number of bets of that
    type is less than the given count, it places the bet (if the bet isn't already on the table.)"""
    def __init__(self, bet_type: typing.Type[Bet] | tuple[typing.Type[Bet], ...],
                 count: int,
                 bet: Bet):
        """If there are less than count number of bets placed by player with a given bet_type, it
        adds the given bet.

        Parameters
        ----------
        bet_type
            The types of bets to count.
        count
            How many of the bets to check against.
        bet
            The bet to place if there are less than count bets of a given type.
        """
        self.bet_type = bet_type
        self.count = count

        super().__init__(bet, key=self.key)

    def key(self, player: "Player") -> bool:
        return self.less_than_count_bets_of_type(player) and self.bet_is_not_on_table(player)

    def bet_is_not_on_table(self, player) -> bool:
        return self.bet not in player.bets_on_table

    def less_than_count_bets_of_type(self, player):
        return self.get_bets_of_type_count(player) < self.count

    def get_bets_of_type_count(self, player):
        return len(player.get_bets_by_type(bet_type=self.bet_type))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_type={self.bet_type}, count={self.count}, ' \
               f'bet={self.bet})'


class RemoveByType(RemoveIfTrue):
    """Remove any bets that are of the given type(s)."""
    def __init__(self, bet_type: typing.Type[Bet] | tuple[typing.Type[Bet], ...]):
        super().__init__(lambda b, p: isinstance(b, bet_type))


class OddsStrategy(Strategy):
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

    def update_bets(self, player: 'Player') -> None:
        """Add an Odds bet to the given base_types in the amount determined by the odds_multiplier.

        Parameters
        ----------
        player
            The player to add the odds bet to.
        """
        for bet in player.bets_on_table:
            if isinstance(bet, self.base_type):
                if isinstance(bet, (PassLine, DontPass)):
                    point = player.table.point.number
                elif isinstance(bet, (Come, DontCome)):
                    point = bet.point
                else:
                    raise NotImplementedError

                if point in self.odds_multiplier:
                    multiplier = self.odds_multiplier[point]
                else:
                    return

                amount = bet.bet_amount * multiplier
                odds_bet = bet.get_odds_bet(amount, player.table)
                IfBetNotExist(odds_bet).update_bets(player)

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


class OddsAmountStrategy(Strategy):
    def __init__(self, base_type: typing.Type[PassLine | DontPass | Come | DontCome],
                 odds_amounts: dict[int, typing.SupportsFloat]):
        self.base_type = base_type
        self.odds_amounts = odds_amounts

    def get_bet_type(self):
        print(self.base_type)
        if issubclass(self.base_type, (PassLine, Come)):
            return Odds
        elif issubclass(self.base_type, (DontPass, DontCome)):
            return LayOdds
        else:
            raise NotImplementedError

    def update_bets(self, player: 'Player') -> None:
        for number, amount in self.odds_amounts.items():
            bet = self.get_bet_type()(number, amount)
            if bet.allowed(player) and not bet.already_placed(player):
                player.add_bet(bet)
