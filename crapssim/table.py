import copy
import typing

from crapssim.dice import Dice

from .bet import Bet, BetResult
from .point import Point
from .strategy import BetPassLine, Strategy

__all__ = ["TableUpdate", "TableSettings", "Table", "Player"]


class TableUpdate:
    """Object for processing a table after the dice has been rolled."""

    def run(
        self,
        table: "Table",
        dice_outcome: typing.Iterable[int] | None = None,
        run_complete: bool = False,
        verbose: bool = False,
    ):
        """Run through the roll logic of the table."""
        self.run_strategies(table, run_complete, verbose)
        self.print_player_summary(table, verbose)
        self.before_roll(table)
        self.update_table_stats(table)
        self.roll(table, dice_outcome, verbose)
        self.after_roll(table)
        self.update_bets(table, verbose)
        self.set_new_shooter(table)
        self.update_numbers(table, verbose)

    @staticmethod
    def run_strategies(table: "Table", run_complete=False, verbose=False):
        if run_complete:
            # Stop adding/modifying bets when run end criteria are met
            # NOTE: this will also stop strategies that pull bets down. Not ideal but workable for now
            return

        for player in table.players:
            player.strategy.update_bets(player)

    @staticmethod
    def print_player_summary(table: "Table", verbose=False):
        for player in table.players:
            if verbose:
                print(
                    f"{player.name}: Bankroll={player.bankroll}, "
                    f"Bet amount={player.total_bet_amount}, Bets={player.bets}"
                )

    @staticmethod
    def before_roll(table: "Table"):
        table.last_roll = table.dice.total

    @staticmethod
    def update_table_stats(table: "Table"):
        table.pass_rolls += 1
        if table.point == "On" and (
            table.dice.total == 7 or table.dice.total == table.point.number
        ):
            table.pass_rolls = 0

    @staticmethod
    def roll(
        table: "Table",
        fixed_outcome: typing.Iterable[int] | None = None,
        verbose: bool = False,
    ):
        if fixed_outcome is not None:
            table.dice.fixed_roll(fixed_outcome)
        else:
            table.dice.roll()
        if verbose:
            print("")
            print(f"Dice out! (roll {table.dice.n_rolls}, shooter {table.n_shooters})")
            print(f"Shooter rolled {table.dice.total} {table.dice.result}")

    @staticmethod
    def after_roll(table: "Table"):
        for player in table.players:
            player.strategy.after_roll(player)

    @staticmethod
    def update_bets(table: "Table", verbose=False):
        for player in table.players:
            player.update_bet(verbose=verbose)

    @staticmethod
    def set_new_shooter(table: "Table"):
        if table.point == "On" and table.dice.total == 7:
            table.new_shooter = True
            table.n_shooters += 1
        else:
            table.new_shooter = False

    @staticmethod
    def update_numbers(table: "Table", verbose: bool):
        "For Come and DontCome bets that 'move' to their number"
        for player, bet in table.yield_player_bets():
            bet.update_number(table)
        table.point.update(table.dice)

        if verbose:
            print(f"Point is {table.point.status} ({table.point.number})")


