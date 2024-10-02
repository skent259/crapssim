import copy
import typing
from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Protocol, TypedDict

from crapssim.dice import Dice
from crapssim.point import Point

ALL_DICE_NUMBERS = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}


class TableSettings(TypedDict):
    ATS_payouts: dict[str, int]  # {"all": 150, "tall": 30, "small": 30}
    field_payouts: dict[int, int]  # {2: 2, 3: 1, 4: 1, 9: 1, 10: 1, 11: 1, 12: 2}
    fire_payouts: dict[int, int]  # {4: 24, 5: 249, 6: 999}
    max_odds: dict[int, int]  # {4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
    max_dont_odds: dict[int, int]  # {4: 6, 5: 6, 6: 6, 8: 6, 9: 6, 10: 6}


class Table(Protocol):
    dice: Dice
    point: Point
    settings: TableSettings


class Player(Protocol):
    table: Table
    bets: list[typing.Type["Bet"]]


@dataclass(slots=True, frozen=True)
class BetResult:
    amount: float
    remove: bool

    @property
    def won(self) -> bool:
        return self.amount > 0

    @property
    def lost(self) -> bool:
        return self.amount < 0

    @property
    def pushed(self) -> bool:
        return self.amount == 0

    @property
    def bankroll_change(self) -> float:
        if self.won:
            return self.amount
        else:
            return 0


class _MetaBetABC(ABCMeta):
    # Trick to get a bet like `PassLine` to have it's repr be `crapssim.bet.PassLine`
    def __repr__(cls):
        return f"crapssim.bet.{cls.__name__}"


class Bet(ABC, metaclass=_MetaBetABC):
    """
    A generic bet for the craps table

    Parameters
    ----------
    amount : typing.SupportsFloat
        Wagered amount for the bet

    Attributes
    ----------
    amount: float
        Wagered amount for the bet
    """

    def __init__(self, amount: typing.SupportsFloat):
        self.amount: float = float(amount)

    @abstractmethod
    def get_result(self, table: Table) -> BetResult:
        pass

    def update_number(self, table: Table):
        pass

    def is_removable(self, table: Table) -> bool:
        return True

    def is_allowed(self, player: Player) -> bool:
        """
        Checks whether the bet is allowed to be placed on the given table.
        May depend on the player's bets also (e.g. for odds bets).

        Parameters
        ----------
        player

        Returns
        -------
        bool
            True if the bet is allowed, otherwise false.
        """
        return True

    def already_placed_bets(self, player: Player):
        return [x for x in player.bets if x._placed_key == self._placed_key]

    def already_placed(self, player: Player) -> bool:
        return len(self.already_placed_bets(player)) > 0

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self)

    @property
    def _hash_key(self) -> typing.Hashable:
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
        if isinstance(other, typing.SupportsFloat):
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
        if isinstance(other, typing.SupportsFloat):
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


class _WinningLosingNumbersBet(Bet, ABC):
    """
    A _WinningLosingNumbersBet has winning numbers, losing numbers, and payout ratios
    (possibly depending on the table) from which the result can be calculated.
    """

    def get_result(self, table: Table) -> BetResult:
        if table.dice.total in self.get_winning_numbers(table):
            result_amount = self.get_payout_ratio(table) * self.amount + self.amount
            should_remove = True
        elif table.dice.total in self.get_losing_numbers(table):
            result_amount = -1 * self.amount
            should_remove = True
        else:
            result_amount = 0
            should_remove = False

        return BetResult(result_amount, should_remove)

    @abstractmethod
    def get_winning_numbers(self, table: Table) -> list[int]:
        pass

    @abstractmethod
    def get_losing_numbers(self, table: Table) -> list[int]:
        pass

    @abstractmethod
    def get_payout_ratio(self, table: Table) -> float:
        pass


class _SimpleBet(_WinningLosingNumbersBet, ABC):
    """
    A _SimpleBet has fixed winning and losing numbers and payout ratio that
    can be known at instantiation and don't depend on the table.
    """

    winning_numbers: list[int] = []
    losing_numbers: list[int] = []
    payout_ratio: int = 1

    def get_winning_numbers(self, table: Table) -> list[int]:
        return self.winning_numbers

    def get_losing_numbers(self, table: Table) -> list[int]:
        return self.losing_numbers

    def get_payout_ratio(self, table: Table) -> float:
        return float(self.payout_ratio)


