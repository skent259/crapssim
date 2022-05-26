"""The strategies included in this module are completed strategies that are runnable by the player
in order to do the intended """


import typing

from crapssim.bet import PassLine, DontPass, Come, DontCome, Place, Place6, Place8, \
    Place5, Place9, Field
from crapssim.strategy.core import CountStrategy, PlaceBetAndMove, BetPointOff, Strategy, \
    IfBetNotExist, BetIfTrue, AggregateStrategy, BetPointOn, RemoveIfTrue

if typing.TYPE_CHECKING:
    from crapssim.table import Player


class BetPassLine(BetPointOff):
    """Strategy that adds a PassLine bet if the point is Off and the player doesn't have a PassLine
    bet already on the table. Equivalent to BetPointOff(PassLine(bet_amount))."""
    def __init__(self, bet_amount: float):
        """Adds a PassLine bet for the given bet_amount if the point is Off and the player doesn't
        have a PassLine bet for that amount already on the table.

        Parameters
        ----------
        bet_amount
            The amount of the PassLine bet.
        """
        self.bet_amount = bet_amount
        super().__init__(PassLine(bet_amount))

    def __repr__(self):
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount})'


class OddsStrategy(Strategy):
    """Strategy that takes an AllowsOdds object and places Odds on it given either a multiplier,
    or a dictionary of points and multipliers."""
    def __init__(self, base_type: PassLine | DontPass | Come | DontCome,
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

    def get_odds_multiplier_repr(self):
        """If the odds_multiplier has multiple values return a dictionary with the values,
        if all the multipliers are the same return an integer of the multiplier."""
        if all([x == self.odds_multiplier[4] for x in self.odds_multiplier.values()]):
            odds_multiplier = self.odds_multiplier[4]
        else:
            odds_multiplier = self.odds_multiplier
        return odds_multiplier

    def __repr__(self):
        return f'{self.__class__.__name__}(base_type={self.base_type}, ' \
               f'odds_multiplier={self.get_odds_multiplier_repr()})'


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

    def __repr__(self):
        return f'{self.__class__.__name__}(odds_multiplier={self.get_odds_multiplier_repr()})'


class TwoCome(CountStrategy):
    """Strategy that adds a Come bet of a certain amount if that bet doesn't exist on the table.
    Equivalent to CountStrategy((Come, ), 2, bet)."""
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
    """Places a PassLine bet and two Come bets. Equivalent to BetPassLine(bet_amount) +
    TwoCome(bet_amount)"""
    def __init__(self, bet_amount: float):
        """Place a PassLine bet and two Come bets of the given bet_amount.

        Parameters
        ----------
        bet_amount
            The amount of the PassLine and Come bets.
        """
        self.bet_amount = bet_amount
        super().__init__(BetPassLine(bet_amount), TwoCome(bet_amount))

    def __repr__(self):
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount})'


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

    def __repr__(self):
        return f'{self.__class__.__name__}(place_bet_amounts={self.place_bet_amounts},' \
               f' skip_point={self.skip_point})'


