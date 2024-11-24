"""The strategies included in this module are completed strategies that are runnable by the player
in order to do the intended """

import typing

from crapssim.bet import Come, DontCome, DontPass, Field, PassLine, Place
from crapssim.strategy.core import (
    AggregateStrategy,
    BetIfTrue,
    BetPointOff,
    BetPointOn,
    CountStrategy,
    IfBetNotExist,
    Player,
    RemoveByType,
    RemoveIfTrue,
    Strategy,
)
from crapssim.strategy.odds import (
    DontPassOddsMultiplier,
    OddsMultiplier,
    PassLineOddsMultiplier,
)
from crapssim.strategy.single_bet import (
    BetCome,
    BetDontPass,
    BetField,
    BetPassLine,
    BetPlace,
    SimpleStrategyMode,
)


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
    """Places a PassLine bet and two Come bets. Equivalent to BetPassLine(amount) +
    TwoCome(amount)"""

    def __init__(self, bet_amount: float):
        """Place a PassLine bet and two Come bets of the given amount.

        Parameters
        ----------
        bet_amount
            The amount of the PassLine and Come bets.
        """
        self.bet_amount = bet_amount
        super().__init__(BetPassLine(bet_amount), TwoCome(bet_amount))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.bet_amount})"


class PassLinePlace68(AggregateStrategy):
    """Bet the PassLine and Place the 6 and the 8. Equivalent to: BetPassLine(pass_line_amount) +
    BetPlace({6: six_amount, 8: eight_amount}, skip_point=skip_point)"""

    def __init__(
        self,
        pass_line_amount: float = 5,
        six_amount: float = 6,
        eight_amount: float = 6,
        skip_point: bool = True,
    ):
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
        six_eight_strategy = BetPlace(
            {6: six_amount, 8: eight_amount}, skip_point=skip_point
        )
        super().__init__(pass_line_strategy, six_eight_strategy)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(pass_line_amount={self.pass_line_amount}, "
            f"six_amount={self.six_amount}, eight_amount={self.eight_amount}, "
            f"skip_point={self.skip_point})"
        )


class PlaceInside(AggregateStrategy):
    """Strategy to have Place bets on all the inside (5, 6, 8, 9) numbers.
    Equivalent to BetPlace({5: x, 6: 6/5*x, 8: 6/5*x, 9: x})"""

    def __init__(self, bet_amount: typing.SupportsFloat | dict[int, float]) -> None:
        """Creates a Strategy to have Place bets on all the inside (5, 6, 8, 9) numbers.

        Parameters
        ----------
        bet_amount
            Either a dictionary of the inside numbers (5, 6, 8, 9) and the bet amounts for each,
            or a number that supports float. If its a number that supports float, the six and eight
            amounts will be the number * (6 / 5) to make the payout a whole number.
        """
        self.bet_amount = bet_amount
        if isinstance(bet_amount, typing.SupportsFloat):
            six_eight_amount = float(bet_amount) * (6 / 5)
            amount_dict = {
                5: bet_amount,
                6: six_eight_amount,
                8: six_eight_amount,
                9: bet_amount,
            }
        else:
            amount_dict = bet_amount
        super().__init__(BetPlace(amount_dict, skip_point=False, skip_come=False))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.bet_amount})"


