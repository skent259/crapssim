import copy
import math
from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Hashable, Literal, Protocol, SupportsFloat, TypedDict, cast

from crapssim.dice import Dice
from crapssim.point import Point

__all__ = [
    "BetResult",
    "Bet",
    "_WinningLosingNumbersBet",
    "_SimpleBet",
    "PassLine",
    "Come",
    "DontPass",
    "DontCome",
    "Odds",
    "Put",
    "Place",
    "Field",
    "CAndE",
    "Any7",
    "Two",
    "Three",
    "Yo",
    "Boxcars",
    "AnyCraps",
    "Horn",
    "World",
    "Big6",
    "Big8",
    "HardWay",
    "Hop",
    "Fire",
    "All",
    "Tall",
    "Small",
    "Buy",
    "Lay",
]
ALL_DICE_NUMBERS = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}


class TableSettings(TypedDict, total=False):
    """Subset of table policy toggles referenced by bet logic."""

    ATS_payouts: dict[str, int]
    field_payouts: dict[int, int]
    fire_payouts: dict[int, int]
    hop_payouts: dict[str, int]
    max_odds: dict[int, int]
    max_dont_odds: dict[int, int]
    vig_rounding: Literal["none", "ceil_dollar", "nearest_dollar"]
    vig_floor: float
    vig_paid_on_win: bool


class Table(Protocol):
    dice: Dice
    point: Point
    settings: TableSettings


class Player(Protocol):
    table: Table
    bets: list["Bet"]

    @property
    def bankroll(self) -> float: ...


@dataclass(slots=True, frozen=True)
class BetResult:
    """
    Represents the outcome of a bet

    This class is used by all Bets for consistency in determining whether the
    bet won, lost or pushed. It provides properties to analyze the bet outcome
    and its impact on a bankroll.
    """

    amount: float
    """The monetary value representing the bet outcome."""
    remove: bool
    """Flag indicating whether this bet result should be removed from table."""
    bet_amount: float = 0
    """The monetary value of the original bet size. Needed only for bets that 
    push and return the wager to the player. Default is zero for quick 
    results that can define wins and losses by comparing against zero."""

    @property
    def won(self) -> bool:
        """Returns True if the bet won (amount more than initial bet)."""
        return self.amount > self.bet_amount

    @property
    def lost(self) -> bool:
        """Returns True if the bet lost (negative amount)."""
        return self.amount < 0

    @property
    def pushed(self) -> bool:
        """Returns True if the bet tied (zero amount)."""
        return self.amount == self.bet_amount

    @property
    def bankroll_change(self) -> float:
        """Calculates the change to the bankroll (amount if bet won, zero otherwise)."""
        return self.amount if self.amount > 0 else 0


class _MetaBetABC(ABCMeta):
    # Trick to get a bet like `PassLine` to have it's repr be `crapssim.bet.PassLine`
    def __repr__(cls):
        return f"crapssim.bet.{cls.__name__}"

    def __str__(cls):
        return f"{cls.__name__}"


def _compact_float(x) -> str:
    return str(int(x)) if isinstance(x, float) and x.is_integer() else format(x, ".15g")


class Bet(ABC, metaclass=_MetaBetABC):
    """
    A generic bet for the craps table.

    The high-level class that defines most of the core bet methods.
    All bets will be a subclass of this.
    """

    def __init__(self, amount: SupportsFloat) -> None:
        self.amount: float = float(amount)
        """Wagered amount for the bet."""

    @abstractmethod
    def get_result(self, table: Table) -> BetResult:
        """
        Core bet logic that determines the result.

        This determines the ultimate amount and whether the
        bet needs to be removed, which is indicated with a
        BetResult object.
        """
        pass

    def cost(self, table: Table) -> float:
        """Total bankroll required to put this bet in action on ``table``."""
        return self.amount

    def update_number(self, table: Table):
        """
        Update the bet's number, if applicable

        This method is required by Come and DontCome bets to
        update their number after the first roll. Since this
        method is used by the Table, it defaults to doing nothing
        for a generic bet.
        """
        pass

    def is_removable(self, table: Table) -> bool:
        """
        Checks whether the bet is removable. May depend on the
        table conditions (e.g. if point is On).

        Returns:
            True if the bet is removable, otherwise false.
        """
        return True

    def is_allowed(self, player: Player) -> bool:
        """
        Checks whether the bet is allowed to be placed on the given table.
        May depend on the player's bets also (e.g. for odds bets).

        Returns:
            True if the bet is allowed, otherwise false.
        """
        return True

    def copy(self) -> "Bet":
        """Create a fresh copy of this bet"""
        new_bet = self.__class__(self.amount)
        return new_bet

    @property
    def _placed_key(self) -> Hashable:
        return type(self)

    @property
    def _hash_key(self) -> Hashable:
        return self._placed_key, self.amount

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return self._hash_key == other._hash_key
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self._hash_key)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.amount})"

    def __add__(self, other: "Bet") -> "Bet":
        if isinstance(other, SupportsFloat):
            amount = self.amount - float(other)
        elif self._placed_key == other._placed_key:
            amount = self.amount + other.amount
        else:
            raise NotImplementedError
        new_bet = copy.copy(self)
        new_bet.amount = amount
        return new_bet

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other: "Bet") -> "Bet":
        if isinstance(other, SupportsFloat):
            amount = self.amount - float(other)
        elif self._placed_key == other._placed_key:
            amount = self.amount - other.amount
        else:
            raise NotImplementedError
        new_bet = copy.copy(self)
        new_bet.amount = amount
        return new_bet

    def __rsub__(self, other):
        return self.__sub__(other)

    def __str__(self) -> str:
        return f"${_compact_float(self.amount)} {self.__class__.__name__}"


