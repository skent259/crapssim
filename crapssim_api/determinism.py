# NOTE:
# This module is reserved for future determinism / snapshot tooling.
# It is currently not imported by the HTTP surface or session management code,
# and changes here should not affect runtime behavior until a determinism
# design is finalized and wired in intentionally.

from __future__ import annotations
import json
import hashlib
from dataclasses import dataclass
from typing import Any, Iterable, Literal

from .rng import SeededRNG

_TapeMethod = Literal["randint", "choice"]


@dataclass(frozen=True)
class TapeEntry:
    method: _TapeMethod
    args: tuple
    result: Any

    def to_json(self) -> dict:
        # Ensure JSON-serializable payload
        def _jsonable(x):
            if isinstance(x, (str, int, float, bool)) or x is None:
                return x
            if isinstance(x, (list, tuple)):
                return [_jsonable(i) for i in x]
            if isinstance(x, dict):
                return {str(k): _jsonable(v) for k, v in x.items()}
            # Fallback to repr for opaque types (deterministic enough for our tape)
            return repr(x)

        return {
            "method": self.method,
            "args": _jsonable(self.args),
            "result": _jsonable(self.result),
        }


def compute_hash(data: Any) -> str:
    """Deterministic short hash over sorted JSON."""
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return h[:16]  # short but stable


class DeterminismHarness:
    """Records RNG calls into a tape and can replay them for parity checks."""

    def __init__(self, seed: int | None = None):
        self.seed = seed
        self._tape: list[TapeEntry] = []
        # SeededRNG will call back into our recorder hooks
        self.rng = SeededRNG(seed=seed, recorder=self)

    # ---- recorder API used by SeededRNG ----
    def _record(self, method: _TapeMethod, args: tuple, result: Any) -> None:
        self._tape.append(TapeEntry(method=method, args=args, result=result))

    # ---- convenience RNG facades (optional sugar for tests/tools) ----
    def randint(self, a: int, b: int) -> int:
        return self.rng.randint(a, b)

    def choice(self, seq: Iterable[Any]) -> Any:
        return self.rng.choice(seq)

    # ---- tape I/O ----
    def export_tape(self) -> dict:
        entries = [e.to_json() for e in self._tape]
        tape = {
            "seed": self.seed,
            "entries": entries,
        }
        tape["run_hash"] = compute_hash(tape)
        return tape

    def replay_tape(self, tape: dict) -> None:
        """Re-run RNG calls and assert parity with a saved tape. Raises AssertionError on mismatch."""
        seed = tape.get("seed", None)
        entries = tape.get("entries", [])
        # fresh harness to avoid mixing current tape with replay tape
        replay_rng = SeededRNG(seed=seed, recorder=None)
        for idx, ent in enumerate(entries):
            m = ent["method"]
            args = ent["args"]
            expected = ent["result"]
            if m == "randint":
                got = replay_rng.randint(*args)
            elif m == "choice":
                # choice uses a sequence; to keep deterministic we work with args[0]
                seq = list(args[0])
                got = replay_rng.choice(seq)
            else:
                raise AssertionError(f"Unknown method in tape at #{idx}: {m}")
            if got != expected:
                raise AssertionError(f"Tape mismatch at #{idx}: expected {expected}, got {got}")
        # Hash must be stable
        assert tape.get("run_hash") == compute_hash({"seed": seed, "entries": entries})
