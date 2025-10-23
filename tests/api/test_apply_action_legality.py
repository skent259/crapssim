from pytest import raises

from crapssim_api.http import apply_action
from crapssim_api.errors import ApiError, ApiErrorCode


def _req(verb, args, puck="OFF", point=None):
    return {"verb": verb, "args": args, "state": {"puck": puck, "point": point}}


def test_place_illegal_on_comeout():
    with raises(ApiError) as e:
        apply_action(_req("place", {"box": 6, "amount": 12}, puck="OFF"))
    assert e.value.code is ApiErrorCode.ILLEGAL_TIMING


def test_place_legal_when_puck_on_with_increment_ok():
    res = apply_action(_req("place", {"box": 6, "amount": 12}, puck="ON", point=6))
    eff = res["effect_summary"]
    assert eff["applied"] is True
    assert eff["bankroll_delta"] == 0.0


def test_increment_violation_on_place6():
    # 6 requires multiples of 6; 7 should fail
    with raises(ApiError) as e:
        # Call endpoint path to exercise envelope
        apply_action(_req("place", {"box": 6, "amount": 7}, puck="ON", point=6))
    assert e.value.code is ApiErrorCode.ILLEGAL_AMOUNT


def test_table_cap_limit_breach():
    with raises(ApiError) as e:
        apply_action(_req("buy", {"box": 4, "amount": 50000}, puck="ON", point=4))
    assert e.value.code is ApiErrorCode.LIMIT_BREACH


def test_line_bet_only_on_comeout():
    with raises(ApiError) as e:
        apply_action(_req("pass_line", {"amount": 10}, puck="ON", point=6))
    assert e.value.code is ApiErrorCode.ILLEGAL_TIMING
