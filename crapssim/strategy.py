import typing

from crapssim.bet import DontPass, LayOdds, DontCome
from crapssim.bet import Field
from crapssim.bet import PassLine, Odds, Come, Bet
from crapssim.bet import Place, Place4, Place5, Place6, Place8, Place9, Place10

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

STRATEGY_TYPE = typing.Union[typing.Callable[['Player', 'Table', int, dict[str, int] | None], dict[str, int] | None],
                             typing.Callable[['Player', 'Table', int, None], None]]


def passline(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None) -> None:
    # Pass line bet
    if table.point == "Off" and not player.has_bet("PassLine"):
        player.bet(PassLine(unit), table)


def passline_odds(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None,
                  mult: int | str | float = 1) -> None:
    passline(player, table, unit)
    # Pass line odds
    if mult == "345":
        if table.point == "On":
            if table.point.number in [4, 10]:
                mult = 3
            elif table.point.number in [5, 9]:
                mult = 4
            elif table.point.number in [6, 8]:
                mult = 5
    else:
        mult = float(mult)

    if (
            table.point == "On"
            and player.has_bet("PassLine")
            and not player.has_bet("Odds")
    ):
        player.bet(Odds(float(mult * unit), player.get_bet("PassLine")), table)


def passline_odds2(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None) -> None:
    passline_odds(player, table, unit, strat_info=None, mult=2)


def passline_odds345(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None) -> None:
    passline_odds(player, table, unit, strat_info=None, mult="345")


def pass2come(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None) -> None:
    passline(player, table, unit)

    # Come bet (2)
    if table.point == "On" and player.num_bet("Come") < 2:
        player.bet(Come(unit), table)


def place(player: 'Player', table: 'Table', unit: int | float = 5,
          strat_info: dict[str, set] | None = None, skip_point: bool = True) -> None:
    if strat_info is None:
        strat_info = {"numbers": {6, 8}}
    strat_info["numbers"] = set(strat_info["numbers"]).intersection({4, 5, 6, 8, 9, 10})
    if skip_point:
        strat_info["numbers"] -= {table.point.number}

    # Place the provided numbers when point is ON
    if table.point == "On":
        if not player.has_bet("Place4") and 4 in strat_info["numbers"]:
            player.bet(Place4(unit), table)
        if not player.has_bet("Place5") and 5 in strat_info["numbers"]:
            player.bet(Place5(unit), table)
        if not player.has_bet("Place6") and 6 in strat_info["numbers"]:
            player.bet(Place6(6 / 5 * unit), table)
        if not player.has_bet("Place8") and 8 in strat_info["numbers"]:
            player.bet(Place8(6 / 5 * unit), table)
        if not player.has_bet("Place9") and 9 in strat_info["numbers"]:
            player.bet(Place9(unit), table)
        if not player.has_bet("Place10") and 10 in strat_info["numbers"]:
            player.bet(Place10(unit), table)

    # Move the bets off the point number if it shows up later
    if skip_point and table.point == "On":
        if player.has_bet("Place4") and table.point.number == 4:
            player.remove(player.get_bet("Place4"))
        if player.has_bet("Place5") and table.point.number == 5:
            player.remove(player.get_bet("Place5"))
        if player.has_bet("Place6") and table.point.number == 6:
            player.remove(player.get_bet("Place6"))
        if player.has_bet("Place8") and table.point.number == 8:
            player.remove(player.get_bet("Place8"))
        if player.has_bet("Place9") and table.point.number == 9:
            player.remove(player.get_bet("Place9"))
        if player.has_bet("Place10") and table.point.number == 10:
            player.remove(player.get_bet("Place10"))


def place68(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None) -> None:
    passline(player, table, unit, strat_info=None)
    # Place 6 and 8 when point is ON
    p_has_place_bets = player.has_bet(
        "Place4", "Place5", "Place6", "Place8", "Place9", "Place10"
    )
    if table.point == "On" and not p_has_place_bets:
        if table.point.number == 6:
            player.bet(Place8(6 / 5 * unit), table)
        elif table.point.number == 8:
            player.bet(Place6(6 / 5 * unit), table)
        else:
            player.bet(Place8(6 / 5 * unit), table)
            player.bet(Place6(6 / 5 * unit), table)


def dontpass(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None) -> None:
    # Don't pass bet
    if table.point == "Off" and not player.has_bet("DontPass"):
        player.bet(DontPass(unit), table)


