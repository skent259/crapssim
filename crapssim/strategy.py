import typing

from crapssim.bet import DontPass, LayOdds, DontCome
from crapssim.bet import Field
from crapssim.bet import PassLine, Odds, Come, Bet
from crapssim.bet import Place, Place4, Place5, Place6, Place8, Place9, Place10

if typing.TYPE_CHECKING:
    from crapssim import Player

"""
Various betting strategies that are based on conditions of the Crapsplayer.table.
Each strategy must take a player.table and a player_object, and implicitly 
uses the methods from the player object.
"""

"""
Fundamental Strategies
"""

STRATEGY_TYPE = typing.Union[typing.Callable[['Player', 'player.table', int, dict[str, int] | None], dict[str, int] | None],
                             typing.Callable[['Player', 'player.table', int, None], None]]


def passline(player: 'Player'):
    """ If the point is off place a bet on the Pass Line.

    Parameters
    ----------
    player
        Player object that is using the strategy.

    Returns
    -------
    None
        Dictionary of strategy info.
    """
    # Pass line bet
    if player.table.point == "Off" and not player.has_bets(PassLine):
        player.add_bet(PassLine(player.unit))


def passline_odds(player: 'Player', mult: int | str = 1) -> None:
    """ If the point is off place a bet on the Pass Line. If the point is on, bet the Pass Line Odds.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        mult
            Multiplier integers for the odds or "345" for 345x odds.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    passline(player)

    # Pass line odds
    if mult == "345":
        if player.table.point == "On":
            if player.table.point.number in [4, 10]:
                mult = 3
            elif player.table.point.number in [5, 9]:
                mult = 4
            elif player.table.point.number in [6, 8]:
                mult = 5
    else:
        mult = float(mult)

    if (
            player.table.point == "On"
            and player.has_bets(PassLine)
            and not player.has_bets(Odds)
    ):
        player.add_odds(player.table, mult * player.unit, [PassLine], point=player.table.point.number)


def passline_odds2(player: 'Player') -> None:
    """ Pass Line bet when point is off, 2x odds bet when point is on.

        Parameters
        ----------
        player
            Player object that is using the strategy.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    passline_odds(player, mult=2)


def passline_odds345(player: 'Player') -> None:
    """ Pass Line bet when point is off, 345x odds bet when point is on.

        Parameters
        ----------
        player
            Player object that is using the strategy.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    passline_odds(player, mult='345')


def pass2come(player: 'Player') -> None:
    """ Pass Line bet followed by 2 come bets when point is on.

        Parameters
        ----------
        player
            Player object that is using the strategy.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    passline(player)

    # Come bet (2)
    if player.table.point == "On" and player.count_bets(Come) < 2:
        player.add_bet(Come(player.unit))


def place(player: 'Player', skip_point: bool = True, numbers: set[int] | None = None) -> \
        None:
    """ Place bets, ie 3, 4, 5, 6, 8, 9, 10

        Parameters
        ----------
        player
            Player object that is using the strategy.
        numbers: set
            Point numbers to place bets on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """

    if numbers is None:
        numbers: set[int] = {6, 8}

    numbers = set(numbers).intersection({4, 5, 6, 8, 9, 10})

    if skip_point:
        numbers -= {player.table.point.number}

    # Place the provided numbers when point is ON
    if player.table.point == "On":
        if not player.has_bets(Place4) and 4 in numbers:
            player.add_bet(Place4(player.unit))
        if not player.has_bets(Place5) and 5 in numbers:
            player.add_bet(Place5(player.unit))
        if not player.has_bets(Place6) and 6 in numbers:
            player.add_bet(Place6(6 / 5 * player.unit))
        if not player.has_bets(Place8) and 8 in numbers:
            player.add_bet(Place8(6 / 5 * player.unit))
        if not player.has_bets(Place9) and 9 in numbers:
            player.add_bet(Place9(player.unit))
        if not player.has_bets(Place10) and 10 in numbers:
            player.add_bet(Place10(player.unit))

    # Move the bets off the point number if it shows up later
    if skip_point and player.table.point == "On":
        if player.has_bets(Place4) and player.table.point.number == 4:
            player.remove_bet(player.get_bet(Place4))
        if player.has_bets(Place5) and player.table.point.number == 5:
            player.remove_bet(player.get_bet(Place5))
        if player.has_bets(Place6) and player.table.point.number == 6:
            player.remove_bet(player.get_bet(Place6))
        if player.has_bets(Place8) and player.table.point.number == 8:
            player.remove_bet(player.get_bet(Place8))
        if player.has_bets(Place9) and player.table.point.number == 9:
            player.remove_bet(player.get_bet(Place9))
        if player.has_bets(Place10) and player.table.point.number == 10:
            player.remove_bet(player.get_bet(Place10))


