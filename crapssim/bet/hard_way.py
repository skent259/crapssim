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

    def get_placed_key(self) -> typing.Hashable:
        return HardWay, self.number
