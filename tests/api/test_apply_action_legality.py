import pytest

pytest.importorskip("pydantic")

from pytest import raises

from crapssim_api.errors import ApiError, ApiErrorCode
from crapssim_api.http import apply_action, roll, start_session


def _session_with_point(seed: int = 404) -> str:
    session_id = start_session({"seed": seed})["session_id"]
    roll({"session_id": session_id, "dice": [3, 3]})
    return session_id


def test_pass_line_rejected_when_point_on() -> None:
    session_id = start_session({"seed": 111})["session_id"]
    apply_action(
        {"verb": "pass_line", "args": {"amount": 10}, "session_id": session_id}
    )
    roll({"session_id": session_id, "dice": [3, 3]})

    with raises(ApiError) as exc:
        apply_action(
            {"verb": "pass_line", "args": {"amount": 5}, "session_id": session_id}
        )

    assert exc.value.code is ApiErrorCode.TABLE_RULE_BLOCK


def test_come_bet_requires_point_on() -> None:
    session_id = start_session({"seed": 222})["session_id"]
    with raises(ApiError) as exc:
        apply_action({"verb": "come", "args": {"amount": 10}, "session_id": session_id})
    assert exc.value.code is ApiErrorCode.TABLE_RULE_BLOCK


def test_come_bet_allowed_after_point_on() -> None:
    session_id = _session_with_point()
    result = apply_action(
        {"verb": "come", "args": {"amount": 10}, "session_id": session_id}
    )
    effect = result["effect_summary"]
    assert effect["applied"] is True
    assert effect["bankroll_delta"] < 0


def test_state_hint_does_not_override_engine() -> None:
    session_id = start_session({"seed": 333})["session_id"]
    apply_action(
        {"verb": "pass_line", "args": {"amount": 10}, "session_id": session_id}
    )
    roll({"session_id": session_id, "dice": [3, 3]})

    with raises(ApiError) as exc:
        apply_action(
            {
                "verb": "pass_line",
                "args": {"amount": 5},
                "session_id": session_id,
                "state": {"puck": "OFF", "point": None},
            }
        )

    assert exc.value.code is ApiErrorCode.TABLE_RULE_BLOCK
