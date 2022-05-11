import copy
import typing
from abc import ABC, abstractmethod

from crapssim.bet import Bet, PassLine, Odds, Come, Place, DontPass, LayOdds, Place6, Place8, Place5, Place9, DontCome, \
    AllowsOdds, BaseOdds

if typing.TYPE_CHECKING:
    from crapssim.player import Player
    from crapssim.table import Table

"""
Various betting strategies that are based on conditions of the CrapsTable.
Each strategy must take a table and a player_object, and implicitly 
uses the methods from the player object.
"""

"""
Fundamental Strategies
"""


class Strategy(ABC):
    def before_roll(self, player: 'Player', table: 'Table'):
        """Method that can update the Strategy from the table/player before the dice are rolled."""
        pass

    def after_roll(self, player: 'Player', table: 'Table'):
        """Method that can update the Strategy from the table/player after the dice are rolled but
        before the bets are updated."""
        pass

    def after_bets_updated(self, player: 'Player', table: 'Table'):
        """Method that can update the Strategy from the table/player after the bets on the table
         are updated but before the table is updated"""
        pass

    def after_table_update(self, player: 'Player', table: 'Table'):
        """Method that can update the Strategy from the table/player after the table is updated."""
        pass

    @abstractmethod
    def update_bets(self, player: 'Player', table: 'Table'):
        """Add, remove, or change the bets on the table."""
        pass

    def __add__(self, other: 'Strategy'):
        return AggregateStrategy(self, other)


class AggregateStrategy(Strategy):
    def __init__(self, *strategies):
        self.strategies = strategies

    def update_bets(self, player: 'Player', table: 'Table'):
        for strategy in self.strategies:
            strategy.update_bets(player, table)


class CriteriaStrategy(Strategy, ABC):
    """Add bet if certain criteria is True."""

    def __init__(self, bet: Bet):
        self.bet = bet

    def update_bets(self, player: 'Player', table: 'Table'):
        if self.criteria(player, table):
            player.place_bet(self.bet, table)

    @abstractmethod
    def criteria(self, player: 'Player', table: 'Table') -> bool:
        pass


class BetNotPlaced(CriteriaStrategy):
    """Add bets if they're not already on the table."""

    def criteria(self, player: 'Player', table: 'Table') -> bool:
        return self.bet not in player.bets_on_table

    def update_bets(self, player: 'Player', table: 'Table'):
        if not self.bet.already_placed(player) and self.criteria(player, table):
            player.place_bet(copy.deepcopy(self.bet), table)


class BetPointOff(BetNotPlaced):
    """Place a bet if the point is off and the bet isn't already on the table."""

    def criteria(self, player: 'Player', table: 'Table') -> bool:
        return table.point.status == 'Off' and super().criteria(player, table)


class BetFromPoint(BetNotPlaced):
    """Place a bet if not already on table depending on what the point number is."""

    def __init__(self, bet: Bet, points: typing.Iterable[int]):
        super().__init__(bet)
        self.points = points

    def criteria(self, player: 'Player', table: 'Table') -> bool:
        return table.point in self.points and super().criteria(player, table)


class BetPointOn(BetFromPoint):
    """Place a bet if not already on table depending if the point is on."""

    def __init__(self, bet: Bet):
        super().__init__(bet, points=(4, 5, 6, 8, 9, 10))


class BetPassLine(BetPointOff):
    def __init__(self, bet_amount: float):
        self.bet_amount = bet_amount
        super().__init__(PassLine(bet_amount))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.bet_amount == other.bet_amount


class OddsStrategy(Strategy):
    """Place odds based on a multiplier of whatever the base_odds are for the item."""

    def __init__(self, allows_odds_type: AllowsOdds,
                 odds_multiplier: dict[int, int] | int):
        self.allows_odds_type = allows_odds_type

        if isinstance(odds_multiplier, int):
            self.odds_multiplier = {x: odds_multiplier for x in (4, 5, 6, 8, 9, 10)}
        else:
            self.odds_multiplier = odds_multiplier

    def update_bets(self, player: 'Player', table: 'Table'):
        for bet in player.bets_on_table:
            if isinstance(bet, self.allows_odds_type) and bet.point is not None:
                amount = bet.bet_amount * self.odds_multiplier[bet.point]
                odds_bet = bet.get_odds_bet(amount)
                BetNotPlaced(odds_bet).update_bets(player, table)


