import typing
from dataclasses import dataclass

from crapssim.dice import Dice
from crapssim.player import Player


class Table(object):
    """
    Craps Table that contains Dice, Players, the Players' bets, and updates
    them accordingly.  Main method is run() which should simulate a craps
    table until a specified number of rolls plays out or all players run out
    of money.

    Attributes
    ----------
    players : list
        List of player objects at the table
    point : string
        The point for the table.  It is either "Off" when point is off or "On"
        when point is on.
    bet_update_info : dictionary
        Contains information from updating bets, for given player and a bet
        name, this is status of last bet (win/loss), and win amount.
    dice : Dice
        Dice for the table
    payouts : dice[str, list[int]]
        Field payouts for the table
    pass_rolls : int
        Number of rolls for the current pass
    last_roll : int
        Total of the last roll for the table
    n_shooters : int
        How many shooters the table has had.
    new_shooter : bool
        Returns True if the previous shooters roll just ended and the next shooter hasn't shot.
    """

    def __init__(self) -> None:
        self.players: list[Player] = []
        self.point: Point = Point()
        self.dice: Dice = Dice()
        self.bet_update_info: dict | None = None
        self.payouts: dict[str, typing.Any] = {'field_ratios': {2: 2, 3: 1, 4: 1, 9: 1, 10: 1, 11: 1, 12: 2},
                                               'fire_points': {4: 24, 5: 249, 6: 999}}
        self.pass_rolls: int = 0
        self.last_roll: int | None = None
        self.n_shooters: int = 1
        self.new_shooter: bool = True

    @classmethod
    def with_payouts(cls, **kwargs: list[int]) -> 'Table':
        """ Return a table with the payouts specified in **kwargs.

        Parameters
        ----------
        **kwargs : list[int]
            The tables payouts.

        Returns
        -------
        Table
            The table with the specified payouts.

        """
        table = cls()
        for name, value in kwargs.items():
            table.payouts[name] = value
        return table

    def set_payouts(self, name: str, value: list[int]) -> None:
        """ Set a payout.

        Parameters
        ----------
        name : str
            Name of the payout.
        value : list[int]
            Rolls for the payout.
        """
        self.payouts[name] = value

    def add_player(self, player_object: Player) -> None:
        """ Add player object to the table

        Parameters
        ----------
        player_object : Player
            Player object to add to the table.
        """
        if player_object not in self.players:
            self.players.append(player_object)
        player_object.table = self

    def _setup_run(self, verbose: bool) -> None:
        """
        Setup the table to run and ensure that there is at least one player.

        Parameters
        ----------
        verbose
            If True prints a welcome message and the initial players.
        """
        if verbose:
            print("Welcome to the Craps Table!")
        self.ensure_one_player()
        if verbose:
            print(f"Initial players: {[p.name for p in self.players]}")

    def run(self, max_rolls: int,
            max_shooter: float | int = float("inf"),
            verbose: bool = True,
            runout: bool = False) -> None:
        """
        Runs the craps table until a stopping condition is met.

        Parameters
        ----------
        max_shooter : float | int
            Maximum number of shooters to run for
        max_rolls : int
            Maximum number of rolls to run for
        verbose : bool
            If true, print results from table during each roll
        runout : bool
            If true, continue past max_rolls until player has no more bets on the table
        """

        self._setup_run(verbose)

        continue_rolling = True
        while continue_rolling:
            self.add_player_bets(verbose=verbose)
            self.roll_and_update(verbose)

            continue_rolling = self.should_keep_rolling(max_rolls, max_shooter, runout)

    def fixed_run(self, dice_outcomes: typing.Iterable[typing.Iterable], verbose: bool = False) -> None:
        """
        Give a series of fixed dice outcome and run as if that is what was rolled.

        Parameters
        ----------
        dice_outcomes
            Iterable with two integers representing the dice faces.
        verbose
            If true, print results from table during each roll
        """

        for dice_outcome in dice_outcomes:
            self.add_player_bets(verbose=verbose)
            self.fixed_roll_and_update(dice_outcome)

    def roll_and_update(self, verbose: bool = False) -> None:
        """
        Roll dice, update player bets, and update table.

        Parameters
        ----------
        verbose
            If true, prints out information about the roll and the bets
        """
        self.roll(verbose=verbose)
        self.update_player_bets(verbose=verbose)
        self.update_table(verbose=verbose)

    def fixed_roll_and_update(self, dice_outcome: typing.Iterable[int], verbose: bool = False) -> None:
        """
        Roll dice with fixed dice_outcome, update player bets, and update table.

        Parameters
        ----------
        dice_outcome
            Iterable of the two integers representing the chosen dice faces.
        verbose
            If true, prints out information about the roll and the bets
        """
        self.fixed_roll(dice_outcome=dice_outcome, verbose=verbose)
        self.update_player_bets(verbose=verbose)
        self.update_table(verbose=verbose)

    def roll(self, verbose: bool = False) -> None:
        """
        Convenience method to roll the dice with two random numbers.

        Parameters
        ----------
        verbose
            If true, prints out that the Dice are out and what number the shooter rolled.

        """
        self.new_shooter = False
        self.dice.roll()

        if verbose:
            print("")
            print("Dice out!")
            print(f"Shooter rolled {self.dice.total} {self.dice.result}")

    def fixed_roll(self, dice_outcome: typing.Iterable[int], verbose=False) -> None:
        """
        Convenience method to roll the dice with two fixed numbers.

        Parameters
        ----------
        verbose
            If true, prints out that the Dice are out and what number the shooter rolled.
        dice_outcome
            Iterable of two integers representing the chosen dice faces.
        """
        self.new_shooter = False
        self.dice.fixed_roll(dice_outcome)

        if verbose:
            print("")
            print("Dice out!")
            print(f"Shooter rolled {self.dice.total} {self.dice.result}")

    def should_keep_rolling(self, max_rolls: int, max_shooter: int, runout: bool) -> bool:
        """
        Determines whether the program should keep running or not.

        Parameters
        ----------
        max_rolls
            Maximum number of rolls to run for
        max_shooter
            Maximum number of shooters to run for
        runout
            If true, continue past max_rolls until player has no more bets on the table

        Returns
        -------
        If True, the program should continue running. If False the program should stop running.
        """
        if runout:
            return (self.dice.n_rolls < max_rolls
                    and self.n_shooters <= max_shooter
                    and all(x.bankroll > x.unit for x in self.players)
                    ) or self.player_has_bets
        else:
            return (
                    self.dice.n_rolls < max_rolls
                    and self.n_shooters <= max_shooter
                    and all(x.bankroll > x.unit for x in self.players)
            )

    def ensure_one_player(self) -> None:
        """ Make sure there is at least one player at the table
        """
        if len(self.players) == 0:
            self.add_player(Player(500.0, name="Player1"))

    def add_player_bets(self, verbose: bool = False) -> None:
        """ Implement each player's betting strategy.

        Parameters
        ----------
        verbose
            If True, print the players current bets.
        """
        for p in self.players:
            p.add_strategy_bets()

            if verbose:
                bets = [f"{b.name}{b.subname}: ${b.bet_amount}" for b in p.bets_on_table]
                if verbose:
                    print(f"{p.name}'s current bets: {bets}")

    def update_player_bets(self, verbose: bool = False) -> None:
        """ Check bets for wins/losses, payout wins to their bankroll, remove bets that have resolved

        Parameters
        ----------
        verbose : bool
            If True, prints whether the player won, lost, etc and the amount
        """
        self.bet_update_info = {}
        for p in self.players:
            info = p.update_bet(verbose)
            self.bet_update_info[p] = info

    def update_table(self, verbose: bool = False) -> None:
        """ update table attributes based on previous dice roll

        Parameters
        ----------
        verbose
            If true, prints out the point and the players total cash
        """
        self.pass_rolls += 1
        if self.point == "On" and self.dice.total == 7:
            self.new_shooter = True
            self.n_shooters += 1
        if self.point == "On" and (self.dice.total == 7 or self.dice.total == self.point.number):
            self.pass_rolls = 0

        self.point.update(self.dice)
        self.last_roll = self.dice.total

        if verbose:
            print(f"Point is {self.point.status} ({self.point.number})")
            print(f"Total Player Cash is ${self.total_player_cash}")

    def get_player(self, player_name: str) -> typing.Union['Player', bool]:
        """
        Given the name of a player return the player object.

        Parameters
        ----------
        player_name : str
            Name of the player

        Returns
        -------
        Player, bool
            If player is found return player, otherwise return False

        """
        for p in self.players:
            if p.name == player_name:
                return p
        return False

    @property
    def player_has_bets(self) -> bool:
        """
        Returns whether any of the players on the table have any active bets.

        Returns
        -------
        True if any of the players have bets on the table, otherwise False.

        """
        return sum([len(p.bets_on_table) for p in self.players]) > 0

    @property
    def total_player_cash(self) -> float:
        """
        Returns the total sum of all players total_bet_amounts and bankroll.

        Returns
        -------
        The total sum of all players total_bet_amounts and bankroll.
        """
        return sum([p.total_bet_amount + p.bankroll for p in self.players])