def layodds(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None,
            win_mult: typing.SupportsFloat | str = 1) -> None:
    # Assume that someone tries to win the `win_mult` times the unit on each bet, which corresponds
    # well to the max_odds on a table.
    # For `win_mult` = "345", this assumes max of 3-4-5x odds
    dontpass(player, table, unit)
    mult = 1
    # Lay odds for don't pass
    if win_mult == "345":
        mult = 6.0
    else:
        win_mult = float(win_mult)
        if table.point == "On":
            if table.point.number in [4, 10]:
                mult = 2 * win_mult
            elif table.point.number in [5, 9]:
                mult = 3 / 2 * win_mult
            elif table.point.number in [6, 8]:
                mult = 6 / 5 * win_mult

    if (
            table.point == "On"
            and player.has_bet("DontPass")
            and not player.has_bet("LayOdds")
    ):
        player.bet(LayOdds(mult * unit, player.get_bet("DontPass")), table)


"""
Detailed Strategies
"""


def place68_2come(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None) -> None:
    """
    Once point is established, place 6 and 8, with 2 additional come bets.
    The goal is to be on four distinct numbers, moving place bets if necessary
    """
    current_numbers = []
    for bet in player.bets_on_table:
        current_numbers += bet.winning_numbers
    current_numbers = list(set(current_numbers))

    if table.point == "On" and len(player.bets_on_table) < 4:
        # always place 6 and 8 when they aren't come bets or place bets already
        if 6 not in current_numbers:
            player.bet(Place6(6 / 5 * unit), table)
        if 8 not in current_numbers:
            player.bet(Place8(6 / 5 * unit), table)

    # add come of passline bets to get on 4 numbers
    if player.num_bet("Come", "PassLine") < 2 and len(player.bets_on_table) < 4:
        if table.point == "On":
            player.bet(Come(unit), table)
        if table.point == "Off" and (
                player.has_bet("Place6") or player.has_bet("Place8")
        ):
            player.bet(PassLine(unit), table)

    # if come bet or passline goes to 6 or 8, move place bets to 5 or 9
    pass_come_winning_numbers = []
    if player.has_bet("PassLine"):
        pass_come_winning_numbers += player.get_bet("PassLine").winning_numbers
    if player.has_bet("Come"):
        pass_come_winning_numbers += player.get_bet("Come", "Any").winning_numbers

    if 6 in pass_come_winning_numbers:
        if player.has_bet("Place6"):
            player.remove(player.get_bet("Place6"))
        if 5 not in current_numbers:
            player.bet(Place5(unit), table)
        elif 9 not in current_numbers:
            player.bet(Place9(unit), table)
    elif 8 in pass_come_winning_numbers:
        if player.has_bet("Place8"):
            player.remove(player.get_bet("Place8"))
        if 5 not in current_numbers:
            player.bet(Place5(unit), table)
        elif 9 not in current_numbers:
            player.bet(Place9(unit), table)


def ironcross(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None) -> None:
    passline(player, table, unit)
    passline_odds(player, table, unit, strat_info=None, mult=2)
    place(player, table, 2 * unit, strat_info={"numbers": {5, 6, 8}})

    if table.point == "On":
        if not player.has_bet("Field"):
            player.bet(
                Field(
                    unit,
                    double=table.payouts["fielddouble"],
                    triple=table.payouts["fieldtriple"],
                ), table
            )


def hammerlock(player: 'Player', table: 'Table', unit: int = 5, strat_info: dict[str, str] | None = None) \
        -> dict[str, str] | None:
    passline(player, table, unit)
    layodds(player, table, unit, win_mult="345")

    if strat_info is None:
        strat_info = {}

    place_nums = set()
    for bet in player.bets_on_table:
        if isinstance(bet, Place):
            place_nums.add(bet.winning_numbers[0])
    place_point_nums = place_nums.copy()
    if table.point.number:
        place_point_nums.add(table.point.number)

    has_place68 = (6 in place_nums) or (8 in place_nums)
    has_place5689 = (
            (5 in place_nums) or (6 in place_nums) or (8 in place_nums) or (9 in place_nums)
    )

    # 3 phases, place68, place_inside, takedown
    if strat_info is None or table.point == "Off":
        strat_info = {"mode": "place68"}
        for bet_nm in ["Place5", "Place6", "Place8", "Place9"]:
            player.remove_if_present(bet_nm)

    if strat_info["mode"] == "place68":
        if table.point == "On" and has_place68 and place_nums != {6, 8}:
            # assume that a place 6/8 has won
            if player.has_bet("Place6"):
                player.remove(player.get_bet("Place6"))
            if player.has_bet("Place8"):
                player.remove(player.get_bet("Place8"))
            strat_info["mode"] = "place_inside"
            place(
                player,
                table,
                unit,
                strat_info={"numbers": {5, 6, 8, 9}},
                skip_point=False,
            )
        else:
            place(
                player,
                table,
                2 * unit,
                strat_info={"numbers": {6, 8}},
                skip_point=False,
            )
    elif strat_info["mode"] == "place_inside":
        if table.point == "On" and has_place5689 and place_nums != {5, 6, 8, 9}:
            # assume that a place 5/6/8/9 has won
            for bet_nm in ["Place5", "Place6", "Place8", "Place9"]:
                player.remove_if_present(bet_nm)
            strat_info["mode"] = "takedown"
        else:
            place(
                player,
                table,
                unit,
                strat_info={"numbers": {5, 6, 8, 9}},
                skip_point=False,
            )
    elif strat_info["mode"] == "takedown" and table.point == "Off":
        strat_info = None

    return strat_info


