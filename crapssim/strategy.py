import copy
import typing
from abc import ABC, abstractmethod

from crapssim.bet import Bet, PassLine, Come, Place, DontPass, Place6, Place8, Place5, Place9, AllowsOdds, \
    Field, DontCome

if typing.TYPE_CHECKING:
    from crapssim.table import Player

"""
Various betting strategies that are based on conditions of the CrapsTable.
Each strategy must take a table and a player_object, and implicitly 
uses the methods from the player object.
"""

"""
Fundamental Strategies
"""


class Strategy(ABC):
    """ A Strategy is assigned to a player and determines what bets the player
    is going to make, remove, or change.
    """

    def after_roll(self, player: 'Player') -> None:
        """Method that can update the Strategy from the table/player after the dice are rolled but
        before the bets and the table are updated. For example, if you wanted to know whether the point changed
        from on to off you could do self.point_lost = table.point.status = "On" and table.dice.roll.total == 7.
        You couldn't do this in update_bets since the table has already been updated with point.status = Off.

        Parameters
        ----------
        player
            The Player to check for bets, etc.
        """
        pass

    @abstractmethod
    def update_bets(self, player: 'Player'):
        """Add, remove, or change the bets on the table. This method is applied after the dice are rolled,
        the bets are updated, and the table is updated."""
        pass

    def __add__(self, other: 'Strategy'):
        return AggregateStrategy(self, other)

    def __eq__(self, other: 'Strategy'):
        if isinstance(other, Strategy):
            return self.__dict__ == other.__dict__


class AggregateStrategy(Strategy):
    def __init__(self, *strategies: Strategy):
        """A combination of multiple strategies. Strategies are applied in the order that is given.

        Parameters
        ----------
        strategies
            The strategies to combine to make the new strategy.
        """
        self.strategies = strategies

    def update_bets(self, player: 'Player'):
        for strategy in self.strategies:
            strategy.update_bets(player)


class BetIfTrue(Strategy):
    def __init__(self, bet: Bet, key: typing.Callable[['Player'], bool]):
        """Place the given bet if a criteria is True based on a given callable key with the parameters
         of Player and Table returning True if the bet should be place, otherwise False.

        Parameters
        ----------
        bet
            The Bet to place if key is True.
        key
            Callable with parameters of player and table returning a boolean to decide whether to place the bet.
        """
        super().__init__()
        self.bet = bet
        self.key = key

    def update_bets(self, player: 'Player'):
        """If the key is True add the bet to the player and table.

        Parameters
        ----------
        player
            The Player to add the bet for.
        """
        if self.key(player):
            player.add_bet(copy.copy(self.bet))


class RemoveIfTrue(Strategy):
    def __init__(self, key: typing.Callable[['Bet', 'Player'], bool]):
        """Strategy that goes through all of the players bets, and if the key returns True
        remove the bet.

        Parameters
        ----------
        key
            Callable with parameters of bet and player return True if the bet should be removed
            otherwise returning False.
        """
        super().__init__()
        self.key = key

    def update_bets(self, player: 'Player'):
        """For each of the players bets if the key is True remove the bet from the table.

        Parameters
        ----------
        player
            The Player to remove the bets for.
        """
        for bet in player.bets_on_table:
            if self.key(bet, player):
                player.remove_bet(bet)


class IfBetNotExist(BetIfTrue):
    def __init__(self, bet: Bet):
        """Add bets if it's not already on the table.

        Parameters
        ----------
        bet
            The bet to add if it isn't already on the table.
        """
        super().__init__(bet,
                         lambda p: bet not in p.bets_on_table if isinstance(bet, Bet) else
                         not any(isinstance(x, bet) for x in p.bets_on_table))


