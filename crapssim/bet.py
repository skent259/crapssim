import typing
from abc import ABC

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
    name : string
        Name for the bet
    subname : string
        Subname, usually denotes number for a come/don't come bet
    winning_numbers : list
        Numbers to roll for this bet to win
    losing_numbers : list
        Numbers to roll that cause this bet to lose
    payout_ratio : float
        Ratio that bet pays out on a win
    removable : bool
        Whether the bet can be removed or not
    """

    def __init__(self, bet_amount: typing.SupportsFloat, player, table=None):
        self.bet_amount: float = float(bet_amount)
        self.name: str = str()
        self.subname: str = str()
        self.winning_numbers: list[int] = []
        self.losing_numbers: list[int] = []
        self.payout_ratio: float = float(1)
        self.removable: bool = True
        self.player: Player | None = player
        self.table: Table | None = table

    def _update_bet(self) -> tuple[str | None, float, bool]:
        """
        Returns whether the bets status is win, lose or None and if win the amount won.

        Parameters
        ----------

        Returns
        -------
        tuple[str | None, float]
            The status of the bet and the amount of the winnings.
        """
        status: str | None = None
        win_amount: float = 0.0
        remove = False

        if self.table.dice.total in self.winning_numbers:
            status = "win"
            remove = True
            win_amount = self.payout_ratio * self.bet_amount
        elif self.table.dice.total in self.losing_numbers:
            status = "lose"
            remove = True

        return status, win_amount, remove

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


"""
Passline and Come bets
"""


class PassLine(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "PassLine"
        self.winning_numbers: list[int] = [7, 11]
        self.losing_numbers: list[int] = [2, 3, 12]
        self.payout_ratio: float = 1.0
        self.prepoint: bool = True

    def _update_bet(self) -> tuple[str | None, float, bool]:
        status: str | None = None
        win_amount: float = 0.0
        remove: bool = False

        if self.table.dice.total in self.winning_numbers:
            status = "win"
            remove = True
            win_amount = self.payout_ratio * self.bet_amount
        elif self.table.dice.total in self.losing_numbers:
            status = "lose"
            remove = True
        elif self.prepoint:
            self.winning_numbers = [self.table.dice.total]
            self.losing_numbers = [7]
            self.prepoint = False
            self.removable = False

        return status, win_amount, remove

    def allowed(self, table: 'Table') -> bool:
        if table.point.status == 'Off':
            return True
        return False


class Come(PassLine):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Come"

    def _update_bet(self) -> tuple[str | None, float, bool]:
        status, win_amount, remove = super()._update_bet()
        if not self.prepoint and self.subname == "":
            self.subname = "".join(str(e) for e in self.winning_numbers)
        return status, win_amount, remove

    def allowed(self, table: 'Table') -> bool:
        if table.point.status == 'On':
            return True
        return False


"""
Passline/Come bet odds
"""


class Odds(Bet):
    def __init__(self, bet_amount: typing.SupportsFloat, bet_object: Bet):
        super().__init__(bet_amount, None)
        self.bet_object = bet_object

        if not isinstance(bet_object, PassLine) and not isinstance(bet_object, Come):
            raise TypeError('bet_object must be either a PassLine or Come Bet.')

        self.name: str = "Odds"
        self.subname: str = "".join(str(e) for e in bet_object.winning_numbers)
        self.winning_numbers: list[int] = bet_object.winning_numbers
        self.losing_numbers: list[int] = bet_object.losing_numbers

        if self.winning_numbers == [4] or self.winning_numbers == [10]:
            self.payout_ratio = 2 / 1
        elif self.winning_numbers == [5] or self.winning_numbers == [9]:
            self.payout_ratio = 3 / 2
        elif self.winning_numbers == [6] or self.winning_numbers == [8]:
            self.payout_ratio = 6 / 5

    def allowed(self, table: 'Table') -> bool:
        if isinstance(self.bet_object, PassLine):
            if table.point.status == 'Off':
                return False
            else:
                return True

"""
Place Bets on 4,5,6,8,9,10
"""


class Place(Bet):
    def _update_bet(self) -> tuple[str | None, float, bool]:
        # place bets are inactive when point is "Off"
        if self.table.point == "On":
            return super()._update_bet()
        else:
            return None, 0, False


class Place4(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Place4"
        self.winning_numbers: list[int] = [4]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = 9 / 5


class Place5(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Place5"
        self.winning_numbers: list[int] = [5]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = 7 / 5


class Place6(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Place6"
        self.winning_numbers: list[int] = [6]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = 7 / 6


class Place8(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Place8"
        self.winning_numbers: list[int] = [8]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = 7 / 6


class Place9(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Place9"
        self.winning_numbers: list[int] = [9]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = 7 / 5


class Place10(Place):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Place10"
        self.winning_numbers: list[int] = [10]
        self.losing_numbers: list[int] = [7]
        self.payout_ratio: float = 9 / 5


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
        super().__init__(bet_amount, None)
        self.name: str = "Field"
        self.double_winning_numbers: list[int] = double
        self.triple_winning_numbers: list[int] = triple
        self.winning_numbers: list[int] = [2, 3, 4, 9, 10, 11, 12]
        self.losing_numbers: list[int] = [5, 6, 7, 8]

    def _update_bet(self) -> tuple[str | None, float, bool]:
        status: str | None = None
        win_amount: float = 0
        remove: bool = True

        if self.table.dice.total in self.triple_winning_numbers:
            status = "win"
            win_amount = 3 * self.bet_amount
        elif self.table.dice.total in self.double_winning_numbers:
            status = "win"
            win_amount = 2 * self.bet_amount
        elif self.table.dice.total in self.winning_numbers:
            status = "win"
            win_amount = 1 * self.bet_amount
        elif self.table.dice.total in self.losing_numbers:
            status = "lose"

        return status, win_amount, remove


"""
Don't pass and Don't come bets
"""


class DontPass(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "DontPass"
        self.winning_numbers: list[int] = [2, 3]
        self.losing_numbers: list[int] = [7, 11]
        self.push_numbers: list[int] = [12]
        self.payout_ratio: float = 1.0
        self.prepoint: bool = True

    def _update_bet(self) -> tuple[str | None, float, bool]:
        status: str | None = None
        win_amount: float = 0.0
        remove: bool = False

        if self.table.dice.total in self.winning_numbers:
            status = "win"
            remove = True
            win_amount = self.payout_ratio * self.bet_amount
        elif self.table.dice.total in self.losing_numbers:
            status = "lose"
            remove = True
        elif self.table.dice.total in self.push_numbers:
            remove = True
        elif self.prepoint:
            self.winning_numbers = [7]
            self.losing_numbers = [self.table.dice.total]
            self.push_numbers = []
            self.prepoint = False

        return status, win_amount, remove

    def allowed(self, table: 'Table') -> bool:
        if table.point.status == 'Off':
            return True
        return False


class DontCome(DontPass):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "DontCome"

    def _update_bet(self) -> tuple[str | None, float, bool]:
        status, win_amount, remove = super()._update_bet()
        if not self.prepoint and self.subname == "":
            self.subname = "".join(str(e) for e in self.losing_numbers)
        return status, win_amount, remove

    def allowed(self, table: 'Table') -> bool:
        if table.point.status == 'On':
            return True
        return False


"""
Don't pass/Don't come lay odds
"""


class LayOdds(Bet):
    def __init__(self, bet_amount: float, bet_object: Bet):
        super().__init__(bet_amount, None)
        self.name: str = "LayOdds"
        self.subname: str = "".join(str(e) for e in bet_object.losing_numbers)
        self.winning_numbers: list[int] = bet_object.winning_numbers
        self.losing_numbers: list[int] = bet_object.losing_numbers

        if self.losing_numbers == [4] or self.losing_numbers == [10]:
            self.payout_ratio = 1 / 2
        elif self.losing_numbers == [5] or self.losing_numbers == [9]:
            self.payout_ratio = 2 / 3
        elif self.losing_numbers == [6] or self.losing_numbers == [8]:
            self.payout_ratio = 5 / 6


"""
Center-table Bets
"""


class Any7(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Any7"
        self.winning_numbers: list[int] = [7]
        self.losing_numbers: list[int] = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
        self.payout_ratio: int = 4


class Two(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Two"
        self.winning_numbers: list[int] = [2]
        self.losing_numbers: list[int] = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.payout_ratio: int = 30


class Three(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Three"
        self.winning_numbers: list[int] = [3]
        self.losing_numbers: list[int] = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.payout_ratio: int = 15


class Yo(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Yo"
        self.winning_numbers: list[int] = [11]
        self.losing_numbers: list[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
        self.payout_ratio: int = 15


class Boxcars(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Boxcars"
        self.winning_numbers: list[int] = [12]
        self.losing_numbers: list[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.payout_ratio: int = 30


class AnyCraps(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "AnyCraps"
        self.winning_numbers: list[int] = [2, 3, 12]
        self.losing_numbers: list[int] = [4, 5, 6, 7, 8, 9, 10, 11]
        self.payout_ratio: int = 7


class CAndE(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "CAndE"
        self.winning_numbers: list[int] = [2, 3, 11, 12]
        self.losing_numbers: list[int] = [4, 5, 6, 7, 8, 9, 10]

    def _update_bet(self) -> tuple[str | None, float, bool]:
        status: str | None = None
        win_amount: float = 0
        remove: bool = True

        if self.table.dice.total in self.winning_numbers:
            status = "win"
            if self.table.dice.total in [2, 3, 12]:
                payout_ratio = 3
            elif self.table.dice.total in [11]:
                payout_ratio = 7
            win_amount = payout_ratio * self.bet_amount
        elif self.table.dice.total in self.losing_numbers:
            status = "lose"

        return status, win_amount, remove


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
        super().__init__(bet_amount, None)
        self.number: int | None = None
        self.winning_result: list[int | None] = [None, None]

    def _update_bet(self) -> tuple[str | None, float, bool]:
        status: str | None = None
        win_amount: float = 0.0
        remove: bool = False

        if self.table.dice.result == self.winning_result:
            status = "win"
            remove = True
            win_amount = self.payout_ratio * self.bet_amount
        elif self.table.dice.total in [self.number, 7]:
            status = "lose"
            remove = True

        return status, win_amount, remove


class Hard4(Hardway):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Hard4"
        self.winning_result: list[int | None] = [2, 2]
        self.number: int = 4
        self.payout_ratio: int = 7


class Hard6(Hardway):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Hard6"
        self.winning_result: list[int | None] = [3, 3]
        self.number: int = 6
        self.payout_ratio: int = 9


class Hard8(Hardway):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Hard8"
        self.winning_result: list[int | None] = [4, 4]
        self.number: int = 8
        self.payout_ratio: int = 9


class Hard10(Hardway):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
        self.name: str = "Hard10"
        self.winning_result: list[int | None] = [5, 5]
        self.number: int = 10
        self.payout_ratio: int = 7


class Fire(Bet):
    def __init__(self, bet_amount: float):
        super().__init__(bet_amount, None)
        self.name: str = "Fire"
        self.bet_amount: float = bet_amount
        self.points_made: list[int] = []
        self.current_point: int | None = None

    def _update_bet(self) -> tuple[str | None, float, bool]:
        status, win_amount, remove = None, 0.0, False
        if self.current_point is None and self.table.dice.total in (4, 5, 6, 8, 9, 10):
            self.current_point = self.table.dice.total
        elif self.current_point is not None and self.current_point == self.table.dice.total:
            if self.current_point not in self.points_made:
                self.points_made = list(set(self.points_made + [self.table.dice.total]))
                if len(self.points_made) == 4:
                    status, win_amount, remove = 'win', 24 * self.bet_amount, False
                elif len(self.points_made) == 5:
                    status, win_amount, remove = 'win', 249 * self.bet_amount, False
                elif len(self.points_made) == 6:
                    status, win_amount, remove = 'win', 999 * self.bet_amount, True
            self.current_point = None
        elif self.current_point is not None and self.table.dice.total == 7:
            status, win_amount, remove = 'lose', 0.0, True
        return status, win_amount, remove

    def allowed(self, table: 'Table') -> bool:
        return table.new_shooter
