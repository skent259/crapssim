import typing
from abc import ABC, abstractmethod, ABCMeta

if typing.TYPE_CHECKING:
    from crapssim.table import Table
    from crapssim import Player, Table


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
    def get_payout_ratio(self, table: "Table") -> float:
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def is_removable(self, player: "Player") -> bool:
        return True

    def allowed(self, player: "Player") -> bool:
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

    @abstractmethod
    def get_status(self, table: "Table") -> str | None:
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
        return player.has_bets_by_type(type(self))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return isinstance(other, type(self)) and other.bet_amount == self.bet_amount
        else:
            raise NotImplementedError

    @abstractmethod
    def __hash__(self) -> int:
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount})'


class WinningLosingNumbersBet(Bet, ABC):
    @abstractmethod
    def get_winning_numbers(self, table: "Table") -> list[int]:
        pass

    @abstractmethod
    def get_losing_numbers(self, table: "Table") -> list[int]:
        pass

    def get_status(self, table: "Table") -> str | None:
        if table.dice.total in self.get_winning_numbers(table):
            return "win"
        elif table.dice.total in self.get_losing_numbers(table):
            return "lose"
        return None


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

    def __hash__(self) -> int:
        return hash((PassLine, self.bet_amount))


class Come(WinningLosingNumbersBet):
    def __init__(self, bet_amount: typing.SupportsFloat, point: int | None = None):
        super().__init__(bet_amount)
        self.point = point
        self._status: str | None = None

    def get_payout_ratio(self, table: "Table") -> float:
        return 1.0

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if self.point is None:
            return [7, 11]
        return [self.point]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if self.point is None:
            return [2, 3, 12]
        return [7]

    def get_status(self, table: "Table") -> str | None:
        return self._status

    def update(self, table: "Table") -> None:
        if self.point is None and table.dice.total in (4, 5, 6, 8, 9, 10):
            self.point = table.dice.total
        else:
            self._status = super().get_status(table)

    def is_removable(self, player: "Player") -> bool:
        if self.point is not None:
            return False
        return True

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'On':
            return True
        return False

    def already_placed(self, player: "Player") -> bool:
        return player.has_bets_by_type(type(self), point=self.point)

    def get_odds_bet(self, bet_amount: typing.SupportsFloat, table: "Table") -> "Odds":
        if self.point is not None:
            return Odds(self.point, bet_amount)
        else:
            raise ValueError

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return isinstance(other, type(self)) and \
                   other.bet_amount == self.bet_amount and \
                   other.point == self.point
        else:
            raise NotImplementedError

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount}, point={self.point})'

    def __hash__(self) -> int:
        return hash((Come, self.bet_amount, self.point))


"""
Passline/Come bet odds
"""


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

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return isinstance(other, Odds) and self.bet_amount == other.bet_amount \
                   and self.number == other.number
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash((Odds, self.bet_amount, self.number))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(number={self.number}, bet_amount={self.bet_amount})'


class Odds4(Odds):
    payout_ratio: float = 2 / 1

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(4, bet_amount)


class Odds5(Odds):
    payout_ratio: float = 3 / 2

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(5, bet_amount)


class Odds6(Odds):
    payout_ratio: float = 6 / 5

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(6, bet_amount)


class Odds8(Odds):
    payout_ratio: float = 6 / 5

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(8, bet_amount)


class Odds9(Odds):
    payout_ratio: float = 3 / 2

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(9, bet_amount)


class Odds10(Odds):
    payout_ratio: float = 2 / 1

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(10, bet_amount)


"""
Place Bets on 4,5,6,8,9,10
"""


class Place(WinningLosingNumbersBet):
    payout_ratios = {4: 9 / 5, 5: 7 / 5, 6: 7 / 6, 8: 7 / 6, 9: 7 / 5, 10: 9 / 5}
    losing_numbers: list[int] = [7]

    def __init__(self, number: int, bet_amount: typing.SupportsFloat):
        super().__init__(bet_amount)
        self.payout_ratio = self.payout_ratios[number]
        self.winning_numbers = [number]

    def update(self, table: "Table") -> None:
        # place bets are inactive when point is "Off"
        if table.point == "On":
            super().update(table)

    def get_payout_ratio(self, table: "Table") -> float:
        return self.payout_ratio

    def get_winning_numbers(self, table: "Table") -> list[int]:
        return self.winning_numbers

    def get_losing_numbers(self, table: "Table") -> list[int]:
        return self.losing_numbers

    def already_placed(self, player: "Player") -> bool:
        return any(isinstance(x, Place) and x.winning_numbers == self.winning_numbers
                   for x in player.bets_on_table)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return isinstance(other, Place) and \
                   self.winning_numbers == other.winning_numbers and \
                   self.bet_amount == other.bet_amount
        else:
            raise NotImplementedError

    def __hash__(self) -> int:
        return hash((Place, self.bet_amount))

    def __repr__(self) -> str:
        return f'Place(number={self.winning_numbers[0]}, bet_amount={self.bet_amount})'


