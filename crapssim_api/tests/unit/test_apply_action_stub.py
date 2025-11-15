import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from pytest import raises

from crapssim_api.errors import ApiError, ApiErrorCode
from crapssim_api.http import apply_action, start_session


def test_hardway_bet_executes_on_engine():
    session_id = start_session({"seed": 101})["session_id"]
    result = apply_action(
        {
            "verb": "hardway",
            "args": {"number": 6, "amount": 5},
            "session_id": session_id,
        }
    )
    effect = result["effect_summary"]
    assert effect["applied"] is True
    assert effect["bankroll_delta"] == pytest.approx(-5.0)
    assert effect["note"] == "applied via engine"


def test_unknown_verb_raises_unsupported():
    session_id = start_session({"seed": 202})["session_id"]
    with raises(ApiError) as exc:
        apply_action({"verb": "foo", "args": {}, "session_id": session_id})
    assert exc.value.code is ApiErrorCode.UNSUPPORTED_BET


def test_bad_args_not_dict():
    session_id = start_session({"seed": 303})["session_id"]
    with raises(ApiError) as exc:
        apply_action({"verb": "place", "args": 123, "session_id": session_id})
    assert exc.value.code is ApiErrorCode.BAD_ARGS


def test_bad_args_empty_verb():
    session_id = start_session({"seed": 404})["session_id"]
    with raises(ApiError) as exc:
        apply_action({"verb": "", "args": {}, "session_id": session_id})
    assert exc.value.code is ApiErrorCode.BAD_ARGS
