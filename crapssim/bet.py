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
    subname : string
        Subname, usually denotes number for a come/don't come bet
    """

    def __init__(self, bet_amount: typing.SupportsFloat, player=None, table=None):
        self.bet_amount: float = float(bet_amount)
        self.subname: str = str()
        self.player: Player | None = player
        self.table: Table | None = table

    @property
    @abstractmethod
    def payout_ratio(self):
        pass

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def removable(self):
        return True

    def allowed(self, table: 'Table') -> bool:
        """
        Checks whether the bet is allowed to be placed on the given table.

        Parameters
        ----------
        table : Table
            The table to check the bet against.

        Returns
        -------
        bool
            True if the bet is allowed, otherwise false.
        """
        return True

    @property
    @abstractmethod
    def status(self) -> str | bool:
        pass

    @property
    def win_amount(self) -> float:
        if self.status == "win":
            return self.payout_ratio * self.bet_amount
        return 0.0

    @property
    def remove(self) -> bool:
        if self.status is not None:
            return True
        return False

    def _update_bet(self) -> tuple[str | None, float, bool]:
        """
        Returns whether the bets status is win, lose or None and if win the amount won.

        Returns
        -------
        tuple[str | None, float]
            The status of the bet and the amount of the winnings.
        """
        return self.status, self.win_amount, self.remove


class WinningLosingNumbersBet(Bet, ABC):
    @property
    @abstractmethod
    def winning_numbers(self):
        pass

    @property
    @abstractmethod
    def losing_numbers(self):
        pass

    @property
    def status(self) -> str | None:
        if self.table.dice.total in self.winning_numbers:
            return "win"
        elif self.table.dice.total in self.losing_numbers:
            return "lose"
        return None


"""
Passline and Come bets
"""


class PassLine(WinningLosingNumbersBet):
    payout_ratio: float = 1.0

    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.point: int | None = None
        self.new_point: bool = False

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

    @property
    def remove(self):
        if self.new_point is True:
            return False
        return super().remove

    def _update_bet(self) -> tuple[str | None, float, bool]:
        self.new_point = False

        if self.point is None and self.status not in ("win", "lose"):
            self.point = self.table.dice.total
            self.new_point = True

        return self.status, self.win_amount, self.remove

    @property
    def removable(self):
        if self.point is not None:
            return False
        return True

    def allowed(self, table: 'Table') -> bool:
        if table.point.status == 'Off':
            return True
        return False


class Come(PassLine):
    def _update_bet(self) -> tuple[str | None, float, bool]:
        super()._update_bet()
        if self.point is not None and self.subname == "":
            self.subname = str(self.point)
        return self.status, self.win_amount, self.remove

    def allowed(self, table: 'Table') -> bool:
        if table.point.status == 'On':
            return True
        return False


"""
Passline/Come bet odds
"""


class Odds(WinningLosingNumbersBet):
    def __init__(self, bet_amount: typing.SupportsFloat, bet_object: PassLine | Come):
        super().__init__(bet_amount, None)
        self.bet_object = bet_object

        if not isinstance(bet_object, PassLine) and not isinstance(bet_object, Come):
            raise TypeError('bet_object must be either a PassLine or Come Bet.')

        self.subname: str = "".join(str(e) for e in bet_object.winning_numbers)

    @property
    def winning_numbers(self):
        return self.bet_object.winning_numbers

    @property
    def losing_numbers(self):
        return self.bet_object.losing_numbers

    @property
    def payout_ratio(self):
        if self.winning_numbers in ([4], [10]):
            return 2 / 1
        elif self.winning_numbers in ([5], [9]):
            return 3 / 2
        elif self.winning_numbers in ([6], [8]):
            return 6 / 5
        else:
            raise NotImplementedError

    def allowed(self, table: 'Table') -> bool:
        if isinstance(self.bet_object, PassLine):
            if table.point.status == 'Off':
                return False
            return True


"""
Place Bets on 4,5,6,8,9,10
"""


class Place(WinningLosingNumbersBet, ABC):
    def _update_bet(self) -> tuple[str | None, float, bool]:
        # place bets are inactive when point is "Off"
        if self.table.point == "On":
            return super()._update_bet()
        return None, 0, False


class Place4(Place):
    payout_ratio: float = 9 / 5
    winning_numbers: list[int] = [4]
    losing_numbers: list[int] = [7]


class Place5(Place):
    payout_ratio: float = 7 / 5
    winning_numbers: list[int] = [5]
    losing_numbers: list[int] = [7]


class Place6(Place):
    payout_ratio: float = 7 / 6
    winning_numbers: list[int] = [6]
    losing_numbers: list[int] = [7]


class Place8(Place):
    payout_ratio: float = 7 / 6
    winning_numbers: list[int] = [8]
    losing_numbers: list[int] = [7]


class Place9(Place):
    payout_ratio: float = 7 / 5
    winning_numbers: list[int] = [9]
    losing_numbers: list[int] = [7]


class Place10(Place):
    payout_ratio: float = 9 / 5
    winning_numbers: list[int] = [10]
    losing_numbers: list[int] = [7]


"""
Field bet
"""


class Field(WinningLosingNumbersBet):
    @property
    def payout_ratio(self):
        if self.table.dice.total in self.table.payouts['field_payouts']:
            return self.table.payouts['field_payouts'][self.table.dice.total]
        return 0

    @property
    def winning_numbers(self):
        return list(self.table.payouts['field_payouts'])

    @property
    def losing_numbers(self):
        return list(x for x in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] if x not in self.table.payouts['field_payouts'])


"""
Don't pass and Don't come bets
"""


class DontPass(WinningLosingNumbersBet):
    payout_ratio: float = 1.0

    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.push_numbers: list[int] = [12]
        self.point: int | None = None
        self.new_point: bool = False

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

    @property
    def remove(self) -> bool:
        if self.point is None and self.table.dice.total == 12:
            return True
        if self.new_point is True:
            return False
        return super().remove

    def _update_bet(self) -> tuple[str | None, float, bool]:
        self.new_point = False
        if self.point is None and self.table.dice.total in (4, 5, 6, 8, 9, 10):
            self.point = self.table.dice.total
            self.new_point = True
        return self.status, self.win_amount, self.remove

    def allowed(self, table: 'Table') -> bool:
        if table.point.status == 'Off':
            return True
        return False


class DontCome(DontPass):
    def _update_bet(self) -> tuple[str | None, float, bool]:
        super()._update_bet()
        if self.point is not None and self.subname == "":
            self.subname = "".join(str(e) for e in self.losing_numbers)
        return self.status, self.win_amount, self.remove

    def allowed(self, table: 'Table') -> bool:
        if table.point.status == 'On':
            return True
        return False


"""
Don't pass/Don't come lay odds
"""


class LayOdds(WinningLosingNumbersBet):
    def __init__(self, bet_amount: float, bet_object: DontPass | DontCome):
        super().__init__(bet_amount, None)
        self.bet_object = bet_object
        self.subname: str = "".join(str(e) for e in bet_object.losing_numbers)

    @property
    def winning_numbers(self):
        return self.bet_object.winning_numbers

    @property
    def losing_numbers(self):
        return self.bet_object.losing_numbers

    @property
    def payout_ratio(self):
        if self.losing_numbers in ([4], [10]):
            return 1 / 2
        elif self.losing_numbers in ([5], [9]):
            return 2 / 3
        elif self.losing_numbers in ([6], [8]):
            return 5 / 6
        else:
            raise NotImplementedError


"""
Center-table Bets
"""


class Any7(WinningLosingNumbersBet):
    payout_ratio: int = 4
    winning_numbers: list[int] = [7]
    losing_numbers: list[int] = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]


class Two(WinningLosingNumbersBet):
    payout_ratio: int = 30
    winning_numbers: list[int] = [2]
    losing_numbers: list[int] = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


class Three(WinningLosingNumbersBet):
    payout_ratio: int = 15
    winning_numbers: list[int] = [3]
    losing_numbers: list[int] = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12]


class Yo(WinningLosingNumbersBet):
    payout_ratio: int = 15
    winning_numbers: list[int] = [11]
    losing_numbers: list[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]


class Boxcars(WinningLosingNumbersBet):
    payout_ratio: int = 30
    winning_numbers: list[int] = [12]
    losing_numbers: list[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


class AnyCraps(WinningLosingNumbersBet):
    payout_ratio: int = 7
    winning_numbers: list[int] = [2, 3, 12]
    losing_numbers: list[int] = [4, 5, 6, 7, 8, 9, 10, 11]


class CAndE(WinningLosingNumbersBet):
    winning_numbers: list[int] = [2, 3, 11, 12]
    losing_numbers: list[int] = [4, 5, 6, 7, 8, 9, 10]

    @property
    def payout_ratio(self):
        if self.table.dice.total in [2, 3, 12]:
            return 3
        elif self.table.dice.total in [11]:
            return 7
        else:
            raise NotImplementedError


class HardWay(Bet, ABC):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)

    @property
    @abstractmethod
    def number(self):
        pass

    @property
    def winning_result(self):
        return [self.number / 2, self.number / 2]

    @property
    def status(self):
        if self.table.dice.result == self.winning_result:
            return "win"
        elif self.table.dice.total in [self.number, 7]:
            return "lose"
        return None


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
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.bet_amount: float = bet_amount
        self.points_made: list[int] = []
        self.current_point: int | None = None
        self.new_point_made: bool = False

    @property
    def status(self):
        if self.new_point_made and len(self.points_made) in self.table.payouts['fire_points']:
            return "win"
        elif self.current_point is not None and self.table.dice.total == 7:
            return "lose"
        return None

    @property
    def win_amount(self) -> float:
        if self.status == "win":
            return self.payout_ratio * self.bet_amount
        else:
            return 0.0

    @property
    def remove(self) -> bool:
        if len(self.points_made) == 6 or self.status == "lose":
            return True
        return False

    def _update_bet(self) -> tuple[str | None, float, bool]:
        self.new_point_made = False
        if self.current_point is None and self.table.dice.total in (4, 5, 6, 8, 9, 10):
            self.current_point = self.table.dice.total
        elif self.current_point is not None and self.current_point == self.table.dice.total:
            self.point_made()
        return self.status, self.win_amount, self.remove

    def point_made(self):
        if self.table.dice.total not in self.points_made:
            self.new_point_made = True
            self.points_made = self.points_made + [self.table.dice.total]
        self.current_point = None

    def allowed(self, table: 'Table') -> bool:
        return table.new_shooter

    @property
    def payout_ratio(self):
        if len(self.points_made) in self.table.payouts['fire_points']:
            return self.table.payouts['fire_points'][len(self.points_made)]
        else:
            raise NotImplementedError