class _WinningLosingNumbersBet(Bet, ABC):
    """
    A bet that has winning numbers, losing numbers, and payout ratios

    These values (possibly depending on the table) are used to
    calculate the result.
    """

    def get_result(self, table: Table) -> BetResult:
        """Core bet logic that determines the result.

        Wins are based on having dice total in the winning numbers
        (which may depend on the table), which will pay the payout_ratio
        times the bet amount plus the original bet amount back. Losses
        happen when dice total is in the losing numbers, which result
        in a loss of the original bet amount. Otherwise the bet stays
        on the table.
        """
        if table.dice.total in self.get_winning_numbers(table):
            result_amount = self.get_payout_ratio(table) * self.amount + self.amount
            should_remove = True
        elif table.dice.total in self.get_losing_numbers(table):
            result_amount = -1 * self.amount
            should_remove = True
        elif table.dice.total in self.get_push_numbers(table):
            result_amount = self.amount
            should_remove = True
        else:
            result_amount = 0
            should_remove = False

        return BetResult(result_amount, should_remove, self.amount)

    @abstractmethod
    def get_winning_numbers(self, table: Table) -> list[int]:
        """Returns the winnings numbers, based on table features"""
        pass

    @abstractmethod
    def get_losing_numbers(self, table: Table) -> list[int]:
        """Returns the losing numbers, based on table features"""
        pass

    def get_push_numbers(self, table: Table) -> list[int]:
        """Returns the push numbers, based on table features"""
        return []

    @abstractmethod
    def get_payout_ratio(self, table: Table) -> float:
        """Returns the payout ratio (X to 1), based on table features"""
        pass


class _SimpleBet(_WinningLosingNumbersBet, ABC):
    """
    A bet that has fixed winning and losing numbers and payout ratio

    Essentially, the numbers and payout ratio can be known
    at instantiation and don't depend on the table.
    """

    winning_numbers: list[int] = []
    """Winning numbers for the bet"""
    losing_numbers: list[int] = []
    """Losing numbers for the bet"""
    payout_ratio: int = 1
    """Payout ratio for the bet"""

    def get_winning_numbers(self, table: Table) -> list[int]:
        """Returns the winning numbers (table not used here)"""
        return self.winning_numbers

    def get_losing_numbers(self, table: Table) -> list[int]:
        """Returns the losing numbers (table not used here)"""
        return self.losing_numbers

    def get_payout_ratio(self, table: Table) -> float:
        """Returns the payout ratio (table not used here)"""
        return float(self.payout_ratio)


# Passline and related bets ---------------------------------------------------


class PassLine(_WinningLosingNumbersBet):
    """
    Pass Line bet in craps.

    A bet where the player wins if the first roll is 7 or 11,
    loses if the first roll is 2, 3, or 12, and establishes a point number
    for subsequent rolls. Once a point is set, the player wins by rolling
    the point number again before rolling a 7. Pays 1 to 1.
    """

    def get_winning_numbers(self, table: Table) -> list[int]:
        """Winnings numbers are 7, 11 before point is set,
        and the point number after point is set. Uses table
        to determine the point number and status.
        """
        if table.point.number is None:
            return [7, 11]
        return [table.point.number]

    def get_losing_numbers(self, table: Table) -> list[int]:
        """Losing numbers are 2, 3, 12 before point is set,
        and 7 after point is set. Uses table to determine the
        point number and status.
        """
        if table.point.number is None:
            return [2, 3, 12]
        return [7]

    def get_payout_ratio(self, table: Table) -> float:
        """PassLine always pays out 1:1"""
        return 1.0

    def is_removable(self, table: Table) -> bool:
        """PassLine is removable if the point is off

        Returns:
            True if the bet is removable, otherwise false.
        """
        return table.point.status == "Off"

    def is_allowed(self, player: Player) -> bool:
        """PassLine is allowed if the point if off

        Returns:
            True if the bet is allowed, otherwise false.
        """
        return player.table.point.status == "Off"


