import typing

from crapssim.bet import WinningLosingNumbersBet
from crapssim.point import Point

if typing.TYPE_CHECKING:
    from crapssim.table import Table, Player


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

    def get_status(self, table: "Table") -> str | None:
        if table.point.status == 'Off' and table.last_roll in (4, 5, 6, 8, 9, 10):
            return None
        return super().get_status(table)

    def is_removable(self, player: "Player") -> bool:
        if player.table.point.status == 'On':
            return False
        return True

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'Off':
            return True
        return False


class Come(WinningLosingNumbersBet):
    def __init__(self, bet_amount: typing.SupportsFloat, point: Point | int | None = None):
        super().__init__(bet_amount)

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

    def update_point(self, player: 'Player'):
        if self.point.status == 'Off' and player.table.dice.total in (4, 5, 6, 8, 9, 10):
            player.bets.remove(self)
            player.bets.append(Come(self.amount, player.table.dice.total))

    def is_removable(self, player: "Player") -> bool:
        if self.point.status == 'On':
            return False
        return True

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'On':
            return True
        return False

    def get_hash_key(self) -> typing.Hashable:
        return type(self), self.amount, self.point

    def get_placed_key(self) -> typing.Hashable:
        return Come, self.point

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.amount}, point={self.point})'


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

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'Off':
            return True
        return False

    def get_status(self, table: "Table") -> str | None:
        if table.point.status is None and table.dice.total in (4, 5, 6, 8, 9, 10):
            return None
        return super().get_status(table)


class DontCome(WinningLosingNumbersBet):
    def __init__(self, bet_amount: typing.SupportsFloat, point: int | None = None) -> None:
        super().__init__(bet_amount)

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

    def update_point(self, player: 'Player'):
        if self.point.status == 'Off' and player.table.dice.total in (4, 5, 6, 8, 9, 10):
            player.bets.remove(self)
            player.bets.append(DontCome(self.amount, player.table.dice.total))

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'On':
            return True
        return False

    def get_hash_key(self):
        return type(self), self.amount, self.point

    def get_placed_key(self) -> typing.Hashable:
        return DontCome, self.point

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.amount}, point={self.point})'
