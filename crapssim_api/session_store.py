from __future__ import annotations

from typing import Any, Dict

from crapssim.table import Table

from .hand_state import HandState


def _default_seed_for(session_id: str) -> int:
    """Derive a stable seed for ad-hoc sessions.

    The Python built-in ``hash`` is randomized per-process, so we use a
    deterministic hash to keep behaviour repeatable across runs.
    """

    try:
        data = session_id.encode("utf-8")
    except AttributeError:  # pragma: no cover - defensive fallback
        data = str(session_id).encode("utf-8")
    # ``zlib.crc32`` returns an unsigned 32-bit checksum that is stable across
    # processes and interpreter invocations.
    import zlib

    return zlib.crc32(data) & 0xFFFFFFFF


class SessionStore:
    def __init__(self):
        self._s: Dict[str, Dict[str, Any]] = {}

    def _new_state(self, session_id: str, seed: int | None) -> Dict[str, Any]:
        rng_seed = seed if seed is not None else _default_seed_for(session_id)
        return {
            "hand": HandState(),
            "roll_seq": 0,
            "last_dice": None,
            "table": Table(seed=rng_seed),
            "seed": seed,
            "rng_seed": rng_seed,
        }

    def create(self, session_id: str, *, seed: int | None) -> Dict[str, Any]:
        state = self._new_state(session_id, seed)
        self._s[session_id] = state
        return state

    def ensure(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self._s:
            self._s[session_id] = self._new_state(session_id, None)
        state = self._s[session_id]
        # ``table`` can be cleared in tests; make sure it exists before use.
        if "table" not in state or state["table"] is None:
            rng_seed = state.get("seed")
            seed_value = rng_seed if isinstance(rng_seed, int) else _default_seed_for(session_id)
            state["table"] = Table(seed=seed_value)
            state.setdefault("rng_seed", seed_value)
        return state

    def get(self, session_id: str) -> Dict[str, Any]:
        return self.ensure(session_id)


SESSION_STORE = SessionStore()
