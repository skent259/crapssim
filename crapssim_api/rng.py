from __future__ import annotations
import random
from typing import Iterable, TypeVar

T = TypeVar("T")


class SeededRNG:
    """Thin wrapper to keep RNG calls centralized and seedable."""

    def __init__(self, seed: int | None = None):
        self._random = random.Random(seed)
        self.seed = seed

    def randint(self, a: int, b: int) -> int:
        return self._random.randint(a, b)

    def choice(self, seq: Iterable[T]) -> T:
        seq = list(seq)
        if not seq:
            raise ValueError("choice() on empty sequence")
        return self._random.choice(seq)