class Place4(Place):
    payout_ratio: float = Place.payout_ratios[4]
    winning_numbers: list[int] = [4]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(4, bet_amount)


class Place5(Place):
    payout_ratio: float = Place.payout_ratios[5]
    winning_numbers: list[int] = [5]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(5, bet_amount)


class Place6(Place):
    payout_ratio: float = Place.payout_ratios[6]
    winning_numbers: list[int] = [6]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(6, bet_amount)


class Place8(Place):
    payout_ratio: float = Place.payout_ratios[8]
    winning_numbers: list[int] = [8]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(8, bet_amount)


class Place9(Place):
    payout_ratio: float = Place.payout_ratios[9]
    winning_numbers: list[int] = [9]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(9, bet_amount)


class Place10(Place):
    payout_ratio: float = Place.payout_ratios[10]
    winning_numbers: list[int] = [10]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(10, bet_amount)


"""
Field bet
"""


class OneRollBet(WinningLosingNumbersBet, ABC):
    """WinningLosingNumbersBet where if the number isn't in the winning_numbers,
    it is in the losing_numbers."""

    def __init__(self, winning_numbers: list[int], bet_amount: typing.SupportsFloat):
        self.winning_numbers = winning_numbers
        super().__init__(bet_amount)

    def get_winning_numbers(self, table: "Table") -> list[int]:
        return self.winning_numbers

    def get_losing_numbers(self, table: "Table") -> list[int]:
        return [x for x in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                if x not in self.get_winning_numbers(table)]

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass


class Field(OneRollBet):
    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__([2, 3, 4, 9, 10, 11, 12], bet_amount)

    def get_payout_ratio(self, table: "Table") -> float:
        if table.dice.total in table.settings['field_payouts']:
            return float(table.settings['field_payouts'][table.dice.total])
        return 0.0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bet):
            raise NotImplementedError
        return isinstance(other, Field) and self.bet_amount == other.bet_amount

    def __hash__(self) -> int:
        return hash((type(self), self.bet_amount))


"""
Don't pass and Don't come bets
"""


class DontPass(WinningLosingNumbersBet):
    def get_payout_ratio(self, table: "Table") -> float:
        return 1

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

    def __hash__(self) -> int:
        return hash((DontPass, self.bet_amount))


class DontCome(WinningLosingNumbersBet):
    def __init__(self, bet_amount: typing.SupportsFloat, point: int | None = None) -> None:
        super().__init__(bet_amount)
        self.point = point
        self._status: str | None = None

    def get_payout_ratio(self, table: "Table") -> float:
        return 1.0

    def get_winning_numbers(self, table: "Table") -> list[int]:
        if self.point is None:
            return [2, 3]
        return [7]

    def get_losing_numbers(self, table: "Table") -> list[int]:
        if self.point is None:
            return [7, 11]
        return [self.point]

    def update(self, table: "Table") -> None:
        if self.point is None and table.dice.total in (4, 5, 6, 8, 9, 10):
            self.point = table.dice.total
        else:
            self._status = super().get_status(table)

    def allowed(self, player: "Player") -> bool:
        if player.table.point.status == 'On':
            return True
        return False

    def get_status(self, table: "Table") -> str | None:
        return self._status

    def get_odds_bet(self, bet_amount: typing.SupportsFloat, table: "Table") -> "LayOdds":
        if self.point is not None:
            return LayOdds(self.point, bet_amount)
        else:
            raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return isinstance(other, type(self)) and \
                   self.bet_amount == other.bet_amount and \
                   self.point == other.point
        else:
            raise NotImplementedError

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bet_amount={self.bet_amount}, point={self.point})'

    def already_placed(self, player: "Player") -> bool:
        return player.has_bets_by_type(type(self), point=self.point)

    def __hash__(self) -> int:
        return hash((type(self), self.bet_amount))


"""
Don't pass/Don't come lay odds
"""


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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet):
            return isinstance(other, LayOdds) and self.bet_amount == other.bet_amount \
                   and self.number == other.number
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash((LayOdds, self.bet_amount, self.number))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(number={self.number}, bet_amount={self.bet_amount})'


class LayOdds4(LayOdds):
    losing_numbers: list[int] = [4]
    payout_ratio: float = 1 / 2

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(4, bet_amount)


