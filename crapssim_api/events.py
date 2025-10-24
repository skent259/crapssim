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


def build_point_set(
    session_id: str,
    hand_id: int,
    roll_seq: int,
    bankroll_before: str,
    bankroll_after: str,
    point: int,
) -> Dict[str, Any]:
    return build_event(
        session_id,
        hand_id,
        roll_seq,
        "point_set",
        bankroll_before,
        bankroll_after,
        {"point": point},
    )


def build_point_made(
    session_id: str,
    hand_id: int,
    roll_seq: int,
    bankroll_before: str,
    bankroll_after: str,
    point: int,
) -> Dict[str, Any]:
    return build_event(
        session_id,
        hand_id,
        roll_seq,
        "point_made",
        bankroll_before,
        bankroll_after,
        {"point": point},
    )


def build_seven_out(
    session_id: str,
    hand_id: int,
    roll_seq: int,
    bankroll_before: str,
    bankroll_after: str,
) -> Dict[str, Any]:
    return build_event(
        session_id,
        hand_id,
        roll_seq,
        "seven_out",
        bankroll_before,
        bankroll_after,
        {},
    )


def build_hand_ended(
    session_id: str,
    hand_id: int,
    roll_seq: int,
    bankroll_before: str,
    bankroll_after: str,
    end_reason: str,
) -> Dict[str, Any]:
    return build_event(
        session_id,
        hand_id,
        roll_seq,
        "hand_ended",
        bankroll_before,
        bankroll_after,
        {"end_reason": end_reason},
    )
