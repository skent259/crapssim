from bet import *
"""
Various betting strategies that are based on conditions of the CrapsTable.
Each strategy must take a table and a player_object, and implicitly 
uses the methods from the player object.
"""

def _strat_passline(player, table, unit=5):
    # Pass line bet
    if table.point == "Off" and not player._has_bet("passline"):
        player.bet(passline(unit))

def _strat_passline_odds(player, table, unit=5, mult=1):
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

def _strat_passline_odds2(player, table, unit=5):
    _strat_passline_odds(player, table, unit, mult=2)

def _strat_passline_odds345(player, table, unit=5):
    _strat_passline_odds(player, table, unit, mult="345")


def _strat_pass2come(player, table, unit=5):
    _strat_passline(player, table, unit)

    # Come bet (2)
    if table.point == "On" and player._num_bet("come") < 2:
        player.bet(come(unit))

def _strat_place68(player, table, unit=6):
    _strat_passline(player, table, unit)
    # Place 6 and 8 when point is ON   
    p_has_place_bets = player._has_bet("place4","place5","place6","place8","place9","place10")
    if table.point == "On" and not p_has_place_bets:
        if table.point_number == 6:
            player.bet(place8(unit))
        elif table.point_number == 8:
            player.bet(place6(unit))
        else:
            player.bet(place8(unit))
            player.bet(place6(unit))
    

def _strat_place68_2come(player, table, unit=5):
    """ 
    Once point is established, place 6 and 8, with 2 additional come bets.
    The goal is to be on four distinct numbers.  
    """
    current_numbers = []
    for bet in player.bets_on_table:
        current_numbers += bet.winning_numbers
    current_numbers = list(set(current_numbers))

    if table.point == "On":
        # always place 6 and 8 when they aren't come bets or place bets already
        if 6 not in current_numbers:
            player.bet(place6(6/5*unit))
        if 8 not in current_numbers:
            player.bet(place8(6/5*unit))
        # add come of passline bets to get on 4 numbers
        
        
        
    if player._num_bet("come","passline") < 2:
        if table.point == "On":
            player.bet(come(unit))



        
