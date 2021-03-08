class Player(object):
    """
    Player standing at the craps table

    Parameters
    ----------
    bankroll : float
        Starting amount of cash for the player, will be updated during play
    bet_strategy : function(table, player, unit=5)
        A function that implements a particular betting strategy.  See betting_strategies.py
    name : string, optional (default = "Player")
        Name of the player

    Attributes
    ----------
    bets_on_table : list
        List of betting objects for the player
    total_bet_amount : int
        Sum of bet value for the player
    """

    def __init__(self, bankroll, bet_strategy=None, name="Player"):
        self.bankroll = bankroll
        self.bet_strategy = bet_strategy
        self.name = name
        self.bets_on_table = []
        self.total_bet_amount = 0
        # TODO: initial betting strategy

    def bet(self, bet_object):
        if self.bankroll >= bet_object.bet_amount:
            self.bankroll -= bet_object.bet_amount
            self.bets_on_table.append(
                bet_object
            )  # TODO: make sure this only happens if that bet isn't on the table, otherwise wager amount gets updated
            self.total_bet_amount += bet_object.bet_amount

    def remove(self, bet_object):
        # TODO: add bet attribute for whether a bet can be removed and put condition in here
        if bet_object in self.bets_on_table:
            self.bankroll += bet_object.bet_amount
            self.bets_on_table.remove(bet_object)
            self.total_bet_amount -= bet_object.bet_amount

    def has_bet(self, *bets_to_check):
        """ returns True if bets_to_check and self.bets_on_table has at least one thing in common """
        bet_names = {b.name for b in self.bets_on_table}
        return bool(bet_names.intersection(bets_to_check))

    def get_bet(self, bet_name, bet_subname=""):
        """returns first betting object matching bet_name and bet_subname.
        If bet_subname="Any", returns first betting object matching bet_name"""
        if bet_subname == "Any":
            bet_name_list = [b.name for b in self.bets_on_table]
            ind = bet_name_list.index(bet_name)
        else:
            bet_name_list = [[b.name, b.subname] for b in self.bets_on_table]
            ind = bet_name_list.index([bet_name, bet_subname])
        return self.bets_on_table[ind]

    def num_bet(self, *bets_to_check):
        """ returns the total number of bets in self.bets_on_table that match bets_to_check """
        bet_names = [b.name for b in self.bets_on_table]
        return sum([i in bets_to_check for i in bet_names])

    def remove_if_present(self, bet_name, bet_subname=""):
        if self.has_bet(bet_name):
            self.remove(self.get_bet(bet_name, bet_subname))

    def _add_strategy_bets(self, table, *args, **kwargs):
        """ Implement the given betting strategy """
        return self.bet_strategy(self, table, *args, **kwargs)

    def _update_bet(self, table_object, dice_object, verbose=False):
        info = {}
        for b in self.bets_on_table[:]:
            status, win_amount = b._update_bet(table_object, dice_object)

            if status == "win":
                self.bankroll += win_amount + b.bet_amount
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if verbose:
                    print(f"{self.name} won ${win_amount} on {b.name} bet!")
            elif status == "lose":
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if verbose:
                    print(f"{self.name} lost ${b.bet_amount} on {b.name} bet.")
            elif status == "push":
                self.bankroll += b.bet_amount
                self.total_bet_amount -= b.bet_amount
                self.bets_on_table.remove(b)
                if verbose:
                    print(f"{self.name} pushed ${b.bet_amount} on {b.name} bet.")

            info[b.name] = {"status": status, "win_amount": win_amount}
        return info