class PassLinePlace68(AggregateStrategy):
    """Bet the PassLine and Place the 6 and the 8. Equivalent to: BetPassLine(pass_line_amount) +
        BetPlace({6: six_amount, 8: eight_amount}, skip_point=skip_point)"""
    def __init__(self,
                 pass_line_amount: float = 5,
                 six_amount: float = 6,
                 eight_amount: float = 6,
                 skip_point: bool = True):
        """Bet the PassLine and Place the 6 and the 8. Equivalent to:
        BetPassLine(pass_line_amount) +
        BetPlace({6: six_amount, 8: eight_amount}, skip_point=skip_point)

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
        self.pass_line_amount = pass_line_amount
        self.six_amount = six_amount
        self.eight_amount = eight_amount
        self.skip_point = skip_point

        pass_line_strategy = BetPassLine(pass_line_amount)
        six_eight_strategy = BetPlace({6: six_amount, 8: eight_amount}, skip_point=skip_point)
        super().__init__(pass_line_strategy, six_eight_strategy)

    def __repr__(self):
        return f'{self.__class__.__name__}(pass_line_amount={self.pass_line_amount}, ' \
               f'six_amount={self.six_amount}, eight_amount={self.eight_amount}, ' \
               f'skip_point={self.skip_point})'


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

    def __repr__(self):
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount})'


class BetLayOdds(OddsStrategy):
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

    def __repr__(self):
        return f'{self.__class__.__name__}(odds_multiplier={self.get_odds_multiplier_repr()})'


class Place68Move59(PlaceBetAndMove):
    """Strategy that makes place bets on the six and eight, and then if a PassLine or Come bet with
    that point comes up, moves to the place bet to 5 or 9.

        Equivalent to:
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

        PlaceBetAndMove(starting_bets, check_bets, bet_movements)"""
    def __init__(self, pass_come_amount: float = 5,
                 six_eight_amount: float = 6,
                 five_nine_amount: float = 5):
        """Makes Place bets of 6 and 8 for the six_eight_amount, then if a PassLine or Come bet
        comes with the pass_come_amount, moves those bets to the five and nine with the
        five_nine_amount.

        Parameters
        ----------
        pass_come_amount
            The amount of the PassLine and Come bets.
        six_eight_amount
            The amount of the Place6 and Place8 bets.
        five_nine_amount
            The amount of the Place5 and Place9 bets.
        """
        self.pass_come_amount = pass_come_amount
        self.six_eight_amount = six_eight_amount
        self.five_nine_amount = five_nine_amount
        super().__init__(starting_bets=[Place6(six_eight_amount),
                                        Place8(six_eight_amount)],
                         check_bets=[PassLine(pass_come_amount),
                                     PassLine(pass_come_amount),
                                     Come(pass_come_amount, point=6),
                                     Come(pass_come_amount, point=8)],
                         bet_movements={Place6(six_eight_amount): Place5(5),
                                        Place8(six_eight_amount): Place5(5),
                                        Place5(five_nine_amount): Place9(five_nine_amount),
                                        Place9(five_nine_amount): None})

    def __repr__(self):
        return f'{self.__class__.__name__}(pass_come_amount={self.pass_come_amount}, ' \
               f'six_eight_amount={self.six_eight_amount}, ' \
               f'five_nine_amount={self.five_nine_amount})'


class PassLinePlace68Move59(AggregateStrategy):
    """Strategy that makes a PassLine bet, makes Place bets on the six and eight, and then moves
    them back to the 5 and 9 if the point for the PassLine (also the tables point) is six or
    eight. Equivalent to BetPassLine(pass_line_amount) + Place68Move59(pass_line_amount,
    six_eight_amount, five_nine_amount)."""
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
        self.pass_line_amount = pass_line_amount
        self.six_eight_amount = six_eight_amount
        self.five_nine_amount = five_nine_amount
        pass_line_strategy = BetPassLine(pass_line_amount)
        place_bet_and_move_strategy = Place68Move59(pass_line_amount,
                                                    six_eight_amount,
                                                    five_nine_amount)
        super().__init__(pass_line_strategy, place_bet_and_move_strategy)

    def __repr__(self):
        return f'{self.__class__.__name__}(pass_line_amount={self.pass_line_amount}, ' \
               f'six_eight_amount={self.six_eight_amount}, ' \
               f'five_nine_amount={self.five_nine_amount})'


class Place682Come(AggregateStrategy):
    """Strategy that makes place bets on the 6 and 8 places two come bets moving the six and eight
    to five or nine if the Come or PassLine bets points come up to those numbers. Also, if there is
    a Place6 or Place8 bet and the point if Off make a PassLine bet."""
    def __init__(self, pass_come_amount: float = 5,
                 six_eight_amount: float = 6,
                 five_nine_amount: float = 5):
        """Place the six and the eight and place two come bets moving the six and eight to five or
        nine if the Come or PassLine bets points come up to those numbers. Also, if there is a
        Place6 or Place8 bet and the point if Off make a PassLine bet.

        Parameters
        ----------
        pass_come_amount
            The amount of the Come bet.
        six_eight_amount
            The amount of the Place6 and Place8 bets.
        five_nine_amount
            The amount of the Place5 and Place9 bets.
        """
        self.pass_come_amount = pass_come_amount
        self.six_eight_amount = six_eight_amount
        self.five_nine_amount = five_nine_amount

        def pass_line_key(player: "Player") -> bool:
            return (player.table.point.status == 'Off' and
             any(isinstance(x, (Place6, Place8)) for x in player.bets_on_table) and
             player.count_bets(Place, PassLine, Come) < 4)

        pass_line_strategy = BetIfTrue(PassLine(pass_come_amount), pass_line_key)

        def come_key(player: "Player") -> bool:
            come_count = len([b for b in player.bets_on_table if isinstance(b, Come)])
            place_passline_come_count = len(
                [b for b in player.bets_on_table if isinstance(b, (PassLine, Come, Place))]
            )
            return player.table.point.status == 'On' \
                   and place_passline_come_count < 4 and come_count < 2

        come_strategy = BetIfTrue(Come(pass_come_amount), come_key)
        place_strategy = Place68Move59(pass_come_amount=pass_come_amount,
                                       six_eight_amount=six_eight_amount,
                                       five_nine_amount=five_nine_amount)
        super().__init__(pass_line_strategy, come_strategy, place_strategy)

    def __repr__(self):
        return f'{self.__class__.__name__}(pass_come_amount={self.pass_come_amount}, ' \
               f'six_eight_amount={self.six_eight_amount}, ' \
               f'five_nine_amount={self.five_nine_amount})'


class IronCross(AggregateStrategy):
    """Strategy that bets the PassLine, bets the PassLine Odds, and bets Place on the 5, 6, and 8.
    If the point is on and there is no bet on the field, place a bet on the field. Equivalent to:
    BetPassLine(...) + PassLineOdds(2), + BetPlace({...}) + BetPointOn(Field(...))"""
    def __init__(self, base_amount: float):
        """Creates the IronCross strategy based on the base_amount, using that number to determine
        the amounts for all the other numbers.

        Parameters
        ----------
        base_amount
            The base amount of the bets. This amount is used for the PassLine and Field.
            base_amount * (6/5) * 2 is used for placing the six and eight, and base amount * 2
            is used for placing the five.
        """
        self.base_amount = base_amount
        place_six_eight_amount = (6 / 5) * base_amount * 2
        place_five_amount = base_amount * 2

        super().__init__(BetPassLine(base_amount),
                         PassLineOdds(2),
                         BetPlace({5: place_five_amount,
                                   6: place_six_eight_amount,
                                   8: place_six_eight_amount}),
                         BetPointOn(Field(base_amount)))


    def __repr__(self):
        return f'{self.__class__.__name__}(base_amount={self.base_amount})'


class HammerLock(Strategy):
    """Strategy that makes a PassLine bet and a DontPass bet when the point is off. Once the point
    is on, adds LayOdds to the DontPass bet, and Places the 6 and 8. If either of those place bets
    win, shifts the bets outside to the 5, 6, 8, and 9. If one of those wins, all place bets get
    taken down.
    """
    def __init__(self, base_amount: float):
        """Creates the HammerLock strategy with all bet amounts being created from the given
        base_amount.

        Parameters
        ----------
        base_amount
            the base amount for PassLine and DontPass Bets, and Place5 and Place9 bets. Place6 and
            Place8 starts at (6/5) * 2 * this amount and if it wins moves to (6 / 5) * this amount.
        """
        self.base_amount = base_amount
        self.start_six_eight_amount = (6 / 5) * base_amount * 2
        self.end_six_eight_amount = (6 / 5) * base_amount
        self.five_nine_amount = base_amount
        self.odds_multiplier = 6

        self.place_win_count: int = 0

    def after_roll(self, player: 'Player') -> None:
        """Update the place_win_count based on how many Place bets are won. If table.point.status is
        On and the dice total is 7 (meaning the shooter sevens out) reset place_win_count to 0.

        Parameters
        ----------
        player
        """
        place_bets = [bet for bet in player.bets_on_table if isinstance(bet, Place)]
        winning_place_bets = [bet for bet in place_bets if bet.get_status(player.table) == 'win']
        self.place_win_count += len(winning_place_bets)
        if player.table.point.status == 'On' and player.table.dice.total == 7:
            self.place_win_count = 0

    def point_off(self, player: "Player") -> None:
        """If the point is Off add a PassLine and a DontPass bet if they don't already exist.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        RemoveIfTrue(lambda b, p: isinstance(b, Place)).update_bets(player)
        strategy = IfBetNotExist(PassLine(self.base_amount)) + \
                   IfBetNotExist(DontPass(self.base_amount))
        strategy.update_bets(player)

    def place68(self, player: "Player") -> None:
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

    def place5689(self, player: "Player") -> None:
        """Place the 5, 6, 8 and 9.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        RemoveIfTrue(lambda b, p: isinstance(b, Place)).update_bets(player)
        BetPlace({5: self.five_nine_amount,
                  6: self.end_six_eight_amount,
                  8: self.end_six_eight_amount,
                  9: self.five_nine_amount}, skip_point=False).update_bets(player)

    def update_bets(self, player: 'Player') -> None:
        """If the point is off bet the PassLine and DontPass line. If the point is on bet the
        Place6 and Place8 until one wins, then bet the Place 5, 6, 8, and 9. LayOdds whenever
        possible.

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

    def __repr__(self):
        return f'{self.__class__.__name__}(base_amount={self.base_amount})'