# Passline and related bets ---------------------------------------------------


class PassLine(_WinningLosingNumbersBet):
    def get_winning_numbers(self, table: Table) -> list[int]:
        if table.point.number is None:
            return [7, 11]
        return [table.point.number]

    def get_losing_numbers(self, table: Table) -> list[int]:
        if table.point.number is None:
            return [2, 3, 12]
        return [7]

    def get_payout_ratio(self, table: Table) -> float:
        return 1.0

    def is_removable(self, table: Table) -> bool:
        return table.point.status == "Off"

    def is_allowed(self, player: Player) -> bool:
        return player.table.point.status == "Off"


class Come(_WinningLosingNumbersBet):
    def __init__(self, amount: typing.SupportsFloat, number: int | None = None):
        super().__init__(amount)
        possible_numbers = (4, 5, 6, 7, 8, 9, 10)
        if number in possible_numbers:
            self.number = number
        else:
            self.number = None

    def get_winning_numbers(self, table: Table) -> list[int]:
        if self.number is None:
            return [7, 11]
        return [self.number]

    def get_losing_numbers(self, table: Table) -> list[int]:
        if self.number is None:
            return [2, 3, 12]
        return [7]

    def get_payout_ratio(self, table: Table) -> float:
        return 1.0

    def update_number(self, table: Table):
        possible_numbers = (4, 5, 6, 7, 8, 9, 10)
        if self.number is None and table.dice.total in possible_numbers:
            self.number = table.dice.total

    def is_removable(self, table: Table) -> bool:
        return self.number is None

    def is_allowed(self, player: Player) -> bool:
        return player.table.point.status == "On"

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.amount}, number={self.number})"


class DontPass(_WinningLosingNumbersBet):
    def get_winning_numbers(self, table: Table) -> list[int]:
        if table.point.number is None:
            return [2, 3]
        return [7]

    def get_losing_numbers(self, table: Table) -> list[int]:
        if table.point.number is None:
            return [7, 11]
        return [table.point.number]

    def get_payout_ratio(self, table: Table) -> float:
        return 1.0

    def is_allowed(self, player: Player) -> bool:
        return player.table.point.status == "Off"


class DontCome(_WinningLosingNumbersBet):
    def __init__(self, amount: typing.SupportsFloat, number: int | None = None):
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

    def get_payout_ratio(self, table: Table) -> float:
        return 1.0

    def update_number(self, table: Table):
        possible_numbers = (4, 5, 6, 7, 8, 9, 10)
        if self.number is None and table.dice.total in possible_numbers:
            self.number = table.dice.total

    def is_allowed(self, player: Player) -> bool:
        return player.table.point.status == "On"

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.amount}, number={self.number})"


# Odds bets -------------------------------------------------------------------


class Odds(_WinningLosingNumbersBet):
    def __init__(
        self,
        base_type: typing.Type[PassLine | DontPass | Come | DontCome],
        number: int,
        amount: float,
    ):
        super().__init__(amount)
        self.base_type = base_type
        self.number = number

    @property
    def light_side(self) -> bool:
        return issubclass(self.base_type, (PassLine, Come))

    @property
    def dark_side(self) -> bool:
        return issubclass(self.base_type, (DontPass, DontCome))

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
        max_bet = self.get_max_odds(player.table) * self.base_amount(player)
        return self.amount <= max_bet

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

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), self.base_type, self.number

    def __repr__(self):
        return (
            f"Odds(base_type={self.base_type}, number={self.number}, "
            f"amount={self.amount})"
        )


# Place bets ------------------------------------------------------------------


class Place(_SimpleBet):
    payout_ratios = {4: 9 / 5, 5: 7 / 5, 6: 7 / 6, 8: 7 / 6, 9: 7 / 5, 10: 9 / 5}
    losing_numbers: list[int] = [7]

    def __init__(self, number: int, amount: typing.SupportsFloat):
        super().__init__(amount)
        self.number = number
        self.payout_ratio = self.payout_ratios[number]
        self.winning_numbers = [number]

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"Place({self.winning_numbers[0]}, amount={self.amount})"


