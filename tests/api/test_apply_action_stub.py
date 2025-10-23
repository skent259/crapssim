from pytest import raises

from crapssim_api.errors import ApiError, ApiErrorCode
from crapssim_api.http import apply_action


def test_known_verb_stub_ok():
    res = apply_action({"verb": "place", "args": {"box": 6, "amount": 12}})
    eff = res["effect_summary"]
    assert eff["applied"] is True
    assert eff["bankroll_delta"] == 0.0
    assert eff["verb"] == "place"
    assert "note" in eff


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
