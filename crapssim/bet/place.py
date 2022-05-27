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

    def update(self, table: "Table") -> None:
        # place bets are inactive when point is "Off"
        if table.point == "On":
            super().update(table)

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


class Place4(Place):
    payout_ratio: float = Place.payout_ratios[4]
    winning_numbers: list[int] = [4]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(4, bet_amount)


class Place5(Place):
    payout_ratio: float = Place.payout_ratios[5]
    winning_numbers: list[int] = [5]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(5, bet_amount)


class Place6(Place):
    payout_ratio: float = Place.payout_ratios[6]
    winning_numbers: list[int] = [6]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(6, bet_amount)


class Place8(Place):
    payout_ratio: float = Place.payout_ratios[8]
    winning_numbers: list[int] = [8]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(8, bet_amount)


class Place9(Place):
    payout_ratio: float = Place.payout_ratios[9]
    winning_numbers: list[int] = [9]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(9, bet_amount)


class Place10(Place):
    payout_ratio: float = Place.payout_ratios[10]
    winning_numbers: list[int] = [10]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(10, bet_amount)