class Risk12(Strategy):
    """Strategy that makes a PassLine and Field bet before the point is established. Once the point
    is established, places either the 6 the 8, or both depending on if the player won enough
    pre-point to cover those bets."""
    def __init__(self) -> None:
        """Pass line and field bet before the point is established. Once the point is established
        place the 6 and 8.
        """
        super().__init__()
        self.pre_point_winnings = 0

    def after_roll(self, player: 'Player') -> None:
        """Determine the pre-point winnings which is used to determine which bets to place when the
        point is on.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        if player.table.point.status == 'Off' and any(
                x.get_status(player.table) == 'win' for x in player.bets_on_table):
            self.pre_point_winnings += sum(x.get_return_amount(player.table)
                                           for x in player.bets_on_table
                                           if x.get_status(player.table) == 'win')
        elif player.table.point.status == 'On' and player.table.dice.total == 7:
            self.pre_point_winnings = 0

    @staticmethod
    def point_off(player: 'Player') -> None:
        """Place a 5 PassLine and Field bet.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        RemoveIfTrue(lambda b, p: isinstance(b, Place)
                                  and p.table.last_roll is not None
                                  and p.table.last_roll == 7).update_bets(player)
        IfBetNotExist(PassLine(5)).update_bets(player)
        IfBetNotExist(Field(5)).update_bets(player)

    def point_on(self, player: 'Player') -> None:
        """If your winnings were enough to cover the place bets (throwing in another dollar for
        each) make the place bets.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        if self.pre_point_winnings >= 6 - 1:
            if player.table.point.number != 6:
                IfBetNotExist(Place6(6)).update_bets(player)
            else:
                IfBetNotExist(Place8(6)).update_bets(player)
        if self.pre_point_winnings >= 12 - 2:
            BetPlace({6: 6, 8: 6}).update_bets(player)

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
    BetPassLine(bet_amount) + BetPointOff(DontPass(bet_amount)) +
    PassLineOdds({4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3})
    """

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        self.bet_amount = bet_amount
        super().__init__(BetPassLine(bet_amount),
                         BetPointOff(DontPass(bet_amount)),
                         PassLineOdds({4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}))

    def __repr__(self):
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount})'