class BetPointOff(BetIfTrue):
    def __init__(self, bet: Bet):
        """Add a bet if the table point is Off.

        Parameters
        ----------
        bet
            The bet to add if the point is Off.
        """
        super().__init__(bet, lambda p: p.table.point.status == "Off" and bet not in p.bets_on_table)

    def __eq__(self, other):
        if isinstance(other, Strategy):
            return isinstance(other, BetPointOff) and self.bet == other.bet
        else:
            raise NotImplementedError


class BetPointOn(BetIfTrue):
    def __init__(self, bet: Bet):
        """Add a bet if the point is On.

        Parameters
        ----------
        bet
            The bet to add if the point is On.
        """
        super().__init__(bet, lambda p: p.table.point.status == "On" and bet not in p.bets_on_table)


class BetPassLine(BetPointOff):
    def __init__(self, bet_amount: float):
        """Add a PassLine bet if of bet_amount if the point is Off.

        Parameters
        ----------
        bet_amount
            The amount of the PassLine bet.
        """
        self.bet_amount = bet_amount
        super().__init__(PassLine(bet_amount))


class OddsStrategy(Strategy):
    def __init__(self, base_type: AllowsOdds,
                 odds_multiplier: dict[int, int] | int):
        """Takes an AllowsOdds item (ex. PassLine, Come, DontPass) and adds a BaseOdds bet (either Odds or LayOdds)
         based on the odds_multiplier given.

        Parameters
        ----------
        base_type
            The bet that odds will be added to.
        odds_multiplier
            If odds_multipler is an integer adds multiplier * base_bets amount to the odds. If the odds multiplier is a
            dictionary of Integers looks at the dictionary to determine what odds multiplier to use depending
            on the given point.
        """
        self.base_type = base_type

        if isinstance(odds_multiplier, int):
            self.odds_multiplier = {x: odds_multiplier for x in (4, 5, 6, 8, 9, 10)}
        else:
            self.odds_multiplier = odds_multiplier

    def update_bets(self, player: 'Player'):
        """Add and Odds bet to the given base_types in the amount determined by the odds_multiplier.

        Parameters
        ----------
        player
            The player to add the odds bet to.
        """
        for bet in player.bets_on_table:
            if isinstance(bet, self.base_type) and bet.point is not None:
                amount = bet.bet_amount * self.odds_multiplier[bet.point]
                odds_bet = bet.get_odds_bet(amount)
                IfBetNotExist(odds_bet).update_bets(player)


