import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from crapssim import Table, Player


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