class FieldWinProgression(Strategy):
    """Strategy that every time a Field bet is won, moves to the next amount in the progression and
    places a Field bet for that amount."""
    def __init__(self, progression: list[typing.SupportsFloat]) -> None:
        """Creates the given the progression.

        Parameters
        ----------
        progression
            A list of bet amounts to make on the Field. As you win, progresses farther up list.
        """
        self.progression = progression
        self.current_progression = 0

    def after_roll(self, player: 'Player') -> None:
        win = all(x for x in player.bets_on_table if x.get_status(player.table) == 'win')

        if win:
            self.current_progression += 1
        else:
            self.current_progression = 0

    def update_bets(self, player: 'Player') -> None:
        if self.current_progression >= len(self.progression):
            bet_amount = self.progression[-1]
        else:
            bet_amount = self.progression[self.current_progression]
        IfBetNotExist(player.add_bet(Field(bet_amount)))

    def __repr__(self):
        return f'{self.__class__.__name__}(progression={self.progression})'


class DiceDoctor(FieldWinProgression):
    """Field progression strategy with progressive increases and decreases. Equivalent to:
    FieldWinProgression([10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150])"""
    def __init__(self) -> None:
        """Field bet with a progression if you win of [10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75,
        150]
        """
        super().__init__([10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150])

    def __repr__(self):
        return f'{self.__class__.__name__}()'


