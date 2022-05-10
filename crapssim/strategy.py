import copy
import typing
from abc import ABC, abstractmethod

from crapssim.bet import Bet, PassLine, Odds, Come, Place, DontPass, LayOdds, Place6, Place8, Place5, Place9

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


class BetPointOff(Strategy):
    """Place a bet if the point is off and the bet isn't already on the table."""

    def __init__(self, bet: Bet):
        super().__init__()
        self.bet = bet

    def update_bets(self, player: 'Player', table: 'Table'):
        if self.bet not in player.bets_on_table:
            player.place_bet(self.bet, table)


class BetFromPoint(Strategy):
    """Place a bet if not already on table depending on what the point number is."""

    def __init__(self, bet: Bet, points: typing.Iterable[int]):
        super().__init__()
        self.bet = bet
        self.points = points

    def update_bets(self, player: 'Player', table: 'Table'):
        if table.point.number in self.points and self.bet not in player.bets_on_table:
            player.place_bet(self.bet, table)


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


class PassLineOdds(Strategy):
    def __init__(self, odds: dict[int, int] | int | None = None):
        if odds is None:
            self.odds = {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
        elif isinstance(odds, int):
            self.odds = {x: odds for x in (4, 5, 6, 8, 9, 10)}
        elif isinstance(odds, dict):
            self.odds = odds
        else:
            raise NotImplementedError

    def update_bets(self, player: 'Player', table: 'Table'):
        if table.point.status == 'On':
            number = table.point.number
            amount = self.odds[number] * sum(x.bet_amount for x in player.get_bets(PassLine))
            bet = Odds.by_number(number, amount)
            if bet not in player.bets_on_table:
                player.place_bet(bet, table)


class TwoCome(Strategy):
    def __init__(self, bet_amount: float):
        self.bet_amount = bet_amount

    def update_bets(self, player: 'Player', table: 'Table'):
        if player.count_bets(Come) < 2:
            player.place_bet(Come(self.bet_amount), table)


class Pass2Come(AggregateStrategy):
    def __init__(self, bet_amount: float):
        super().__init__(BetPassLine(bet_amount), TwoCome(bet_amount))


class BetPlace(Strategy):
    def __init__(self, bet_amounts: dict[int],
                 skip_point: bool = True):
        super().__init__()
        self.bet_amounts = bet_amounts
        self.skip_point = skip_point

    def update_bets(self, player: 'Player', table: 'Table'):
        if table.point.status == 'Off':
            return

        self.place_bets(player, table)

    def place_bets(self, player, table):
        for bet_number in self.bet_amounts:
            if self.skip_point and table.point.number == bet_number:
                continue
            amount = self.bet_amounts[bet_number]
            bet = Place.by_number(bet_number, amount)
            if bet not in player.bets_on_table:
                player.place_bet(bet, table)


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


class BetLayOdds(Strategy):
    def __init__(self, odds: dict[int, int] | int | None = None):
        if odds is None:
            self.odds = {x: 6 for x in (4, 5, 6, 8, 9, 10)}
        elif isinstance(odds, int):
            self.odds = {x: odds for x in (4, 5, 6, 8, 9, 10)}
        elif isinstance(odds, dict):
            self.odds = odds
        else:
            raise NotImplementedError

    def update_bets(self, player: 'Player', table: 'Table'):
        if table.point.status == 'On':
            number = table.point.number
            amount = self.odds[number] * sum(x.bet_amount for x in player.get_bets(DontPass))
            bet = LayOdds.by_number(number, amount)
            if bet not in player.bets_on_table:
                player.place_bet(bet, table)


class Place682Come(Strategy):
    def __init__(self, pass_come_amount: float = 5,
                 place_amounts: dict[int, float] = None):
        self.pass_come_amount = pass_come_amount

        if place_amounts is None:
            self.place_amounts = {5: 5, 6: 6, 8: 6, 9: 5}
        else:
            self.place = place_amounts

    def place_68(self, player: 'Player', table: 'Table'):
        if table.point.status == 'Off':
            return
        if player.count_bets(Place, PassLine, Odds) <= 4:
            if not player.has_bets(Place6):
                player.place_bet(Place6(self.place_amounts[6]), table)
            if not player.has_bets(Place8):
                player.place_bet(Place8(self.place_amounts[8]), table)

    def place_59(self, player: 'Player', table: 'Table'):
        if player.count_bets(point=5) == 0:
            player.place_bet(Place5(self.place_amounts[5]), table)
        elif player.count_bets(point=9) == 0:
            player.place_bet(Place9(self.place_amounts[9]), table)

    def add_pass_line_come(self, player: 'Player', table):
        if player.count_bets(Place, PassLine, Odds) >= 4:
            return

        if table.point.status == 'Off' and \
                player.has_bets(winning_numbers=[6]) and \
                player.has_bets(winning_numbers=[8]):
            player.place_bet(PassLine(self.pass_come_amount), table)
        elif table.point.status == 'On':
            player.place_bet(Come(self.pass_come_amount), table)

    def move_bets(self, player, table):
        for bet in player.get_bets(Come, PassLine):
            if bet.point == 6 and player.has_bets(Place6):
                player.remove_bet(player.get_bet(Place6))
                self.place_59(player, table)
            if bet.point == 8 and player.has_bets(Place8):
                player.remove_bet(player.get_bet(Place8))
                self.place_59(player, table)

    def update_bets(self, player: 'Player', table: 'Table'):
        self.place_68(player, table)
        self.add_pass_line_come(player, table)
        self.move_bets(player, table)



    # def point_off(self, player: 'Player', table: 'Table'):
    #     if not player.count_bets(Place, Come, PassLine) >= 4:
    #         player.place_bet(PassLine(self.pass_come_amount), table)
    #
    # def has_bet(self, player, number):
    #     return len([x for x in player.bets_on_table if isinstance(x, (PassLine, Come, Place))
    #             and x.winning_numbers == [number]]) > 0
    #
    # def point_on(self, player: 'Player', table: 'Table'):
    #     self.place_68(player, table)
    #
    #     if not player.count_bets(Place, Come, PassLine) >= 4:
    #         player.place_bet(Come(self.pass_come_amount), table)
    #
    #     self.move_bets(player, table)
    #
    # def move_bets(self, player: 'Player', table: 'Table'):
    #     for winning_number in (6, 8):
    #         if player.has_bets(Place, winning_number=winning_number) and \
    #                 player.has_bets(PassLine, Come, winning_number=winning_number):
    #             old_bet = player.get_bet(Place, winning_number=winning_number)
    #             player.remove_bet(old_bet)
    #
    #             new_number = {6: 5, 8: 9}[winning_number]
    #             new_amount = self.place_amounts[new_number]
    #             new_bet = Place.by_number(new_number, new_amount)
    #             player.place_bet(new_bet, table)
    #
    # def update_bets(self, player: 'Player', table: 'Table'):
    #     if table.point.status == 'Off':
    #         self.point_off(player, table)
    #     else:
    #         self.point_on(player, table)