# _WinningLosingNumbersBets with variable payouts -----------------------------------------------------------------


class Field(_WinningLosingNumbersBet):
    winning_numbers = [2, 3, 4, 9, 10, 11, 12]
    losing_numbers = [5, 6, 7, 8]

    def get_winning_numbers(self, table: Table) -> list[int]:
        return self.winning_numbers

    def get_losing_numbers(self, table: Table) -> list[int]:
        return self.losing_numbers

    def get_payout_ratio(self, table: Table) -> float:
        if table.dice.total in table.settings["field_payouts"]:
            return float(table.settings["field_payouts"][table.dice.total])
        return 0.0


class CAndE(_WinningLosingNumbersBet):
    winning_numbers: list[int] = [2, 3, 11, 12]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {2, 3, 11, 12})

    def get_winning_numbers(self, table: Table) -> list[int]:
        return self.winning_numbers

    def get_losing_numbers(self, table: Table) -> list[int]:
        return self.losing_numbers

    def get_payout_ratio(self, table: Table) -> float:
        if table.dice.total in [2, 3, 12]:
            return 3.0
        elif table.dice.total in [11]:
            return 7.0
        else:
            raise NotImplementedError


# Simple bets in the middle of the table --------------------------------------


class Any7(_SimpleBet):
    winning_numbers: list[int] = [7]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {7})
    payout_ratio: int = 4


class Two(_SimpleBet):
    winning_numbers: list[int] = [2]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {2})
    payout_ratio: int = 30


class Three(_SimpleBet):
    winning_numbers: list[int] = [3]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {3})
    payout_ratio: int = 15


class Yo(_SimpleBet):
    winning_numbers: list[int] = [11]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {11})
    payout_ratio: int = 15


class Boxcars(_SimpleBet):
    winning_numbers: list[int] = [12]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {12})
    payout_ratio: int = 30


class AnyCraps(_SimpleBet):
    winning_numbers: list[int] = [2, 3, 12]
    losing_numbers: list[int] = list(ALL_DICE_NUMBERS - {2, 3, 12})
    payout_ratio: int = 7


# HardWay Bets ----------------------------------------------------------------


class HardWay(Bet):
    payout_ratios = {4: 7, 6: 9, 8: 9, 10: 7}

    def __init__(self, number: int, amount: typing.SupportsFloat) -> None:
        super().__init__(amount)
        self.number = number
        self.payout_ratio = self.payout_ratios[number]

    def get_result(self, table: Table) -> BetResult:
        if table.dice.result == self.winning_result:
            result_amount = self.payout_ratios[self.number] * self.amount + self.amount
            should_remove = True
        elif table.dice.total in (7, self.number):
            result_amount = -1 * self.amount
            should_remove = True
        else:
            result_amount = 0
            should_remove = False
        return BetResult(result_amount, should_remove)

    @property
    def winning_result(self) -> list[int]:
        return (int(self.number / 2), int(self.number / 2))

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.number}, amount={self.amount})"


# Fire bet -------------------------------------------------------------------


class Fire(Bet):
    def __init__(self, amount: float):
        super().__init__(amount)
        self.points_made: set[int] = set()
        self.ended: bool = False

    def get_result(self, table: Table) -> BetResult:

        if table.point.status == "Off":
            return BetResult(amount=0, remove=False)

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

        return BetResult(result_amount, remove=ended)

    def is_removable(self, table: Table) -> bool:
        return table.new_shooter

    def is_allowed(self, player: Player) -> bool:
        return player.table.new_shooter


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

        return BetResult(result_amount, should_remove)

    def is_removable(self, table: Table) -> bool:
        return table.new_shooter

    def is_allowed(self, player: Player) -> bool:
        return player.table.new_shooter


class All(_ATSBet):
    type: str = "all"
    numbers: list[int] = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]


class Tall(_ATSBet):
    type: str = "tall"
    numbers: list[int] = [8, 9, 10, 11, 12]


class Small(_ATSBet):
    type: str = "small"
    numbers: list[int] = [2, 3, 4, 5, 6]