class Come(_WinningLosingNumbersBet):
    """
    Come bet in craps.

    Similar to the Pass Line bet, but can be placed after a point is established.
    The first roll determines the Come bet's point number, but also wins on 7, 11
    and loses on 2, 3, 12. The bet wins in subsequent rolls if the
    point number is rolled before a 7, and loses if a 7 is rolled before
    the point number. Pays 1 to 1.
    """

    def __init__(self, amount: SupportsFloat, number: int | None = None):
        super().__init__(amount)
        possible_numbers = (4, 5, 6, 7, 8, 9, 10)
        if number in possible_numbers:
            self.number = number
        else:
            self.number = None

    def get_winning_numbers(self, table: Table) -> list[int]:
        """Winnings numbers are 7, 11 before the number is set,
        and the number after it is set. Number is stored within
        the bet.
        """
        if self.number is None:
            return [7, 11]
        return [self.number]

    def get_losing_numbers(self, table: Table) -> list[int]:
        """Losing numbers are 2, 3, 12 before the number is set,
        and 7 after it is set. Number is stored within
        the bet.
        """
        if self.number is None:
            return [2, 3, 12]
        return [7]

    def get_payout_ratio(self, table: Table) -> float:
        """Come always pays out 1:1"""
        return 1.0

    def update_number(self, table: Table):
        """
        Update the bet's number to the first number rolled if it's in (4, 5, 6, 8, 9, 10).
        """
        possible_numbers = (4, 5, 6, 8, 9, 10)
        if self.number is None and table.dice.total in possible_numbers:
            self.number = table.dice.total

    def is_removable(self, table: Table) -> bool:
        """Come bet is removable is it's number has not been established yet (first roll).

        Returns:
            True if the bet is removable, otherwise false.
        """
        return self.number is None

    def is_allowed(self, player: Player) -> bool:
        """Come bet is only allowed if the table's point is on (accessed via player).

        Returns:
            True if the bet is allowed, otherwise false.
        """
        return player.table.point.status == "On"

    def copy(self) -> "Bet":
        """Create a fresh copy of this bet with no number"""
        new_bet = self.__class__(self.amount, number=None)
        return new_bet

    @property
    def _placed_key(self) -> Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.amount}, number={self.number})"

    def __str__(self) -> str:
        number_str = f"({self.number})" if self.number is not None else ""
        return f"{super().__str__()}{number_str}"


class DontPass(_WinningLosingNumbersBet):
    """
    Don't Pass bet in craps.

    The opposite of the Pass Line bet. The player wins if the first roll is 2 or 3,
    pushes on 12, and loses if the first roll is 7 or 11. After a point is
    established, the player wins by rolling a 7 before the point number. Bet pays 1 to 1.
    """

    def get_winning_numbers(self, table: Table) -> list[int]:
        """Winnings numbers are 2 or 3 before point is set,
        and 7 after point is set. Uses table to determine the point
        number and status.
        """
        if table.point.number is None:
            return [2, 3]
        return [7]

    def get_losing_numbers(self, table: Table) -> list[int]:
        """Losing numbers are 7 or 11 before point is set,
        and table point number after point is set. Uses table to determine the
        point number and status.
        """
        if table.point.number is None:
            return [7, 11]
        return [table.point.number]

    def get_push_numbers(self, table: "Table") -> list[int]:
        if table.point.number is None:
            return [12]
        return []

    def get_payout_ratio(self, table: Table) -> float:
        """Don't pass always pays out 1:1"""
        return 1.0

    def is_allowed(self, player: Player) -> bool:
        """Don't Pass is allowed if the point if off.

        Returns:
            True if the bet is allowed, otherwise false.
        """
        return player.table.point.status == "Off"


class DontCome(_WinningLosingNumbersBet):
    """
    Don't Come bet in craps.

    Similar to the Don't Pass bet, but can be placed after a point is
    established, but also wins on 2, 3, pushes on 12, and loses on 7 or 11.
    The first roll determines the Don't Come bet's number. The bet wins in
    subsequent rolls if a 7 is rolled before the point number, and loses if
    the number is rolled before a 7. Pays 1 to 1.
    """

    def __init__(self, amount: SupportsFloat, number: int | None = None):
        super().__init__(amount)
        possible_numbers = (4, 5, 6, 7, 8, 9, 10)
        if number in possible_numbers:
            self.number = number
        else:
            self.number = None

    def get_winning_numbers(self, table: Table) -> list[int]:
        if self.number is None:
            return [2, 3]
        return [7]

    def get_losing_numbers(self, table: Table) -> list[int]:
        if self.number is None:
            return [7, 11]
        return [self.number]

    def get_push_numbers(self, table: "Table") -> list[int]:
        if self.number is None:
            return [12]
        return []

    def get_payout_ratio(self, table: Table) -> float:
        """Don't Come always pays out 1:1"""
        return 1.0

    def update_number(self, table: Table):
        possible_numbers = (4, 5, 6, 7, 8, 9, 10)
        if self.number is None and table.dice.total in possible_numbers:
            self.number = table.dice.total

    def is_allowed(self, player: Player) -> bool:
        """Don't Come is only allowed if the table's point is on (accessed via player).

        Returns:
            True if the bet is allowed, otherwise false.
        """
        return player.table.point.status == "On"

    def copy(self) -> "Bet":
        """Create a fresh copy of this bet, with no number"""
        new_bet = self.__class__(self.amount, number=None)
        return new_bet

    @property
    def _placed_key(self) -> Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.amount}, number={self.number})"

    def __str__(self) -> str:
        number_str = f"({self.number})" if self.number is not None else ""
        return f"{super().__str__()}{number_str}"


# Odds bets -------------------------------------------------------------------