class Place68Move59(Strategy):
    """Strategy that makes place bets on the six and eight, and then if a PassLine or Come bet with
    that point comes up, moves the place bet to 5 or 9."""

    def __init__(
        self,
        pass_come_amount: float = 5,
        six_eight_amount: float = 6,
        five_nine_amount: float = 5,
    ):
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
        super().__init__()
        self.pass_come_amount = pass_come_amount
        self.six_eight_amount = six_eight_amount
        self.five_nine_amount = five_nine_amount

    def completed(self, player: Player) -> bool:
        """The strategy is completed if the player has no bets on the table, and the players
        bankroll is too low to make any of the other bets.

        Parameters
        ----------
        player
            The Player whose bankroll and bets to check.

        Returns
        -------
        True if the strategy can't continue, otherwise False.
        """
        return (
            len(player.bets) == 0
            and player.bankroll < self.pass_come_amount
            and player.bankroll < self.six_eight_amount
            and player.bankroll < self.five_nine_amount
        )

    def get_pass_line_come_points(self, player: Player) -> list[int]:
        """Get the point number (or the table point number in the case of PassLine) for any PassLine
        or Come bets on the table.

        Parameters
        ----------
        player
            The player to check the bets for.

        Returns
        -------
        A list of integers of the points for the PassLine and Come bets.
        """
        pass_line_come_points = []
        for number in (6, 8, 9, 10):
            if (
                player.table.point.number == number
                and PassLine(self.pass_come_amount) in player.bets
            ):
                pass_line_come_points.append(number)
            elif Come(self.pass_come_amount, number) in player.bets:
                pass_line_come_points.append(number)
        return pass_line_come_points

    def update_bets(self, player: Player) -> None:
        """Do nothing if the point status is Off, otherwise go through the numbers 6, 8, 5 and 9.
        If the player has both a PassLine or Come bet for that number and a Place bet, remove the
        Place bet, otherwise move on to the next number. If the player doesn't have a PassLine or
        Come bet for that number, and the place bet for that number isn't already on the table,
        make a Place bet for that number.

        Parameters
        ----------
        player
            The player to check on bets and add bets for.
        """
        place_amounts = {
            5: self.five_nine_amount,
            6: self.six_eight_amount,
            8: self.six_eight_amount,
            9: self.five_nine_amount,
        }

        if player.table.point.status == "Off":
            return

        for number in (6, 8, 5, 9):
            bet = Place(number, place_amounts[number])

            if number in self.get_pass_line_come_points(player):
                if bet in player.bets:
                    player.remove_bet(bet)
                continue

            if len([x for x in player.bets if isinstance(x, Place)]) < 2:
                IfBetNotExist(bet).update_bets(player)


