import typing

from crapssim.dice import Dice
from .bet import Bet
from .strategy import Strategy, BetPassLine


class TableUpdate:
    """Object for processing a table after the dice has been rolled."""
    def run(self, table: 'Table',
            dice_outcome: typing.Iterable[int] | None = None,
            verbose: bool = False):
        """Run through the roll logic of the table."""
        self.set_new_shooter(table)
        self.run_strategies(table)
        self.before_roll(table)
        self.update_table_stats(table)
        self.roll(table, dice_outcome, verbose)
        self.after_roll(table)
        self.update_bets(table)
        self.update_points(table, verbose)

    @staticmethod
    def before_roll(table: 'Table'):
        table.last_roll = table.dice.total

    @staticmethod
    def roll(table: 'Table',
             fixed_outcome: typing.Iterable[int] | None = None,
             verbose: bool = False):
        if fixed_outcome is not None:
            table.dice.fixed_roll(fixed_outcome)
        else:
            table.dice.roll()
        if verbose:
            print("")
            print("Dice out!")
            print(f"Shooter rolled {table.dice.total} {table.dice.result}")

    @staticmethod
    def after_roll(table: 'Table'):
        for player in table.players:
            player.bet_strategy.after_roll(player)

    @staticmethod
    def update_bets(table: 'Table'):
        for player in table.players:
            player.update_bet()

    @staticmethod
    def update_table_stats(table: 'Table'):
        table.pass_rolls += 1
        if table.point == "On" and (table.dice.total == 7 or
                                    table.dice.total == table.point.number):
            table.pass_rolls = 0

    @staticmethod
    def set_new_shooter(table: 'Table'):
        if table.n_shooters == 0 or (table.point == "On" and table.dice.total == 7):
            table.new_shooter = True
            table.n_shooters += 1
        else:
            table.new_shooter = False

    @staticmethod
    def update_points(table: 'Table', verbose: bool):
        for player, bet in table.yield_player_bets():
            bet.update_point(table.dice)
        table.point.update(table.dice)

        if verbose:
            print(f"Point is {table.point.status} ({table.point.number})")
            print(f"Total Player Cash is ${table.total_player_cash}")

    @staticmethod
    def run_strategies(table: 'Table'):
        for player in table.players:
            player.bet_strategy.update_bets(player)