class Odds(_WinningLosingNumbersBet):
    """
    Odds bet (for PassLine, DontPass, Come, or Dontcome) in craps.

    A supplementary bet placed behind Pass Line, Don't Pass, Come, or Don't Come bets.
    Offers true odds payouts, meaning the house has no edge. The payout varies
    depending on the point number and whether it's a "light side" (Pass/Come)
    or "dark side" (Don't Pass/Don't Come) bet.
    """

    def __init__(
        self,
        base_type: type["PassLine | DontPass | Come | DontCome | Put"],
        number: int,
        amount: float,
        always_working: bool = False,
    ):
        super().__init__(amount)
        self.base_type = base_type
        self.number = number
        self.always_working = always_working

    @property
    def light_side(self) -> bool:
        return issubclass(self.base_type, (PassLine, Come, Put))

    @property
    def dark_side(self) -> bool:
        return issubclass(self.base_type, (DontPass, DontCome))

    def get_result(self, table: Table) -> BetResult:

        if table.point.status == "Off" and not self.always_working:

            if table.dice.total in (
                self.get_losing_numbers(table) + self.get_winning_numbers(table)
            ):
                # Bet "pushes" and returns to the player
                return BetResult(
                    amount=self.amount, remove=True, bet_amount=self.amount
                )

        return super().get_result(table)

    def get_winning_numbers(self, table: Table) -> list[int]:
        if self.light_side:
            return [self.number]
        elif self.dark_side:
            return [7]

    def get_losing_numbers(self, table: Table) -> list[int]:
        if self.light_side:
            return [7]
        elif self.dark_side:
            return [self.number]

    def get_payout_ratio(self, table: Table) -> float:
        light_ratios = {4: 2, 5: 3 / 2, 6: 6 / 5, 8: 6 / 5, 9: 3 / 2, 10: 2}
        dark_ratios = {n: 1 / x for n, x in light_ratios.items()}

        if self.light_side:
            return light_ratios[self.number]
        elif self.dark_side:
            return dark_ratios[self.number]

    def is_allowed(self, player: Player) -> bool:
        """Odds are allowed if they do not exceed the table maximums.

        Returns:
            True if the bet is allowed, otherwise false.
        """
        max_bet = self.get_max_odds(player.table) * self.base_amount(player)
        allowed = self.amount <= max_bet
        return allowed

    def get_max_odds(self, table: Table) -> float:
        if self.light_side:
            return table.settings["max_odds"][self.number]
        elif self.dark_side:
            return table.settings["max_dont_odds"][self.number]
        else:
            raise NotImplementedError

    def base_amount(self, player: Player):
        base_bets = [
            x
            for x in player.bets
            if isinstance(x, self.base_type)
            and x.get_winning_numbers(player.table)
            == self.get_winning_numbers(player.table)
        ]
        return sum(x.amount for x in base_bets)

    def copy(self) -> "Bet":
        """Create a fresh copy of this bet"""
        new_bet = self.__class__(
            self.base_type, self.number, self.amount, self.always_working
        )
        return new_bet

    def _get_always_working_repr(self) -> str:
        """Since the default is false, only need to print when True"""
        return (
            f", always_working={self.always_working})" if self.always_working else ")"
        )

    @property
    def _placed_key(self) -> Hashable:
        return type(self), self.base_type, self.number

    def __repr__(self):
        return (
            f"Odds(base_type={self.base_type!r}, "
            f"number={self.number}, amount={self.amount}"
            f"{self._get_always_working_repr()}"
        )

    def __str__(self) -> str:
        number_str = f", {self.number}" if self.number is not None else ""

        if issubclass(self.base_type, (PassLine, DontPass)):
            return f"{super().__str__()}({self.base_type})"
        elif issubclass(self.base_type, (Come, Put, DontCome)):
            return f"{super().__str__()}({self.base_type}{number_str})"


class Put(_SimpleBet):
    """Flat line bet on a box number; point must be ON and odds obey table policy."""

    losing_numbers: list[int] = [7]

    def __init__(self, number: int, amount: SupportsFloat) -> None:
        super().__init__(amount)
        self.number = number
        self.winning_numbers = [number]
        self.payout_ratio = 1.0

    def is_allowed(self, player: "Player") -> bool:
        return player.table.point == "On"

    def copy(self) -> "Put":
        return self.__class__(self.number, self.amount)

    @property
    def _placed_key(self) -> Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"Put({self.number}, amount={self.amount})"

    def __str__(self) -> str:
        return f"{super().__str__()}({self.number})"


# Place bets ------------------------------------------------------------------


class Place(_SimpleBet):
    """
    Place bet (on 4, 5, 6, 8, 9, or 10) in craps.

    A bet on a specific number (4, 5, 6, 8, 9, or 10) being rolled before a 7.
    Each number has a different payout ratio reflecting its probability of being rolled.
    Remains active until the number or a 7 is rolled.
    """

    payout_ratios = {4: 9 / 5, 5: 7 / 5, 6: 7 / 6, 8: 7 / 6, 9: 7 / 5, 10: 9 / 5}
    """Stores the place bet payouts: 9 to 5 on (4, 10), 7 to 5 on (5, 9), and 7 to 6 on (6, 8)."""
    losing_numbers: list[int] = [7]

    def __init__(self, number: int, amount: SupportsFloat):
        super().__init__(amount)
        self.number = number
        """The placed number, which determines payout ratio"""
        self.payout_ratio = self.payout_ratios[number]
        self.winning_numbers = [number]

    def copy(self) -> "Bet":
        """Create a fresh copy of this bet"""
        new_bet = self.__class__(self.number, self.amount)
        return new_bet

    @property
    def _placed_key(self) -> Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"Place({self.winning_numbers[0]}, amount={self.amount})"

    def __str__(self) -> str:
        return f"{super().__str__()}({self.number})"


