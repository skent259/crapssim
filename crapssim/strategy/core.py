"""Core strategies are strategies that can be either subclassed, or initialized to create other
strategies with the intended usage. Each of the strategies included in this package are intended
to be used as building blocks when creating strategies."""

import inspect
import typing
from abc import ABC, abstractmethod

from crapssim.bet import Bet, PassLine, Come
from crapssim.bet.place import Place
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
        for strategy in self.strategies:
            if not strategy.completed(player):
                strategy.update_bets(player)

    def completed(self, player: 'Player') -> None:
        print([x.completed(player) for x in self.strategies])
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
        if self.key(player):
            player.add_bet(self.bet)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet={self.bet}, ' \
               f'key={self.key})'


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
        new_bets = []
        for bet in player.bets_on_table:
            if not self.key(bet, player):
                new_bets.append(bet)
        player.bets_on_table = new_bets

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(key={inspect.getsource(self.key)})'


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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Strategy):
            return isinstance(other, BetPointOff) and self.bet == other.bet
        raise NotImplementedError

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
    type is less than the given count, it places the bet."""
    def __init__(self, bet_types: typing.Iterable[typing.Type[Bet]], count: int, bet: Bet):
        """If there are less than count number of bets placed by player with a given bet_type, it
        adds the given bet.

        Parameters
        ----------
        bet_types
            The types of bets to count.
        count
            How many of the bets to check against.
        bet
            The bet to place if there are less than count bets of a given type.
        """
        self.bet_types = bet_types
        self.count = count

        def key(player: "Player") -> bool:
            bets_of_type = [x for x in player.bets_on_table if isinstance(x, tuple(self.bet_types))]
            bets_of_type_count = len(bets_of_type)
            return bets_of_type_count < self.count and bet not in player.bets_on_table
        super().__init__(bet, key=key)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet={self.bet})'


class PlaceBetAndMove(Strategy):
    """Strategy that makes Place bets and then moves the bet to other Places if an AllowsOdds bet
    gets moved to a bet with the same number."""
    def __init__(self, starting_bets: list[Place],
                 check_bets: list[PassLine | DontPass | Come | DontCome],
                 bet_movements: dict[Place, Place | None]):
        """Makes the starting place bets in starting_bets and then if one of the check_bets gets
        moved to the same point as one of the place bets, the bet gets moved to a different bet
        depending on the bet_movements dictionary.

        Parameters
        ----------
        starting_bets
            Starting bets placed on the table.
        check_bets
            If one of these bets ended up having the same point as one of the place bets,
            move to a different bet.
        bet_movements
            If the place bet is at a point of a check bet return the bet to replace it with
            or None to remove it.
        """

        self.starting_bets = starting_bets
        self.check_bets = check_bets
        self.bet_movements = bet_movements

    def check_bets_on_table(self, player: 'Player') -> list[PassLine | DontPass | Come | DontCome]:
        """Returns any bets the player has on the table that are in check_bets.

        Parameters
        ----------
        player
            The player to check the bets for.

        Returns
        -------
        list[AllowsOdds]
            A list of all the check bets that are on the table.
        """
        return [x for x in player.bets_on_table if isinstance(x, (PassLine, DontPass,
                                                                  Come, DontCome))
                and x in self.check_bets]

    def check_numbers(self, player: 'Player') -> list[int]:
        """Returns the points of all the check bets that are currently on the table.

        Parameters
        ----------
        player
            The player to get the check bets points from.

        Returns
        -------
        list[int]
            A list of points of bets that are check_bets the player has on the table.
        """
        check_numbers = []
        for bet in self.check_bets:
            if bet in player.bets_on_table:
                check_numbers += bet.get_winning_numbers(player.table)
        return check_numbers

    def place_starting_bets(self, player: 'Player') -> None:
        """Place the initial place bets.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        for bet in self.starting_bets:
            if bet not in player.bets_on_table and player.table.point.status != "Off":
                player.add_bet(bet)

    def bets_to_move(self, player: 'Player') -> list[Place]:
        """A list of the bets that need to bet moved to a different bet.

        Parameters
        ----------
        player
            The player to place the bets for.

        Returns
        -------
        list[Place]
            A list of the bets that need to be moved to a different bet.
        """
        return [x for x in self.bet_movements if x.winning_numbers[0] in
                self.check_numbers(player) and x in player.bets_on_table]

    def move_bets(self, player: 'Player') -> None:
        """Move any bets that need to be moved to a different bet as determined by bet_movements.

        Parameters
        ----------
        player
            The player to move the bets for.
        """
        while len(self.bets_to_move(player)) > 0:
            old_bet = self.bets_to_move(player)[0]
            new_bet = self.bet_movements[old_bet]
            while new_bet in player.bets_on_table:
                new_bet = self.bet_movements[new_bet]
            player.remove_bet(old_bet)
            if new_bet is not None:
                player.add_bet(new_bet)

    def update_bets(self, player: 'Player') -> None:
        """Place the initial bets and move them to the desired location.

        Parameters
        ----------
        player
            The player to move the bets for.
        """
        self.place_starting_bets(player)
        self.move_bets(player)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(starting_bets={self.starting_bets}, ' \
               f'check_bets={self.check_bets}, bet_movements={self.bet_movements})'


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