def risk12(player: 'Player', table: 'Table', unit: int = 5, strat_info: None | dict[str, int] = None) -> dict[str, int]:
    passline(player, table, unit)

    if strat_info is None:
        strat_info = dict()

    if table.pass_rolls == 0:
        strat_info = {"winnings": 0}
    elif table.point == "Off":
        if table.last_roll in table.payouts["fielddouble"]:
            # win double from the field, lose pass line, for a net of 1 unit win
            strat_info["winnings"] += unit
        elif table.last_roll in table.payouts["fieldtriple"]:
            # win triple from the field, lose pass line, for a net of 2 unit win
            strat_info["winnings"] += 2 * unit
        elif table.last_roll == 11:
            # win the field and pass line, for a net of 2 units win
            strat_info["winnings"] += 2 * unit

    if table.point == "Off":
        player.bet(
            Field(
                unit,
                double=table.payouts["fielddouble"],
                triple=table.payouts["fieldtriple"],
            ), table
        )
        if table.last_roll == 7:
            for bet_nm in ["Place6", "Place8"]:
                player.remove_if_present(bet_nm)
    elif table.point.number in [4, 9, 10]:
        place(player, table, unit, strat_info={"numbers": {6, 8}})
    elif table.point.number in [5, 6, 8]:
        # lost field bet, so can't automatically cover the 6/8 bets.  Need to rely on potential early winnings
        if strat_info["winnings"] >= 2 * unit:
            place(player, table, unit, strat_info={"numbers": {6, 8}})
        elif strat_info["winnings"] >= 1 * unit:
            if table.point.number != 6:
                place(player, table, unit, strat_info={"numbers": {6}})
            else:
                place(player, table, unit, strat_info={"numbers": {8}})

    return strat_info


def knockout(player: 'Player', table: 'Table', unit: int = 5, strat_info: None = None) -> None:
    passline_odds345(player, table, unit)
    dontpass(player, table, unit)


def dicedoctor(player: 'Player', table: 'Table', unit: int = 5, strat_info: None | dict[str, int] = None) -> \
        dict[str, int]:
    if strat_info is None or table.last_roll in Field(0).losing_numbers:
        strat_info = {"progression": 0}
    else:
        strat_info["progression"] += 1

    bet_progression = [10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150]
    prog = strat_info["progression"]
    if prog < len(bet_progression):
        amount = bet_progression[prog] * unit / 5
    elif prog % 2 == 0:
        # alternate between second to last and last
        amount = bet_progression[len(bet_progression) - 2] * unit / 5
    else:
        amount = bet_progression[len(bet_progression) - 1] * unit / 5

    player.bet(
        Field(
            amount,
            double=table.payouts["fielddouble"],
            triple=table.payouts["fieldtriple"],
        ), table
    )

    return strat_info


