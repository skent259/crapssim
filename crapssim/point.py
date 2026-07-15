"""Point state helpers for craps tables."""

from crapssim import Dice


class Point:
    """
    The point on a craps or crapless table.

    Attributes
    ----------
    number : int
        The point number (in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]) is status == 'On'
    """

    def __init__(self, number: int | None = None) -> None:
        self.number: int | None = number

    @property
    def status(self) -> str:
        """Return whether the point is on or off."""
        if self.number is None:
            return "Off"
        else:
            return "On"

    def __hash__(self) -> int:
        return hash(self.number)

    def __repr__(self):
        return f"Point(number={self.number})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.status.lower() == other.lower() or str(self.number) == other
        elif isinstance(other, int) and other in (2, 3, 4, 5, 6, 8, 9, 10, 11, 12):
            # Point equality supports all crapless-capable point numbers so callers can compare
            # against a point value regardless of active ruleset. Legality of those numbers is
            # handled by the table rules, not by Point itself.
            return other == self.number
        elif isinstance(other, Point):
            return other.status == self.status and other.number == self.number
        else:
            raise NotImplementedError

    def __gt__(self, other: object) -> bool:
        if self.number is None:
            raise NotImplementedError
        if isinstance(other, str):
            return self.number > int(other)
        elif isinstance(other, int):
            return self.number > other
        elif isinstance(other, Point):
            if other.number is None:
                raise NotImplementedError
            return self.number > other.number
        else:
            raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        if self.number is None:
            raise NotImplementedError
        if isinstance(other, str):
            return self.number < int(other)
        elif isinstance(other, int):
            return self.number < other
        elif isinstance(other, Point):
            if other.number is None:
                raise NotImplementedError
            return self.number < other.number
        else:
            raise NotImplementedError

    def __ge__(self, other: object) -> bool:
        if self.number is None:
            raise NotImplementedError
        return self.__eq__(other) or self.__gt__(other)

    def __le__(self, other: object) -> bool:
        if self.number is None:
            raise NotImplementedError
        return self.__eq__(other) or self.__lt__(other)

    def update(self, dice_object: Dice, point_numbers: list[int] | None = None) -> None:
        """
        Given a Dice object update the points status and number.

        Parameters
        ----------
        dice_object : Dice
            The Dice you want to update the point with
        point_numbers : list[int], optional
            The point numbers to use for the update.
            If None, defaults to [4, 5, 6, 8, 9, 10].
        """
        numbers = point_numbers or [4, 5, 6, 8, 9, 10]
        if self.status == "Off" and dice_object.total in numbers:
            self.number = dice_object.total
        elif self.status == "On" and dice_object.total in [7, self.number]:
            self.number = None