class PassLineOdds(OddsStrategy):
    def __init__(self, odds: dict[int, int] | int | None = None):
        """Add odds to PassLine bets with the multipler specified by odds.

        Parameters
        ----------
        odds
            If odds is an integer the bet amount is the PassLine bet amount * odds. If it's a dictionary
            it uses the PassLine bet's point to determine the multiplier. Defaults to
            {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3} which are 345x odds.
        """
        if odds is None:
            odds = {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
        super().__init__(PassLine, odds)


class CountStrategy(BetIfTrue):
    def __init__(self, bet_types: typing.Iterable[typing.Type[Bet]], count: int, bet: Bet):
        """If there are less than x number of bets placed by player with a given type, place
        the given bet.

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
        self.key = (lambda p: len([x for x in p.bets_on_table if isinstance(x, self.bet_types)]) < self.count
                                 and bet not in p.bets_on_table)
        super().__init__(bet, key=self.key)


class TwoCome(CountStrategy):
    def __init__(self, bet_amount: float):
        """If there are less than two Come bets placed, place a Come bet.

        Parameters
        ----------
        bet_amount
            Amount of the come bet.
        """
        bet = Come(bet_amount)
        super().__init__((Come,), 2, bet)


class Pass2Come(AggregateStrategy):
    def __init__(self, bet_amount: float):
        """Place a PassLine bet and two Come bets. Equivalent to
        BetPassLine(bet_amount) + TwoCome(bet_amount)

        Parameters
        ----------
        bet_amount
        """
        super().__init__(BetPassLine(bet_amount), TwoCome(bet_amount))


class BetPlace(Strategy):
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

    def update_bets(self, player: 'Player'):
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
            IfBetNotExist(Place.by_number(number, amount)).update_bets(player)


class PassLinePlace68(AggregateStrategy):
    def __init__(self,
                 pass_line_amount: float = 5,
                 six_amount: float = 6,
                 eight_amount: float = 6,
                 skip_point=True):
        """Bet the PassLine and Place the 6 and the 8. Equivalent to:
        BetPassLine(pass_line_amount) + BetPlace({6: six_amount, 8: eight_amount}, skip_point=skip_point)

        Parameters
        ----------
        pass_line_amount
            How much to bet on the PassLine
        six_amount
            How much to bet on the six
        eight_amount
            How much to bet on the eight
        skip_point
            If True, don't place the six or eight if that is the number of the point.
        """
        pass_line_strategy = BetPassLine(pass_line_amount)
        six_eight_strategy = BetPlace({6: six_amount, 8: eight_amount}, skip_point=skip_point)
        super().__init__(pass_line_strategy, six_eight_strategy)


class BetDontPass(BetPointOff):
    def __init__(self, bet_amount: float):
        """If the point is off place a DontPass bet of a given amount.

        Parameters
        ----------
        bet_amount
            The amount of the DontPass bet to place.
        """
        super().__init__(DontPass(bet_amount))


class BetLayOdds(OddsStrategy):
    def __init__(self, odds: dict[int, int] | int | None = None):
        """Add odds to DontPass bets with the multipler specified by odds.

        Parameters
        ----------
        odds
            If odds is an integer the bet amount is the PassLine bet amount * odds. If it's a dictionary
            it uses the PassLine bet's point to determine the multiplier. Defaults to 6.
        """
        if odds is None:
            odds = 6
        super().__init__(DontPass, odds)


class PlaceBetAndMove(Strategy):
    def __init__(self, starting_bets: list[Place],
                 check_bets: list[AllowsOdds],
                 bet_movements: dict[Place, Place | None]):
        """Make place bets and then move it to another place or remove it if certain check_bets move
        to the same number.

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

    def check_bets_on_table(self, player: 'Player') -> list[AllowsOdds]:
        """Returns any bets the player has on the table that are check bets.

        Parameters
        ----------
        player
            The player to check the bets for.

        Returns
        -------
        list[AllowsOdds]
            A list of all of the check bets that are on the table.
        """
        return [x for x in player.bets_on_table if x in self.check_bets]

    def check_numbers(self, player: 'Player') -> list[int]:
        """Returns the points of all the check bets that are currently on the table.

        Parameters
        ----------
        player
            The player to get the check bets points from.

        Returns
        -------
        list[int]
            A list of points of bets that are check bets the player has on the table.
        """
        return [x.point for x in self.check_bets_on_table(player)]

    def place_starting_bets(self, player: 'Player'):
        """Place the initial place bets.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        for bet in self.starting_bets:
            BetIfTrue(bet, lambda p: bet not in p.bets_on_table and p.table.point.status != 'Off'). \
                update_bets(player)

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
        return [x for x in self.bet_movements if x.winning_number in
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
            player.add_bet(copy.copy(new_bet))

    def update_bets(self, player: 'Player'):
        """Place the initial bets and move them to the desired location.

        Parameters
        ----------
        player
            The player to move the bets for.
        """
        self.place_starting_bets(player)
        self.move_bets(player)


class Place68Move59(PlaceBetAndMove):
    def __init__(self, pass_come_amount: float = 5,
                 six_eight_amount: float = 6,
                 five_nine_amount: float = 5):
        """Place 6 and 8 and move to 5 and 9 if a PassLine or Come bet with that point comes up.

        Equivalent of:
        starting_bets = [
            Place6(six_eight_amount),
            Place8(six_eight_amount)
        ]
        check_bets = [
            PassLine(pass_come_amount, point=6),
            PassLine(pass_come_amount, point=8),
            Come(pass_come_amount, point=6),
            Come(pass_come_amount, point=8)
        ]
        bet_movements = {
            Place6(six_eight_amount):
            Place5(5),
            Place8(six_eight_amount): Place5(5),
            Place5(five_nine_amount): Place9(five_nine_amount),
            Place9(five_nine_amount): None
        }

        PlaceBetAndMove(starting_bets, check_bets, bet_movements)

        Parameters
        ----------
        pass_come_amount
            The amount of the PassLine and Come bets.
        six_eight_amount
            The amount of the Place6 and Place8 bets.
        five_nine_amount
            The amount of the Place5 and Place9 bets.
        """
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
        """Place a PassLine bet, Place the six and eight, and move them to 5 9 if the point for the
        PassLine bet is a 6 or 8.

        Equivalent of BetPassLine(...) + Place68Move59(...)

        Parameters
        ----------
        pass_line_amount
            The amount of the PassLine bet.
        six_eight_amount
            The amount of the Place6 and Place8 bets.
        five_nine_amount
            The amount of the Place5 and Place9 bets.
        """
        pass_line_strategy = BetPassLine(pass_line_amount)
        place_bet_and_move_strategy = Place68Move59(pass_line_amount, six_eight_amount, five_nine_amount)
        super().__init__(pass_line_strategy, place_bet_and_move_strategy)


class Place682Come(AggregateStrategy):
    def __init__(self, pass_come_amount: float = 5,
                 six_eight_amount: float = 6,
                 five_nine_amount: float = 5):
        """Place the six and the eight and place two come bets moving the six and eight to five or nine
        if the Come or PassLine bets points come up to those numbers. Also, if there is a Place6 or Place8
        bet and the point if Off make a PassLine bet.

        Parameters
        ----------
        pass_come_amount
            The amount of the Come bet.
        six_eight_amount
            The amount of the Place6 and Place8 bets.
        five_nine_amount
            The amount of the Place5 and Place9 bets.
        """

        def pass_line_key(p):
            (p.table.point.status == 'Off' and
             any(isinstance(x, (Place6, Place8)) for x in p.bets_on_table) and
             p.count_bets(Place, PassLine, Come) <= 4)

        pass_line_strategy = BetIfTrue(PassLine(pass_come_amount), pass_line_key)
        come_key = lambda p: p.table.point.status == 'On' and p.count_bets(Place, PassLine, Come) <= 4
        come_strategy = BetIfTrue(Come(pass_come_amount), come_key)
        place_strategy = Place68Move59(pass_come_amount=pass_come_amount,
                                       six_eight_amount=six_eight_amount,
                                       five_nine_amount=five_nine_amount)
        super().__init__(pass_line_strategy, come_strategy, place_strategy)


class IronCross(AggregateStrategy):
    def __init__(self, base_amount: float):
        """Bet the Pass Line, the Pass Line Odds, and Place on 5, 6, and 8. If point is on and no bet on the field, place
        a bet on the field.

        Equivalent to:
        BetPassLine(...) + PassLineOdds(2), + BetPlace({...}) + BetPointOn(Field(...))

        Parameters
        ----------
        base_amount
            The base amount of the bets. This amount is used for the PassLine and Field.
            base_amount * (6/5) * 2 is used for placing the six and eight, and base amount * 2 is used for
            placing the five.
        """
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
        """Pass Line Bet, Don't Pass bet with a lay of odds. A phased place bet approach, starting inside and then
        shifting outside eventually taking bet down if two place bets win.

        Parameters
        ----------
        base_amount
            Base amount for PassLine and DontPass Bets, and Place5 and Place9 bets. Place6 and Place8 starts at
            (6/5) * 2 * this amount and if it wins moves to (6 / 5) * this amount.
        """
        self.base_amount = base_amount
        self.start_six_eight_amount = (6 / 5) * base_amount * 2
        self.end_six_eight_amount = (6 / 5) * base_amount
        self.five_nine_amount = base_amount
        self.odds_multiplier = 6

        self.place_win_count: int = 0

    def after_roll(self, player: 'Player'):
        """Update the place_win_count based on how many Place bets are won. If table.point.status is On and the
        dice total is 7 (meaning the shooter sevens out) reset place_win_count to 0.

        Parameters
        ----------
        player
        """
        self.place_win_count += len([bet for bet in player.get_bets(Place) if bet.get_status(player.table) == 'win'])
        if player.table.point.status == 'On' and player.table.dice.total == 7:
            self.place_win_count = 0

    def point_off(self, player):
        """If the point is Off add a PassLine and a DontPass bet if they don't already exist.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        strategy = IfBetNotExist(PassLine(self.base_amount)) + IfBetNotExist(DontPass(self.base_amount))
        strategy.update_bets(player)

    def place68(self, player):
        """Place the 6 and 8 (regardless of the point) and then lay odds on DontPass bets.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        PassLinePlace68(self.base_amount,
                        self.start_six_eight_amount,
                        self.start_six_eight_amount,
                        skip_point=False).update_bets(player)

    def place5689(self, player):
        """Place the 5, 6, 8 and 9.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        RemoveIfTrue(lambda b, p: b == Place6(self.start_six_eight_amount)
                                     or b == Place8(self.start_six_eight_amount)).update_bets(player)
        BetPlace({5: self.five_nine_amount,
                  6: self.end_six_eight_amount,
                  8: self.end_six_eight_amount,
                  9: self.five_nine_amount}, skip_point=False).update_bets(player)

    def update_bets(self, player: 'Player'):
        """If the point is off bet the PassLine and DontPass line. If the point is on bet the Place6 and Place8 until
        one wins, then bet the Place 5, 6, 8, and 9. LayOdds whenever possible.

        Parameters
        ----------
        player
            Player to place the bets for.
        """
        if player.table.point.status == 'Off':
            self.point_off(player)
        elif self.place_win_count == 0:
            self.place68(player)
        elif self.place_win_count == 1:
            self.place5689(player)
        elif self.place_win_count == 2:
            RemoveIfTrue(lambda b, p: isinstance(b, Place)).update_bets(player)
        BetLayOdds(self.odds_multiplier).update_bets(player)


class Risk12(Strategy):
    def __init__(self):
        """Pass line and field bet before the point is established. Once the point is established place the 6 and 8.
        """
        super().__init__()
        self.pre_point_winnings = 0

    def after_roll(self, player: 'Player'):
        """Determine the pre-point winnings which is used to determine which bets to place when the
        point is on.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        if player.table.point.status == 'Off' and any(x.get_status(player.table) == 'win' for x in player.bets_on_table):
            self.pre_point_winnings += sum(x.get_return_amount(player.table)
                                           for x in player.bets_on_table
                                           if x.get_status(player.table) == 'win')
        elif player.table.point.status == 'On' and player.table.dice.total == 7:
            self.pre_point_winnings = 0

    @staticmethod
    def point_off(player: 'Player'):
        """Place a 5 PassLine and Field bet.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        IfBetNotExist(PassLine(5)).update_bets(player)
        IfBetNotExist(Field(5)).update_bets(player)

    def point_on(self, player: 'Player') -> None:
        """If your winnings were enough to cover the place bets (throwing in another dollar for each) make
        the place bets.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        if self.pre_point_winnings >= 6 - 1:
            IfBetNotExist(Place6(6)).update_bets(player)
        if self.pre_point_winnings >= 12 - 2:
            IfBetNotExist(Place8(6)).update_bets(player)

    def update_bets(self, player: 'Player') -> None:
        """If the point is off make a Field and PassLine bet. If the point is on
        Place the 6 and 8 if you made enough pre-point to cover the bets.

        Parameters
        ----------
        player
            The player to make the bets for.
        """
        if player.table.point.status == 'Off':
            self.point_off(player)
        elif player.table.point.status == 'On':
            self.point_on(player)


class Knockout(AggregateStrategy):
    """PassLine and Don't bet prior to point, 345x PassLine Odds after point.

    Equivalent to:
    BetPassLine(bet_amount) + BetPointOff(DontPass(bet_amount)) + PassLineOdds({4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3})
    """

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(BetPassLine(bet_amount),
                         BetPointOff(DontPass(bet_amount)),
                         PassLineOdds({4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}))


class FieldWinProgression(Strategy):
    def __init__(self, progression: list[typing.SupportsFloat]):
        """Every time the field wins move to the next progression, else restart
        at the beginning.

        Parameters
        ----------
        progression
            A list of bet amounts to make on the Field. As you win, progresses farther up list.
        """
        self.progression = progression
        self.current_progression = 0

    def after_roll(self, player: 'Player'):
        win = all(x for x in player.bets_on_table if x.get_status(player.table) == 'win')

        if win:
            self.current_progression += 1
        else:
            self.current_progression = 0

    def update_bets(self, player: 'Player'):
        if self.current_progression >= len(self.progression):
            bet_amount = self.progression[-1]
        else:
            bet_amount = self.progression[self.current_progression]
        IfBetNotExist(player.add_bet(Field(bet_amount)))


class DiceDoctor(FieldWinProgression):
    def __init__(self):
        """Field bet with a progression if you win of [10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150]
        """
        super().__init__([10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150])


class Place68CPR(Strategy):
    def __init__(self, bet_amount: float = 6):
        """If point is on place the 6 & 8. If you win press the bet. If you win again reduce the bet.

        Parameters
        ----------
        bet_amount
            The starting amount of bet to place.
        """
        self.starting_amount = bet_amount
        self.press_amount = 2 * self.starting_amount

        self.win_one_amount = bet_amount * (7 / 6)
        self.win_two_amount = bet_amount * 2 * (7 / 6)

        self.six_winnings = 0
        self.eight_winnings = 0

    def after_roll(self, player: 'Player'):
        """Get the winnings on the Place 6 and 8 bets to determine whether to press or regress.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        self.six_winnings = sum(x.get_win_amount(player.table) for x in player.bets_on_table if isinstance(x, Place6))
        self.eight_winnings = sum(x.get_win_amount(player.table) for x in player.bets_on_table if isinstance(x, Place8))

    def ensure_bets_exist(self, player: 'Player'):
        """Ensure that there is always a place 6 or place 8 bet if the point is On.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        for bet in (Place6(self.starting_amount), Place8(self.starting_amount)):
            BetIfTrue(bet, lambda p: p.table.point.status == 'On' and bet not in p.bets_on_table). \
                update_bets(player)

    def press(self, player: 'Player'):
        """Double the bet amount of the place bets.

        Parameters
        ----------
        player
            The player to make the bets for.
        """
        if self.six_winnings == self.win_one_amount:
            player.add_bet(Place6(self.starting_amount))
        if self.eight_winnings == self.win_one_amount:
            player.add_bet(Place8(self.starting_amount))

    def update_bets(self, player: 'Player'):
        """Ensure that a Place6 and Place8 bet always exist for the player of base amount.
        Press the bet if you win and haven't pressed the bet yet.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        self.ensure_bets_exist(player)
        self.press(player)


class Place68DontCome2Odds(AggregateStrategy):
    def __init__(self, six_eight_amount: float = 6,
                 dont_come_amount: float = 5):
        """Place the 6 and 8 along with a Don't Come bet with 2x odds.

        Parameters
        ----------
        six_eight_amount
            The amount of the Place6 and Place8 bet.
        dont_come_amount
            The amount of the DontCome bet.
        """
        super().__init__(BetPlace({6: six_eight_amount, 8: six_eight_amount}, skip_point=False),
                         BetIfTrue(DontCome(dont_come_amount),
                                   lambda p: not any(isinstance(x, DontCome) for x in p.bets_on_table)),
                         OddsStrategy(DontCome, 2))