def place68(player: 'Player') -> None:
    """ Place the 6 and the 8.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        player.table
            player.table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    passline(player)
    # Place 6 and 8 when point is ON
    p_has_place_bets = player.has_bets(
        Place4, Place5, Place6, Place8, Place9, Place10
    )
    if player.table.point == "On" and not p_has_place_bets:
        if player.table.point.number == 6:
            player.add_bet(Place8(6 / 5 * player.unit))
        elif player.table.point.number == 8:
            player.add_bet(Place6(6 / 5 * player.unit))
        else:
            player.add_bet(Place8(6 / 5 * player.unit))
            player.add_bet(Place6(6 / 5 * player.unit))


def dontpass(player: 'Player') -> None:
    """ Place a bet on the Don't Pass line.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        player.table
            player.table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    # Don't pass bet
    if player.table.point == "Off" and not player.has_bets(DontPass):
        player.add_bet(DontPass(player.unit))


def layodds(player: 'Player', win_mult: int | str = 1) -> None:
    """ Place a lay bet.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        player.table
            player.table object that the strategy is being used on.
        win_mult: str | int
            Either '345' or an integer that will be multiplied against the odds to calculate bet.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    # Assume that someone tries to win the `win_mult` times the unit on each bet, which corresponds
    # well to the max_odds on a player.table.
    # For `win_mult` = "345", this assumes max of 3-4-5x odds
    dontpass(player)
    mult = 1
    # Lay odds for don't pass
    if win_mult == "345":
        mult = 6.0
    else:
        win_mult = float(win_mult)
        if player.table.point == "On":
            if player.table.point.number in [4, 10]:
                mult = 2 * win_mult
            elif player.table.point.number in [5, 9]:
                mult = 3 / 2 * win_mult
            elif player.table.point.number in [6, 8]:
                mult = 6 / 5 * win_mult

    if (
            player.table.point == "On"
            and player.has_bets(DontPass)
            and not player.has_bets(LayOdds)
    ):
        player.add_odds(player.table, mult * player.unit, [DontPass], player.table.point.number)


"""
Detailed Strategies
"""


def place68_2come(player: 'Player') -> None:
    """ Once point is established, place 6 and 8, with 2 additional come bets.
        The goal is to be on four distinct numbers, moving place bets if necessary

        Parameters
        ----------
        player
            Player object that is using the strategy.
        player.table
            player.table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    """

    """
    current_numbers = []
    for bet in player.bets_on_table:
        current_numbers += bet.winning_numbers
    current_numbers = list(set(current_numbers))

    if player.table.point == "On" and len(player.bets_on_table) < 4:
        # always place 6 and 8 when they aren't come bets or place bets already
        if 6 not in current_numbers:
            player.add_bet(Place6(6 / 5 * player.unit))
        if 8 not in current_numbers:
            player.add_bet(Place8(6 / 5 * player.unit))

    # add come of passline bets to get on 4 numbers
    if player.count_bets(Come, PassLine) < 2 and len(player.bets_on_table) < 4:
        if player.table.point == "On":
            player.add_bet(Come(player.unit))
        if player.table.point == "Off" and (
                player.has_bets(Place6) or player.has_bets(Place8)
        ):
            player.add_bet(PassLine(player.unit))

    # if come bet or passline goes to 6 or 8, move place bets to 5 or 9
    pass_come_winning_numbers = []
    if player.has_bets(PassLine):
        pass_come_winning_numbers += player.get_bet(PassLine).winning_numbers
    if player.has_bets(Come):
        pass_come_winning_numbers += player.get_bet(Come).winning_numbers

    if 6 in pass_come_winning_numbers:
        if player.has_bets(Place6):
            player.remove_bet(player.get_bet(Place6))
        if 5 not in current_numbers:
            player.add_bet(Place5(player.unit))
        elif 9 not in current_numbers:
            player.add_bet(Place9(player.unit))
    elif 8 in pass_come_winning_numbers:
        if player.has_bets(Place8):
            player.remove_bet(player.get_bet(Place8))
        if 5 not in current_numbers:
            player.add_bet(Place5(player.unit))
        elif 9 not in current_numbers:
            player.add_bet(Place9(player.unit))


