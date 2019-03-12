from dice import Dice
from player import Player
# from bet import *
import betting_strategies as strat
import sys

class CrapsTable(object):
    """
    Craps Table that contains Dice, Players, the Players' bets, and updates them accordingly.  Main method is run() which should simulate a craps table until a specified number of rolls plays out or all players run out of money.  

    Parameters
    ----------
    NONE

    Attributes
    ----------
    players : list
        List of player objects at the table
    total_player_cash : float
        Sum of all players bankroll and bets on table
    point : string 
        The point for the table.  It is either "Off" when point is off or "On" when point is on. 
    point_number : int 
        The point number when point is "On" and None when point is "Off" 
    player_has_bets : bool
        Boolean value for whether any player has a bet on the table.
    
    """
    def __init__(self):
        self.players = []
        self.point = "Off"
        self.point_number = None
        self.player_has_bets = False

    def _add_player(self, player_object):
        """ Add player object to the table """
        if player_object not in self.players:
            self.players.append(player_object)
            
    def run(self, max_rolls, verbose=True, runout=False):
        """
        Runs the craps table until a stopping condition is met. 

        Parameters
        ----------
        max_rolls : int
            Maximum number of rolls to run for
        verbose : bool
            If true, print results from table during each roll
        runout : bool
            If true, continue past max_rolls until player has no more bets on the table
        """
        self.dice = Dice()
        if verbose: print("Welcome to the Craps Table!")
        
        # make sure at least one player is at table
        if not self.players:
            self._add_player(Player(500, "Player1"))
        if verbose: print("Initial players: {}".format( [p.name for p in self.players] ))

        # maybe wrap this into update table or something
        self.total_player_cash = sum([p.total_bet_amount+p.bankroll for p in self.players]) 
       
        continue_rolling = True
        while continue_rolling:
            
            # players make their bets
            self._add_player_bets()
            for p in self.players:
                bets = ["{}{}, ${}".format(b.name, b.subname, b.bet_amount) for b in p.bets_on_table]
                if verbose: print("{}'s current bets: {}".format(p.name, bets))
                # if verbose: print("{}'s current bets: {}".format(p.name, {b.name: b.bet_amount for b in p.bets_on_table} ))
    
            if verbose: print("")
            self.dice.roll()
            if verbose: print("Dice out!")
            if verbose: print("Shooter rolled {} {}".format(self.dice.total_, self.dice.result_))

            self._update_player_bets(self.dice, verbose)
            self._update_table(self.dice)
            if verbose: print("Point is {} ({})".format(self.point, self.point_number))
            if verbose: print("Total Player Cash is ${}".format(self.total_player_cash))
            
            # evaluate the stopping condition
            if runout:
                continue_rolling = (self.dice.n_rolls_ < max_rolls and self.total_player_cash > 0) or self.player_has_bets
            else: 
                continue_rolling = (self.dice.n_rolls_ < max_rolls and self.total_player_cash > 0)
         
    def _add_player_bets(self):
        """ Implement each player's betting strategy """
        """ TODO: restrict bets that shouldn't be possible based on table"""
        """ TODO: Make the unit parameter specific to each player, and make it more general """
        for p in self.players:
            p.add_bet(self) # unit = 10 to change unit

    def _update_player_bets(self, dice, verbose = False):
        """ check bets for wins/losses, payout wins to their bankroll, remove bets that have resolved """
        for p in self.players:
            p._update_bet(self, dice, verbose)

    def _update_table(self, dice):
        """ update table attributes based on previous dice roll """
        if self.point == "Off" and dice.total_ in [4,5,6,8,9,10]:
            self.point = "On"
            self.point_number = dice.total_
        elif self.point == "On" and (dice.total_ == 7 or dice.total_ == self.point_number):
            self.point = "Off"
            self.point_number = None 

        self.total_player_cash = sum([p.total_bet_amount+p.bankroll for p in self.players]) 

        self.player_has_bets = sum([len(p.bets_on_table) for p in self.players]) >= 1


if __name__ == "__main__":

    sim = True
    printout = True

    n_sim = 100
    n_roll = 144
    bankroll = 1000
    strategy = strat._strat_passline
    strategy_name = "passline" # don't include any "_" in this
    runout = True
    runout_str = "-runout" if runout else ""
        
    if sim:
        # Run simulation of n_roll rolls (estimated rolls/hour with 5 players) 1000 times
        outfile_name = "./output/simulations/{}_sim-{}_roll-{}_br-{}{}.txt".format(strategy_name, n_sim, n_roll, bankroll, runout_str)
        with open(outfile_name, 'w') as f_out:
            f_out.write("total_cash,n_rolls")
            f_out.write(str('\n'))
            for i in range(n_sim):
                table = CrapsTable()
                table._add_player(Player(500, strategy))
                table.run(n_roll, verbose=False, runout=runout)
                out = "{},{}".format(table.total_player_cash, table.dice.n_rolls_)
                f_out.write(str(out))
                f_out.write(str('\n'))

    if printout:
        # Run one simulation with verbose=True to check strategy
        outfile_name = "./output/printout/{}_roll-{}_br-{}{}.txt".format(strategy_name, n_roll, bankroll, runout_str)
        with open(outfile_name, 'w') as f_out:
            sys.stdout = f_out
            table = CrapsTable()
            table._add_player(Player(500, strategy))
            table.run(n_roll, verbose=True)
            # out = table.total_player_cash
            # f_out.write(str(out))
            # f_out.write(str('\n'))

    sys.stdout = sys.__stdout__ # reset stdout
        

        

    
    

        