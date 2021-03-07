from crapssim.bet import PassLine, Odds, Come
from crapssim.bet import DontPass, LayOdds
from crapssim.bet import Place, Place4, Place5, Place6, Place8, Place9, Place10
from crapssim.bet import Field

"""
Various betting strategies that are based on conditions of the CrapsTable.
Each strategy must take a table and a player_object, and implicitly 
uses the methods from the player object.
"""

"""
Fundamental Strategies
"""


def passline(player, table, unit=5, strat_info=None):
    # Pass line bet
    if table.point == "Off" and not player.has_bet("PassLine"):
        player.bet(PassLine(unit))


def passline_odds(player, table, unit=5, strat_info=None, mult=1):
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
        player.bet(Odds(mult * unit, player.get_bet("PassLine")))


def passline_odds2(player, table, unit=5, strat_info=None):
    passline_odds(player, table, unit, strat_info=None, mult=2)


def passline_odds345(player, table, unit=5, strat_info=None):
    passline_odds(player, table, unit, strat_info=None, mult="345")


def pass2come(player, table, unit=5, strat_info=None):
    passline(player, table, unit)

    # Come bet (2)
    if table.point == "On" and player.num_bet("Come") < 2:
        player.bet(Come(unit))


def place(player, table, unit=5, strat_info={"numbers": {6, 8}}, skip_point=True):
    strat_info["numbers"] = set(strat_info["numbers"]).intersection({4, 5, 6, 8, 9, 10})
    if skip_point:
        strat_info["numbers"] -= {table.point.number}

    # Place the provided numbers when point is ON
    if table.point == "On":
        if not player.has_bet("Place4") and 4 in strat_info["numbers"]:
            player.bet(Place4(unit))
        if not player.has_bet("Place5") and 5 in strat_info["numbers"]:
            player.bet(Place5(unit))
        if not player.has_bet("Place6") and 6 in strat_info["numbers"]:
            player.bet(Place6(6 / 5 * unit))
        if not player.has_bet("Place8") and 8 in strat_info["numbers"]:
            player.bet(Place8(6 / 5 * unit))
        if not player.has_bet("Place9") and 9 in strat_info["numbers"]:
            player.bet(Place9(unit))
        if not player.has_bet("Place10") and 10 in strat_info["numbers"]:
            player.bet(Place10(unit))

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


def place68(player, table, unit=5, strat_info=None):
    passline(player, table, unit, strat_info=None)
    # Place 6 and 8 when point is ON
    p_has_place_bets = player.has_bet(
        "Place4", "Place5", "Place6", "Place8", "Place9", "Place10"
    )
    if table.point == "On" and not p_has_place_bets:
        if table.point.number == 6:
            player.bet(Place8(6 / 5 * unit))
        elif table.point.number == 8:
            player.bet(Place6(6 / 5 * unit))
        else:
            player.bet(Place8(6 / 5 * unit))
            player.bet(Place6(6 / 5 * unit))


def dontpass(player, table, unit=5, strat_info=None):
    # Don't pass bet
    if table.point == "Off" and not player.has_bet("DontPass"):
        player.bet(DontPass(unit))


def layodds(player, table, unit=5, strat_info=None, win_mult=1):
    # Assume that someone tries to win the `win_mult` times the unit on each bet, which corresponds
    # well to the max_odds on a table.
    # For `win_mult` = "345", this assumes max of 3-4-5x odds
    dontpass(player, table, unit)

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
        player.bet(LayOdds(mult * unit, player.get_bet("DontPass")))


"""
Detailed Strategies
"""


def place68_2come(player, table, unit=5, strat_info=None):
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
            player.bet(Place6(6 / 5 * unit))
        if 8 not in current_numbers:
            player.bet(Place8(6 / 5 * unit))

    # add come of passline bets to get on 4 numbers
    if player.num_bet("Come", "PassLine") < 2 and len(player.bets_on_table) < 4:
        if table.point == "On":
            player.bet(Come(unit))
        if table.point == "Off" and (
            player.has_bet("Place6") or player.has_bet("Place8")
        ):
            player.bet(PassLine(unit))

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
            player.bet(Place5(unit))
        elif 9 not in current_numbers:
            player.bet(Place9(unit))
    elif 8 in pass_come_winning_numbers:
        if player.has_bet("Place8"):
            player.remove(player.get_bet("Place8"))
        if 5 not in current_numbers:
            player.bet(Place5(unit))
        elif 9 not in current_numbers:
            player.bet(Place9(unit))


