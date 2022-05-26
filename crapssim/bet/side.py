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
        self.new_point_made: bool = False

    def get_status(self, table: "Table") -> str | None:
        if self.new_point_made and len(self.points_made) in table.settings['fire_points']:
            return "win"
        elif self.current_point is not None and table.dice.total == 7:
            return "lose"
        return None

    def should_remove(self, table: "Table") -> bool:
        if len(self.points_made) == 6 or self.get_status(table) == "lose":
            return True
        return False

    def update(self, table: "Table") -> None:
        self.new_point_made = False
        if self.current_point is None and table.dice.total in (4, 5, 6, 8, 9, 10):
            self.current_point = table.dice.total
        elif self.current_point is not None and self.current_point == table.dice.total:
            self.point_made(table)

    def point_made(self, table: "Table") -> None:
        if table.dice.total not in self.points_made:
            self.new_point_made = True
            self.points_made = self.points_made + [table.dice.total]
        self.current_point = None

    def allowed(self, player: "Player") -> bool:
        return player.table.new_shooter

    def get_payout_ratio(self, table: "Table") -> float:
        if len(self.points_made) in table.settings['fire_points']:
            return float(table.settings['fire_points'][len(self.points_made)])
        else:
            raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet) and not isinstance(other, type(self)):
            return False
        elif isinstance(other, type(self)):
            return self.bet_amount == other.bet_amount and \
                   self.points_made == other.points_made
        else:
            raise NotImplementedError

    def __hash__(self) -> int:
        return hash((Fire, self.bet_amount, tuple(self.points_made)))