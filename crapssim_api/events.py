from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Event:
    id: str
    type: str
    roll_seq: int | None = None
    hand_id: int | None = None
    ts: str | None = None
    bankroll_before: str | None = None
    bankroll_after: str | None = None
    meta: dict[str, Any] | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        # Keep a compact payload
        return {k: v for k, v in d.items() if v is not None}
