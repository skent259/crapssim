import hashlib
import datetime
from typing import Any, Dict


def _now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def make_event_id(session_id: str, hand_id: int, roll_seq: int, etype: str) -> str:
    s = f"{session_id}/{hand_id}/{roll_seq}/{etype}"
    return hashlib.sha1(s.encode()).hexdigest()[:12]


def build_event(
    session_id: str,
    hand_id: int,
    roll_seq: int,
    etype: str,
    bankroll_before: str,
    bankroll_after: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "type": etype,
        "id": make_event_id(session_id, hand_id, roll_seq, etype),
        "ts": _now_iso(),
        "hand_id": hand_id,
        "roll_seq": roll_seq,
        "bankroll_before": bankroll_before,
        "bankroll_after": bankroll_after,
        "data": data,
    }
