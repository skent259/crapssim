from crapssim import Dice


class Point:
    """
    The point on a craps table.

    Attributes
    ----------
    number : int
        The point number (in [4, 5, 6, 8, 9, 10]) is status == 'On'
    """

    def __init__(self, number: int | None = None) -> None:
        self.number: int | None = number

    @property
    def status(self) -> str:
        if self.number is None:
            return 'Off'
        else:
            return 'On'

    def __hash__(self) -> int:
        return hash(self.number)

    def __repr__(self):
        return f'Point(number={self.number})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.status.lower() == other.lower() or str(self.number) == other
        elif isinstance(other, int) and other in (4, 5, 6, 8, 9, 10):
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

    def update(self, dice_object: Dice) -> None:
        """
        Given a Dice object update the points status and number.

        Parameters
        ----------
        dice_object : Dice
            The Dice you want to update the point with
        """
        if self.status == "Off" and dice_object.total in [4, 5, 6, 8, 9, 10]:
            self.number = dice_object.total
        elif self.status == "On" and dice_object.total in [7, self.number]:
            self.number = None