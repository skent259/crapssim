import typing
from crapssim.bet import Bet, PassLine, Come, DontPass, DontCome, WinningLosingNumbersBet

if typing.TYPE_CHECKING:
    from crapssim import Table, Player


class Odds(WinningLosingNumbersBet):
    def __init__(self, base_type: typing.Type[PassLine | DontPass | Come | DontCome],
                 number: int,
                 bet_amount: float):
        super().__init__(bet_amount)
        self.base_type = base_type
        self.number = number

    @property
    def light_side(self) -> bool:
        return issubclass(self.base_type, (PassLine, Come))

    @property
    def dark_side(self) -> bool:
        return issubclass(self.base_type, (DontPass, DontCome))

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if self.light_side:
            return [self.number]
        elif self.dark_side:
            return [7]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if self.light_side:
            return [7]
        elif self.dark_side:
            return [self.number]

    def get_payout_ratio(self, table: "Table") -> float:
        if self.light_side:
            return {4: 2 / 1, 5: 3 / 2, 6: 6 / 5, 8: 6 / 5, 9: 3 / 2, 10: 2 / 1}[self.number]
        elif self.dark_side:
            return {4: 1 / 2, 5: 2 / 3, 6: 5 / 6, 8: 5 / 6, 9: 2 / 3, 10: 1 / 2}[self.number]

    def get_base_bets(self, player: "Player") -> list[Bet]:
        return [x for x in player.bets if isinstance(x, self.base_type)
                and x.get_winning_numbers(player.table) == self.get_winning_numbers(player.table)]

    def get_base_amount(self, player: "Player"):
        return sum(x.amount for x in self.get_base_bets(player))

    def get_max_odds(self, table: "Table") -> float:
        if self.light_side:
            return table.settings['max_odds'][self.number]
        elif self.dark_side:
            return table.settings['max_dont_odds'][self.number]
        else:
            raise NotImplementedError

    def get_max_bet(self, player: "Player") -> float:
        return self.get_max_odds(player.table) * self.get_base_amount(player)

    def allowed(self, player: "Player") -> bool:
        return self.amount <= self.get_max_bet(player)

    def get_placed_key(self) -> typing.Hashable:
        return self.__class__, self.base_type, self.number

    def __repr__(self):
        return f'Odds(base_type={self.base_type}, number={self.number}, ' \
               f'bet_amount={self.amount})'
