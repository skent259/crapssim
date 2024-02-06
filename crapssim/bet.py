import copy
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

from crapssim.point import Point

if typing.TYPE_CHECKING:
    from crapssim.table import Player, Table


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


class Bet(ABC):
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
    def get_result(self, table: "Table") -> BetResult:
        pass

    def is_removable(self, player: "Player") -> bool:
        return True

    def is_allowed(self, player: "Player") -> bool:
        """
        Checks whether the bet is allowed to be placed on the given table.

        Parameters
        ----------
        player

        Returns
        -------
        bool
            True if the bet is allowed, otherwise false.
        """
        return True

    def update_point(self, player: "Player"):
        pass

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self)

    @property
    def _hash_key(self) -> typing.Hashable:
        return self._placed_key, self.amount

    def already_placed_bets(self, player: "Player"):
        return [x for x in player.bets if x._placed_key == self._placed_key]

    def already_placed(self, player: "Player") -> bool:
        return len(self.already_placed_bets(player)) > 0

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


class WinningLosingNumbersBet(Bet, ABC):
    @abstractmethod
    def get_winning_numbers(self, table: "Table") -> list[int]:
        pass

    @abstractmethod
    def get_losing_numbers(self, table: "Table") -> list[int]:
        pass

    @abstractmethod
    def get_payout_ratio(self, table: "Table") -> float:
        pass

    def get_result(self, table: "Table") -> BetResult:
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


# Passline and related bets ---------------------------------------------------


class PassLine(WinningLosingNumbersBet):
    def get_payout_ratio(self, table: "Table") -> float:
        return 1.0

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if table.point.number is None:
            return [7, 11]
        return [table.point.number]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if table.point.number is None:
            return [2, 3, 12]
        return [7]

    def is_removable(self, player: "Player") -> bool:
        return player.table.point.status == "Off"

    def is_allowed(self, player: "Player") -> bool:
        return player.table.point.status == "Off"


class Come(WinningLosingNumbersBet):
    def __init__(self, amount: typing.SupportsFloat, point: Point | int | None = None):
        super().__init__(amount)

        if point is None or isinstance(point, int):
            point = Point(point)

        self.point = point

    def get_payout_ratio(self, table: "Table") -> float:
        return 1.0

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if self.point == Point(None):
            return [7, 11]
        return [self.point.number]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if self.point == Point(None):
            return [2, 3, 12]
        return [7]

    def update_point(self, player: "Player"):
        possible_points = (4, 5, 6, 7, 8, 9, 10)
        if self.point.status == "Off" and player.table.dice.total in possible_points:
            player.bets.remove(self)
            player.bets.append(Come(self.amount, player.table.dice.total))

    def is_removable(self, player: "Player") -> bool:
        return self.point.status == "Off"

    def is_allowed(self, player: "Player") -> bool:
        return player.table.point.status == "On"

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), self.point

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.amount}, point={self.point})"


class DontPass(WinningLosingNumbersBet):
    def get_payout_ratio(self, table: "Table") -> float:
        return 1.0

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if table.point.number is None:
            return [2, 3]
        return [7]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if table.point.number is None:
            return [7, 11]
        return [table.point.number]

    def is_allowed(self, player: "Player") -> bool:
        return player.table.point.status == "Off"


class DontCome(WinningLosingNumbersBet):
    def __init__(self, amount: typing.SupportsFloat, point: int | None = None) -> None:
        super().__init__(amount)

        if point is None or isinstance(point, int):
            point = Point(point)

        self.point = point

    def get_payout_ratio(self, table: "Table") -> float:
        return 1.0

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if self.point is None:
            return [2, 3]
        return [7]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if self.point is None:
            return [7, 11]
        return [self.point.number]

    def update_point(self, player: "Player"):
        possible_points = (4, 5, 6, 7, 8, 9, 10)
        if self.point.status == "Off" and player.table.dice.total in possible_points:
            player.bets.remove(self)
            player.bets.append(DontCome(self.amount, player.table.dice.total))

    def is_allowed(self, player: "Player") -> bool:
        return player.table.point.status == "On"

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), self.point

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.amount}, point={self.point})"


# Odds bets -------------------------------------------------------------------


class Odds(WinningLosingNumbersBet):
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

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if self.light_side:
            return [self.number]
        elif self.dark_side:
            return [7]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if self.light_side:
            return [7]
        elif self.dark_side:
            return [self.number]

    def get_payout_ratio(self, table: "Table") -> float:
        light_ratios = {4: 2, 5: 3 / 2, 6: 6 / 5, 8: 6 / 5, 9: 3 / 2, 10: 2}
        dark_ratios = {n: 1 / x for n, x in light_ratios.items()}

        if self.light_side:
            return light_ratios[self.number]
        elif self.dark_side:
            return dark_ratios[self.number]

    def get_base_bets(self, player: "Player") -> list[Bet]:
        return [
            x
            for x in player.bets
            if isinstance(x, self.base_type)
            and x.get_winning_numbers(player.table)
            == self.get_winning_numbers(player.table)
        ]

    def get_base_amount(self, player: "Player"):
        return sum(x.amount for x in self.get_base_bets(player))

    def get_max_odds(self, table: "Table") -> float:
        if self.light_side:
            return table.settings["max_odds"][self.number]
        elif self.dark_side:
            return table.settings["max_dont_odds"][self.number]
        else:
            raise NotImplementedError

    def get_max_bet(self, player: "Player") -> float:
        return self.get_max_odds(player.table) * self.get_base_amount(player)

    def is_allowed(self, player: "Player") -> bool:
        return self.amount <= self.get_max_bet(player)

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), self.base_type, self.number

    def __repr__(self):
        return (
            f"Odds(base_type={self.base_type}, number={self.number}, "
            f"amount={self.amount})"
        )