class Point:
    """
    The point on a craps table.

    Parameters
    ----------
    NONE

    Attributes
    ----------
    status : str
        Either 'On' or 'Off', depending on whether a point is set
    number : int
        The point number (in [4, 5, 6, 8, 9, 10]) is status == 'On'
    """

    def __init__(self) -> None:
        self.status: str = "Off"
        self.number: int | None = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.status.lower() == other.lower() or str(self.number) == other
        elif isinstance(other, int) and other in (4, 5, 6, 8, 9, 10):
            return other == self.number
        elif isinstance(other, Point):
            return other.status == self.status and other.number == self.number
        else:
            raise NotImplementedError

    def __gt__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.number > int(other)
        elif isinstance(other, int):
            return self.number > other
        elif isinstance(other, Point):
            return self.number > other.number
        else:
            raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.number < int(other)
        elif isinstance(other, int):
            return self.number < other
        elif isinstance(other, Point):
            return self.number < other.number
        else:
            raise NotImplementedError

    def __ge__(self, other: object) -> bool:
        return self.__eq__(other) or self.__gt__(other)

    def __le__(self, other: object) -> bool:
        return self.__eq__(other) or self.__lt__(other)

    def update(self, dice_object: Dice) -> None:
        """
        Given a Dice object update the points status and number.

        Parameters
        ----------
        dice_object : Dice
            The Dice you want to update the point with
        """
        if self.status == "Off" and dice_object.total in [4, 5, 6, 8, 9, 10]:
            self.status = "On"
            self.number = dice_object.total
        elif self.status == "On" and dice_object.total in [7, self.number]:
            self.status = "Off"
            self.number = None


