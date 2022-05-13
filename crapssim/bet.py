import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from crapssim.table import Table
    from crapssim.player import Player


class Bet(ABC):
    """
    A generic bet for the craps table

    Parameters
    ----------
    bet_amount : typing.SupportsFloat
        Wagered amount for the bet

    Attributes
    ----------
    bet_amount: float
        Wagered amount for the bet
    """

    def __init__(self, bet_amount: typing.SupportsFloat):
        self.bet_amount: float = float(bet_amount)

    @abstractmethod
    def get_payout_ratio(self, table: "Table"):
        pass

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def removable(self):
        return True

    def allowed(self, table: "Table", player: "Player") -> bool:
        """
        Checks whether the bet is allowed to be placed on the given table.

        Parameters
        ----------
        player
        table

        Returns
        -------
        bool
            True if the bet is allowed, otherwise false.
        """
        return True

    @abstractmethod
    def get_status(self, table: "Table") -> str | bool:
        pass

    def get_win_amount(self, table: "Table") -> float:
        if self.get_status(table) == "win":
            return self.get_payout_ratio(table) * self.bet_amount
        return 0.0

    def get_return_amount(self, table: "Table") -> float:
        status = self.get_status(table)
        if status == "win":
            return self.get_win_amount(table) + self.bet_amount
        if status is None and self.should_remove(table) is True:
            return self.bet_amount
        else:
            return 0

    def should_remove(self, table: "Table") -> bool:
        if self.get_status(table) is not None:
            return True
        return False

    def update(self, table: "Table") -> None:
        """
        Returns whether the bets status is win, lose or None and if win the amount won.

        Returns
        -------
        tuple[str | None, float]
            The status of the bet and the amount of the winnings.
        """
        pass

    def already_placed(self, player: "Player") -> bool:
        return player.has_bets(type(self))

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount})'


class WinningLosingNumbersBet(Bet, ABC):
    @property
    @abstractmethod
    def winning_numbers(self):
        pass

    @property
    @abstractmethod
    def losing_numbers(self):
        pass

    def get_status(self, table: "Table") -> str | None:
        if table.dice.total in self.winning_numbers:
            return "win"
        elif table.dice.total in self.losing_numbers:
            return "lose"
        return None

    def __eq__(self, other):
        if isinstance(other, Bet) and not isinstance(other, type(self)):
            return False
        elif isinstance(other, type(self)):
            return self.bet_amount == other.bet_amount and \
                   self.winning_numbers == other.winning_numbers and \
                   self.losing_numbers == other.losing_numbers
        else:
            raise NotImplementedError

    def __hash__(self):
        return hash((self.__class__, self.bet_amount,
                     tuple(self.winning_numbers),
                     tuple(self.losing_numbers)))


class SingleWinningNumberBet(WinningLosingNumbersBet, ABC):
    """WinningLosingNumbersBet where only one number wins."""
    @property
    @abstractmethod
    def winning_number(self):
        pass

    @property
    def winning_numbers(self):
        return [self.winning_number]


class SingleLosingNumberBet(WinningLosingNumbersBet, ABC):
    @property
    @abstractmethod
    def losing_number(self):
        pass

    @property
    def losing_numbers(self):
        return [self.losing_number]


class StaticPayoutRatio(Bet, ABC):
    @property
    @abstractmethod
    def payout_ratio(self):
        pass

    def get_payout_ratio(self, table: "Table"):
        return self.payout_ratio


"""
Passline and Come bets
"""


