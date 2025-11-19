import copy
from typing import Generator, Iterable, Literal, SupportsFloat, TypedDict

from crapssim.dice import Dice, DicePair

from .bet import Bet, BetResult, Odds, Put
from .point import Point
from .strategy import BetPassLine, Strategy

__all__ = ["TableUpdate", "TableSettings", "Table", "Player"]


class TableUpdate:
    """Helpers for progressing the table state after each roll."""

    def run(
        self,
        table: "Table",
        dice_outcome: DicePair | None = None,
        run_complete: bool = False,
        verbose: bool = False,
    ) -> None:
        """Execute the full roll/update lifecycle.

        Args:
            table: Active table instance being updated.
            dice_outcome: Optional dice pair to use instead of rolling.
            run_complete: If True, skip strategy updates that place/remove bets.
            verbose: If True, print descriptive output for debugging.

        Returns:
            None: Always returns ``None``.
        """
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
    def run_strategies(
        table: "Table", run_complete: bool = False, verbose: bool = False
    ) -> None:
        """Update strategy-driven bets before the roll.

        Args:
            table: Active table instance being updated.
            run_complete: Flag indicating whether the simulation hit stop conditions.
            verbose: Unused, kept for compatibility with existing call sites.

        Returns:
            None: Always returns ``None``.
        """
        if run_complete:
            # Stop adding/modifying bets when run end criteria are met
            # NOTE: this will also stop strategies that pull bets down. Not ideal but workable for now
            return

        for player in table.players:
            player.strategy.update_bets(player)

    @staticmethod
    def print_player_summary(table: "Table", verbose: bool = False) -> None:
        """Emit a summary of each player's bankroll and bets when verbose.

        Returns:
            None: Always returns ``None``.
        """
        for player in table.players:
            if verbose:
                print(
                    f"{player.name}: Bankroll={player.bankroll}, "
                    f"Bet amount={player.total_bet_amount}, "
                    f"Bets=[{', '.join([str(bet) for bet in player.bets])}]"
                )

    @staticmethod
    def before_roll(table: "Table") -> None:
        pass

    @staticmethod
    def update_table_stats(table: "Table") -> None:
        table.pass_rolls += 1
        if table.point == "On" and (
            table.dice.total == 7 or table.dice.total == table.point.number
        ):
            table.pass_rolls = 0

    @staticmethod
    def roll(
        table: "Table",
        fixed_outcome: DicePair | None = None,
        verbose: bool = False,
    ) -> None:
        """Advance the game by one roll.

        Args:
            table: The active table.
            fixed_outcome: Optional dice pair to make the roll deterministic.
            verbose: If True, print event details for debugging.

        Side effects:
            - Updates dice, resolves/removes bets, mutates bankrolls accordingly.

        Returns:
            None: Always returns ``None``.
        """
        if fixed_outcome is not None:
            table.dice.fixed_roll(fixed_outcome)
        else:
            table.dice.roll()
        if verbose:
            print("")
            print(f"Dice out! (roll {table.dice.n_rolls}, shooter {table.n_shooters})")
            print(f"Shooter rolled {table.dice.total} {table.dice.result}")

        table.last_roll = table.dice.total

    @staticmethod
    def after_roll(table: "Table") -> None:
        for player in table.players:
            player.strategy.after_roll(player)

    @staticmethod
    def update_bets(table: "Table", verbose: bool = False) -> None:
        """Settle each player's bets against the most recent roll.

        Returns:
            None: Always returns ``None``.
        """
        for player in table.players:
            player.update_bet(verbose=verbose)

    @staticmethod
    def set_new_shooter(table: "Table") -> None:
        if table.point == "On" and table.dice.total == 7:
            table.new_shooter = True
            table.n_shooters += 1
        else:
            table.new_shooter = False

    @staticmethod
    def update_numbers(table: "Table", verbose: bool) -> None:
        """Advance moving bets (Come/DontCome) and update the point.

        Returns:
            None: Always returns ``None``.
        """
        for player, bet in table.yield_player_bets():
            bet.update_number(table)
        table.point.update(table.dice)

        if verbose:
            print(f"Point is {table.point.status} ({table.point.number})")