class PassLinePlace68Move59(AggregateStrategy):
    """Strategy that makes a PassLine bet, makes Place bets on the six and eight, and then moves
    them back to the 5 and 9 if the point for the PassLine (also the tables point) is six or
    eight. Equivalent to BetPassLine(pass_line_amount) + Place68Move59(pass_line_amount,
    six_eight_amount, five_nine_amount)."""

    def __init__(
        self,
        pass_line_amount: float = 5,
        six_eight_amount: float = 6,
        five_nine_amount: float = 5,
    ):
        """Place a PassLine bet, Place the six and eight, and move them to 5 9 if the point for the
        PassLine bet is a 6 or 8.

        Equivalent to BetPassLine(...) + Place68Move59(...)

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
        super().__init__(
            BetPassLine(pass_line_amount),
            Place68Move59(pass_line_amount, six_eight_amount, five_nine_amount),
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(pass_line_amount={self.pass_line_amount}, "
            f"six_eight_amount={self.six_eight_amount}, "
            f"five_nine_amount={self.five_nine_amount})"
        )


class Place682Come(AggregateStrategy):
    """Strategy that bets the PassLine if the point is off and there are less than 4 bets on the
    table. If the point is On, places the 6 and 8 and if there are less than 2 Come bets on the
    table and less than 4 bets overall places a Come bet."""

    def __init__(
        self,
        pass_come_amount: float = 5,
        six_eight_amount: float = 6,
        five_nine_amount: float = 5,
        *strategies: Strategy,
    ):
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
        super().__init__(*strategies)
        self.pass_come_amount = pass_come_amount
        self.six_eight_amount = six_eight_amount
        self.five_nine_amount = five_nine_amount

    def update_bets(self, player: Player) -> None:
        """If the player has less than 2 PassLine and Come bets, make the bet (depending on whether
        the point is on or off.) If the point is on, place the 6 and 8 unless there is a PassLine or
        Come bet with those then move them to the 5 or 9.

        Parameters
        ----------
        player
            The player to check on and make the bets for.
        """

        pass_come_count = len(
            [x for x in player.bets if isinstance(x, (PassLine, Come))]
        )
        if pass_come_count < 2:
            BetPassLine(self.pass_come_amount).update_bets(player)  # if point off
            BetCome(self.pass_come_amount).update_bets(player)  # if point on

        Place68Move59(
            self.pass_come_amount, self.six_eight_amount, self.five_nine_amount
        ).update_bets(player)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(pass_come_amount={self.pass_come_amount}, "
            f"six_eight_amount={self.six_eight_amount}, "
            f"five_nine_amount={self.five_nine_amount})"
        )


class IronCross(AggregateStrategy):
    """Strategy that bets the PassLine, bets the PassLine Odds, and bets Place on the 5, 6, and 8.
    If the point is on and there is no bet on the field, place a bet on the field. Equivalent to:
    BetPassLine(...) + PassLineOddsMultiplier(2), + BetPlace({...}) + BetPointOn(Field(...))
    """

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
        place_amounts = {
            5: base_amount * 2,
            6: (6 / 5) * base_amount * 2,
            8: (6 / 5) * base_amount * 2,
        }

        super().__init__(
            BetPassLine(base_amount),
            PassLineOddsMultiplier(2),
            BetPlace(place_amounts, skip_point=True),
            BetPointOn(Field(base_amount)),
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(base_amount={self.base_amount})"


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

    def completed(self, player: Player) -> bool:
        """The strategy is completed if the player can no longer make the initial PassLine bet
        because their bankroll is too low, and they have no more bets on the table.

        Parameters
        ----------
        player

        Returns
        -------

        """
        return player.bankroll < self.base_amount and len(player.bets) == 0

    def after_roll(self, player: Player) -> None:
        """Update the place_win_count based on how many Place bets are won. If table.point.status is
        On and the dice total is 7 (meaning the shooter sevens out) reset place_win_count to 0.

        Parameters
        ----------
        player
        """
        place_bets = player.get_bets_by_type((Place,))
        winning_place_bets = [
            bet for bet in place_bets if bet.get_result(player.table).won
        ]
        self.place_win_count += len(winning_place_bets)
        if player.table.point.status == "On" and player.table.dice.total == 7:
            self.place_win_count = 0

    def update_bets(self, player: Player) -> None:
        """If the point is off bet the PassLine and DontPass line. If the point is on bet the
        Place6 and Place8 until one wins, then bet the Place 5, 6, 8, and 9. LayOdds whenever
        possible.

        Parameters
        ----------
        player
            Player to place the bets for.
        """
        if player.table.point.status == "Off":
            self.pass_and_dontpass(player)
        elif self.place_win_count == 0:
            self.place68(player)
        elif self.place_win_count == 1:
            self.place5689(player)
        elif self.place_win_count == 2:
            RemoveByType(Place).update_bets(player)
        DontPassOddsMultiplier(self.odds_multiplier).update_bets(player)

    def pass_and_dontpass(self, player: Player) -> None:
        """Update bets when point is Off: add a PassLine and a DontPass bet if they don't already exist."""
        RemoveByType(Place).update_bets(player)
        BetPassLine(
            self.base_amount, SimpleStrategyMode.ADD_IF_NON_EXISTENT
        ).update_bets(player)
        BetDontPass(
            self.base_amount, SimpleStrategyMode.ADD_IF_NON_EXISTENT
        ).update_bets(player)

    def place68(self, player: Player) -> None:
        """Update bets to Place the 6 and 8 (regardless of the point) and then lay odds on DontPass bets."""
        place_bet_amounts = {
            6: self.start_six_eight_amount,
            8: self.start_six_eight_amount,
        }
        BetPlace(place_bet_amounts, skip_point=False).update_bets(player)

    def place5689(self, player: Player) -> None:
        """Update bets to Place the 5, 6, 8 and 9."""
        RemoveByType(Place).update_bets(player)
        place_bet_amounts = {
            5: self.five_nine_amount,
            6: self.end_six_eight_amount,
            8: self.end_six_eight_amount,
            9: self.five_nine_amount,
        }
        BetPlace(place_bet_amounts, skip_point=False).update_bets(player)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(base_amount={self.base_amount})"


