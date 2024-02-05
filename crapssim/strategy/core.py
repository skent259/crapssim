"""Core strategies are strategies that can be either subclassed, or initialized to create other
strategies with the intended usage. Each of the strategies included in this package are intended
to be used as building blocks when creating strategies."""

import typing
from abc import ABC, abstractmethod

from crapssim.bet import Bet

if typing.TYPE_CHECKING:
    from crapssim.table import Player


class Strategy(ABC):
    """A Strategy is assigned to a player and determines what bets the player
    is going to make, remove, or change.
    """

    def after_roll(self, player: "Player") -> None:
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

    @abstractmethod
    def completed(self, player: "Player") -> bool:
        """If True, the Strategy is completed and the Player stops playing. If False, the Player
        keeps playing the Strategy."""

    @abstractmethod
    def update_bets(self, player: "Player") -> None:
        """Add, remove, or change the bets on the table.

        This method is applied after the dice are rolled,
        the bets are updated, and the table is updated."""

    def __add__(self, other: "Strategy") -> "AggregateStrategy":
        return AggregateStrategy(self, other)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Strategy):
            return self.__class__ == other.__class__
        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


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

    def update_bets(self, player: "Player") -> None:
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

    def completed(self, player: "Player") -> bool:
        """Returns True if all the strategies in the AggregateStrategy are completed.

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

    def __init__(self, bet: Bet, key: typing.Callable[["Player"], bool]):
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

    def update_bets(self, player: "Player") -> None:
        """If the key is True add the bet to the player and table.

        Parameters
        ----------
        player
            The Player to add the bet for.
        """
        if self.key(player) and self.bet.is_allowed(player):
            player.add_bet(self.bet)

    def completed(self, player: "Player") -> bool:
        """The strategy is completed when the player  can't make a bet because their bankroll is too
         low and the player doesn't have any bets left on the table.

        Parameters
        ----------
        player
            The player to check whether the

        Returns
        -------
        True if the Player can't continue the strategy, otherwise False.
        """
        return (
            self.bet.amount > player.bankroll
            and sum(x.amount for x in player.bets) == 0
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bet={self.bet}, " f"key={self.key})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Strategy):
            return isinstance(other, type(self)) and self.bet == other.bet
        raise NotImplementedError


class RemoveIfTrue(Strategy):
    """Strategy that removes all bets that are True for a given key. The key takes the Bet and the
    Player as parameters."""

    def __init__(self, key: typing.Callable[["Bet", "Player"], bool]):
        """The strategy will remove all bets that are true for the given key.

        Parameters
        ----------
        key
            Callable with parameters of bet and player return True if the bet should be removed
            otherwise returning False.
        """
        super().__init__()
        self.key = key

    def update_bets(self, player: "Player") -> None:
        """For each of the players bets if the key is True remove the bet from the table.

        Parameters
        ----------
        player
            The Player to remove the bets for.
        """
        bets_to_remove = []
        for bet in player.bets:
            if self.key(bet, player):
                bets_to_remove.append(bet)
        for bet in bets_to_remove:
            player.remove_bet(bet)

    def completed(self, player: "Player") -> bool:
        """The strategy is completed when the player doesn't have any bets left on the table.

        Parameters
        ----------
        player
            The player to check whether the

        Returns
        -------
        True if the Player can't continue the strategy, otherwise False.
        """
        return sum(x.amount for x in player.bets) == 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(key={self.key})"


class ReplaceIfTrue(Strategy):
    """Strategy that iterates through the bets on the table and if the given key is true, replaces
    the bet with the given bet."""

    def __init__(self, bet: Bet, key: typing.Callable[[Bet, "Player"], bool]):
        self.key = key
        self.bet = bet

    def update_bets(self, player: "Player") -> None:
        """Iterate through each bet for the player and if the self.key(bet, player) is True, remove
        the bet and replace it with self.bet.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        for bet in player.bets:
            if self.key(bet, player):
                player.remove_bet(bet)
                player.add_bet(self.bet)

    def completed(self, player: "Player") -> bool:
        """The strategy is completed when the player  can't make a bet because their bankroll is too
         low and the player doesn't have any bets left on the table.

        Parameters
        ----------
        player
            The player to check whether the

        Returns
        -------
        True if the Player can't continue the strategy, otherwise False.
        """
        return (
            self.bet.amount > player.bankroll
            and sum(x.amount for x in player.bets) == 0
        )


