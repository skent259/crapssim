import typing
from abc import ABC, abstractmethod

from crapssim.bet import WinningLosingNumbersBet, Bet

if typing.TYPE_CHECKING:
    from crapssim import Table, Player


class OneRollBet(WinningLosingNumbersBet, ABC):
    """WinningLosingNumbersBet where if the number isn't in the winning_numbers,
    it is in the losing_numbers."""

    def __init__(self, winning_numbers: list[int], bet_amount: typing.SupportsFloat):
        self.winning_numbers = winning_numbers
        super().__init__(bet_amount)

    def get_winning_numbers(self, table: "Table") -> list[int]:
        return self.winning_numbers

    def get_losing_numbers(self, table: "Table") -> list[int]:
        return [x for x in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                if x not in self.get_winning_numbers(table)]

    def get_placed_key(self) -> typing.Hashable:
        return OneRollBet, tuple(self.winning_numbers)


class Field(OneRollBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__([2, 3, 4, 9, 10, 11, 12], bet_amount)

    def get_payout_ratio(self, table: "Table") -> float:
        if table.dice.total in table.settings['field_payouts']:
            return float(table.settings['field_payouts'][table.dice.total])
        return 0.0


class StaticRatioOneRollBet(OneRollBet):
    def __init__(self, winning_numbers: list[int],
                 payout_ratio: typing.SupportsFloat,
                 bet_amount: typing.SupportsFloat):
        super().__init__(winning_numbers, bet_amount)
        self.payout_ratio = payout_ratio

    def get_payout_ratio(self, table: "Table") -> float:
        return float(self.payout_ratio)

    def get_placed_key(self) -> typing.Hashable:
        return StaticRatioOneRollBet, tuple(self.winning_numbers), self.payout_ratio


class Any7(StaticRatioOneRollBet):
    payout_ratio: int = 4
    winning_numbers: list[int] = [7]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class Two(StaticRatioOneRollBet):
    payout_ratio: int = 30
    winning_numbers: list[int] = [2]

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class Three(StaticRatioOneRollBet):
    payout_ratio: int = 15
    winning_numbers: list[int] = [3]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class Yo(StaticRatioOneRollBet):
    payout_ratio: int = 15
    winning_numbers: list[int] = [11]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class Boxcars(StaticRatioOneRollBet):
    payout_ratio: int = 30
    winning_numbers: list[int] = [12]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class AnyCraps(StaticRatioOneRollBet):
    payout_ratio: int = 7
    winning_numbers: list[int] = [2, 3, 12]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class CAndE(OneRollBet):
    winning_numbers: list[int] = [2, 3, 11, 12]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, bet_amount)

    def get_payout_ratio(self, table: "Table") -> float:
        if table.dice.total in [2, 3, 12]:
            return 3.0
        elif table.dice.total in [11]:
            return 7.0
        else:
            raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bet):
            raise NotImplementedError
        return isinstance(other, CAndE) and self.bet_amount == other.bet_amount

    def __hash__(self) -> int:
        return hash((CAndE, self.bet_amount))