class Risk12(Strategy):
    """Strategy that makes a PassLine and Field bet before the point is established. Once the point
    is established, places either the 6 the 8, or both depending on if the player won enough
    pre-point to cover those bets."""

    def __init__(self) -> None:
        """Pass line and field bet before the point is established. Once the point is established
        place the 6 and 8.
        """
        super().__init__()
        self.pre_point_winnings: float = 0.0

    def completed(self, player: Player) -> bool:
        """The strategy is completed if the Player can no longer make the initial PassLine bet, and
        the player has no bets on the table.

        Parameters
        ----------
        player
            The player to check the bets and bankroll for.

        Returns
        -------
        True if the player can no longer continue the strategy, otherwise False.
        """
        return player.bankroll < 5 and len(player.bets) == 0

    def after_roll(self, player: Player) -> None:
        """Determine the pre-point winnings which is used to determine which bets to place when the
        point is on.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        bet_results = [x.get_result(player.table) for x in player.bets]
        if player.table.point.status == "Off" and any(x.won for x in bet_results):
            self.pre_point_winnings += sum(x.bankroll_change for x in bet_results)
        elif player.table.point.status == "On" and player.table.dice.total == 7:
            self.pre_point_winnings = 0

    @staticmethod
    def point_off(player: Player) -> None:
        """Place a 5 PassLine and Field bet.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        IfBetNotExist(PassLine(5)).update_bets(player)
        IfBetNotExist(Field(5)).update_bets(player)

    def point_on(self, player: Player) -> None:
        """If your winnings were enough to cover the place bets (throwing in another dollar for
        each) make the place bets.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        if self.pre_point_winnings >= 6 - 1:
            if player.table.point.number != 6:
                IfBetNotExist(Place(6, 6)).update_bets(player)
            else:
                IfBetNotExist(Place(8, 6)).update_bets(player)
        if self.pre_point_winnings >= 12 - 2:
            BetPlace({6: 6, 8: 6}).update_bets(player)

    def update_bets(self, player: Player) -> None:
        """If the point is off make a Field and PassLine bet. If the point is on
        Place the 6 and 8 if you made enough pre-point to cover the bets.

        Parameters
        ----------
        player
            The player to make the bets for.
        """
        if player.table.point.status == "Off":
            self.point_off(player)
        elif player.table.point.status == "On":
            self.point_on(player)


class Knockout(AggregateStrategy):
    """PassLine and Don't bet prior to point, 345x PassLine Odds after point.

    Equivalent to:
    BetPassLine(amount) + BetPointOff(DontPass(amount)) +
    PassLineOddsMultiplier({4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3})
    """

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        self.bet_amount = bet_amount
        super().__init__(
            BetPassLine(bet_amount),
            BetPointOff(DontPass(bet_amount)),
            PassLineOddsMultiplier({4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}),
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.bet_amount})"


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

    def completed(self, player: Player) -> bool:
        """If the players bankroll is below the minimum amount in the progression and if they
        have no more bets on the table the strategy is completed.

        Parameters
        ----------
        player
            The player to check the bankroll and bets for.

        Returns
        -------
        True if the
        """
        return (
            player.bankroll < min(float(x) for x in self.progression)
            and len(player.bets) == 0
        )

    def after_roll(self, player: Player) -> None:
        """If the field bet wins, increase the progression by 1, if it loses reset the progression
        to 0.

        Parameters
        ----------
        player
            The player to check the winning bets for.
        """

        win = all(x.get_result(player.table).won for x in player.bets)

        if win:
            self.current_progression += 1
        else:
            self.current_progression = 0

    def update_bets(self, player: Player) -> None:
        """If a field bet isn't on the table, place one for the current progression amount.

        Parameters
        ----------
        player
            The player to place the bet for.
        """
        if self.current_progression >= len(self.progression):
            bet_amount = self.progression[-1]
        else:
            bet_amount = self.progression[self.current_progression]
        IfBetNotExist(Field(bet_amount)).update_bets(player)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(progression={self.progression})"


class DiceDoctor(FieldWinProgression):
    """Field progression strategy with progressive increases and decreases. Equivalent to:
    FieldWinProgression([10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150])"""

    def __init__(self) -> None:
        """Field bet with a progression if you win of [10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75,
        150]
        """
        super().__init__([10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Place68CPR(Strategy):
    """Strategy that places the 6 and 8. If either of those bets win, the bet is pressed to 2 *
    the bet amount. If the bet is won again, it is reduced to the original bet amount.
    """

    def __init__(self, bet_amount: float = 6) -> None:
        """If point is on place the 6 & 8 of the amount. If you win press the bet 2 . If you win
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

        self.six_winnings = 0.0
        self.eight_winnings = 0.0

    def completed(self, player: Player) -> bool:
        """Returns True if the players bankroll is below the bet amount and the player no longer
        has bets on the table.

        Parameters
        ----------
        player

        Returns
        -------

        """
        return player.bankroll < self.starting_amount and len(player.bets) == 0

    def after_roll(self, player: Player) -> None:
        """Get the winnings on the Place 6 and 8 bets to determine whether to press or regress.

        Parameters
        ----------
        player
            The player to check the bets for.
        """
        place_bets = player.get_bets_by_type((Place,))
        place_six_bets = [x for x in place_bets if x.number == 6]
        place_six_win_amounts = [
            x.get_result(player.table).amount - x.amount
            for x in place_six_bets
            if x.get_result(player.table).won
        ]
        self.six_winnings = sum(place_six_win_amounts)
        place_eight_bets = [x for x in place_bets if x.number == 8]
        place_eight_win_amounts = [
            x.get_result(player.table).amount - x.amount
            for x in place_eight_bets
            if x.get_result(player.table).won
        ]
        self.eight_winnings = sum(place_eight_win_amounts)

    def ensure_bets_exist(self, player: Player) -> None:
        """Ensure that there is always a place 6 or place 8 bet if the point is On.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        if player.table.point.status == "Off":
            return
        for number in (6, 8):
            if (
                Place(number, self.starting_amount) not in player.bets
                and Place(number, self.press_amount) not in player.bets
            ):
                player.add_bet(Place(number, self.starting_amount))

    def press(self, player: Player) -> None:
        """Double the bet amount of the place bets.

        Parameters
        ----------
        player
            The player to make the bets for.
        """
        if self.six_winnings == self.win_one_amount:
            player.add_bet(Place(6, self.starting_amount))
        if self.eight_winnings == self.win_one_amount:
            player.add_bet(Place(8, self.starting_amount))

    def update_bets(self, player: Player) -> None:
        """Ensure that a Place6 and Place8 bet always exist for the player of base amount.
        Press the bet if you win and haven't pressed the bet yet.

        Parameters
        ----------
        player
            The player to place the bets for.
        """
        self.ensure_bets_exist(player)
        self.press(player)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.bet_amount})"


class Place68DontCome2Odds(AggregateStrategy):
    """Strategy that adds a DontCome bet when the point is Off, places the 6 and 8 when the point
    is On and adds 2x Odds to the DontCome bet."""

    def __init__(
        self, six_eight_amount: float = 6, dont_come_amount: float = 5
    ) -> None:
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
        super().__init__(
            BetPlace({6: six_eight_amount, 8: six_eight_amount}, skip_point=False),
            BetIfTrue(
                DontCome(dont_come_amount),
                lambda p: len(p.get_bets_by_type((DontCome,))) == 0,
            ),
            OddsMultiplier(DontCome, 2),
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(six_eight_amount={self.six_eight_amount}, "
            f"dont_come_amount={self.dont_come_amount})"
        )