class LayOdds5(LayOdds):
    losing_numbers: list[int] = [5]
    payout_ratio: float = 2 / 3

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(5, bet_amount)


class LayOdds6(LayOdds):
    losing_numbers: list[int] = [6]
    payout_ratio: float = 5 / 6

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(6, bet_amount)


class LayOdds8(LayOdds):
    losing_numbers: list[int] = [8]
    payout_ratio: float = 5 / 6

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(8, bet_amount)


class LayOdds9(LayOdds):
    losing_numbers: list[int] = [9]
    payout_ratio: float = 2 / 3

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(9, bet_amount)


class LayOdds10(LayOdds):
    losing_numbers: list[int] = [10]
    payout_ratio: float = 1 / 2

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(10, bet_amount)


"""
Center-table Bets
"""


class StaticRatioOneRollBet(OneRollBet):
    def __init__(self, winning_numbers: list[int],
                 payout_ratio: typing.SupportsFloat,
                 bet_amount: typing.SupportsFloat):
        super().__init__(winning_numbers, bet_amount)
        self.payout_ratio = payout_ratio

    def get_payout_ratio(self, table: "Table") -> float:
        return float(self.payout_ratio)

    def _key(self) -> tuple[list[int], typing.SupportsFloat, float]:
        return self.winning_numbers, self.payout_ratio, self.bet_amount

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bet):
            raise NotImplementedError
        return isinstance(other, StaticRatioOneRollBet) and self._key() == other._key()

    def __hash__(self) -> int:
        return hash((StaticRatioOneRollBet, self._key()))


class Any7(StaticRatioOneRollBet):
    payout_ratio: int = 4
    winning_numbers: list[int] = [7]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class Two(StaticRatioOneRollBet):
    payout_ratio: int = 30
    winning_numbers: list[int] = [2]

    def __init__(self, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class Three(StaticRatioOneRollBet):
    payout_ratio: int = 15
    winning_numbers: list[int] = [3]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class Yo(StaticRatioOneRollBet):
    payout_ratio: int = 15
    winning_numbers: list[int] = [11]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class Boxcars(StaticRatioOneRollBet):
    payout_ratio: int = 30
    winning_numbers: list[int] = [12]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class AnyCraps(StaticRatioOneRollBet):
    payout_ratio: int = 7
    winning_numbers: list[int] = [2, 3, 12]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, self.payout_ratio, bet_amount)


class CAndE(OneRollBet):
    winning_numbers: list[int] = [2, 3, 11, 12]

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.winning_numbers, bet_amount)

    def get_payout_ratio(self, table: "Table") -> float:
        if table.dice.total in [2, 3, 12]:
            return 3.0
        elif table.dice.total in [11]:
            return 7.0
        else:
            raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bet):
            raise NotImplementedError
        return isinstance(other, CAndE) and self.bet_amount == other.bet_amount

    def __hash__(self) -> int:
        return hash((CAndE, self.bet_amount))


class HardWay(Bet):
    payout_ratios = {4: 7, 6: 9, 8: 9, 10: 7}

    def __init__(self, number: int, bet_amount: typing.SupportsFloat) -> None:
        super().__init__(bet_amount)
        self.number = number
        self.payout_ratio = self.payout_ratios[number]

    @property
    def winning_result(self) -> list[int]:
        return [int(self.number / 2), int(self.number / 2)]

    def get_payout_ratio(self, table: "Table") -> float:
        return float(self.payout_ratio)

    def get_status(self, table: "Table") -> str | None:
        if table.dice.result == self.winning_result:
            return "win"
        elif table.dice.total in [self.number, 7]:
            return "lose"
        return None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bet) and not isinstance(other, type(self)):
            return False
        elif isinstance(other, type(self)):
            return self.number == other.number and self.bet_amount == other.bet_amount
        else:
            raise NotImplementedError

    def __hash__(self) -> int:
        return hash((type(self), self.number, self.bet_amount))


class Hard4(HardWay):
    payout_ratio: int = HardWay.payout_ratios[4]
    number: int = 4

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.number, bet_amount)


class Hard6(HardWay):
    payout_ratio: int = HardWay.payout_ratios[6]
    number: int = 6

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.number, bet_amount)


class Hard8(HardWay):
    payout_ratio: int = HardWay.payout_ratios[8]
    number: int = 8

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.number, bet_amount)


class Hard10(HardWay):
    payout_ratio: int = HardWay.payout_ratios[10]
    number: int = 10

    def __init__(self, bet_amount: typing.SupportsFloat):
        super().__init__(self.number, bet_amount)


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