def ironcross(player: 'Player', mult: int | str = 1) -> None:
    """ Bet the Pass Line, the Pass Line Odds, and Place on 5, 6, and 8. If point is on and no bet on the field, place
        a bet on the field.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        player.table
            player.table object that the strategy is being used on.
        mult
            Either '345' or an integer that will be multiplied against the odds to calculate bet.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    passline(player)
    passline_odds(player, mult)
    place(player, numbers={5, 6, 8})

    if player.table.point == "On":
        if not player.has_bets(Field):
            player.add_bet(Field(player.unit))


def hammerlock(player: 'Player', mode: str | None = None) -> dict[str, str]:
    """ Pass Line Bet, Don't Pass bet with a lay of odds. A phased place bet approach, starting inside and then
        shifting outside eventually taking bet down if two place bets win.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        player.table
            player.table object that the strategy is being used on.
        mode: str
            Current phase of the Hammerlock, either "place68", "place_inside" or "takedown"

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    passline(player)
    layodds(player, win_mult="345")

    place_nums = set()
    for bet in player.bets_on_table:
        if isinstance(bet, Place):
            place_nums.add(bet.winning_numbers[0])
    place_point_nums = place_nums.copy()
    if player.table.point.number:
        place_point_nums.add(player.table.point.number)

    has_place68 = (6 in place_nums) or (8 in place_nums)
    has_place5689 = (
            (5 in place_nums) or (6 in place_nums) or (8 in place_nums) or (9 in place_nums)
    )
    # 3 phases, place68, place_inside, takedown
    if mode is None or player.table.point == "Off":
        mode = 'place68'
        for bet_nm in [Place5, Place6, Place8, Place9]:
            player.remove_if_present(bet_nm)

    if mode == "place68":
        if player.table.point == "On" and has_place68 and place_nums != {6, 8}:
            # assume that a place 6/8 has won
            if player.has_bets(Place6):
                player.remove_bet(player.get_bet(Place6))
            if player.has_bets(Place8):
                player.remove_bet(player.get_bet(Place8))
            mode = "place_inside"
            place(player, skip_point=False, numbers={5, 6, 8, 9})
        else:
            place(player, skip_point=False, numbers={6, 8})
    elif mode == "place_inside":
        if player.table.point == "On" and has_place5689 and place_nums != {5, 6, 8, 9}:
            # assume that a place 5/6/8/9 has won
            for bet_nm in [Place5, Place6, Place8, Place9]:
                player.remove_if_present(bet_nm)
            mode = "takedown"
        else:
            place(player, skip_point=False, numbers={5, 6, 8, 9})
    elif mode == "takedown" and player.table.point == "Off":
        mode = None

    player.strat_info['mode'] = mode


def risk12(player: 'Player', winnings: typing.SupportsFloat = 0) -> dict[str, int]:
    """ Pass line and field bet before the point is established. Once the point is established place the 6 and 8.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        player.table
            player.table object that the strategy is being used on.
        winnings: float
            Amount that has been won thus far.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    passline(player)

    if player.table.pass_rolls == 0:
        winnings = 0

    if player.table.point == "Off" and player.table.last_roll in player.table.settings["field_payouts"]:
        if player.table.settings["field_payouts"][player.table.last_roll] == 2:
            # win double from the field, lose pass line, for a net of 1 unit win
            winnings += player.unit
        elif player.table.settings["field_payouts"][player.table.last_roll] == 3:
            # win triple from the field, lose pass line, for a net of 2 unit win
            winnings += 2 * player.unit
        elif player.table.last_roll == 11:
            # win the field and pass line, for a net of 2 units win
            winnings += 2 * player.unit

    if player.table.point == "Off":
        player.add_bet(Field(player.unit))
        if player.table.last_roll == 7:
            for bet_nm in [Place6, Place8]:
                player.remove_if_present(bet_nm)
    elif player.table.point.number in [4, 9, 10]:
        place(player, numbers={6, 8})
    elif player.table.point.number in [5, 6, 8]:
        # lost field bet, so can't automatically cover the 6/8 bets.  Need to rely on potential early winnings
        if winnings >= 2 * player.unit:
            place(player, numbers={6, 8})
        elif winnings >= 1 * player.unit:
            if player.table.point.number != 6:
                place(player, numbers={6})
            else:
                place(player, numbers={8})

    player.strat_info['winnings'] = winnings


def knockout(player: 'Player') -> None:
    """ Pass line bet, don't pass bet, 345x odds behind the pass line bet.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        player.table
            player.table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    passline_odds345(player)
    dontpass(player)