class BaseOdds(SingleWinningNumberBet, SingleLosingNumberBet, StaticPayoutRatio, ABC):
    @property
    @abstractmethod
    def base_bet_types(self) -> tuple[typing.Type[WinningLosingNumbersBet]]:
        pass

    @property
    @abstractmethod
    def table_odds_setting(self) -> str:
        pass

    @property
    @abstractmethod
    def key_number(self):
        pass

    @staticmethod
    @abstractmethod
    def by_number(number: int, bet_amount: float):
        pass

    def get_base_bets(self, player: "Player") -> list['AllowsOdds']:
        base_bets = player.get_bets(*self.base_bet_types, winning_numbers=self.winning_numbers)
        return base_bets

    def get_max_odds(self, table: "Table") -> int:
        return table.settings[self.table_odds_setting][self.key_number]

    def get_base_amount(self, player: "Player"):
        return sum(x.bet_amount for x in self.get_base_bets(player))

    def get_max_bet(self, table: "Table", player: "Player") -> typing.SupportsFloat:
        base_bet_amount = self.get_base_amount(player)
        max_odds = self.get_max_odds(table)
        return base_bet_amount * max_odds

    def allowed(self, table: "Table", player: "Player") -> bool:
        return self.get_max_bet(table, player) >= self.bet_amount


class AllowsOdds(WinningLosingNumbersBet, StaticPayoutRatio, ABC):
    payout_ratio: float = 1.0

    def __init__(self, bet_amount: float,
                 point: int | None = None,
                 new_point: bool = False):
        super().__init__(bet_amount)
        self.point: int = point
        self.new_point: bool = new_point

    def place_odds(self, bet_amount: typing.SupportsFloat, player: "Player", table):
        player.place_bet(self.get_odds_bet(bet_amount), table)

    def get_odds_bet(self, bet_amount: typing.SupportsFloat):
        return self.odds_type.by_number(self.point, bet_amount)

    @property
    @abstractmethod
    def odds_type(self) -> typing.Type[BaseOdds]:
        pass

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.point == other.point

    def __repr__(self):
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount}, point={self.point})'


class PassLine(AllowsOdds):
    @property
    def odds_type(self) -> typing.Type[BaseOdds]:
        return Odds

    @property
    def key_number(self) -> int:
        return self.winning_numbers[0]

    @property
    def winning_numbers(self):
        if self.point is None:
            return [7, 11]
        return [self.point]

    @property
    def losing_numbers(self):
        if self.point is None:
            return [2, 3, 12]
        return [7]

    def get_status(self, table: "Table"):
        if self.new_point:
            return None
        return super().get_status(table)

    def update(self, table: "Table") -> None:
        self.new_point = False
        if self.point is None and self.get_status(table) not in ("win", "lose"):
            self.point = table.dice.total
            self.new_point = True

    @property
    def removable(self):
        if self.point is not None:
            return False
        return True

    def allowed(self, table: "Table", player: "Player") -> bool:
        if table.point.status == 'Off':
            return True
        return False


class Come(PassLine):
    def allowed(self, table: "Table", player: "Player") -> bool:
        if table.point.status == 'On':
            return True
        return False

    def already_placed(self, player: "Player") -> bool:
        return player.has_bets(type(self), point=self.point)


"""
Passline/Come bet odds
"""


class Odds(BaseOdds, ABC):
    base_bet_types: tuple[typing.Type[WinningLosingNumbersBet]] = (PassLine, Come)
    table_odds_setting: str = 'max_odds'
    losing_number: list[int] = 7

    @property
    def key_number(self):
        return self.winning_number

    @staticmethod
    def by_number(number: int, bet_amount: float):
        return {4: Odds4, 5: Odds5, 6: Odds6, 8: Odds8, 9: Odds9, 10: Odds10}[number](bet_amount)


class Odds4(Odds):
    winning_number: int = 4
    payout_ratio: float = 2 / 1


class Odds5(Odds):
    winning_number: int = 5
    payout_ratio: float = 3 / 2


class Odds6(Odds):
    winning_number: int = 6
    payout_ratio: float = 6 / 5


class Odds8(Odds):
    winning_number: int = 8
    payout_ratio: float = 6 / 5


class Odds9(Odds):
    winning_number: int = 9
    payout_ratio: float = 3 / 2


class Odds10(Odds):
    winning_number: int = 10
    payout_ratio: float = 2 / 1


