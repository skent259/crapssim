"""Core strategies are strategies that can be either subclassed, or initialized to create other
strategies with the intended usage. Each of the strategies included in this package are intended
to be used as building blocks when creating strategies."""

from abc import ABC, abstractmethod
from typing import Callable, Protocol, SupportsFloat

from crapssim.bet import Bet, HardWay, Hop, Place
from crapssim.dice import Dice
from crapssim.point import Point

__all__ = [
    "Strategy",
    "AggregateStrategy",
    "NullStrategy",
    "AddIfTrue",
    "RemoveIfTrue",
    "ReplaceIfTrue",
    "AddIfNotBet",
    "AddIfPointOff",
    "AddIfPointOn",
    "AddIfNewShooter",
    "CountStrategy",
    "RemoveIfPointOff",
    "RemoveByType",
    "WinProgression",
]


class Table(Protocol):
    """Table functionality needed for strategy module."""

    dice: Dice
    point: Point
    new_shooter: bool


class Player(Protocol):
    """Player functionality needed for strategy module."""

    table: Table
    bankroll: float
    bets: list[Bet]

    def add_bet(self, bet: Bet) -> None: ...

    def already_placed_bets(self, bet: Bet) -> list[Bet]: ...

    def already_placed(self, bet: Bet) -> bool: ...

    def get_bets_by_type(self, bet_type: type[Bet] | tuple[type[Bet], ...]): ...

    def remove_bet(self, bet: Bet) -> None: ...


class Strategy(ABC):
    """A Strategy is assigned to a player and determines what bets the player
    is going to make, remove, or change.
    """

    def after_roll(self, player: Player) -> None:
        """
        Update the Strategy after the dice are rolled but before the bets and the table are updated.

        For example, if you wanted to know whether the
        point changed from on to off you could do `self.point_lost = table.point.status = "On" and
        table.dice.roll.total == 7`. You could not do this in :func:`Strategy`'s :func:`update_bets`
        method, since the table has already been updated setting the point's status to Off. Other examples
        include counting the number of place bets that had won after the roll, counting total winnings
        for certain bets, or recording the starting bankroll upon a new shooter (to later have logic
        based on winnings of that shooter).

        Parameters
        ----------
        player
            The Player to check for bets, etc.
        """

    @abstractmethod
    def completed(self, player: Player) -> bool:
        """If True, the Strategy is completed and the Player stops playing. If False, the Player
        keeps playing the Strategy."""

    @abstractmethod
    def update_bets(self, player: Player) -> None:
        """
        Add, remove, or change the bets on the table.

        This method is applied after the dice are rolled, the bets are updated,
        and the table is updated. It triggers in :py:meth:`.table.TableUpdate.run_strategies`.
        """

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

    def update_bets(self, player: Player) -> None:
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

    def completed(self, player: Player) -> bool:
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


class NullStrategy(Strategy):
    """Strategy that bets nothing."""

    def update_bets(self, player: Player) -> None:
        pass

    def completed(self, player: Player) -> bool:
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class AddIfTrue(Strategy):
    """Strategy that places a bet if a given key taking Player as a parameter is True."""

    def __init__(self, bet: Bet, key: Callable[[Player], bool]):
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

    def update_bets(self, player: Player) -> None:
        """If the key is True add the bet to the player and table.

        Parameters
        ----------
        player
            The Player to add the bet for.
        """
        if self.key(player) and self.bet.is_allowed(player):
            player.add_bet(self.bet.copy())

    def completed(self, player: Player) -> bool:
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

    def __init__(self, key: Callable[["Bet", Player], bool]):
        """The strategy will remove all bets that are true for the given key.

        Parameters
        ----------
        key
            Callable with parameters of bet and player return True if the bet should be removed
            otherwise returning False.
        """
        super().__init__()
        self.key = key

    def update_bets(self, player: Player) -> None:
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

    def completed(self, player: Player) -> bool:
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

    def __init__(self, bet: Bet, key: Callable[[Bet, Player], bool]):
        self.key = key
        self.bet = bet

    def update_bets(self, player: Player) -> None:
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
                player.add_bet(self.bet.copy())

    def completed(self, player: Player) -> bool:
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


class AddIfNotBet(AddIfTrue):
    """Strategy that adds a bet if it isn't on the table for that player. Equivalent of
    AddIfTrue(bet, lambda p: bet not in p.bets)"""

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


