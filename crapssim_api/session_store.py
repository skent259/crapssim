from __future__ import annotations

from typing import Any, Dict

from .hand_state import HandState


class SessionStore:
    def __init__(self):
        self._s: Dict[str, Dict[str, Any]] = {}

    def ensure(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self._s:
            self._s[session_id] = {
                "hand": HandState(),
                "roll_seq": 0,
                "last_dice": None,
            }
        return self._s[session_id]

    def get(self, session_id: str) -> Dict[str, Any]:
        return self.ensure(session_id)


SESSION_STORE = SessionStore()