def dicedoctor(player: 'Player', progression: int = 0) -> dict[str, int]:
    """ Field bet with a progression if you win.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        player.table
            player.table object that the strategy is being used on.
        progression
            How far into the progression list the strategy is

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    if player.table.last_roll not in player.table.settings['field_payouts']:
        progression = 0

    bet_progression = [10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150]
    if progression < len(bet_progression):
        amount = bet_progression[progression] * player.unit / 5
    elif progression % 2 == 0:
        # alternate between second to last and last
        amount = bet_progression[len(bet_progression) - 2] * player.unit / 5
    else:
        amount = bet_progression[len(bet_progression) - 1] * player.unit / 5

    player.add_bet(Field(amount))

    progression += 1

    player.strat_info['progression'] = progression


# def place68_cpr(player: 'Player', player.table: 'player.table', unit: int = 5, strat_info: dict[]=None) -> dict[str, str]:
#     """ place 6 & 8 after point is establish.  Then collect, press, and regress (in that order) on each win """
#     ## NOTE: NOT WORKING
#     if strat_info is None:
#         strat_info = {"mode6": "collect", "mode8": "collect"}
#
#     if player.table.point == "On":
#         # always place 6 and 8 when they aren't place bets already
#         if not player.has_bets("Place6"):
#             player.bet(Place6(6 / 5 * unit))
#         if not player.has_bets("Place8"):
#             player.bet(Place8(6 / 5 * unit))
#
#     if player.table.bet_update_info is not None:
#         # place6
#         if player.has_bets("Place6"):
#             bet = player.get_bet("Place6")
#             if (
#                 player.table.bet_update_info[player].get(bet.name) is not None
#             ):  # bet has not yet been updated; skip
#                 # print("level3")
#                 # print(player.table.bet_update_info[player][bet.name])
#                 if player.table.bet_update_info[player][bet.name]["status"] == "win":
#                     # print("place6 mode: {}".format(strat_info["mode6"]))
#                     if strat_info["mode6"] == "press":
#                         player.remove_bet(bet)
#                         player.bet(Place6(2 * bet.bet_amount))
#                         strat_info["mode6"] = "regress"
#                     elif strat_info["mode6"] == "regress":
#                         player.remove_bet(bet)
#                         player.bet(Place6(6 / 5 * unit))
#                         strat_info["mode6"] = "collect"
#                     elif strat_info["mode6"] == "collect":
#                         strat_info["mode6"] = "press"
#                     # print("updated place6 mode: {}".format(strat_info["mode6"]))
#         # place8
#         if player.has_bets("Place8"):
#             bet = player.get_bet("Place8")
#             if (
#                 player.table.bet_update_info[player].get(bet.name) is not None
#             ):  # bet has not yet been updated; skip
#                 # print("level3")
#                 # print(player.table.bet_update_info[player][bet.name])
#                 if player.table.bet_update_info[player][bet.name]["status"] == "win":
#                     # print("place8 mode: {}".format(strat_info["mode8"]))
#                     if strat_info["mode8"] == "press":
#                         player.remove_bet(bet)
#                         player.bet(Place8(2 * bet.bet_amount))
#                         strat_info["mode8"] = "regress"
#                     elif strat_info["mode8"] == "regress":
#                         player.remove_bet(bet)
#                         player.bet(Place8(6 / 5 * unit))
#                         strat_info["mode8"] = "collect"
#                     elif strat_info["mode8"] == "collect":
#                         strat_info["mode8"] = "press"
#
#     print(strat_info)
#     return strat_info


def place68_dontcome2odds(player: 'Player') -> None:
    """ Place the 6 and 8, bet don't come with 2x odds.

        Parameters
        ----------
        player
            Player object that is using the strategy.
        player.table
            player.table object that the strategy is being used on.

        Returns
        -------
        None
            Dictionary of strategy info.
        """
    place(player, skip_point=False, numbers={6, 8})

    current_numbers = []
    for bet in player.bets_on_table:
        current_numbers += bet.winning_numbers
    current_numbers = list(set(current_numbers))

    dont_come_losing_numbers = []
    if player.has_bets(DontCome):
        dont_come_losing_numbers += player.get_bet(DontCome).losing_numbers

    if 6 in dont_come_losing_numbers:
        if player.has_bets(Place6):
            player.remove_bet(player.get_bet(Place6))
        if 5 not in current_numbers:
            player.add_bet(Place5(player.unit))
    elif 8 in dont_come_losing_numbers:
        if player.has_bets(Place8):
            player.remove_bet(player.get_bet(Place8))
        if 9 not in current_numbers:
            player.add_bet(Place9(player.unit))

    if player.table.point == "On" and player.count_bets(DontCome) < 1:
        player.add_bet(DontCome(player.unit))

    if player.has_bets(DontCome):
        dc: Bet = player.get_bet(DontCome)

        if not isinstance(dc, DontCome):
            raise TypeError
        mult = 1
        win_mult: int | float = 2
        # Lay odds for don't come
        if win_mult == "345":
            mult = 6.0
        else:
            win_mult = float(win_mult)
            # print([[b.name, b.subname] for b in player.bets_on_player.table])
            if not dc.point is None:
                lose_num = dc.losing_numbers[0]
                if lose_num in [4, 10]:
                    mult = 2 * win_mult
                elif lose_num in [5, 9]:
                    mult = 3 / 2 * win_mult
                elif lose_num in [6, 8]:
                    mult = 6 / 5 * win_mult

        if not player.has_bets(LayOdds) and not dc.point is None:
            player.add_odds(player.table, mult * player.unit, [DontCome], dc.point)