def ironcross(player, table, unit=5, strat_info=None):
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
                )
            )


def hammerlock(player, table, unit=5, strat_info=None):
    passline(player, table, unit)
    layodds(player, table, unit, win_mult="345")

    place_nums = set()
    for bet in player.bets_on_table:
        if isinstance(bet, Place):
            place_nums.add(bet.winning_numbers[0])
    place_point_nums = place_nums.copy()
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


def risk12(player, table, unit=5, strat_info=None):
    passline(player, table, unit)

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
            )
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


def knockout(player, table, unit=5, strat_info=None):
    passline_odds345(player, table, unit)
    dontpass(player, table, unit)


def dicedoctor(player, table, unit=5, strat_info=None):
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
        )
    )

    return strat_info


def place68_cpr(player, table, unit=5, strat_info=None):
    """ place 6 & 8 after point is establish.  Then collect, press, and regress (in that order) on each win """
    ## NOTE: NOT WORKING
    if strat_info is None:
        strat_info = {"mode6": "collect", "mode8": "collect"}

    if table.point == "On":
        # always place 6 and 8 when they aren't place bets already
        if not player.has_bet("Place6"):
            player.bet(Place6(6 / 5 * unit))
        if not player.has_bet("Place8"):
            player.bet(Place8(6 / 5 * unit))

    if table.bet_update_info is not None:
        # place6
        if player.has_bet("Place6"):
            bet = player.get_bet("Place6")
            if (
                table.bet_update_info[player].get(bet.name) is not None
            ):  # bet has not yet been updated; skip
                # print("level3")
                # print(table.bet_update_info[player][bet.name])
                if table.bet_update_info[player][bet.name]["status"] == "win":
                    # print("place6 mode: {}".format(strat_info["mode6"]))
                    if strat_info["mode6"] == "press":
                        player.remove(bet)
                        player.bet(Place6(2 * bet.bet_amount))
                        strat_info["mode6"] = "regress"
                    elif strat_info["mode6"] == "regress":
                        player.remove(bet)
                        player.bet(Place6(6 / 5 * unit))
                        strat_info["mode6"] = "collect"
                    elif strat_info["mode6"] == "collect":
                        strat_info["mode6"] = "press"
                    # print("updated place6 mode: {}".format(strat_info["mode6"]))
        # place8
        if player.has_bet("Place8"):
            bet = player.get_bet("Place8")
            if (
                table.bet_update_info[player].get(bet.name) is not None
            ):  # bet has not yet been updated; skip
                # print("level3")
                # print(table.bet_update_info[player][bet.name])
                if table.bet_update_info[player][bet.name]["status"] == "win":
                    # print("place8 mode: {}".format(strat_info["mode8"]))
                    if strat_info["mode8"] == "press":
                        player.remove(bet)
                        player.bet(Place8(2 * bet.bet_amount))
                        strat_info["mode8"] = "regress"
                    elif strat_info["mode8"] == "regress":
                        player.remove(bet)
                        player.bet(Place8(6 / 5 * unit))
                        strat_info["mode8"] = "collect"
                    elif strat_info["mode8"] == "collect":
                        strat_info["mode8"] = "press"

    print(strat_info)
    return strat_info


if __name__ == "__main__":
    # Test a betting strategy

    from player import Player
    from dice import Dice
    from table import Table

    # table = CrapsTable()
    # table._add_player(Player(500, place68_2come))

    d = Dice()
    p = Player(500, place68_2come)
    p.bet(PassLine(5))
    p.bet(Place6(6))
    print(p.bets_on_table)
    print(p.bankroll)
    print(p.total_bet_amount)