class PassLineOdds(OddsStrategy):
    def __init__(self, odds: dict[int, int] | int | None = None):
        if odds is None:
            odds = {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
        super().__init__(PassLine, odds)


class CountStrategy(BetNotPlaced):
    """If there are less bets of bet_types than count, place a bet if it doesn't exist."""

    def __init__(self, bet_types: typing.Iterable[typing.Type[Bet]], count: int, bet: Bet):
        self.bet_types = bet_types
        self.count = count
        super().__init__(bet)

    def criteria(self, player: 'Player', table: 'Table') -> bool:
        return len([x for x in player.bets_on_table if isinstance(x, tuple(self.bet_types))]) < self.count


class TwoCome(CountStrategy):
    def __init__(self, bet_amount: float):
        bet = Come(bet_amount)
        super().__init__((Come,), 2, bet)


class Pass2Come(AggregateStrategy):
    def __init__(self, bet_amount: float):
        super().__init__(BetPassLine(bet_amount), TwoCome(bet_amount))


class BetPlace(Strategy):
    def __init__(self, place_bet_amounts: dict[int, float], skip_point: bool = True):
        super().__init__()
        self.place_bet_amounts = place_bet_amounts
        self.skip_point = skip_point

    def update_bets(self, player: 'Player', table: 'Table'):
        for number, amount in self.place_bet_amounts.items():
            if self.skip_point and number == table.point.number:
                continue
            if table.point.status == 'Off':
                continue
            BetNotPlaced(Place.by_number(number, amount)).update_bets(player, table)


class Place68(AggregateStrategy):
    def __init__(self,
                 pass_line_amount: float = 5,
                 six_amount: float = 6,
                 eight_amount: float = 6):
        pass_line_strategy = BetPassLine(pass_line_amount)
        six_eight_strategy = BetPlace({6: six_amount, 8: eight_amount}, skip_point=True)
        super().__init__(pass_line_strategy, six_eight_strategy)


class BetDontPass(BetPointOff):
    def __init__(self, bet_amount: float):
        super().__init__(DontPass(bet_amount))


class BetLayOdds(OddsStrategy):
    def __init__(self, odds: dict[int, int] | int | None = None):
        if odds is None:
            odds = {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
        super().__init__(DontPass, odds)


class PlaceBetAndMove(Strategy):
    """Make place bets and then move it to another place or remove it if certain bets move
    to the same number

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

    def __init__(self, starting_bets: list[Place],
                 check_bets: list[AllowsOdds],
                 bet_movements: dict[Place, Place | None]):

        self.starting_bets = starting_bets
        self.check_bets = check_bets
        self.bet_movements = bet_movements

    def check_bets_on_table(self, player: 'Player') -> AllowsOdds:
        return [x for x in player.bets_on_table if x in self.check_bets]

    def check_numbers(self, player: 'Player'):
        return [x.point for x in self.check_bets_on_table(player)]

    def place_starting_bets(self, player: 'Player', table: 'Table'):
        if table.point.status == 'Off':
            return

        for bet in self.starting_bets:
            if bet not in player.bets_on_table:
                player.place_bet(bet, table)

    def bets_to_move(self, player: 'Player') -> list[Place]:
        return [x for x in self.bet_movements if x.winning_number in
                self.check_numbers(player) and x in player.bets_on_table]

    def move_bets(self, player: 'Player', table: 'Table') -> None:
        while len(self.bets_to_move(player)) > 0:
            old_bet = self.bets_to_move(player)[0]
            new_bet = self.bet_movements[old_bet]
            while new_bet in player.bets_on_table:
                new_bet = self.bet_movements[new_bet]
            player.remove_bet(old_bet)
            player.place_bet(new_bet, table)

    def update_bets(self, player: 'Player', table: 'Table'):
        self.place_starting_bets(player, table)
        self.move_bets(player, table)


class Place68Move59(PlaceBetAndMove):
    """Place 6 and 8 and move to 5 and 9 if a PassLine or Come bet with that point comes up."""

    def __init__(self, pass_come_amount: float = 5,
                 six_eight_amount: float = 6,
                 five_nine_amount: float = 5):
        super().__init__(starting_bets=[Place6(six_eight_amount),
                                        Place8(six_eight_amount)],
                         check_bets=[PassLine(pass_come_amount, point=6),
                                     PassLine(pass_come_amount, point=8),
                                     Come(pass_come_amount, point=6),
                                     Come(pass_come_amount, point=8)],
                         bet_movements={Place6(six_eight_amount): Place5(5),
                                        Place8(six_eight_amount): Place5(5),
                                        Place5(five_nine_amount): Place9(five_nine_amount),
                                        Place9(five_nine_amount): None})


class PassLinePlace68Move59(AggregateStrategy):
    def __init__(self, pass_line_amount: float = 5,
                 six_eight_amount: float = 6,
                 five_nine_amount: float = 5):
        pass_line_strategy = BetPassLine(pass_line_amount)
        place_bet_and_move_strategy = Place68Move59(pass_line_amount, six_eight_amount, five_nine_amount)
        super().__init__(pass_line_strategy, place_bet_and_move_strategy)


class PlaceIfOtherBetsExist(Strategy):
    """If any of the other bets exist in check bets, place these bets."""

    def __init__(self,
                 bets_to_place: list[Bet],
                 check_bets: list[Bet]):
        self.bets_to_place = bets_to_place
        self.check_bets = check_bets

    def check_bets_exist(self, player: 'Player'):
        return any(x in player.bets_on_table for x in self.check_bets)

    def add_bets(self, player: 'Player', table: 'Table'):
        for bet in self.bets_to_place:
            if bet not in player.bets_on_table:
                player.place_bet(bet, table)

    def update_bets(self, player: 'Player', table: 'Table'):
        if self.check_bets_exist(player):
            self.add_bets(player, table)


class Place682Come(Strategy):
    def __init__(self, pass_come_amount: float = 5,
                 six_eight_amount: float = 6,
                 five_nine_amount: float = 5):
        self.pass_come_amount = pass_come_amount
        self.six_eight_amount = six_eight_amount
        self.five_nine_amount = five_nine_amount

    def add_pass_line_come(self, player: 'Player', table):
        if player.count_bets(Place, PassLine, Odds) >= 4:
            return

        if table.point.status == 'Off' and \
                player.has_bets(winning_numbers=[6]) and \
                player.has_bets(winning_numbers=[8]):
            player.place_bet(PassLine(self.pass_come_amount), table)
        elif table.point.status == 'On':
            player.place_bet(Come(self.pass_come_amount), table)

    def update_bets(self, player: 'Player', table: 'Table'):
        self.add_pass_line_come(player, table)
        Place68Move59(pass_come_amount=self.pass_come_amount,
                      six_eight_amount=self.six_eight_amount,
                      five_nine_amount=self.five_nine_amount).update_bets(player, table)
