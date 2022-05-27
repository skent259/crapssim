import typing

from crapssim.bet import Bet

if typing.TYPE_CHECKING:
    from crapssim import Table, Player


class Fire(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.bet_amount: float = bet_amount
        self.points_made: list[int] = []
        self.current_point: int | None = None
        self._status: str | None = None

    def get_status(self, table: "Table") -> str | None:
        return self._status

    def should_remove(self, table: "Table") -> bool:
        if len(self.points_made) == 6 or self._status == "lose":
            return True
        return False

    def update(self, table: "Table") -> None:
        if self.current_point is None and table.dice.total in (4, 5, 6, 8, 9, 10):
            self.current_point = table.dice.total
        elif self.current_point is not None and self.current_point == table.dice.total:
            self.point_made(table)
        elif self.current_point is not None and table.dice.total == 7:
            self._status = 'lose'

    def point_made(self, table: "Table") -> None:
        if table.dice.total not in self.points_made:
            self.points_made = self.points_made + [table.dice.total]
            if len(self.points_made) in table.settings['fire_points']:
                self._status = 'win'
        else:
            self._status = None
        self.current_point = None

    def allowed(self, player: "Player") -> bool:
        return player.table.new_shooter

    def get_payout_ratio(self, table: "Table") -> float:
        if len(self.points_made) in table.settings['fire_points']:
            return float(table.settings['fire_points'][len(self.points_made)])
        else:
            raise NotImplementedError
