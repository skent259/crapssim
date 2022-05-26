import typing

from crapssim.bet.base import Bet

if typing.TYPE_CHECKING:
    from crapssim import Table


class HardWay(Bet):
    payout_ratios = {4: 7, 6: 9, 8: 9, 10: 7}

    def __init__(self, number: int, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(bet_amount)
        self.number = number
        self.payout_ratio = self.payout_ratios[number]

    @property
    def winning_result(self) -> list[int]:
        return [int(self.number / 2), int(self.number / 2)]

    def get_payout_ratio(self, table: "Table") -> float:
        return float(self.payout_ratio)

    def get_status(self, table: "Table") -> str | None:
        if table.dice.result == self.winning_result:
            return "win"
        elif table.dice.total in [self.number, 7]:
            return "lose"
        return None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet) and not isinstance(other, type(self)):
            return False
        elif isinstance(other, type(self)):
            return self.number == other.number and self.bet_amount == other.bet_amount
        else:
            raise NotImplementedError

    def __hash__(self) -> int:
        return hash((type(self), self.number, self.bet_amount))


class Hard4(HardWay):
    payout_ratio: int = HardWay.payout_ratios[4]
    number: int = 4

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.number, bet_amount)


class Hard6(HardWay):
    payout_ratio: int = HardWay.payout_ratios[6]
    number: int = 6

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.number, bet_amount)


class Hard8(HardWay):
    payout_ratio: int = HardWay.payout_ratios[8]
    number: int = 8

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.number, bet_amount)


class Hard10(HardWay):
    payout_ratio: int = HardWay.payout_ratios[10]
    number: int = 10

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.number, bet_amount)