def _compute_vig(
    bet_amount: float,
    rounding: Literal["ceil_dollar", "nearest_dollar", "none"] = "nearest_dollar",
    floor: float = 0.0,
) -> float:
    """Return commission in dollars using a fixed 5% rate on ``bet_amount``."""

    vig = bet_amount * 0.05

    if rounding == "ceil_dollar":
        vig = math.ceil(vig)
    elif rounding == "nearest_dollar":
        vig = math.floor(vig + 0.5)

    vig = max(vig, floor)

    return float(vig)


def _vig_policy(
    settings: TableSettings,
) -> tuple[Literal["ceil_dollar", "nearest_dollar", "none"], float]:
    """Pull table vig rules from TableSettings."""

    rounding = settings.get("vig_rounding", "nearest_dollar")
    if rounding not in {"ceil_dollar", "nearest_dollar", "none"}:
        rounding = "nearest_dollar"
    floor_value = float(settings.get("vig_floor", 0.0) or 0.0)
    return (
        cast(Literal["ceil_dollar", "nearest_dollar", "none"], rounding),
        floor_value,
    )


class Buy(_SimpleBet):
    """True-odds bet on 4/5/6/8/9/10 that charges vig per table policy.

    Vig (commission) may be taken on the win or upfront based on ``vig_paid_on_win``.
    """

    true_odds = {4: 2.0, 10: 2.0, 5: 1.5, 9: 1.5, 6: 1.2, 8: 1.2}
    losing_numbers: list[int] = [7]

    def __init__(self, number: int, amount: SupportsFloat) -> None:
        if number not in (4, 5, 6, 8, 9, 10):
            raise ValueError(f"Invalid Buy number: {number}")
        super().__init__(amount)
        self.number = number
        self.payout_ratio = self.true_odds[number]
        self.winning_numbers = [number]
        """Base amount that determines true-odds payouts."""

    def vig(self, table: "Table") -> float:
        rounding, floor = _vig_policy(table.settings)
        return _compute_vig(self.amount, rounding=rounding, floor=floor)

    def cost(self, table: "Table") -> float:
        if table.settings.get("vig_paid_on_win", True):
            return self.amount
        return self.amount + self.vig(table)

    def get_result(self, table: "Table") -> BetResult:
        if table.dice.total == self.number:
            result_amount = self.payout_ratio * self.amount + self.amount
            if table.settings.get("vig_paid_on_win", True):
                result_amount -= self.vig(table)
            remove = True
        elif table.dice.total == 7:
            result_amount = -self.cost(table)
            remove = True
        else:
            result_amount = 0
            remove = False
        return BetResult(result_amount, remove, self.amount)

    def copy(self) -> "Buy":
        new_bet = self.__class__(self.number, self.amount)
        return new_bet

    @property
    def _placed_key(self) -> Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"Buy({self.number}, amount={self.amount})"

    def __str__(self) -> str:
        return f"{super().__str__()}({self.number})"


class Lay(_SimpleBet):
    """True-odds bet against 4/5/6/8/9/10, paying if 7 arrives first.

    Commission may be taken on the win or upfront based on ``vig_paid_on_win``.
    Note that the vig is taken on the amount won, not the bet amount,
    since this is typically done in a casino (e.g. Laying the 4 for $40, which
    pays $20, would have a $1 vig).
    """

    true_odds = {4: 0.5, 10: 0.5, 5: 2 / 3, 9: 2 / 3, 6: 5 / 6, 8: 5 / 6}
    winning_numbers: list[int] = [7]

    def __init__(self, number: int, amount: SupportsFloat) -> None:
        if number not in (4, 5, 6, 8, 9, 10):
            raise ValueError(f"Invalid Lay number: {number}")
        super().__init__(amount)
        self.number = number
        self.payout_ratio = self.true_odds[number]
        self.losing_numbers = [number]
        """Base amount risked against the box number."""

    def vig(self, table: "Table") -> float:
        rounding, floor = _vig_policy(table.settings)
        gross_win = self.amount * self.payout_ratio
        return _compute_vig(gross_win, rounding=rounding, floor=floor)

    def cost(self, table: "Table") -> float:
        if table.settings.get("vig_paid_on_win", True):
            return self.amount
        return self.amount + self.vig(table)

    def get_result(self, table: "Table") -> BetResult:
        if table.dice.total == 7:
            result_amount = self.payout_ratio * self.amount + self.amount
            if table.settings.get("vig_paid_on_win", True):
                result_amount -= self.vig(table)
            remove = True
        elif table.dice.total == self.number:
            result_amount = -self.cost(table)
            remove = True
        else:
            result_amount = 0
            remove = False
        return BetResult(result_amount, remove, self.amount)

    def copy(self) -> "Lay":
        new_bet = self.__class__(self.number, self.amount)
        return new_bet

    @property
    def _placed_key(self) -> Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"Lay({self.number}, amount={self.amount})"

    def __str__(self) -> str:
        return f"{super().__str__()}({self.number})"


# _WinningLosingNumbersBets with variable payouts -----------------------------------------------------------------