class AddIfPointOff(AddIfTrue):
    """Strategy that adds a bet if the table point is Off, and the Player doesn't have a bet on the
    table. Equivalent to AddIfTrue(bet, lambda p: p.table.point.status == "Off"
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


class AddIfPointOn(AddIfTrue):
    """Strategy that adds a bet if the table point is On, and the Player doesn't have a bet on the
    table. Equivalent to AddIfTrue(bet, lambda p: p.table.point.status == "On"
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


class AddIfNewShooter(AddIfTrue):
    """Strategy that adds a bet if there is a new shooter at the table, and the Player doesn't have a bet on the
    table. Equivalent to AddIfTrue(bet, lambda p: p.table.new_shooter and bet not in p.bets)
    """

    def __init__(self, bet: Bet):
        """Add a bet if the point is On.

        Parameters
        ----------
        bet
            The bet to add if the point is On.
        """
        super().__init__(bet, lambda p: p.table.new_shooter and bet not in p.bets)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bet={self.bet})"


class CountStrategy(AddIfTrue):
    """Strategy that checks how many bets exist of a certain type. If the number of bets of that
    type is less than the given count, it places the bet (if the bet isn't already on the table.)
    """

    def __init__(
        self,
        bet_type: type[Bet] | tuple[type[Bet], ...],
        count: int,
        bet: Bet,
    ) -> None:
        """Configure the count rule and bet to place.

        Args:
            bet_type: Bet type(s) to count.
            count: Maximum allowed instances before adding a new bet.
            bet: Bet to place when below ``count``.
        """
        self.bet_type = bet_type
        self.count = count

        super().__init__(bet, key=self.key)

    def key(self, player: Player) -> bool:
        """Return True when the player is below the threshold for ``bet_type``."""
        count_of_bets_with_type = len(player.get_bets_by_type(bet_type=self.bet_type))
        identical_bet_is_not_on_table = self.bet not in player.bets

        return count_of_bets_with_type < self.count and identical_bet_is_not_on_table

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(bet_type={self.bet_type!r}, count={self.count}, "
            f"bet={self.bet!r})"
        )


class RemoveIfPointOff(RemoveIfTrue):
    """Strategy that removes a bet if the table point is Off

    This will match bets based on type, and number for Place and Hardway bets.
    It will not consider bet amounts when matching."""

    def __init__(self, bet: Bet) -> None:
        """Configure removal logic for the provided bet template.

        Args:
            bet: Bet instance describing which wagers to remove when the point is off.
        """
        if not any([isinstance(bet, x) for x in [Place, HardWay, Hop]]):
            key = (
                lambda b, p: isinstance(b, type(self.bet))
                and p.table.point.status == "Off"
            )

        if isinstance(bet, Place):
            key = (
                lambda b, p: isinstance(b, Place)
                and b.number == self.bet.number
                and p.table.point.status == "Off"
            )
        if isinstance(bet, HardWay):
            key = (
                lambda b, p: isinstance(b, HardWay)
                and b.number == self.bet.number
                and p.table.point.status == "Off"
            )
        if isinstance(bet, Hop):
            key = (
                lambda b, p: isinstance(b, Hop)
                and b.result == self.bet.result
                and p.table.point.status == "Off"
            )

        super().__init__(key)
        self.bet = bet

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bet={self.bet})"


class RemoveByType(RemoveIfTrue):
    """Remove any bets that are of the given type(s)."""

    def __init__(self, bet_type: type[Bet] | tuple[type[Bet], ...]) -> None:
        """Remove all bets matching ``bet_type``."""
        super().__init__(lambda b, p: isinstance(b, bet_type))


class WinProgression(Strategy):
    """Strategy that every time a bet is won, moves to the next amount in the progression and
    places a Field bet for that amount."""

    def __init__(self, first_bet: Bet, multipliers: list[SupportsFloat]) -> None:
        """Configure the baseline bet and multiplier progression.

        Args:
            first_bet: Initial bet template, including starting amount.
            multipliers: Sequence of bankroll multipliers applied after wins.
        """
        self.bet = first_bet
        self.multipliers = multipliers
        self.current_progression = 0

    def completed(self, player: Player) -> bool:
        """Return True when bankroll is below minimum multiplier and no bets remain."""
        return (
            player.bankroll < min(float(x) for x in self.multipliers)
            and len(player.bets) == 0
        )

    def after_roll(self, player: Player) -> None:
        """Advance or reset the progression based on whether the bet won."""

        win = all(x.get_result(player.table).won for x in player.bets)

        if win:
            self.current_progression += 1
        else:
            self.current_progression = 0

    def update_bets(self, player: Player) -> None:
        """Ensure a bet exists scaled by the current progression step."""
        new_bet = self.bet.copy()
        if self.current_progression >= len(self.multipliers):
            new_bet.amount = self.bet.amount * self.multipliers[-1]
        else:
            new_bet.amount = (
                self.bet.amount * self.multipliers[self.current_progression]
            )
        AddIfNotBet(new_bet).update_bets(player)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(first_bet={self.bet}, multipliers={self.multipliers})"