if __name__ == "__main__":
    import sys

    # import strategy
    from crapssim.strategy import dicedoctor

    sim = False
    printout = True

    n_sim = 100
    n_roll = 144
    n_shooter = 2
    bankroll = 1000
    strategy = dicedoctor
    strategy_name = "dicedoctor"  # don't include any "_" in this
    runout = True
    runout_str = "-runout" if runout else ""

    if sim:
        # Run simulation of n_roll rolls (estimated rolls/hour with 5 players) 1000 times
        outfile_name = f"./output/simulations/{strategy_name}_sim-{n_sim}_roll-{n_roll}_br-{bankroll}{runout_str}.txt"
        with open(outfile_name, "w") as f_out:
            f_out.write("total_cash,n_rolls")
            f_out.write(str("\n"))
            for i in range(n_sim):
                table = Table()
                table.add_player(Player(bankroll, strategy))
                table.run(n_roll, n_shooter, verbose=False, runout=runout)
                out = f"{table.total_player_cash},{table.dice.n_rolls}"
                f_out.write(str(out))
                f_out.write(str("\n"))

    if printout:
        # Run one simulation with verbose=True to check strategy
        outfile_name = f"./output/printout/{strategy_name}_roll-{n_roll}_br-{bankroll}{runout_str}.txt"
        with open(outfile_name, "w") as f_out:
            sys.stdout = f_out
            table = Table()
            table.add_player(Player(bankroll, strategy))
            table.run(n_roll, verbose=True)
            # out = table.total_player_cash
            # f_out.write(str(out))
            # f_out.write(str('\n'))

    sys.stdout = sys.__stdout__  # reset stdout

    # table = Table().with_payouts(fielddouble=[2], fieldtriple=[12])
    # print(table)
    # print(table.payouts)
