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
        self.player: Player | None = None
        self.table: Table | None = None

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

    def allowed(self, player) -> bool:
        """
        Checks whether the bet is allowed to be placed on the given table.

        Parameters
        ----------
        player

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

    def _update_bet(self) -> None:
        """
        Returns whether the bets status is win, lose or None and if win the amount won.

        Returns
        -------
        tuple[str | None, float]
            The status of the bet and the amount of the winnings.
        """
        pass

    def already_placed(self, player: "Player") -> bool:
        return player.has_bet(type(self))


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


class AllowsOdds(WinningLosingNumbersBet):
    @abstractmethod
    def place_odds(self, bet_amount: typing.SupportsFloat):
        pass


class PassLine(AllowsOdds):
    payout_ratio: float = 1.0

    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
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

    def _update_bet(self) -> None:
        self.new_point = False

        if self.point is None and self.status not in ("win", "lose"):
            self.point = self.table.dice.total
            self.new_point = True

    @property
    def removable(self):
        if self.point is not None:
            return False
        return True

    def allowed(self, player) -> bool:
        if player.table.point.status == 'Off':
            return True
        return False

    def place_odds(self, bet_amount: typing.SupportsFloat):
        number = self.winning_numbers[0]
        odds_type = {4: Odds4, 5: Odds5, 6: Odds6, 8: Odds8, 9: Odds9, 10: Odds10}[number]
        bet = odds_type(bet_amount)
        self.player.bet(bet)


class Come(PassLine):
    def allowed(self, player) -> bool:
        if player.table.point.status == 'On':
            return True
        return False

    def already_placed(self, player: "Player") -> bool:
        return player.has_bet(type(self), point=self.point)


"""
Passline/Come bet odds
"""


class BaseOdds(WinningLosingNumbersBet, ABC):
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
    def winning_number(self) -> int:
        pass

    @property
    def winning_numbers(self) -> list[int]:
        return [self.winning_number]

    @property
    @abstractmethod
    def key_number(self):
        pass

    @property
    @abstractmethod
    def losing_number(self):
        pass

    @property
    def losing_numbers(self):
        return [self.losing_number]

    def get_base_bets(self, player: "Player") -> list[WinningLosingNumbersBet]:
        base_bets = [x for x in player.bets_on_table if
                     isinstance(x, self.base_bet_types)
                     and x.winning_numbers == [self.winning_numbers]]
        return base_bets

    def get_max_odds(self, table: "Table") -> int:
        return table.settings[self.table_odds_setting][self.key_number]

    def get_max_bet(self, player: "Player") -> typing.SupportsFloat:
        base_bet_amount = sum(x.bet_amount for x in self.get_base_bets(player))
        max_odds = self.get_max_odds(player.table)
        return base_bet_amount * max_odds

    def allowed(self, player) -> bool:
        return self.get_max_bet(player) <= self.bet_amount


class Odds(BaseOdds, ABC):
    base_bet_types: tuple[typing.Type[WinningLosingNumbersBet]] = (PassLine, Come)
    table_odds_setting: str = 'max_odds'
    losing_number: list[int] = 7

    @property
    def key_number(self):
        return self.winning_number


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


class Place(WinningLosingNumbersBet, ABC):
    def _update_bet(self) -> None:
        # place bets are inactive when point is "Off"
        if self.table.point == "On":
            super()._update_bet()


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
        if self.table.dice.total in self.table.settings['field_payouts']:
            return self.table.settings['field_payouts'][self.table.dice.total]
        return 0

    @property
    def winning_numbers(self):
        return list(self.table.settings['field_payouts'])

    @property
    def losing_numbers(self):
        return list(x for x in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] if x not in self.table.settings['field_payouts'])


"""
Don't pass and Don't come bets
"""


class DontPass(AllowsOdds):
    payout_ratio: float = 1.0

    def __init__(self, bet_amount: float):
        super().__init__(bet_amount)
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

    def _update_bet(self) -> None:
        self.new_point = False
        if self.point is None and self.table.dice.total in (4, 5, 6, 8, 9, 10):
            self.point = self.table.dice.total
            self.new_point = True

    def allowed(self, player) -> bool:
        if player.table.point.status == 'Off':
            return True
        return False

    def place_odds(self, bet_amount: typing.SupportsFloat):
        number = self.losing_numbers[0]
        odds_type = {4: LayOdds4,
                     5: LayOdds5,
                     6: LayOdds6,
                     8: LayOdds8,
                     9: LayOdds9,
                     10: Odds10}[number]
        bet = odds_type(bet_amount)
        self.player.bet(bet)


class DontCome(DontPass):
    def allowed(self, player) -> bool:
        if player.table.point.status == 'On':
            return True
        return False


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
        super().__init__(bet_amount)

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
        super().__init__(bet_amount)
        self.bet_amount: float = bet_amount
        self.points_made: list[int] = []
        self.current_point: int | None = None
        self.new_point_made: bool = False

    @property
    def status(self):
        if self.new_point_made and len(self.points_made) in self.table.settings['fire_points']:
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

    def _update_bet(self) -> None:
        self.new_point_made = False
        if self.current_point is None and self.table.dice.total in (4, 5, 6, 8, 9, 10):
            self.current_point = self.table.dice.total
        elif self.current_point is not None and self.current_point == self.table.dice.total:
            self.point_made()

    def point_made(self):
        if self.table.dice.total not in self.points_made:
            self.new_point_made = True
            self.points_made = self.points_made + [self.table.dice.total]
        self.current_point = None

    def allowed(self, player) -> bool:
        return player.table.new_shooter

    @property
    def payout_ratio(self):
        if len(self.points_made) in self.table.settings['fire_points']:
            return self.table.settings['fire_points'][len(self.points_made)]
        else:
            raise NotImplementedError
