import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from pytest import raises

from crapssim_api.errors import ApiError, ApiErrorCode
from crapssim_api.http import apply_action, start_session


def test_known_verb_stub_ok():
    sid = start_session({"seed": 101})["session_id"]
    res = apply_action({"verb": "hardway", "args": {"amount": 5}, "session_id": sid})
    eff = res["effect_summary"]
    assert eff["applied"] is True
    assert eff["bankroll_delta"] == 0.0
    assert eff["verb"] == "hardway"
    assert "validated" in eff["note"]


def test_unknown_verb_raises_unsupported():
    with raises(ApiError) as e:
        apply_action({"verb": "foo", "args": {}})
    assert e.value.code is ApiErrorCode.UNSUPPORTED_BET


def test_bad_args_not_dict():
    with raises(ApiError) as e:
        apply_action({"verb": "place", "args": 123})
    assert e.value.code is ApiErrorCode.BAD_ARGS


def test_bad_args_empty_verb():
    with raises(ApiError) as e:
        apply_action({"verb": "", "args": {}})
    assert e.value.code is ApiErrorCode.BAD_ARGS