"""
Place Bets on 4,5,6,8,9,10
"""


class Place(SingleWinningNumberBet, SingleLosingNumberBet, StaticPayoutRatio, ABC):
    def update(self, table: "Table") -> None:
        # place bets are inactive when point is "Off"
        if table.point == "On":
            super().update(table)

    @staticmethod
    def by_number(number: int, bet_amount: float):
        bet_type = {4: Place4,
                    5: Place5,
                    6: Place6,
                    8: Place8,
                    9: Place9,
                    10: Place10}[number]
        return bet_type(bet_amount)


class Place4(Place):
    payout_ratio: float = 9 / 5
    winning_number: int = 4
    losing_number: list[int] = 7


class Place5(Place):
    payout_ratio: float = 7 / 5
    winning_number: int = 5
    losing_number: list[int] = 7


class Place6(Place):
    payout_ratio: float = 7 / 6
    winning_number: int = 6
    losing_number: list[int] = 7


class Place8(Place):
    payout_ratio: float = 7 / 6
    winning_number: int = 8
    losing_number: list[int] = 7


class Place9(Place):
    payout_ratio: float = 7 / 5
    winning_number: int = 9
    losing_number: list[int] = 7


class Place10(Place):
    payout_ratio: float = 9 / 5
    winning_number: int = 10
    losing_number: list[int] = 7


"""
Field bet
"""


class OneRollBet(WinningLosingNumbersBet, ABC):
    """WinningLosingNumbersBet where if the number isn't in the winning_numbers, it is in the losing_numbers."""
    @property
    def losing_numbers(self):
        return [x for x in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] if x not in self.winning_numbers]


class Field(OneRollBet):
    def get_payout_ratio(self, table: "Table"):
        if table.dice.total in table.settings['field_payouts']:
            return table.settings['field_payouts'][table.dice.total]
        return 0

    @property
    def winning_numbers(self):
        return [2, 3, 4, 9, 10, 11, 12]


"""
Don't pass and Don't come bets
"""


class DontPass(AllowsOdds):
    @property
    def odds_type(self) -> typing.Type[BaseOdds]:
        return LayOdds

    @property
    def key_number(self) -> int:
        return self.losing_numbers[0]

    @property
    def winning_numbers(self):
        if self.point is None:
            return [2, 3]
        return [7]

    @property
    def losing_numbers(self):
        if self.point is None:
            return [7, 11]
        return [self.point]

    def update(self, table: "Table") -> None:
        self.new_point = False
        if self.point is None and table.dice.total in (4, 5, 6, 8, 9, 10):
            self.point = table.dice.total
            self.new_point = True

    def allowed(self, table: "Table", player) -> bool:
        if table.point.status == 'Off':
            return True
        return False

    def get_status(self, table: "Table") -> str | None:
        if self.new_point:
            return None
        return super().get_status(table)


class DontCome(DontPass):
    def allowed(self, table: "Table", player) -> bool:
        if table.point.status == 'On':
            return True
        return False

    def already_placed(self, player: "Player") -> bool:
        return player.has_bets(type(self), point=self.point)


"""
Don't pass/Don't come lay odds
"""


class LayOdds(BaseOdds, ABC):
    base_bet_types: typing.Type[AllowsOdds] = (DontPass, DontCome)
    table_odds_setting: str = 'max_dont_odds'
    winning_number: int = 7

    @property
    def key_number(self):
        return self.losing_number

    @staticmethod
    def by_number(number: int, bet_amount: float):
        return {4: LayOdds4,
                5: LayOdds5,
                6: LayOdds6,
                8: LayOdds8,
                9: LayOdds9,
                10: LayOdds10}[number](bet_amount)


class LayOdds4(LayOdds):
    losing_number: int = 4
    payout_ratio: float = 1 / 2


class LayOdds5(LayOdds):
    losing_number: int = 5
    payout_ratio: float = 2 / 3