class Field(_WinningLosingNumbersBet):
    """
    Field bet in craps.

    A one-roll bet that wins if the next roll is 2, 3, 4, 9, 10, 11, or 12.
    Loses if 5, 6, 7, or 8 are rolled. Offers variable payouts for specific numbers
    as defined in the table settings (:func:`~crapssim.table.TableSettings`,
    "field_payouts":, which default to 2 to 1 for (2, 12) and 1 to 1 otherwise.
    """

    winning_numbers = [2, 3, 4, 9, 10, 11, 12]
    """Field wins on 2, 3, 4, 9, 10, 11, or 12"""
    losing_numbers = [5, 6, 7, 8]
    """Field loses on 5, 6, 7, or 8"""

    def get_winning_numbers(self, table: Table) -> list[int]:
        """Returns the winning numbers (table not used here)"""
        return self.winning_numbers

    def get_losing_numbers(self, table: Table) -> list[int]:
        """Returns the losing numbers (table not used here)"""
        return self.losing_numbers

    def get_payout_ratio(self, table: Table) -> float:
        """Returns the payout ratio (X to 1) based on table settings
        (:func:`~crapssim.table.TableSettings`, "field_payouts":
        """
        if table.dice.total in table.settings["field_payouts"]:
            return float(table.settings["field_payouts"][table.dice.total])
        return 0.0


class CAndE(_WinningLosingNumbersBet):
    """
    Craps and Eleven (C & E) bet in craps.

    A one-roll bet that wins if the next roll is 2, 3, 11, or 12.
    Offers different payout ratios for different winning numbers:
    - 3 to 1 for 2, 3, and 12
    - 7 to 1 for 11
    Loses on all other numbers.
    """

    winning_numbers: list[int] = [2, 3, 11, 12]
    """Winning numbers are (2, 3, 11, 12)."""
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {2, 3, 11, 12})
    """Losing numbers are anything besides (2, 3, 11, 12)."""

    def get_winning_numbers(self, table: Table) -> list[int]:
        """Returns the winning numbers (table not used here)"""
        return self.winning_numbers

    def get_losing_numbers(self, table: Table) -> list[int]:
        """Returns the losing numbers (table not used here)"""
        return self.losing_numbers

    def get_payout_ratio(self, table: Table) -> float:
        """C & E pays out 3 to 1 for (2, 3, 12) and 7 to 1 for (11)."""
        if table.dice.total in [2, 3, 12]:
            return 3.0
        elif table.dice.total in [11]:
            return 7.0
        else:
            raise NotImplementedError


# Simple bets in the middle of the table --------------------------------------


class Any7(_SimpleBet):
    """
    Any 7 bet (also known as Big Red) in craps.

    A one-roll bet that wins only if the next roll is 7.
    Offers a 4 to 1 payout and loses on all other numbers.
    """

    winning_numbers: list[int] = [7]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {7})
    """Losing number is anything except 7."""
    payout_ratio: int = 4


class Two(_SimpleBet):
    """
    Two (Snake Eyes) bet in craps.

    A one-roll bet that wins only if the next roll is 2.
    Offers a 30 to 1 payout and loses on all other numbers.
    """

    winning_numbers: list[int] = [2]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {2})
    """Losing number is anything except 2."""
    payout_ratio: int = 30


class Three(_SimpleBet):
    """
    Three bet in craps.

    A one-roll bet that wins only if the next roll is 3.
    Offers a 15 to 1 payout and loses on all other numbers.
    """

    winning_numbers: list[int] = [3]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {3})
    """Losing number is anything except 3."""
    payout_ratio: int = 15


class Yo(_SimpleBet):
    """
    Yo (Eleven) bet in craps.

    A one-roll bet that wins only if the next roll is 11.
    Offers a 15 to 1 payout and loses on all other numbers.
    """

    winning_numbers: list[int] = [11]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {11})
    """Losing number is anything except 11."""
    payout_ratio: int = 15


class Boxcars(_SimpleBet):
    """
    Boxcars (Midnight) bet in craps.

    A one-roll bet that wins only if the next roll is 12.
    Offers a 30 to 1 payout and loses on all other numbers.
    """

    winning_numbers: list[int] = [12]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {12})
    """Losing number is anything except 12."""
    payout_ratio: int = 30


class AnyCraps(_SimpleBet):
    """
    Any Craps bet in craps.

    A one-roll bet that wins if the next roll is 2, 3, or 12.
    Offers a 7 to 1 payout and loses on all other numbers.
    """

    winning_numbers: list[int] = [2, 3, 12]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {2, 3, 12})
    """Losing number is anything except (2, 3, 12)."""
    payout_ratio: int = 7


class Horn(_WinningLosingNumbersBet):
    """One-roll bet split across 2, 3, 11, and 12; loses on all other totals."""

    winning_numbers: list[int] = [2, 3, 11, 12]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {2, 3, 11, 12})

    def __init__(self, amount: SupportsFloat) -> None:
        super().__init__(amount)

    def get_winning_numbers(self, table: "Table") -> list[int]:
        return self.winning_numbers

    def get_losing_numbers(self, table: "Table") -> list[int]:
        return self.losing_numbers

    def get_payout_ratio(self, table: "Table") -> float:
        """
        Payout ratios expressed as 'to 1', aligned with single bets and
        adjusting for the full bet amount returned on a win:
        - 2/12: (30 - 3) / 4 = 6.75
        - 3/11: (15 - 3) / 4 = 3.0
        """
        total = table.dice.total
        if total in (2, 12):
            return (30 - 3) / 4
        if total in (3, 11):
            return (15 - 3) / 4
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"Horn(amount={self.amount})"