class TableSettings(TypedDict, total=False):
    """Simulation and payout policy toggles.

    Keys:
      vig_rounding: Literal["none", "ceil_dollar", "nearest_dollar"]
      vig_floor: float
      vig_paid_on_win: bool
      # existing: ATS_payouts, field_payouts, fire_payouts, hop_payouts, max odds, etc.
    """

    ATS_payouts: dict[str, int]
    field_payouts: dict[int, int]
    fire_payouts: dict[int, int]
    hop_payouts: dict[str, int]
    max_odds: dict[int, int]
    max_dont_odds: dict[int, int]
    vig_rounding: Literal["none", "ceil_dollar", "nearest_dollar"]
    vig_floor: float
    vig_paid_on_win: bool


class Table:
    """Runtime state for a craps table simulation."""

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
            "vig_rounding": "nearest_dollar",
            "vig_floor": 0,
            "vig_paid_on_win": False,
        }
        self.pass_rolls: int = 0
        self.last_roll: int | None = None
        self.n_shooters: int = 1
        self.new_shooter: bool = True

    def yield_player_bets(self) -> Generator[tuple["Player", "Bet"], None, None]:
        for player in self.players:
            for bet in player.bets:
                yield player, bet

    def add_player(
        self,
        bankroll: SupportsFloat = 100,
        strategy: Strategy = BetPassLine(5),
        name: str | None = None,
    ) -> "Player":
        """Create and register a new player at this table.

        Args:
            bankroll: Starting bankroll for the player.
            strategy: Strategy assigned to the player.
            name: Optional explicit player name; defaults to ``"Player {n}"``.

        Returns:
            Player: The created :class:`Player` instance.
        """
        if name is None:
            name = f"Player {len(self.players)}"
        new_player = Player(
            table=self, bankroll=bankroll, bet_strategy=strategy, name=name
        )
        self.players.append(new_player)
        return new_player

    def _setup_run(self, verbose: bool) -> None:
        """Ensure the table has at least one player and emit greetings if verbose.

        Returns:
            None: Always returns ``None``.
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
        """Simulate the table until shooter/roll limits or strategies finish.

        Args:
            max_rolls: Maximum number of rolls to process.
            max_shooter: Maximum number of shooters to process.
            verbose: If True, print updates during execution.
            runout: If True, continue resolving remaining bets after hitting limits.

        Returns:
            None: Always returns ``None``.
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
        self, dice_outcomes: Iterable[DicePair], verbose: bool = False
    ) -> None:
        """Run the table using a predetermined dice outcome sequence.

        Args:
            dice_outcomes: Iterable of dice value pairs to apply sequentially.
            verbose: If True, print updates during execution.

        Returns:
            None: Always returns ``None``.
        """
        self._setup_run(verbose=verbose)

        for dice_outcome in dice_outcomes:
            TableUpdate().run(self, dice_outcome, verbose=verbose)

    def is_run_complete(
        self,
        max_rolls: float | int,
        max_shooter: float | int,
    ) -> bool:
        """Return True when roll or shooter limits have been met.

        Args:
            max_rolls: Maximum number of rolls to run for.
            max_shooter: Maximum number of shooters to run for.

        Returns:
            True if the run met limits or all strategies report completion.
        """
        return (
            self.dice.n_rolls >= max_rolls
            or self.n_shooters > max_shooter
            or all(x.strategy.completed(x) for x in self.players)
        )

    def should_keep_rolling(self, run_complete: bool, runout: bool) -> bool:
        """Return True if the simulation loop should continue.

        Args:
            run_complete: Whether roll/shooter limits and strategies finished.
            runout: If True, continue until all player bets are resolved.

        Returns:
            True to continue the run, False to stop.
        """
        if runout:
            return (not run_complete) or self.player_has_bets
        else:
            return not run_complete

    def ensure_one_player(self) -> None:
        """Ensure there is at least one player registered on the table.

        Returns:
            None: Always returns ``None``.
        """
        if len(self.players) == 0:
            self.add_player()

    @property
    def player_has_bets(self) -> bool:
        """Whether any player currently has active bets."""
        return sum([len(p.bets) for p in self.players]) > 0

    @property
    def total_player_cash(self) -> float:
        """Total bankroll plus outstanding bet amounts across all players."""
        return sum([p.total_player_cash for p in self.players])


