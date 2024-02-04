import typing

from crapssim.bet.base import Bet, BetResult

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

    def get_placed_key(self) -> typing.Hashable:
        return HardWay, self.number

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
