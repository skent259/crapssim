from __future__ import annotations
from typing import Any


def snapshot_from_table(table: Any) -> dict:
    """Return a minimal, stable snapshot dictionary for now.

    NOTE: This is a stub; Phase 4 will fill out full schema.
    We avoid importing engine modules here to keep the skeleton dependency-free.
    """
    return {
        "session_id": None,
        "hand_id": None,
        "roll_seq": None,
        "puck": None,
        "point": None,
        "dice": None,
        "bankroll_after": None,
        "bets": {},
        "working_flags": {},
        "identity": {"engine_version": None, "table_profile": "vanilla", "seed": None},
    }
