"""
The dice are used by the craps Table for keeping track of the latest roll
and the total number of rolls so far. The dice object is mostly handled
internally, but advanced users may access it (through the Table, as table.dice)
for new bets or strategies as needed.
"""

from typing import Generator, Iterable, TypeAlias

import numpy as np

DicePair: TypeAlias = tuple[int, int]
"""Pair of dice represented as (die_one, die_two)."""

DicePairInput: TypeAlias = Iterable[int]
"""Pair of dice represented as an iterable of two integers."""


class Dice:
    """
    Simulate the rolling of a dice.

    Args:
        seed (int): The seed passed to the random number generator.
    """

    def __init__(self, seed=None) -> None:
        self._result: DicePairInput | None = None
        self.n_rolls: int = 0
        """Number of rolls for the dice"""
        self.rng: Generator = np.random.default_rng(seed)
        """Random number generated used when rolling"""

    @property
    def total(self) -> int:
        """Sum of dice outcome, e.g. 8 for (2, 6)"""
        if self._result is not None:
            return sum(self.result)

    @property
    def result(self) -> DicePair:
        """Most recent outcome of the roll of two dice, e.g. (2, 6)"""
        if self._result is not None:
            return tuple(self._result)

    @result.setter
    def result(self, value: DicePairInput) -> DicePair:
        # Allows setting of result, used for some tests, but not recommended
        # NOTE: no checking is done here, so use with caution
        # NOTE: this does not increment the number of rolls
        self._result = value

    def roll(self) -> None:
        """
        Randomly roll the dice

        The randomness of the dice is based on numpy.random,
        which uses the PCG-64 pseudo-random number generation
        (see numpy.random.PCG64`).
        """
        self.n_rolls += 1
        self._result = self.rng.integers(1, 7, size=2).tolist()

    def fixed_roll(self, outcome: DicePairInput) -> None:
        """
        Roll the dice with a specified outcome

        Args:
            outcome: The desired dice result to roll
        """
        self.n_rolls += 1
        self._result = outcome
