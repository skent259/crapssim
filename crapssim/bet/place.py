import typing

from crapssim.bet import WinningLosingNumbersBet, Bet

if typing.TYPE_CHECKING:
    from crapssim import Table, Player


class Place(WinningLosingNumbersBet):
    payout_ratios = {4: 9 / 5, 5: 7 / 5, 6: 7 / 6, 8: 7 / 6, 9: 7 / 5, 10: 9 / 5}
    losing_numbers: list[int] = [7]

    def __init__(self, number: int, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.payout_ratio = self.payout_ratios[number]
        self.number = number
        self.winning_numbers = [number]

    def get_payout_ratio(self, table: "Table") -> float:
        return self.payout_ratio

    def get_winning_numbers(self, table: "Table") -> list[int]:
        return [self.number]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        return self.losing_numbers

    def get_placed_key(self) -> typing.Hashable:
        return Place, self.number

    def __repr__(self) -> str:
        return f'Place(number={self.winning_numbers[0]}, bet_amount={self.bet_amount})'
