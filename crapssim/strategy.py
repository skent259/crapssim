import copy
import typing
from abc import ABC, abstractmethod

from crapssim.bet import Bet, PassLine, Odds, Come, Place, DontPass, Place6, Place8, Place5, Place9, AllowsOdds, Field, \
    DontCome, BaseOdds

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
    def after_roll(self, player: 'Player', table: 'Table'):
        """Method that can update the Strategy from the table/player after the dice are rolled but
        before the bets are updated."""
        pass

    @abstractmethod
    def update_bets(self, player: 'Player', table: 'Table'):
        """Add, remove, or change the bets on the table."""
        pass

    def __add__(self, other: 'Strategy'):
        return AggregateStrategy(self, other)

    def __eq__(self, other: 'Strategy'):
        if isinstance(other, Strategy):
            print(self.__dict__, other.__dict__)
            return self.__dict__ == other.__dict__


class AggregateStrategy(Strategy):
    def __init__(self, *strategies):
        self.strategies = strategies

    def update_bets(self, player: 'Player', table: 'Table'):
        for strategy in self.strategies:
            strategy.update_bets(player, table)


class BetIfTrue(Strategy):
    """Place a bet if a criteria is True based on a given callable, normally a lambda."""

    def __init__(self, bet: Bet, key: typing.Callable[['Player', 'Table'], bool]):
        super().__init__()
        self.bet = bet
        self.key = key

    def update_bets(self, player: 'Player', table: 'Table'):
        if self.key(player, table):
            player.place_bet(copy.copy(self.bet), table)


class IfBetNotExist(BetIfTrue):
    """Add bets if they're not already on the table.
    Bet can either be a specific bet or a type of bet to look for."""

    def __init__(self, bet: Bet):
        super().__init__(bet,
                         lambda p, t: bet not in p.bets_on_table if isinstance(bet, Bet) else
                         not any(isinstance(x, bet) for x in p.bets_on_table))


class BetPointOff(BetIfTrue):
    """Place a bet if the point is off and the bet isn't already on the table."""

    def __init__(self, bet: Bet):
        super().__init__(bet, lambda p, t: t.point.status == "Off" and bet not in p.bets_on_table)


class BetPointOn(BetIfTrue):
    """Place a bet if not already on table depending if the point is on."""

    def __init__(self, bet: Bet):
        super().__init__(bet, lambda p, t: t.point.status == "On" and bet not in p.bets_on_table)


class BetPassLine(BetPointOff):
    def __init__(self, bet_amount: float):
        self.bet_amount = bet_amount
        super().__init__(PassLine(bet_amount))


class OddsStrategy(Strategy):
    """Place odds based on a multiplier of whatever the base_odds are for the item."""

    def __init__(self, base_type: AllowsOdds,
                 odds_multiplier: dict[int, int] | int):
        self.base_type = base_type

        if isinstance(odds_multiplier, int):
            self.odds_multiplier = {x: odds_multiplier for x in (4, 5, 6, 8, 9, 10)}
        else:
            self.odds_multiplier = odds_multiplier

    def update_bets(self, player: 'Player', table: 'Table'):
        for bet in player.bets_on_table:
            if isinstance(bet, self.base_type) and bet.point is not None:
                amount = bet.bet_amount * self.odds_multiplier[bet.point]
                odds_bet = bet.get_odds_bet(amount)
                IfBetNotExist(odds_bet).update_bets(player, table)


