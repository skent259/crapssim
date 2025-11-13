import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from pytest import raises

from crapssim_api.actions import DEFAULT_START_BANKROLL, SessionBankrolls, get_bankroll
from crapssim_api.errors import ApiError, ApiErrorCode
from crapssim_api.http import apply_action


def _req(verb, args, sid="bankroll-test", puck="ON", point=6):
    return {"verb": verb, "args": args, "session_id": sid, "state": {"puck": puck, "point": point}}


def test_insufficient_funds_rejected():
    sid = "lowfunds"
    SessionBankrolls[sid] = 5.0
    with raises(ApiError) as e:
        apply_action(_req("place", {"box": 6, "amount": 12}, sid))
    err = e.value
    assert err.code == ApiErrorCode.INSUFFICIENT_FUNDS
    assert "bankroll" in err.hint


def test_bankroll_deducts_deterministically():
    sid = "deduct"
    SessionBankrolls[sid] = 100.0
    res = apply_action(_req("place", {"box": 6, "amount": 12}, sid))
    after = res["snapshot"]["bankroll_after"]
    assert round(after, 2) == 88.0
    assert SessionBankrolls[sid] == after


def test_table_rule_block_error_envelope_consistency():
    try:
        raise ApiError(ApiErrorCode.TABLE_RULE_BLOCK, "test block", {"session_id": "x", "hand_id": None, "roll_seq": None})
    except ApiError as e:
        assert e.code == ApiErrorCode.TABLE_RULE_BLOCK
        assert isinstance(e.hint, str)
        assert "session_id" in e.at_state


def test_default_bankroll_if_unknown_session():
    sid = "newsession"
    assert get_bankroll(sid) == DEFAULT_START_BANKROLL


def test_buy_action_includes_vig_in_cost():
    sid = "buy-vig"
    SessionBankrolls[sid] = 200.0
    res = apply_action(_req("buy", {"box": 4, "amount": 20}, sid))
    effect = res["effect_summary"]
    assert effect["cash_required"] == pytest.approx(21.0)
    assert effect["vig"]["amount"] == pytest.approx(1.0)
    assert effect["vig"]["paid_on_win"] is False
    assert SessionBankrolls[sid] == pytest.approx(179.0)