class Player:
    """Active participant at a :class:`Table` with a bankroll and bets."""

    def __init__(
        self,
        table: Table,
        bankroll: SupportsFloat,
        bet_strategy: Strategy = BetPassLine(5),
        name: str = "Player",
    ) -> None:
        self.bankroll: float = float(bankroll)
        self.strategy: Strategy = copy.deepcopy(bet_strategy)
        self.name: str = name
        self.bets: list[Bet] = []
        self._table: Table = table

    @property
    def total_bet_amount(self) -> float:
        """Total amount currently wagered on the layout (plus any recoverable vigs)."""
        return sum(x.cost(self.table) for x in self.bets)

    @property
    def total_player_cash(self) -> float:
        """Bankroll plus outstanding bet amounts and vigs."""
        return self.bankroll + self.total_bet_amount

    @property
    def table(self) -> Table:
        """Table the player is seated at."""
        return self._table

    def add_bet(self, bet: Bet) -> None:
        """Attempt to place a bet while respecting bankroll and bet stacking rules.

        Returns:
            None: Always returns ``None``.
        """
        existing_bets: list[Bet] = self.already_placed_bets(bet)
        existing_cost = sum(x.cost(self.table) for x in existing_bets)
        new_bet = sum(existing_bets + [bet])
        new_cost = new_bet.cost(self.table)
        required_cash = new_cost - existing_cost

        if new_bet.is_allowed(self) and required_cash <= self.bankroll + 1e-9:
            for bet in existing_bets:
                self.bets.remove(bet)
            self.bankroll -= required_cash
            self.bets.append(new_bet)

    def already_placed_bets(self, bet: Bet) -> list[Bet]:
        """Return existing bets with the same placement key as ``bet``.

        Args:
            bet: Bet candidate being compared to current layout bets.

        Returns:
            list[Bet]: Bets already placed with the same key.
        """
        return [x for x in self.bets if x._placed_key == bet._placed_key]

    def already_placed(self, bet: Bet) -> bool:
        """Check whether a bet with the same placement key already exists.

        Args:
            bet: Bet candidate being evaluated.

        Returns:
            bool: True if a matching bet already exists.
        """
        return len(self.already_placed_bets(bet)) > 0

    def get_bets_by_type(
        self, bet_type: type[Bet] | tuple[type[Bet], ...]
    ) -> list[Bet]:
        """Return bets whose type matches ``bet_type`` (supports tuples).

        Args:
            bet_type: Bet type or tuple of bet types to match.

        Returns:
            list[Bet]: Bets whose type matches ``bet_type``.
        """
        return [x for x in self.bets if isinstance(x, bet_type)]

    def has_bets(self, bet_type: type[Bet] | tuple[type[Bet], ...]) -> bool:
        """Return True if any bet of ``bet_type`` is currently on the layout.

        Args:
            bet_type: Bet type or tuple of bet types to check for.

        Returns:
            bool: True if any matching bet exists on the layout.
        """
        return len(self.get_bets_by_type(bet_type)) > 0

    def remove_bet(self, bet: Bet) -> None:
        """Remove a bet if it is present and removable.

        Returns:
            None: Always returns ``None``.
        """
        if bet in self.bets and bet.is_removable(self.table):
            self.bankroll += bet.cost(self.table)
            self.bets.remove(bet)

    def add_strategy_bets(self) -> None:
        """Apply the configured strategy to place new bets.

        Returns:
            None: Always returns ``None``.
        """
        if self.strategy is not None:
            self.strategy.update_bets(self)

    def update_bet(self, verbose: bool = False) -> None:
        """Resolve outstanding bets against the latest roll.

        Returns:
            None: Always returns ``None``.
        """
        for bet in self.bets[:]:
            result: BetResult = bet.get_result(self.table)
            self.bankroll += result.bankroll_change

            if verbose:
                self.print_bet_update(bet, result)

            if result.remove:
                self.bets.remove(bet)

    def print_bet_update(self, bet: Bet, result: BetResult) -> None:
        """Emit verbose logging for a bet resolution.

        Returns:
            None: Always returns ``None``.
        """
        if result.won:
            print(f"{self.name} won ${result.amount - bet.amount} on {bet}!")
        elif result.lost:
            print(f"{self.name} lost ${bet.amount} on {bet}.")
        elif result.pushed:
            print(f"{self.name} pushed for ${bet.amount} on {bet}.")
