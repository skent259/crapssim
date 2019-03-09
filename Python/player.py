class Player(object):
    """
    Player standing at the craps table

    Parameters
    ----------
    bankroll : float
        Starting amount of cash for the player, will be updated during play
    name : string, optional (default = "Player")
        Name of the player 

    Attributes
    ----------
    bets_on_table : list
        List of betting objects for the player
    total_bet_amount : int
        Sum of bet value for the player

    
    """

    def __init__(self, bankroll, name="Player"):
        self.bankroll = bankroll
        self.name = name
        self.bets_on_table = []
        self.total_bet_amount = 0
        # TODO: initial betting strategy

    def bet(self, bet_object):
        if self.bankroll >= bet_object.bet_amount:
            self.bankroll -= bet_object.bet_amount
            self.bets_on_table.append(bet_object) # TODO: make sure this only happens if that bet isn't on the table, otherwise wager amount gets updated
            self.total_bet_amount += bet_object.bet_amount    
        else: 
            pass 
            # can't make the bet

    # def add_odds(self, bet_amount, bet_name, bet_subname=""):
    #     """ Take a bet_object and add an odds bet based on the winning number """
    #     bet_object = self._get_bet(bet_name, bet_subname)
    #     proper_winning_number = [i in [4,5,6,8,9,10] for i in bet_object.winning_numbers] == [True]

    #     if bet_object.name in ["passline", "come"] and proper_winning_number:
    #         self.bet(odds(bet_amount, bet_object))
        

    def _update_bet(self, table_object, dice_object, verbose = False):
        for b in self.bets_on_table[:]:
            status, win_amount = b._update_bet(table_object, dice_object)

            if status == "win":
                self.bankroll += win_amount + b.bet_amount
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if verbose: print("{} won ${} on {} bet!".format(self.name, win_amount, b.name))
            elif status == "lose":
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if verbose: print("{} lost ${} on {} bet.".format(self.name, b.bet_amount, b.name))
            else: 
                pass
            
            pass
                    
                
    def _has_bet(self, *bets_to_check):
        """ returns True if bets_to_check and self.bets_on_table has at least one thing in common """
        bet_names = {b.name for b in self.bets_on_table}
        return bool(bet_names.intersection(bets_to_check))

    def _num_bet(self, *bets_to_check):
        """ returns the total number of bets in self.bets_on_table that match bets_to_check """
        bet_names = [b.name for b in self.bets_on_table]
        return sum([i in bets_to_check for i in bet_names])

    def _get_bet(self, bet_name, bet_subname=""):
        """ returns first betting object matching bet_name and bet_subname """
        bet_name_list = [[b.name, b.subname] for b in self.bets_on_table]
        ind = bet_name_list.index([bet_name, bet_subname])
        return self.bets_on_table[ind]