class Place68CPR(Strategy):
    """Strategy that places the 6 and 8. If either of those bets win, the bet is pressed to 2 *
    the bet amount. If the bet is won again, it is reduced to the original bet amount."""

    def __init__(self, bet_amount: float = 6) -> None:
        """If point is on place the 6 & 8 of the bet_amount. If you win press the bet 2 . If you win
        again reduce the bet.

        Parameters
        ----------
        bet_amount
            The starting amount of bet to place.
        """
        self.bet_amount = bet_amount
        self.starting_amount = bet_amount
        self.press_amount = 2 * self.starting_amount

        self.win_one_amount = bet_amount * (7 / 6)
        self.win_two_amount = bet_amount * 2 * (7 / 6)

        self.six_winnings = 0
        self.eight_winnings = 0

    def after_roll(self, player: 'Player') -> None:
        """Get the winnings on the Place 6 and 8 bets to determine whether to press or regress.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        place_six_bets = [x for x in player.bets_on_table if isinstance(x, Place6)]
        place_six_win_amounts = [x.get_win_amount(player.table) for x in place_six_bets]
        self.six_winnings = sum(place_six_win_amounts)
        place_eight_bets = [x for x in player.bets_on_table if isinstance(x, Place8)]
        place_eight_win_amounts = [x.get_win_amount(player.table) for x in place_eight_bets]
        self.eight_winnings = sum(place_eight_win_amounts)

    def ensure_bets_exist(self, player: 'Player') -> None:
        """Ensure that there is always a place 6 or place 8 bet if the point is On.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        for bet in (Place6(self.starting_amount), Place8(self.starting_amount)):
            BetPointOn(bet).update_bets(player)

    def press(self, player: 'Player') -> None:
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

    def update_bets(self, player: 'Player') -> None:
        """Ensure that a Place6 and Place8 bet always exist for the player of base amount.
        Press the bet if you win and haven't pressed the bet yet.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        self.ensure_bets_exist(player)
        self.press(player)

    def __repr__(self):
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount})'


class Place68DontCome2Odds(AggregateStrategy):
    """Strategy that adds a DontCome bet when the point is Off, places the 6 and 8 when the point
    is On and adds 2x Odds to the DontCome bet."""
    def __init__(self, six_eight_amount: float = 6,
                 dont_come_amount: float = 5) -> None:
        """Place the 6 and 8 along with a Don't Come bet with 2x odds.

        Parameters
        ----------
        six_eight_amount
            The amount of the Place6 and Place8 bet.
        dont_come_amount
            The amount of the DontCome bet.
        """
        self.six_eight_amount = six_eight_amount
        self.dont_come_amount = dont_come_amount
        super().__init__(BetPlace({6: six_eight_amount, 8: six_eight_amount}, skip_point=False),
                         BetIfTrue(DontCome(dont_come_amount),
                                   lambda p: not any(isinstance(x, DontCome)
                                                     for x in p.bets_on_table)),
                         OddsStrategy(DontCome, 2))

    def __repr__(self):
        return f'{self.__class__.__name__}(six_eight_amount={self.six_eight_amount}, ' \
               f'dont_come_amount={self.dont_come_amount})'