# def place68_cpr(player: 'Player', table: 'Table', unit: int = 5, strat_info: dict[]=None) -> dict[str, str]:
#     """ place 6 & 8 after point is establish.  Then collect, press, and regress (in that order) on each win """
#     ## NOTE: NOT WORKING
#     if strat_info is None:
#         strat_info = {"mode6": "collect", "mode8": "collect"}
#
#     if table.point == "On":
#         # always place 6 and 8 when they aren't place bets already
#         if not player.has_bet("Place6"):
#             player.bet(Place6(6 / 5 * unit))
#         if not player.has_bet("Place8"):
#             player.bet(Place8(6 / 5 * unit))
#
#     if table.bet_update_info is not None:
#         # place6
#         if player.has_bet("Place6"):
#             bet = player.get_bet("Place6")
#             if (
#                 table.bet_update_info[player].get(bet.name) is not None
#             ):  # bet has not yet been updated; skip
#                 # print("level3")
#                 # print(table.bet_update_info[player][bet.name])
#                 if table.bet_update_info[player][bet.name]["status"] == "win":
#                     # print("place6 mode: {}".format(strat_info["mode6"]))
#                     if strat_info["mode6"] == "press":
#                         player.remove(bet)
#                         player.bet(Place6(2 * bet.bet_amount))
#                         strat_info["mode6"] = "regress"
#                     elif strat_info["mode6"] == "regress":
#                         player.remove(bet)
#                         player.bet(Place6(6 / 5 * unit))
#                         strat_info["mode6"] = "collect"
#                     elif strat_info["mode6"] == "collect":
#                         strat_info["mode6"] = "press"
#                     # print("updated place6 mode: {}".format(strat_info["mode6"]))
#         # place8
#         if player.has_bet("Place8"):
#             bet = player.get_bet("Place8")
#             if (
#                 table.bet_update_info[player].get(bet.name) is not None
#             ):  # bet has not yet been updated; skip
#                 # print("level3")
#                 # print(table.bet_update_info[player][bet.name])
#                 if table.bet_update_info[player][bet.name]["status"] == "win":
#                     # print("place8 mode: {}".format(strat_info["mode8"]))
#                     if strat_info["mode8"] == "press":
#                         player.remove(bet)
#                         player.bet(Place8(2 * bet.bet_amount))
#                         strat_info["mode8"] = "regress"
#                     elif strat_info["mode8"] == "regress":
#                         player.remove(bet)
#                         player.bet(Place8(6 / 5 * unit))
#                         strat_info["mode8"] = "collect"
#                     elif strat_info["mode8"] == "collect":
#                         strat_info["mode8"] = "press"
#
#     print(strat_info)
#     return strat_info


def place68_dontcome2odds(player: 'Player', table: 'Table', unit: int | float = 5,
                          strat_info: None = None) -> None:
    place(player, table, unit, strat_info={"numbers": {6, 8}}, skip_point=False)

    current_numbers = []
    for bet in player.bets_on_table:
        current_numbers += bet.winning_numbers
    current_numbers = list(set(current_numbers))

    dont_come_losing_numbers = []
    if player.has_bet("DontCome"):
        dont_come_losing_numbers += player.get_bet("DontCome", "Any").losing_numbers

    if 6 in dont_come_losing_numbers:
        if player.has_bet("Place6"):
            player.remove(player.get_bet("Place6"))
        if 5 not in current_numbers:
            player.bet(Place5(unit), table)
    elif 8 in dont_come_losing_numbers:
        if player.has_bet("Place8"):
            player.remove(player.get_bet("Place8"))
        if 9 not in current_numbers:
            player.bet(Place9(unit), table)

    if table.point == "On" and player.num_bet("DontCome") < 1:
        player.bet(DontCome(unit), table)

    if player.has_bet("DontCome"):
        dc: Bet = player.get_bet("DontCome", "Any")

        if not isinstance(dc, DontCome):
            raise TypeError
        mult = 1
        win_mult: int | float = 2
        # Lay odds for don't come
        if win_mult == "345":
            mult = 6.0
        else:
            win_mult = float(win_mult)
            # print([[b.name, b.subname] for b in player.bets_on_table])
            if not dc.prepoint:
                lose_num = dc.losing_numbers[0]
                if lose_num in [4, 10]:
                    mult = 2 * win_mult
                elif lose_num in [5, 9]:
                    mult = 3 / 2 * win_mult
                elif lose_num in [6, 8]:
                    mult = 6 / 5 * win_mult

        if not player.has_bet("LayOdds") and not dc.prepoint:
            player.bet(LayOdds(mult * unit, dc), table)


if __name__ == "__main__":
    # Test a betting strategy

    from crapssim.player import Player
    from crapssim.dice import Dice
    from crapssim.table import Table

    # table = CrapsTable()
    # table._add_player(Player(500, place68_2come))

    d = Dice()
    p = Player(500, place68_2come)
    table = Table()
    p.bet(PassLine(5), table)
    p.bet(Place6(6), table)
    print(p.bets_on_table)
    print(p.bankroll)
    print(p.total_bet_amount)