class Table:
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
    dice : Dice
        Dice for the table
    settings : dice[str, list[int]]
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
        self.settings: dict[str, typing.Any] = {'field_payouts': {2: 2, 3: 1, 4: 1, 9: 1, 10: 1,
                                                                  11: 1, 12: 2},
                                                'fire_points': {4: 24, 5: 249, 6: 999},
                                                'max_odds': {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3},
                                                'max_dont_odds': {4: 6, 5: 6, 6: 6, 8: 6, 9: 6,
                                                                  10: 6}}
        self.pass_rolls: int = 0
        self.last_roll: int | None = None
        self.n_shooters: int = 0
        self.new_shooter: bool = True

    def yield_player_bets(self) -> typing.Generator[tuple['Player', 'Bet'], None, None]:
        for player in self.players:
            for bet in player.bets_on_table:
                yield player, bet

    def add_player(self, bankroll: typing.SupportsFloat = 100, strategy: Strategy = BetPassLine(5),
                   name: str = None) -> None:
        """ Add player object to the table

        Parameters
        ----------
        bankroll
            The players bankroll, defaults to 100.
        strategy
            The players strategy, defaults to passline.
        name
            The players name, if None defaults to "Player x" with x being the current number
            of players starting with 0 (ex. Player 0, Player 1, Player 2).

        """
        if name is None:
            name = f'Player {len(self.players)}'
        self.players.append(Player(table=self, bankroll=bankroll, bet_strategy=strategy, name=name))

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
            TableUpdate().run(self, verbose=verbose)
            continue_rolling = self.should_keep_rolling(max_rolls, max_shooter, runout)

    def fixed_run(self, dice_outcomes: typing.Iterable[typing.Iterable], verbose: bool = False) \
            -> None:
        """
        Give a series of fixed dice outcome and run as if that is what was rolled.

        Parameters
        ----------
        dice_outcomes
            Iterable with two integers representing the dice faces.
        verbose
            If true, print results from table during each roll
        """
        self._setup_run(verbose=verbose)

        for dice_outcome in dice_outcomes:
            TableUpdate().run(self, dice_outcome, verbose=verbose)

    def should_keep_rolling(self, max_rolls: float | int, max_shooter: float | int,
                            runout: bool) -> bool:
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
                    and any(x.bet_strategy.completed(x) for x in self.players)
                    ) or self.player_has_bets
        else:
            return (
                    self.dice.n_rolls < max_rolls
                    and self.n_shooters <= max_shooter
                    and any(x.bet_strategy.completed(x) for x in self.players)
            )

    def ensure_one_player(self) -> None:
        """ Make sure there is at least one player at the table
        """
        if len(self.players) == 0:
            self.add_player()

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

    Attributes
    ----------
    number : int
        The point number (in [4, 5, 6, 8, 9, 10]) is status == 'On'
    """

    def __init__(self) -> None:
        self.number: int | None = None

    @property
    def status(self) -> str:
        if self.number is None:
            return 'Off'
        else:
            return 'On'

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
        if self.number is None:
            raise NotImplementedError
        if isinstance(other, str):
            return self.number > int(other)
        elif isinstance(other, int):
            return self.number > other
        elif isinstance(other, Point):
            if other.number is None:
                raise NotImplementedError
            return self.number > other.number
        else:
            raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        if self.number is None:
            raise NotImplementedError
        if isinstance(other, str):
            return self.number < int(other)
        elif isinstance(other, int):
            return self.number < other
        elif isinstance(other, Point):
            if other.number is None:
                raise NotImplementedError
            return self.number < other.number
        else:
            raise NotImplementedError

    def __ge__(self, other: object) -> bool:
        if self.number is None:
            raise NotImplementedError
        return self.__eq__(other) or self.__gt__(other)

    def __le__(self, other: object) -> bool:
        if self.number is None:
            raise NotImplementedError
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
            self.number = dice_object.total
        elif self.status == "On" and dice_object.total in [7, self.number]:
            self.number = None


class Player:
    """
    Player standing at the craps table

    Parameters
    ----------
    bankroll : typing.SupportsFloat
        Starting amount of cash for the player
    bet_strategy : function(table, player, unit=5)
        A function that implements a particular betting strategy.  See betting_strategies.py
    name : string, default = "Player"
        Name of the player

    Attributes
    ----------
    bankroll : typing.SupportsFloat
        Current amount of cash for the player
    name : str
        Name of the player
    bet_strategy :
        A function that implements a particular betting strategy. See betting_strategies.py.
    bets_on_table : list
        List of betting objects for the player
    """

    def __init__(self, table: Table,
                 bankroll: typing.SupportsFloat,
                 bet_strategy: Strategy = BetPassLine(5),
                 name: str = "Player"):
        self.bankroll: float = float(bankroll)
        self.bet_strategy: Strategy = bet_strategy
        self.name: str = name
        self.bets_on_table: list[Bet] = []
        self._table: Table = table

    @property
    def total_bet_amount(self) -> float:
        return sum(x.bet_amount for x in self.bets_on_table)

    @property
    def table(self) -> Table:
        return self._table

    def add_bet(self, bet: Bet) -> None:
        existing_bets: list[Bet] = bet.already_placed_bets(self)
        new_bet = sum(existing_bets + [bet])

        if new_bet.allowed(self):
            for bet in existing_bets:
                self.bets_on_table.remove(bet)
            self.bankroll -= bet.bet_amount
            self.bets_on_table.append(new_bet)

    def get_bets_by_type(self, bet_type: typing.Type[Bet] | tuple[typing.Type[Bet], ...]):
        return [x for x in self.bets_on_table if isinstance(x, bet_type)]

    def remove_bet(self, bet: Bet) -> None:
        if bet in self.bets_on_table and bet.is_removable(self):
            self.bankroll += bet.bet_amount
            self.bets_on_table.remove(bet)

    def add_strategy_bets(self) -> None:
        """ Implement the given betting strategy

        """
        if self.bet_strategy is not None:
            self.bet_strategy.update_bets(self)

    def update_bet(self, verbose: bool = False) -> None:
        for bet in self.bets_on_table[:]:
            bet.update(self.table)

            self.bankroll += bet.get_return_amount(self.table)

            if verbose:
                self.print_bet_update(bet)

            if bet.should_remove(self.table):
                self.bets_on_table.remove(bet)

    def print_bet_update(self, bet: Bet) -> None:
        status = bet.get_status(self.table)
        win_amount = bet.get_win_amount(self.table)
        if status == "win":
            print(f"{self.name} won ${win_amount} on {bet}!")
        elif status == "lose":
            print(f"{self.name} lost ${bet.bet_amount} on {bet}.")
