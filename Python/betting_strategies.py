from bet import *
"""
Various betting strategies that are based on conditions of the CrapsTable.
Each strategy must take a table and a player_object, and implicitly 
uses the methods from the player object.
"""

def _strat_passline(player, table, unit=5, strat_info=None):
    # Pass line bet
    if table.point == "Off" and not player._has_bet("passline"):
        player.bet(passline(unit))

def _strat_passline_odds(player, table, unit=5, strat_info=None, mult=1):
    _strat_passline(player, table, unit)
    # Pass line odds
    if mult == "345":
        if table.point == "On":
            if table.point_number in [4,10]:
                mult = 3
            elif table.point_number in [5,9]:
                mult = 4
            elif table.point_number in [6,8]:
                mult = 5
    else:
        mult = float(mult)

    if table.point == "On" and player._has_bet("passline") and not player._has_bet("odds"):
        player.bet(odds(mult*unit, player._get_bet("passline")))

def _strat_passline_odds2(player, table, unit=5, strat_info=None):
    _strat_passline_odds(player, table, unit, strat_info=None, mult=2)

def _strat_passline_odds345(player, table, unit=5, strat_info=None):
    _strat_passline_odds(player, table, unit, strat_info=None, mult="345")


def _strat_pass2come(player, table, unit=5, strat_info=None):
    _strat_passline(player, table, unit)

    # Come bet (2)
    if table.point == "On" and player._num_bet("come") < 2:
        player.bet(come(unit))

def _strat_place68(player, table, unit=5, strat_info=None):
    _strat_passline(player, table, unit, strat_info=None)
    # Place 6 and 8 when point is ON   
    p_has_place_bets = player._has_bet("place4","place5","place6","place8","place9","place10")
    if table.point == "On" and not p_has_place_bets:
        if table.point_number == 6:
            player.bet(place8(6/5*unit))
        elif table.point_number == 8:
            player.bet(place6(6/5*unit))
        else:
            player.bet(place8(6/5*unit))
            player.bet(place6(6/5*unit))
    

def _strat_place68_2come(player, table, unit=5, strat_info=None):
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
            player.bet(place6(6/5*unit))
        if 8 not in current_numbers:
            player.bet(place8(6/5*unit))
        
    # add come of passline bets to get on 4 numbers           
    if player._num_bet("come","passline") < 2 and len(player.bets_on_table) < 4:
        if table.point == "On":
            player.bet(come(unit))
        if table.point == "Off" and (player._has_bet("place6") or player._has_bet("place8")):
            player.bet(passline(unit))

    # if come bet or passline goes to 6 or 8, move place bets to 5 or 9
    pass_come_winning_numbers = []
    if player._has_bet("passline"): pass_come_winning_numbers += player._get_bet("passline").winning_numbers
    if player._has_bet("come"): pass_come_winning_numbers += player._get_bet("come","Any").winning_numbers
    
    if 6 in pass_come_winning_numbers:
        if player._has_bet("place6"):
            player.remove(player._get_bet("place6"))
        if 5 not in current_numbers:
            player.bet(place5(unit))
        elif 9 not in current_numbers:
            player.bet(place9(unit))
    elif 8 in pass_come_winning_numbers:
        if player._has_bet("place8"): 
            player.remove(player._get_bet("place8"))
        if 5 not in current_numbers:
            player.bet(place5(unit))
        elif 9 not in current_numbers:
            player.bet(place9(unit))
        

def _strat_place68_cpr(player, table, unit=5, strat_info=None):
    """ place 6 & 8 after point is establish.  Then collect, press, and regress (in that order) on each win """
    ## NOTE: NOT WORKING
    if strat_info is None: 
        strat_info = {"mode6":"collect", "mode8":"collect"}
    
    if table.point == "On":
        # always place 6 and 8 when they aren't place bets already
        if not player._has_bet("place6"):
            player.bet(place6(6/5*unit))
        if not player._has_bet("place8"):
            player.bet(place8(6/5*unit))

    if table.bet_update_info is not None:
        # place6
        if player._has_bet("place6"):
            bet = player._get_bet("place6")
            if table.bet_update_info[player].get(bet.name) is not None: # bet has not yet been updated; skip
                # print("level3")
                # print(table.bet_update_info[player][bet.name])
                if table.bet_update_info[player][bet.name]["status"] == "win":
                    # print("place6 mode: {}".format(strat_info["mode6"]))
                    if strat_info["mode6"] == "press":
                        player.remove(bet)
                        player.bet(place6(2*bet.bet_amount))
                        strat_info["mode6"] = "regress"
                    elif strat_info["mode6"] == "regress":
                        player.remove(bet)
                        player.bet(place6(6/5*unit))
                        strat_info["mode6"] = "collect"
                    elif strat_info["mode6"] == "collect":
                        strat_info["mode6"] = "press"
                    # print("updated place6 mode: {}".format(strat_info["mode6"]))
        # place8
        if player._has_bet("place8"):
            bet = player._get_bet("place8")
            if table.bet_update_info[player].get(bet.name) is not None: # bet has not yet been updated; skip
                # print("level3")
                # print(table.bet_update_info[player][bet.name])
                if table.bet_update_info[player][bet.name]["status"] == "win":
                    # print("place8 mode: {}".format(strat_info["mode8"]))
                    if strat_info["mode8"] == "press":
                        player.remove(bet)
                        player.bet(place8(2*bet.bet_amount))
                        strat_info["mode8"] = "regress"
                    elif strat_info["mode8"] == "regress":
                        player.remove(bet)
                        player.bet(place8(6/5*unit))
                        strat_info["mode8"] = "collect"
                    elif strat_info["mode8"] == "collect":
                        strat_info["mode8"] = "press"

    print(strat_info)
    return strat_info

if __name__ == "__main__":
    # Test a betting strategy

    from player import Player
    from dice import Dice
    from CrapsTable import CrapsTable

    # table = CrapsTable()
    # table._add_player(Player(500, _strat_place68_2come))
            
    d = Dice()
    p = Player(500, _strat_place68_2come)
    p.bet(passline(5))
    p.bet(place6(6))
    print(p.bets_on_table)
    print(p.bankroll)
    print(p.total_bet_amount)


    

    


        