class TableSettings(typing.TypedDict):
    """
    Table settings including payouts and max odds.

    This controls the payouts for the ATS (All, Tall, Small), Field,
    Fire, and Hop bets. This also controls the maximum allowable odds
    for the table (both for light-side and dark-side bets).
    """

    ATS_payouts: dict[str, int]  # {"all": 150, "tall": 30, "small": 30}
    field_payouts: dict[int, int]  # {2: 2, 3: 1, 4: 1, 9: 1, 10: 1, 11: 1, 12: 2}
    fire_payouts: dict[int, int]  # {4: 24, 5: 249, 6: 999}
    hop_payouts: dict[str, int]  # {"easy": 15, "hard": 30}
    max_odds: dict[int, int]  # {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
    max_dont_odds: dict[int, int]  # {4: 6, 5: 6, 6: 6, 8: 6, 9: 6, 10: 6}


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

    def __init__(self, seed: int | None = None) -> None:
        self.players: list[Player] = []
        self.point: Point = Point()
        self.seed = seed
        self.dice: Dice = Dice(self.seed)
        self.settings: TableSettings = {
            "ATS_payouts": {"all": 150, "tall": 30, "small": 30},
            "field_payouts": {2: 2, 3: 1, 4: 1, 9: 1, 10: 1, 11: 1, 12: 2},
            "fire_payouts": {4: 24, 5: 249, 6: 999},
            "hop_payouts": {"easy": 15, "hard": 30},
            "max_odds": {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3},
            "max_dont_odds": {4: 6, 5: 6, 6: 6, 8: 6, 9: 6, 10: 6},
        }
        self.pass_rolls: int = 0
        self.last_roll: int | None = None
        self.n_shooters: int = 1
        self.new_shooter: bool = True

    def yield_player_bets(self) -> typing.Generator[tuple["Player", "Bet"], None, None]:
        for player in self.players:
            for bet in player.bets:
                yield player, bet

    def add_player(
        self,
        bankroll: typing.SupportsFloat = 100,
        strategy: Strategy = BetPassLine(5),
        name: str = None,
    ) -> None:
        """Add player object to the table

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
            name = f"Player {len(self.players)}"
        self.players.append(
            Player(table=self, bankroll=bankroll, bet_strategy=strategy, name=name)
        )

    def _setup_run(self, verbose: bool) -> None:
        """
        Setup the table to run and ensure that there is at least one player.

        Parameters
        ----------
        verbose
            If True prints a welcome message and the initial players.
        """
        if verbose and self.dice.n_rolls == 0:
            print("Welcome to the Craps Table!")
        self.ensure_one_player()
        if verbose and self.dice.n_rolls == 0:
            for player in self.players:
                print(
                    f"{player.name}: Strategy={player.strategy}, "
                    f"Bankroll={player.bankroll}"
                )
            print("")
            print("")

    def run(
        self,
        max_rolls: int,
        max_shooter: float | int = float("inf"),
        verbose: bool = True,
        runout: bool = False,
    ) -> None:
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
        n_rolls_start = self.dice.n_rolls
        # logic needs to count starting run as 0 shooters, not easy to set new_shooter in better way
        n_shooter_start = self.n_shooters if self.n_shooters != 1 else 0

        run_complete = False
        continue_rolling = True
        while continue_rolling:
            TableUpdate().run(self, run_complete=run_complete, verbose=verbose)

            run_complete = self.is_run_complete(
                max_rolls + n_rolls_start, max_shooter + n_shooter_start
            )
            continue_rolling = self.should_keep_rolling(run_complete, runout)
            if not continue_rolling:
                self.n_shooters -= 1  # count was added but this shooter never rolled
                TableUpdate().print_player_summary(self, verbose=verbose)

    def fixed_run(
        self, dice_outcomes: typing.Iterable[typing.Iterable], verbose: bool = False
    ) -> None:
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

    def is_run_complete(
        self,
        max_rolls: float | int,
        max_shooter: float | int,
    ) -> bool:
        """
        Determines whether the conditions specified for the run are complete.

        Parameters
        ----------
        max_rolls
            Maximum number of rolls to run for
        max_shooter
            Maximum number of shooters to run for

        Returns
        -------
        If True, run has completed the roll and shooter conditions and strategies have completed.
        """
        return (
            self.dice.n_rolls >= max_rolls
            or self.n_shooters > max_shooter
            or all(x.strategy.completed(x) for x in self.players)
        )

    def should_keep_rolling(self, run_complete: bool, runout: bool) -> bool:
        """
        Determines whether the program should keep running or not.

        Parameters
        ----------
        run_complete
            If true, run has completed the roll and shooter conditions and strategies have completed.
        runout
            If true, continue past max_rolls until player has no more bets on the table

        Returns
        -------
        If True, the program should continue running. If False the program should stop running.
        """
        if runout:
            return (not run_complete) or self.player_has_bets
        else:
            return not run_complete

    def ensure_one_player(self) -> None:
        """Make sure there is at least one player at the table"""
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
        return sum([len(p.bets) for p in self.players]) > 0

    @property
    def total_player_cash(self) -> float:
        """
        Returns the total sum of all players total_bet_amounts and bankroll.

        Returns
        -------
        The total sum of all players total_bet_amounts and bankroll.
        """
        return sum([p.total_player_cash for p in self.players])


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
    bets : list
        List of betting objects for the player
    """

    def __init__(
        self,
        table: Table,
        bankroll: typing.SupportsFloat,
        bet_strategy: Strategy = BetPassLine(5),
        name: str = "Player",
    ):
        self.bankroll: float = float(bankroll)
        self.strategy: Strategy = copy.deepcopy(bet_strategy)
        self.name: str = name
        self.bets: list[Bet] = []
        self._table: Table = table

    @property
    def total_bet_amount(self) -> float:
        return sum(x.amount for x in self.bets)

    @property
    def total_player_cash(self) -> float:
        return self.bankroll + self.total_bet_amount

    @property
    def table(self) -> Table:
        return self._table

    def add_bet(self, bet: Bet) -> None:
        existing_bets: list[Bet] = self.already_placed_bets(bet)
        new_bet = sum(existing_bets + [bet])
        amount_available_to_bet = self.bankroll + sum(x.amount for x in existing_bets)

        if new_bet.is_allowed(self) and new_bet.amount <= amount_available_to_bet:
            for bet in existing_bets:
                self.bets.remove(bet)
            self.bankroll -= bet.amount
            self.bets.append(new_bet)

    def already_placed_bets(self, bet: Bet) -> list[Bet]:
        """
        Returns the bets a player has matching the placed key

        Notably, bets like Place(4, 1.0) will not match to Place(6, 1.0).
        """
        return [x for x in self.bets if x._placed_key == bet._placed_key]

    def already_placed(self, bet: Bet) -> bool:
        return len(self.already_placed_bets(bet)) > 0

    def get_bets_by_type(
        self, bet_type: typing.Type[Bet] | tuple[typing.Type[Bet], ...]
    ):
        """
        Returns the bets a player has matching the type

        Notably, bets like Place(4, 1.0) will match to Place(6, 1.0).
        """
        return [x for x in self.bets if isinstance(x, bet_type)]

    def has_bets(self, bet_type: typing.Type[Bet] | tuple[typing.Type[Bet], ...]):
        return len(self.get_bets_by_type(bet_type)) > 0

    def remove_bet(self, bet: Bet) -> None:
        if bet in self.bets and bet.is_removable(self.table):
            self.bankroll += bet.amount
            self.bets.remove(bet)

    def add_strategy_bets(self) -> None:
        """Implement the given betting strategy"""
        if self.strategy is not None:
            self.strategy.update_bets(self)

    def update_bet(self, verbose: bool = False) -> None:
        for bet in self.bets[:]:
            result: BetResult = bet.get_result(self.table)
            self.bankroll += result.bankroll_change

            if verbose:
                self.print_bet_update(bet, result)

            if result.remove:
                self.bets.remove(bet)

    def print_bet_update(self, bet: Bet, result: BetResult) -> None:
        if result.won:
            print(f"{self.name} won ${result.amount - bet.amount} on {bet}!")
        elif result.lost:
            print(f"{self.name} lost ${bet.amount} on {bet}.")