class PassLineOdds(OddsStrategy):
    def __init__(self, odds: dict[int, int] | int | None = None):
        if odds is None:
            odds = {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
        super().__init__(PassLine, odds)


class CountStrategy(BetIfTrue):
    """If there are less bets of bet_types than count, place a bet if it doesn't exist."""

    def __init__(self, bet_types: typing.Iterable[typing.Type[Bet]], count: int, bet: Bet):
        self.bet_types = bet_types
        self.count = count
        self.key = (lambda p, t: len([x for x in p.bets_on_table if isinstance(x, self.bet_types)]) < self.count
                                 and bet not in p.bets_on_table)
        super().__init__(bet, key=self.key)


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
            IfBetNotExist(Place.by_number(number, amount)).update_bets(player, table)


class PassLinePlace68(AggregateStrategy):
    def __init__(self,
                 pass_line_amount: float = 5,
                 six_amount: float = 6,
                 eight_amount: float = 6,
                 skip_point=True):
        pass_line_strategy = BetPassLine(pass_line_amount)
        six_eight_strategy = BetPlace({6: six_amount, 8: eight_amount}, skip_point=skip_point)
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
                player.place_bet(copy.copy(bet), table)

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
            player.place_bet(copy.copy(new_bet), table)

    def update_bets(self, player: 'Player', table: 'Table'):
        self.place_starting_bets(player, table)
        self.move_bets(player, table)


class Place68Move59(PlaceBetAndMove):
    """Place 6 and 8 and move to 5 and 9 if a PassLine or Come bet with that point comes up.

    Equivalent of:
    starting_bets = [Place6(six_eight_amount), Place8(six_eight_amount)]
    check_bets = [PassLine(pass_come_amount, point=6), PassLine(pass_come_amount, point=8),
                  Come(pass_come_amount, point=6), Come(pass_come_amount, point=8)]
    bet_movements = {Place6(six_eight_amount): Place5(5), Place8(six_eight_amount): Place5(5),
                     Place5(five_nine_amount): Place9(five_nine_amount), Place9(five_nine_amount): None}

    PlaceBetAndMove(starting_bets, check_bets, bet_movements)
    """

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
    """Equivalent of BetPassLine(...) + Place68Move59(...)"""

    def __init__(self, pass_line_amount: float = 5,
                 six_eight_amount: float = 6,
                 five_nine_amount: float = 5):
        pass_line_strategy = BetPassLine(pass_line_amount)
        place_bet_and_move_strategy = Place68Move59(pass_line_amount, six_eight_amount, five_nine_amount)
        super().__init__(pass_line_strategy, place_bet_and_move_strategy)


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


class IronCross(AggregateStrategy):
    """Equivalent of:
     BetPassLine(base_amount) + PassLineOdds(2) +
     BetPlace({5: place_five_amount,
               6: place_six_eight_amount,
               8: place_six_eight_amount}) +
     BetPointOn(Field(base_amount))"""
    def __init__(self, base_amount: float):
        place_six_eight_amount = (6 / 5) * base_amount * 2
        place_five_amount = base_amount * 2

        super().__init__(BetPassLine(base_amount),
                         PassLineOdds(2),
                         BetPlace({5: place_five_amount,
                                   6: place_six_eight_amount,
                                   8: place_six_eight_amount}),
                         BetPointOn(Field(base_amount)))


class HammerLock(Strategy):
    def __init__(self, base_amount: float):
        self.pass_line_amount = base_amount
        self.dont_pass_amount = base_amount
        self.start_six_eight_amount = (6 / 5) * base_amount * 2
        self.end_six_eight_amount = (6 / 5) * base_amount
        self.five_nine_amount = base_amount
        self.odds_multiplier = 6

        self.place_win_count: int = 0
        self.restart: bool = False

    def after_roll(self, player: 'Player', table: 'Table'):
        self.place_win_count += len([bet for bet in player.get_bets(Place) if bet.get_status(table) == 'win'])
        if table.point.status == 'On' and table.dice.total == 7:
            self.restart = True

    def point_off(self, player, table):
        strategy = IfBetNotExist(PassLine(self.pass_line_amount)) + IfBetNotExist(DontPass(self.dont_pass_amount))
        strategy.update_bets(player, table)

    def place68(self, player, table):
        PassLinePlace68(self.pass_line_amount,
                        self.start_six_eight_amount,
                        self.start_six_eight_amount,
                        skip_point=False).update_bets(player, table)
        BetLayOdds(self.odds_multiplier).update_bets(player, table)

    def place5689(self, player, table):
        player.remove_bet(Place6(self.start_six_eight_amount))
        player.remove_bet(Place8(self.start_six_eight_amount))
        BetPlace({5: self.five_nine_amount,
                  6: self.end_six_eight_amount,
                  8: self.end_six_eight_amount,
                  9: self.five_nine_amount}, skip_point=False).update_bets(player, table)

    def remove_place_bets(self, player):
        player.remove_bet(Place5(self.five_nine_amount))
        player.remove_bet(Place6(self.start_six_eight_amount))
        player.remove_bet(Place8(self.start_six_eight_amount))
        player.remove_bet(Place9(self.five_nine_amount))

    def update_bets(self, player: 'Player', table: 'Table'):
        if table.point.status == 'Off':
            self.point_off(player, table)
        elif self.place_win_count == 0:
            self.place68(player, table)
        elif self.place_win_count == 1:
            self.place5689(player, table)
        elif self.place_win_count == 2:
            self.remove_place_bets(player)

        if self.restart:
            self.place_win_count = 0
            self.restart = False


class Risk12(Strategy):
    def __init__(self):
        super().__init__()
        self.pre_point_winnings = 0

    def after_roll(self, player: 'Player', table: 'Table'):
        if table.point.status == 'Off' and any(x.get_status(table) == 'win' for x in player.bets_on_table):
            self.pre_point_winnings += sum(x.get_return_amount(table)
                                           for x in player.bets_on_table
                                           if x.get_status(table) == 'win')
        elif table.point.status == 'On' and table.dice.total == 7:
            self.pre_point_winnings = 0

    @staticmethod
    def point_off(player: 'Player', table: 'Table'):
        IfBetNotExist(PassLine(5)).update_bets(player, table)
        IfBetNotExist(Field(5)).update_bets(player, table)

    def point_on(self, player: 'Player', table: 'Table'):
        if self.pre_point_winnings >= 6 - 2:
            IfBetNotExist(Place6(6)).update_bets(player, table)
        if self.pre_point_winnings >= 12 - 2:
            IfBetNotExist(Place8(6)).update_bets(player, table)

    def update_bets(self, player: 'Player', table: 'Table'):
        if table.point.status == 'Off':
            self.point_off(player, table)
        elif table.point.status == 'On':
            self.point_on(player, table)


class Knockout(AggregateStrategy):
    """PassLine and Don't bet prior to point, 345x odds after point. Equivalent to
    BetPassLine(bet_amount) + BetPointOff(DontPass(bet_amount))
    + PassLineOdds({4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3})"""

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(BetPassLine(bet_amount), BetPointOff(DontPass(bet_amount)),
                         PassLineOdds({4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}))


class FieldWinProgression(Strategy):
    """Every time the field wins move to the next progression, else restart
    at the beginning."""

    def __init__(self, progression: list[typing.SupportsFloat]):
        self.progression = progression
        self.current_progression = 0

    def after_roll(self, player: 'Player', table: 'Table'):
        win = all(x for x in player.bets_on_table if x.get_status(table) == 'win')

        if win:
            self.current_progression += 1
        else:
            self.current_progression = 0

    def update_bets(self, player: 'Player', table: 'Table'):
        if self.current_progression >= len(self.progression):
            bet_amount = self.progression[-1]
        else:
            bet_amount = self.progression[self.current_progression]
        IfBetNotExist(player.place_bet(Field(bet_amount), table))


class DiceDoctor(FieldWinProgression):
    def __init__(self):
        super().__init__([10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150])


class Place68CPR(Strategy):
    def __init__(self, starting_amount: float = 6):
        self.starting_amount = starting_amount
        self.press_amount = 2 * self.starting_amount

        self.win_one_amount = starting_amount * (7 / 6)
        self.win_two_amount = starting_amount * 2 * (7 / 6)

        self.six_winnings = 0
        self.eight_winnings = 0

    def after_roll(self, player: 'Player', table: 'Table'):
        self.six_winnings = sum(x.get_win_amount(table) for x in player.bets_on_table if isinstance(x, Place6))
        self.eight_winnings = sum(x.get_win_amount(table) for x in player.bets_on_table if isinstance(x, Place8))

    def ensure_bets_exist(self, player: 'Player', table: 'Table'):
        """Ensure that there is always a place 6 or place 8 bet if the point is On."""
        if table.point.status == 'Off':
            return
        for bet_type in (Place6, Place8):
            if not player.has_bets(bet_type):
                player.place_bet(bet_type(self.starting_amount), table)

    def press(self, player: 'Player', table: 'Table'):
        if self.six_winnings == self.win_one_amount:
            player.place_bet(Place6(self.starting_amount), table)
        if self.eight_winnings == self.win_one_amount:
            player.place_bet(Place8(self.starting_amount), table)

    def update_bets(self, player: 'Player', table: 'Table'):
        self.ensure_bets_exist(player, table)
        self.press(player, table)


class Place68DontCome2Odds(AggregateStrategy):
    def __init__(self, six_eight_amount: float = 6,
                 dont_come_amount: float = 5):
        super().__init__(BetPlace({6: six_eight_amount, 8: six_eight_amount}, skip_point=False),
                         BetIfTrue(DontCome(dont_come_amount),
                                   lambda p, t: not any(isinstance(x, DontCome) for x in p.bets_on_table)),
                         OddsStrategy(DontCome, 2))