class World(_WinningLosingNumbersBet):
    """One-roll bet covering Horn numbers plus 7; pays break-even on 7."""

    winning_numbers: list[int] = [2, 3, 7, 11, 12]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {2, 3, 7, 11, 12})

    def __init__(self, amount: SupportsFloat) -> None:
        super().__init__(amount)

    def get_winning_numbers(self, table: "Table") -> list[int]:
        return self.winning_numbers

    def get_losing_numbers(self, table: "Table") -> list[int]:
        return self.losing_numbers

    def get_payout_ratio(self, table: "Table") -> float:
        """
        Payout ratios expressed as 'to 1', consistent with simulator and
        adjusting for the full bet amount returned on a win::
        - 2/12: (30 - 4) / 5 = 5.2
        - 3/11: (15 - 4) / 5 = 2.2
        - 7:    (4  - 4) / 5 = 0.0
        """
        total = table.dice.total
        if total in (2, 12):
            return (30 - 4) / 5
        if total in (3, 11):
            return (15 - 4) / 5
        if total == 7:
            return (4 - 4) / 5
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"World(amount={self.amount})"


class Big6(_SimpleBet):
    """Even-money bet that wins on 6 before 7."""

    winning_numbers: list[int] = [6]
    losing_numbers: list[int] = [7]
    payout_ratio: float = 1.0

    def __init__(self, amount: SupportsFloat) -> None:
        super().__init__(amount)
        self.number = 6

    def __repr__(self) -> str:
        return f"Big6(amount={self.amount})"


class Big8(_SimpleBet):
    """Even-money bet that wins on 8 before 7."""

    winning_numbers: list[int] = [8]
    losing_numbers: list[int] = [7]
    payout_ratio: float = 1.0

    def __init__(self, amount: SupportsFloat) -> None:
        super().__init__(amount)
        self.number = 8

    def __repr__(self) -> str:
        return f"Big8(amount={self.amount})"


# HardWay Bets ----------------------------------------------------------------


class HardWay(Bet):
    """
    Hard Way bet (on 4, 6, 8, or 10) in craps.

    A bet on rolling a specific even number (4, 6, 8, or 10)
    with both dice showing the same value (e.g., two 2s for a hard 4).
    Wins if the number is rolled in a "hard" way before either a 7 or
    the number is rolled in a "soft" way.
    """

    payout_ratios = {4: 7, 6: 9, 8: 9, 10: 7}
    """Payout ratios vary: 7 to 1 for hard 4 or 10, 9 to 1 for hard 6 or 8."""

    def __init__(self, number: int, amount: SupportsFloat) -> None:
        super().__init__(amount)
        self.number: int = number
        self.payout_ratio: float = self.payout_ratios[number]

    def get_result(self, table: Table) -> BetResult:
        if table.dice.result == self.winning_result:
            result_amount = self.payout_ratio * self.amount + self.amount
            should_remove = True
        elif table.dice.total in (7, self.number):
            result_amount = -1 * self.amount
            should_remove = True
        else:
            result_amount = 0
            should_remove = False
        return BetResult(result_amount, should_remove, self.amount)

    @property
    def winning_result(self) -> tuple[int, int]:
        """Returns the dice result that wins, e.g. (2, 2) for Hard 4."""
        return (int(self.number / 2), int(self.number / 2))

    def copy(self) -> "Bet":
        """Create a fresh copy of this bet"""
        new_bet = self.__class__(self.number, self.amount)
        return new_bet

    @property
    def _placed_key(self) -> Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.number}, amount={self.amount})"

    def __str__(self) -> str:
        return f"{super().__str__()}({self.number})"


# Hop bets -------------------------------------------------------------------


class Hop(Bet):
    """
    Hop bet in craps.

    A one-roll bet on a specific dice combination.
    Can be an "easy" hop (different values on each die) or a "hard" hop
    (same value on both dice).

    Payouts differ based on whether the hop is easy or hard, and are
    set in the table settings (:func:`~crapssim.table.TableSettings`,
    "hop_payouts")
    - Easy hop: standard payout (default 15 to 1)
    - Hard hop: higher payout (default 30 to 1)
    """

    def __init__(self, result: tuple[int, int], amount: SupportsFloat) -> None:
        super().__init__(amount)
        self.result: tuple[int, int] = tuple(sorted(result))

    def get_result(self, table: Table) -> BetResult:
        if table.dice.result in self.winning_results:
            result_amount = self.payout_ratio(table) * self.amount + self.amount
            should_remove = True
        else:
            result_amount = -1 * self.amount
            should_remove = True
        return BetResult(result_amount, should_remove, self.amount)

    @property
    def is_easy(self) -> bool:
        return self.result[0] != self.result[1]

    @property
    def winning_results(self) -> list[tuple[int, int]]:
        if self.is_easy:
            return [self.result, self.result[::-1]]
        else:
            return [self.result]

    def payout_ratio(self, table: Table) -> int:
        payout_type = "easy" if self.is_easy else "hard"
        return table.settings["hop_payouts"][payout_type]

    def copy(self) -> "Bet":
        """Create a fresh copy of this bet"""
        new_bet = self.__class__(self.result, self.amount)
        return new_bet

    @property
    def _placed_key(self) -> Hashable:
        return type(self), self.result

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.result}, amount={self.amount})"

    def __str__(self) -> str:
        result_str = f"({self.result[0]},{self.result[1]})"
        return f"{super().__str__()}{result_str}"


