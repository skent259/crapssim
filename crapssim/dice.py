import typing

import numpy as np


class Dice:
    """
    Simulate the rolling of a dice

    Attributes
    ----------
    n_rolls : int
        Number of rolls for the dice
    result : tuple[int, int]
        Most recent outcome of the roll of two dice
    total : int
        Sum of dice outcome

    """

    def __init__(self, seed=None) -> None:
        self._result: typing.Iterable[int] | None = None
        self.n_rolls: int = 0
        self.rng = np.random.default_rng(seed)

    @property
    def total(self) -> int:
        if self._result is not None:
            return sum(self.result)

    @property
    def result(self) -> tuple[int, int]:
        if self._result is not None:
            return tuple(self._result)

    @result.setter
    def result(self, value: typing.Iterable[int]) -> tuple[int, int]:
        # Allows setting of result, used for some tests, but not recommended
        # NOTE: no checking is done here, so use with caution
        # NOTE: this does not increment the number of rolls
        self._result = value

    def roll(self) -> None:
        self.n_rolls += 1
        self._result = self.rng.integers(1, 7, size=2).tolist()

    def fixed_roll(self, outcome: typing.Iterable[int]) -> None:
        self.n_rolls += 1
        self._result = outcome
