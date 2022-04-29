import typing
from abc import ABC

from crapssim.dice import Dice

if typing.TYPE_CHECKING:
    from crapssim.table import Table


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
    name : string
        Name for the bet
    subname : string
        Subname, usually denotes number for a come/don't come bet
    winning_numbers : list
        Numbers to roll for this bet to win
    losing_numbers : list
        Numbers to roll that cause this bet to lose
    payoutratio : float
        Ratio that bet pays out on a win
    removable : bool
        Whether the bet can be removed or not
    can_be_placed_point_on : bool
        Whether the bet can be placed when the point is on
    can_be_placed_point_off : bool
        Whether the bet can be placed when the point is off
    """

    def __init__(self, bet_amount: typing.SupportsFloat):
        self.bet_amount: float = float(bet_amount)
        self.name: str = str()
        self.subname: str = str()
        self.winning_numbers: list[int] = []
        self.losing_numbers: list[int] = []
        self.payoutratio: float = float(1)
        self.removable: bool = True
        self.can_be_placed_point_on = True
        self.can_be_placed_point_off = True

    def _update_bet(self, table_object: "Table", dice_object: Dice) -> tuple[str | None, float]:
        """
        Returns whether the bets status is win, lose or None and if win the amount won.

        Parameters
        ----------
        table_object : Table
            The table to check the bet was made on.
        dice_object : Dice
            The dice to check the bet against.

        Returns
        -------
        tuple[str | None, float]
            The status of the bet and the amount of the winnings.
        """
        status: str | None = None
        win_amount: float = 0.0

        if dice_object.total in self.winning_numbers:
            status = "win"
            win_amount = self.payoutratio * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            status = "lose"

        return status, win_amount


"""
Passline and Come bets
"""


class PassLine(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "PassLine"
        self.winning_numbers: list[int] = [7, 11]
        self.losing_numbers: list[int] = [2, 3, 12]
        self.payoutratio: float = 1.0
        self.prepoint: bool = True
        self.can_be_placed_point_on = False

    def _update_bet(self, table_object: "Table", dice_object: Dice) -> tuple[str | None, float]:
        status: str | None = None
        win_amount: float = 0.0

        if dice_object.total in self.winning_numbers:
            status = "win"
            win_amount = self.payoutratio * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            status = "lose"
        elif self.prepoint:
            self.winning_numbers = [dice_object.total]
            self.losing_numbers = [7]
            self.prepoint = False
            self.removable = False

        return status, win_amount


class Come(PassLine):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Come"
        self.can_be_placed_point_off = False
        self.can_be_placed_point_on = True

    def _update_bet(self, table_object: "Table", dice_object: Dice) -> tuple[str | None, float]:
        status, win_amount = super()._update_bet(table_object, dice_object)
        if not self.prepoint and self.subname == "":
            self.subname = "".join(str(e) for e in self.winning_numbers)
        return status, win_amount


"""
Passline/Come bet odds
"""


class Odds(Bet):
    def __init__(self, bet_amount: typing.SupportsFloat, bet_object: Bet):
        super().__init__(bet_amount)

        if not isinstance(bet_object, PassLine) and not isinstance(bet_object, Come):
            raise TypeError('bet_object must be either a PassLine or Come Bet.')
        if isinstance(bet_object, PassLine):
            self.can_be_placed_point_off = False

        self.name: str = "Odds"
        self.subname: str = "".join(str(e) for e in bet_object.winning_numbers)
        self.winning_numbers: list[int] = bet_object.winning_numbers
        self.losing_numbers: list[int] = bet_object.losing_numbers

        if self.winning_numbers == [4] or self.winning_numbers == [10]:
            self.payoutratio = 2 / 1
        elif self.winning_numbers == [5] or self.winning_numbers == [9]:
            self.payoutratio = 3 / 2
        elif self.winning_numbers == [6] or self.winning_numbers == [8]:
            self.payoutratio = 6 / 5


"""
Place Bets on 4,5,6,8,9,10
"""


class Place(Bet):
    def _update_bet(self, table_object: "Table", dice_object: Dice) -> tuple[str | None, float]:
        # place bets are inactive when point is "Off"
        if table_object.point == "On":
            return super()._update_bet(table_object, dice_object)
        else:
            return None, 0


class Place4(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Place4"
        self.winning_numbers: list[int] = [4]
        self.losing_numbers: list[int] = [7]
        self.payoutratio: float = 9 / 5


class Place5(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Place5"
        self.winning_numbers: list[int] = [5]
        self.losing_numbers: list[int] = [7]
        self.payoutratio: float = 7 / 5


class Place6(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Place6"
        self.winning_numbers: list[int] = [6]
        self.losing_numbers: list[int] = [7]
        self.payoutratio: float = 7 / 6


class Place8(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Place8"
        self.winning_numbers: list[int] = [8]
        self.losing_numbers: list[int] = [7]
        self.payoutratio: float = 7 / 6


class Place9(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Place9"
        self.winning_numbers: list[int] = [9]
        self.losing_numbers: list[int] = [7]
        self.payoutratio: float = 7 / 5


class Place10(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Place10"
        self.winning_numbers: list[int] = [10]
        self.losing_numbers: list[int] = [7]
        self.payoutratio: float = 9 / 5


"""
Field bet
"""


class Field(Bet):
    """
    Parameters
    ----------
    double : list
        Set of numbers that pay double on the field bet (default = [2,12])
    triple : list
        Set of numbers that pay triple on the field bet (default = [])
    """

    def __init__(self, bet_amount: float, double: list[int] = [2, 12], triple: list[int] = []):
        super().__init__(bet_amount)
        self.name: str = "Field"
        self.double_winning_numbers: list[int] = double
        self.triple_winning_numbers: list[int] = triple
        self.winning_numbers: list[int] = [2, 3, 4, 9, 10, 11, 12]
        self.losing_numbers: list[int] = [5, 6, 7, 8]

    def _update_bet(self, table_object: "Table", dice_object: Dice) -> tuple[str | None, float]:
        status: str | None = None
        win_amount: float = 0

        if dice_object.total in self.triple_winning_numbers:
            status = "win"
            win_amount = 3 * self.bet_amount
        elif dice_object.total in self.double_winning_numbers:
            status = "win"
            win_amount = 2 * self.bet_amount
        elif dice_object.total in self.winning_numbers:
            status = "win"
            win_amount = 1 * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            status = "lose"

        return status, win_amount


"""
Don't pass and Don't come bets
"""


class DontPass(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "DontPass"
        self.winning_numbers: list[int] = [2, 3]
        self.losing_numbers: list[int] = [7, 11]
        self.push_numbers: list[int] = [12]
        self.payoutratio: float = 1.0
        self.prepoint: bool = True
        self.can_be_placed_point_on = False

    def _update_bet(self, table_object: "Table", dice_object: Dice) -> tuple[str | None, float]:
        status: str | None = None
        win_amount: float = 0.0

        if dice_object.total in self.winning_numbers:
            status = "win"
            win_amount = self.payoutratio * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            status = "lose"
        elif dice_object.total in self.push_numbers:
            status = "push"
        elif self.prepoint:
            self.winning_numbers = [7]
            self.losing_numbers = [dice_object.total]
            self.push_numbers = []
            self.prepoint = False

        return status, win_amount


class DontCome(DontPass):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "DontCome"
        self.can_be_placed_point_off = False
        self.can_be_placed_point_on = True

    def _update_bet(self, table_object: "Table", dice_object: Dice) -> tuple[str | None, float]:
        status, win_amount = super()._update_bet(table_object, dice_object)
        if not self.prepoint and self.subname == "":
            self.subname = "".join(str(e) for e in self.losing_numbers)
        return status, win_amount


"""
Don't pass/Don't come lay odds
"""


class LayOdds(Bet):
    def __init__(self, bet_amount: float, bet_object: Bet):
        super().__init__(bet_amount)
        self.name: str = "LayOdds"
        self.subname: str = "".join(str(e) for e in bet_object.losing_numbers)
        self.winning_numbers: list[int] = bet_object.winning_numbers
        self.losing_numbers: list[int] = bet_object.losing_numbers

        if self.losing_numbers == [4] or self.losing_numbers == [10]:
            self.payoutratio = 1 / 2
        elif self.losing_numbers == [5] or self.losing_numbers == [9]:
            self.payoutratio = 2 / 3
        elif self.losing_numbers == [6] or self.losing_numbers == [8]:
            self.payoutratio = 5 / 6


"""
Center-table Bets
"""


class Any7(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Any7"
        self.winning_numbers: list[int] = [7]
        self.losing_numbers: list[int] = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
        self.payoutratio: int = 4


class Two(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Two"
        self.winning_numbers: list[int] = [2]
        self.losing_numbers: list[int] = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.payoutratio: int = 30


class Three(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Three"
        self.winning_numbers: list[int] = [3]
        self.losing_numbers: list[int] = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.payoutratio: int = 15


class Yo(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Yo"
        self.winning_numbers: list[int] = [11]
        self.losing_numbers: list[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
        self.payoutratio: int = 15


class Boxcars(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Boxcars"
        self.winning_numbers: list[int] = [12]
        self.losing_numbers: list[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.payoutratio: int = 30


class AnyCraps(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "AnyCraps"
        self.winning_numbers: list[int] = [2, 3, 12]
        self.losing_numbers: list[int] = [4, 5, 6, 7, 8, 9, 10, 11]
        self.payoutratio: int = 7


class CAndE(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "CAndE"
        self.winning_numbers: list[int] = [2, 3, 11, 12]
        self.losing_numbers: list[int] = [4, 5, 6, 7, 8, 9, 10]

    def _update_bet(self, table_object: "Table", dice_object: Dice) -> tuple[str | None, float]:
        status: str | None = None
        win_amount: float = 0

        if dice_object.total in self.winning_numbers:
            status = "win"
            if dice_object.total in [2, 3, 12]:
                payoutratio = 3
            elif dice_object.total in [11]:
                payoutratio = 7
            win_amount = payoutratio * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            status = "lose"

        return status, win_amount


class Hardway(Bet):
    """
    Attributes
    ----------
    number : int
        The relevant number that the bet wins and loses on (for hardways)
    winning_result : list(int)
        The combination of dice the bet wins on
    """

    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.number: int | None = None
        self.winning_result: list[int | None] = [None, None]

    def _update_bet(self, table_object: "Table", dice_object: Dice) -> tuple[str | None, float]:
        status: str | None = None
        win_amount: float = 0.0

        if dice_object.result == self.winning_result:
            status = "win"
            win_amount = self.payoutratio * self.bet_amount
        elif dice_object.total in [self.number, 7]:
            status = "lose"

        return status, win_amount


class Hard4(Hardway):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Hard4"
        self.winning_result: list[int | None] = [2, 2]
        self.number: int = 4
        self.payoutratio: int = 7


class Hard6(Hardway):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str ="Hard6"
        self.winning_result: list[int | None] = [3, 3]
        self.number: int = 6
        self.payoutratio: int = 9


class Hard8(Hardway):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str ="Hard8"
        self.winning_result: list[int | None] = [4, 4]
        self.number: int = 8
        self.payoutratio: int = 9


class Hard10(Hardway):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str ="Hard10"
        self.winning_result: list[int | None] = [5, 5]
        self.number: int = 10
        self.payoutratio: int = 7