# Fire bet -------------------------------------------------------------------


class Fire(Bet):
    """
    Fire bet in craps.

    A progressive bet that tracks points made during a shooter's turn.
    Wins with increasing payouts based on the number of unique point
    numbers made before a 7 is rolled.

    Payout escalates as more points are made:
    - Specific payout ratios depend on table settings (:func:`~crapssim.table.TableSettings`,
    "fire_payouts"), default is 24 to 1 for four points, 249 to 1 for five points, and
    999 to 1 for all six points.
    - Automatically ends when all 6 points are made or a 7 is rolled while the point is On.
    """

    def __init__(self, amount: float):
        super().__init__(amount)
        self.points_made: set[int] = set()
        self.ended: bool = False

    def get_result(self, table: Table) -> BetResult:

        if table.point.status == "Off":
            return BetResult(amount=0, remove=False, bet_amount=self.amount)

        if table.dice.total == table.point.number:
            self.points_made.add(table.point.number)

        # Fire pays out on 7 when enough points made
        # Fire pays out automatically when all 6 points are made
        n_points_made = len(self.points_made)
        ended = table.dice.total == 7 or len(self.points_made) == 6

        if ended and n_points_made in table.settings["fire_payouts"]:
            payout_ratio = table.settings["fire_payouts"][n_points_made]
            result_amount = payout_ratio * self.amount + self.amount
        elif ended and n_points_made not in table.settings["fire_payouts"]:
            result_amount = -1 * self.amount
        else:
            result_amount = 0

        return BetResult(result_amount, remove=ended, bet_amount=self.amount)

    def is_removable(self, table: Table) -> bool:
        """Fire bet is removable only if there is a new shooter.

        Returns:
            True if the bet is removable, otherwise false.
        """
        return table.new_shooter

    def is_allowed(self, player: Player) -> bool:
        """Fire bet is allowed if there is a new shooter.

        Returns:
            True if the bet is allowed, otherwise false.
        """
        return player.table.new_shooter


# All-tall-small bets -------------------------------------------------------


class _ATSBet(Bet):
    """Class representing ATS (All, Tall, Small) bets, not a usable bet by itself."""

    numbers: list[int] = []
    type: str = "_ATSBet"

    def __init__(self, amount: float):
        super().__init__(amount)
        self.rolled_numbers: set[int] = set()

    def get_result(self, table: Table) -> BetResult:

        if table.dice.total in self.numbers:
            self.rolled_numbers.add(table.dice.total)

        if self.numbers == list(self.rolled_numbers):
            payout_ratio = table.settings["ATS_payouts"][self.type]
            result_amount = payout_ratio * self.amount + self.amount
            should_remove = True
        elif table.dice.total == 7:
            result_amount = -1 * self.amount
            should_remove = True
        else:
            result_amount = 0
            should_remove = False

        return BetResult(result_amount, should_remove, self.amount)

    def is_removable(self, table: Table) -> bool:
        """All/Tall/Small bets are removable only if the last roll was a 7
        (or starting a round, with a new shooter).

        Returns:
            True if the bet is removable, otherwise false.
        """
        return table.last_roll == 7 or table.new_shooter

    def is_allowed(self, player: Player) -> bool:
        """All/Tall/Small bets are allowed if the last roll was a 7
        (or starting a round, with a new shooter).

        Returns:
            True if the bet is allowed, otherwise false.
        """
        return player.table.last_roll == 7 or player.table.new_shooter


class All(_ATSBet):
    """
    All bet (part of All/Tall/Small bets) in craps.

    Wins when 2, 3, 4, 5, 6, 8, 9, 10, 11, and 12 all roll
    before a 7 rolls. Loses immediately if a 7 is rolled (including come-out
    sevens). Payout ratios are determined by the :func:`~crapssim.table.TableSettings`
    (["ATS_payouts"]["all"]), which defaults to 150 to 1.
    """

    type: str = "all"
    numbers: list[int] = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]


class Tall(_ATSBet):
    """
    Tall bet (part of All/Tall/Small bets) in craps.

    Wins when 8, 9, 10, 11, and 12 all roll
    before a 7 rolls. Loses immediately if a 7 is rolled (including come-out
    sevens). Payout ratios are determined by the :func:`~crapssim.table.TableSettings`
    (["ATS_payouts"]["tall"]), which defaults to 30 to 1.
    """

    type: str = "tall"
    numbers: list[int] = [8, 9, 10, 11, 12]


class Small(_ATSBet):
    """
    Small bet (part of All/Tall/Small bets) in craps.

    Wins when 2, 3, 4, 5, and 6 all roll
    before a 7 rolls. Loses immediately if a 7 is rolled (including come-out
    sevens). Payout ratios are determined by the :func:`~crapssim.table.TableSettings`
    (["ATS_payouts"]["small"]), which defaults to 30.
    """

    type: str = "small"
    numbers: list[int] = [2, 3, 4, 5, 6]