class IfBetNotExist(BetIfTrue):
    """Strategy that adds a bet if it isn't on the table for that player. Equivalent of
    BetIfTrue(bet, lambda p: bet not in p.bets)"""

    def __init__(self, bet: Bet):
        """The strategy adds the given bet object to the table if it is not already on the table.

        Parameters
        ----------
        bet
            The bet to add if it isn't already on the table.
        """
        super().__init__(bet, lambda p: bet not in p.bets)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bet={self.bet})"


class BetPointOff(BetIfTrue):
    """Strategy that adds a bet if the table point is Off, and the Player doesn't have a bet on the
    table. Equivalent to BetIfTrue(bet, lambda p: p.table.point.status == "Off"
                                        and bet not in p.bets)"""

    def __init__(self, bet: Bet):
        """Adds the given bet if the table point is Off and the player doesn't have that bet on the
        table.

        Parameters
        ----------
        bet
            The bet to add if the point is Off.
        """
        super().__init__(
            bet, lambda p: p.table.point.status == "Off" and bet not in p.bets
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bet={self.bet})"


class BetPointOn(BetIfTrue):
    """Strategy that adds a bet if the table point is On, and the Player doesn't have a bet on the
    table. Equivalent to BetIfTrue(bet, lambda p: p.table.point.status == "On"
                                        and bet not in p.bets)"""

    def __init__(self, bet: Bet):
        """Add a bet if the point is On.

        Parameters
        ----------
        bet
            The bet to add if the point is On.
        """
        super().__init__(
            bet, lambda p: p.table.point.status == "On" and bet not in p.bets
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bet={self.bet})"


class CountStrategy(BetIfTrue):
    """Strategy that checks how many bets exist of a certain type. If the number of bets of that
    type is less than the given count, it places the bet (if the bet isn't already on the table.)
    """

    def __init__(
        self,
        bet_type: typing.Type[Bet] | tuple[typing.Type[Bet], ...],
        count: int,
        bet: Bet,
    ):
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
        """Return True if the player has less than count number of bets for a given type and the
        bet that is intended to be placed isn't already on the table.

        Parameters
        ----------
        player
            The player to count the bets for.

        Returns
        -------
        Returns True if the player has less than count number of bets for a given type and the
        bet that is intended to be placed isn't already on the table, otherwise returns False.
        """
        return self.less_than_count_bets_of_type(player) and self.bet_is_not_on_table(
            player
        )

    def bet_is_not_on_table(self, player: "Player") -> bool:
        """Returns True if the selected bet isn't already on the table.

        Parameters
        ----------
        player
            The player whose bets to check against.

        Returns
        -------
        True if the selected bet isn't already on the table, otherwise returns False.
        """
        return self.bet not in player.bets

    def less_than_count_bets_of_type(self, player: "Player") -> bool:
        """Returns True if there are less than count the number of bets on the table for the
        player, otherwise returns False.

        Parameters
        ----------
        player
            The player to count the bets for.

        Returns
        -------
        Returns True if there are less than the count of number of bets on the table, otherwise
        returns False.
        """
        return self.get_bets_of_type_count(player) < self.count

    def get_bets_of_type_count(self, player: "Player") -> int:
        """Returns the number of bets of a given type for the player.

        Parameters
        ----------
        player
            The player to count the bets for.

        Returns
        -------
        The number of bets of a given type for the player
        """
        return len(player.get_bets_by_type(bet_type=self.bet_type))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(bet_type={self.bet_type}, count={self.count}, "
            f"bet={self.bet})"
        )


class RemoveByType(RemoveIfTrue):
    """Remove any bets that are of the given type(s)."""

    def __init__(self, bet_type: typing.Type[Bet] | tuple[typing.Type[Bet], ...]):
        super().__init__(lambda b, p: isinstance(b, bet_type))
