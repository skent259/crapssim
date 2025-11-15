# NOTE:
# This module is reserved for future determinism / snapshot tooling.
# It is currently not imported by the HTTP surface or session management code,
# and changes here should not affect runtime behavior until a determinism
# design is finalized and wired in intentionally.

from __future__ import annotations
import random
from typing import Iterable, TypeVar, Any

T = TypeVar("T")


class SeededRNG:
    """Thin wrapper to keep RNG calls centralized and seedable.

    If a recorder with a `_record(method, args, result)` method is provided,
    all calls are logged for determinism tapes.
    """

    def __init__(self, seed: int | None = None, recorder: Any | None = None):
        self._random = random.Random(seed)
        self.seed = seed
        self._recorder = recorder

    def _record(self, method: str, args: tuple, result: Any) -> None:
        if self._recorder is not None and hasattr(self._recorder, "_record"):
            try:
                self._recorder._record(method, args, result)  # type: ignore[attr-defined]
            except Exception:
                # Recording should never break RNG behavior
                pass

    def randint(self, a: int, b: int) -> int:
        r = self._random.randint(a, b)
        self._record("randint", (a, b), r)
        return r

    def choice(self, seq: Iterable[T]) -> T:
        seq_list = list(seq)
        if not seq_list:
            raise ValueError("choice() on empty sequence")
        r = self._random.choice(seq_list)
        # We record the logical value picked. For determinism, callers should replay with the same sequence.
        self._record("choice", (seq_list,), r)
        return r
