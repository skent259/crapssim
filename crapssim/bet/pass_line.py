import typing
from abc import abstractmethod, ABC

from crapssim.bet import WinningLosingNumbersBet, Bet
from crapssim.point import Point

if typing.TYPE_CHECKING:
    from crapssim.table import Table, Player


class PassLine(WinningLosingNumbersBet):
    def get_payout_ratio(self, table: "Table") -> float:
        return 1.0

    @staticmethod
    def get_odds_bet(bet_amount: typing.SupportsFloat, table: "Table") -> "Odds":
        if table.point.number is not None:
            return Odds(table.point.number, bet_amount)
        else:
            raise ValueError

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
    def get_payout_ratio(self, table: "Table") -> float:
        return 1.0

    def __init__(self, bet_amount: typing.SupportsFloat, point: Point | int | None = None):
        super().__init__(bet_amount)

        if point is None or isinstance(point, int):
            point = Point(point)

        self.point = point

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
            player.bets_on_table.remove(self)
            player.bets_on_table.append(Come(self.bet_amount, player.table.dice.total))

    def is_removable(self, player: "Player") -> bool:
        if self.point.status == 'On':
            return False
        return True

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'On':
            return True
        return False

    def get_odds_bet(self, bet_amount: typing.SupportsFloat, table: "Table") -> "Odds":
        if self.point is not None:
            return Odds(self.point.number, bet_amount)
        else:
            raise ValueError

    def get_hash_key(self) -> typing.Hashable:
        return type(self), self.bet_amount, self.point

    def get_placed_key(self) -> typing.Hashable:
        return Come, self.point

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount}, point={self.point})'


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

    @staticmethod
    def get_odds_bet(bet_amount: typing.SupportsFloat, table: "Table") -> "LayOdds":
        if table.point.number is not None:
            return LayOdds(table.point.number, bet_amount)
        else:
            raise NotImplementedError


class DontCome(WinningLosingNumbersBet):
    def get_payout_ratio(self, table: "Table") -> float:
        return 1.0

    def __init__(self, bet_amount: typing.SupportsFloat, point: int | None = None) -> None:
        super().__init__(bet_amount)

        if point is None or isinstance(point, int):
            point = Point(point)

        self.point = point

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
            player.bets_on_table.remove(self)
            player.bets_on_table.append(DontCome(self.bet_amount, player.table.dice.total))

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'On':
            return True
        return False

    def get_odds_bet(self, bet_amount: typing.SupportsFloat, table: "Table") -> "LayOdds":
        if self.point is not None:
            return LayOdds(self.point.number, bet_amount)
        else:
            raise NotImplementedError

    def get_hash_key(self):
        return type(self), self.bet_amount, self.point

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount}, point={self.point})'

    def get_placed_key(self) -> typing.Hashable:
        return DontCome, self.point


class BaseOdds(Bet):
    def __init__(self, payout_ratios: dict[int, float],
                 number: int,
                 bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.payout_ratios = payout_ratios
        self.number = number

    def get_payout_ratio(self, table: "Table") -> float:
        return float(self.payout_ratios[self.number])

    @abstractmethod
    def get_base_amount(self, player_bets: typing.Iterable[Bet], table_point: int | None) -> float:
        pass

    @abstractmethod
    def get_max_odds(self, player: "Player") -> int:
        pass

    def get_max_bet(self, player: "Player") -> float:
        max_odds = self.get_max_odds(player)
        base_amount = self.get_base_amount(player.bets_on_table, player.table.point.number)
        max_bet = base_amount * max_odds
        return max_bet


class Odds(BaseOdds):
    payout_ratios = {4: 2 / 1, 5: 3 / 2, 6: 6 / 5, 8: 6 / 5, 9: 3 / 2, 10: 2 / 1}

    def __init__(self, number: int, bet_amount: typing.SupportsFloat):
        super().__init__(self.payout_ratios, number, bet_amount)

    def get_status(self, table: "Table") -> str | None:
        if table.dice.total == self.number:
            return 'win'
        elif table.dice.total == 7:
            return 'lose'
        else:
            return None

    def get_base_amount(self, player_bets: typing.Iterable[Bet], table_point: int | None) -> float:
        base_amount = 0.0
        if table_point == self.number:
            pass_line_bets = [x for x in player_bets if isinstance(x, PassLine)]
            base_amount += sum(x.bet_amount for x in pass_line_bets)
        come_bets = [x for x in player_bets if isinstance(x, Come)]
        matching_come_bets = [x for x in come_bets if x.point == self.number]
        base_amount += sum(x.bet_amount for x in matching_come_bets)
        return base_amount

    def get_max_odds(self, player: "Player") -> int:
        max_odds = player.table.settings['max_odds'][self.number]
        return max_odds

    def allowed(self, player: "Player") -> bool:
        max_bet = self.get_max_bet(player)
        return self.bet_amount <= max_bet

    def get_placed_key(self) -> typing.Hashable:
        return Odds, self.number

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(number={self.number}, bet_amount={self.bet_amount})'


class LayOdds(BaseOdds):
    payout_ratios = {4: 1 / 2, 5: 2 / 3, 6: 5 / 6, 8: 5 / 6, 9: 2 / 3, 10: 1 / 2}

    def __init__(self, number: int, bet_amount: typing.SupportsFloat):
        super().__init__(self.payout_ratios, number, bet_amount)

    def get_payout_ratio(self, table: "Table") -> float:
        return self.payout_ratios[self.number]

    def get_status(self, table: "Table") -> str | None:
        if table.dice.total == self.number:
            return 'lose'
        elif table.dice.total == 7:
            return 'win'
        return None

    def get_base_amount(self, player_bets: typing.Iterable[Bet], table_point: int | None) -> float:
        base_amount = 0.0
        if table_point == self.number:
            pass_line_bets = [x for x in player_bets if isinstance(x, PassLine)]
            base_amount += sum(x.bet_amount for x in pass_line_bets)
        come_bets = [x for x in player_bets if isinstance(x, Come)]
        matching_come_bets = [x for x in come_bets if x.point == self.number]
        base_amount += sum(x.bet_amount for x in matching_come_bets)
        return base_amount

    def get_max_odds(self, player: "Player") -> int:
        max_odds = player.table.settings['max_dont_odds'][self.number]
        return max_odds

    def get_placed_key(self) -> typing.Hashable:
        return LayOdds, self.number

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(number={self.number}, bet_amount={self.bet_amount})'