class LayOdds6(LayOdds):
    losing_number: int = 6
    payout_ratio: float = 5 / 6


class LayOdds8(LayOdds):
    losing_number: int = 8
    payout_ratio: float = 5 / 6


class LayOdds9(LayOdds):
    losing_number: int = 9
    payout_ratio: float = 2 / 3


class LayOdds10(LayOdds):
    losing_number: int = 10
    payout_ratio: float = 1 / 2


"""
Center-table Bets
"""


class Any7(OneRollBet, SingleWinningNumberBet, StaticPayoutRatio):
    payout_ratio: int = 4
    winning_number: int = 7


class Two(OneRollBet, SingleWinningNumberBet, StaticPayoutRatio):
    payout_ratio: int = 30
    winning_number: int = 2


class Three(OneRollBet, SingleWinningNumberBet, StaticPayoutRatio):
    payout_ratio: int = 15
    winning_number: int = 3


class Yo(OneRollBet, SingleWinningNumberBet, StaticPayoutRatio):
    payout_ratio: int = 15
    winning_number: int = 11


class Boxcars(OneRollBet, SingleWinningNumberBet, StaticPayoutRatio):
    payout_ratio: int = 30
    winning_number: int = 12


class AnyCraps(OneRollBet, WinningLosingNumbersBet, StaticPayoutRatio):
    payout_ratio: int = 7
    winning_numbers: list[int] = [2, 3, 12]


class CAndE(OneRollBet, WinningLosingNumbersBet):
    winning_numbers: list[int] = [2, 3, 11, 12]

    def get_payout_ratio(self, table: "Table"):
        if table.dice.total in [2, 3, 12]:
            return 3
        elif table.dice.total in [11]:
            return 7
        else:
            raise NotImplementedError


class HardWay(StaticPayoutRatio, ABC):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)

    @property
    @abstractmethod
    def number(self):
        pass

    @property
    def winning_result(self):
        return [self.number / 2, self.number / 2]

    def get_payout_ratio(self, table: "Table"):
        return self.payout_ratio

    def get_status(self, table: "Table"):
        if table.dice.result == self.winning_result:
            return "win"
        elif table.dice.total in [self.number, 7]:
            return "lose"
        return None

    def __eq__(self, other):
        if isinstance(other, Bet) and not isinstance(other, type(self)):
            return False
        elif isinstance(other, type(self)):
            return self.number == other.number and self.bet_amount == other.bet_amount

    def __hash__(self):
        return hash((self.__class__, self.number, self.bet_amount))


class Hard4(HardWay):
    payout_ratio: int = 7
    number: int = 4


class Hard6(HardWay):
    payout_ratio: int = 9
    number: int = 6


class Hard8(HardWay):
    payout_ratio: int = 9
    number: int = 8


class Hard10(HardWay):
    payout_ratio: int = 7
    number: int = 10


class Fire(Bet):
    def __hash__(self):
        return hash((self.__class__, self.bet_amount, tuple(self.points_made),
                     tuple(self.current_point)))

    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.bet_amount: float = bet_amount
        self.points_made: list[int] = []
        self.current_point: int | None = None
        self.new_point_made: bool = False

    def get_status(self, table: "Table"):
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

    def point_made(self, table: "Table"):
        if table.dice.total not in self.points_made:
            self.new_point_made = True
            self.points_made = self.points_made + [table.dice.total]
        self.current_point = None

    def allowed(self, table: "Table", player) -> bool:
        return table.new_shooter

    def get_payout_ratio(self, table: "Table"):
        if len(self.points_made) in table.settings['fire_points']:
            return table.settings['fire_points'][len(self.points_made)]
        else:
            raise NotImplementedError

    def __eq__(self, other: Bet):
        if isinstance(other, Bet) and not isinstance(other, type(self)):
            return False
        elif isinstance(other, type(self)):
            return self.bet_amount == other.bet_amount and \
                self.points_made == other.points_made