# Place bets ------------------------------------------------------------------


class Place(WinningLosingNumbersBet):
    payout_ratios = {4: 9 / 5, 5: 7 / 5, 6: 7 / 6, 8: 7 / 6, 9: 7 / 5, 10: 9 / 5}
    losing_numbers: list[int] = [7]

    def __init__(self, number: int, amount: typing.SupportsFloat):
        super().__init__(amount)
        self.payout_ratio = self.payout_ratios[number]
        self.number = number
        self.winning_numbers = [number]

    def get_payout_ratio(self, table: "Table") -> float:
        return self.payout_ratio

    def get_winning_numbers(self, table: "Table") -> list[int]:
        return [self.number]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        return self.losing_numbers

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), self.number

    def __repr__(self) -> str:
        return f"Place({self.winning_numbers[0]}, amount={self.amount})"


# OneRollBets -----------------------------------------------------------------


class OneRollBet(WinningLosingNumbersBet, ABC):
    """WinningLosingNumbersBet where if the number isn't in the winning_numbers,
    it is in the losing_numbers."""

    def __init__(self, winning_numbers: list[int], amount: typing.SupportsFloat):
        self.winning_numbers = winning_numbers
        super().__init__(amount)

    def get_winning_numbers(self, table: "Table") -> list[int]:
        return self.winning_numbers

    def get_losing_numbers(self, table: "Table") -> list[int]:
        return [
            x
            for x in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
            if x not in self.get_winning_numbers(table)
        ]

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), tuple(self.winning_numbers)


class Field(OneRollBet):
    def __init__(self, amount: typing.SupportsFloat):
        super().__init__(winning_numbers=[2, 3, 4, 9, 10, 11, 12], amount=amount)

    def get_payout_ratio(self, table: "Table") -> float:
        if table.dice.total in table.settings["field_payouts"]:
            return float(table.settings["field_payouts"][table.dice.total])
        return 0.0


class StaticRatioOneRollBet(OneRollBet):
    def __init__(
        self,
        winning_numbers: list[int],
        payout_ratio: typing.SupportsFloat,
        amount: typing.SupportsFloat,
    ):
        super().__init__(winning_numbers, amount)
        self.payout_ratio = payout_ratio

    def get_payout_ratio(self, table: "Table") -> float:
        return float(self.payout_ratio)

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), tuple(self.winning_numbers), self.payout_ratio


class Any7(StaticRatioOneRollBet):
    payout_ratio: int = 4
    winning_numbers: list[int] = [7]

    def __init__(self, amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, amount)


class Two(StaticRatioOneRollBet):
    payout_ratio: int = 30
    winning_numbers: list[int] = [2]

    def __init__(self, amount: typing.SupportsFloat) -> None:
        super().__init__(self.winning_numbers, self.payout_ratio, amount)


class Three(StaticRatioOneRollBet):
    payout_ratio: int = 15
    winning_numbers: list[int] = [3]

    def __init__(self, amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, amount)


class Yo(StaticRatioOneRollBet):
    payout_ratio: int = 15
    winning_numbers: list[int] = [11]

    def __init__(self, amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, amount)


class Boxcars(StaticRatioOneRollBet):
    payout_ratio: int = 30
    winning_numbers: list[int] = [12]

    def __init__(self, amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, amount)


class AnyCraps(StaticRatioOneRollBet):
    payout_ratio: int = 7
    winning_numbers: list[int] = [2, 3, 12]

    def __init__(self, amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, amount)


class CAndE(OneRollBet):
    winning_numbers: list[int] = [2, 3, 11, 12]

    def __init__(self, amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, amount)

    def get_payout_ratio(self, table: "Table") -> float:
        if table.dice.total in [2, 3, 12]:
            return 3.0
        elif table.dice.total in [11]:
            return 7.0
        else:
            raise NotImplementedError


# HardWay Bets ----------------------------------------------------------------


class HardWay(Bet):
    payout_ratios = {4: 7, 6: 9, 8: 9, 10: 7}

    def __init__(self, number: int, amount: typing.SupportsFloat) -> None:
        super().__init__(amount)
        self.number = number
        self.payout_ratio = self.payout_ratios[number]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.number}, amount={self.amount})"

    @property
    def winning_result(self) -> list[int]:
        return [int(self.number / 2), int(self.number / 2)]

    @property
    def _placed_key(self) -> typing.Hashable:
        return type(self), self.number

    def get_result(self, table: "Table") -> BetResult:
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


# Fire bet -------------------------------------------------------------------


class Fire(Bet):
    def __init__(self, amount: float):
        super().__init__(amount)
        self.points_made: list[int] = []
        self.ended: bool = False

    def update_point(self, player: "Player"):
        if player.table.point.status == "Off":
            return

        point_number = player.table.point.number
        dice_total = player.table.dice.total
        if point_number == dice_total and point_number not in self.points_made:
            self.points_made.append(point_number)
        elif dice_total == 7:
            self.ended = True

    def get_result(self, table: "Table") -> BetResult:
        if self.ended and len(self.points_made) in table.settings["fire_points"]:
            payout_ratio = table.settings["fire_points"][len(self.points_made)]
            result_amount = payout_ratio * self.amount + self.amount
            remove = True
        elif self.ended and len(self.points_made) not in table.settings["fire_points"]:
            result_amount = -1 * self.amount
            remove = True
        else:
            result_amount = 0
            remove = False
        return BetResult(result_amount, remove)

    def is_allowed(self, player: "Player") -> bool:
        return player.table.new_shooter
