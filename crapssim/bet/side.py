import typing

from crapssim.bet import Bet, BetResult

if typing.TYPE_CHECKING:
    from crapssim import Table, Player


class Fire(Bet):
    def __init__(self, amount: float):
        super().__init__(amount)
        self.points_made: list[int] = []
        self.ended: bool = False

    def update_point(self, player: 'Player'):
        if player.table.point.status == 'Off':
            return

        point_number = player.table.point.number
        dice_total = player.table.dice.total
        if point_number == dice_total and point_number not in self.points_made:
            self.points_made.append(point_number)
        elif dice_total == 7:
            self.ended = True

    def get_result(self, table: "Table") -> BetResult:
        if self.ended and len(self.points_made) in table.settings['fire_points']:
            payout_ratio = table.settings['fire_points'][len(self.points_made)]
            result_amount = payout_ratio * self.amount + self.amount
            remove = True
        elif self.ended and len(self.points_made) not in table.settings['fire_points']:
            result_amount = -1 * self.amount
            remove = True
        else:
            result_amount = 0
            remove = False
        return BetResult(result_amount, remove)

    def allowed(self, player: "Player") -> bool:
        return player.table.new_shooter
