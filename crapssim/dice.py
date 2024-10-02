import typing

from numpy import random


class Dice:
    """
    Simulate the rolling of a dice

    Attributes
    ----------
    n_rolls : int
        Number of rolls for the dice
    result : array, shape = [2]
        Most recent outcome of the roll of two dice
    total : int
        Sum of dice outcome

    """

    def __init__(self, seed: int | None = None) -> None:
        self.rng = random.default_rng(seed)
        self.total: int = 0
        self.result: typing.Iterable[int] | None = None
        self.n_rolls: int = 0

    def roll(self) -> None:
        self.n_rolls += 1
        self.result = self.rng.integers(1, 7, size=2)
        self.total = sum(self.result)

    def fixed_roll(self, outcome: typing.Iterable[int]) -> None:
        self.n_rolls += 1
        self.result = outcome
        self.total = sum(self.result)
