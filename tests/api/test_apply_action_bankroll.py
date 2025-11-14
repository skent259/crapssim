import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from pytest import raises

from crapssim_api.actions import DEFAULT_START_BANKROLL, SessionBankrolls, get_bankroll
from crapssim_api.errors import ApiError, ApiErrorCode
from crapssim_api.http import apply_action, roll, start_session
from crapssim_api.session_store import SESSION_STORE


def _place_setup(seed: int = 314) -> tuple[str, dict[str, object]]:
    start = start_session({"seed": seed})
    session_id = start["session_id"]
    # Establish a point so box bets become legal
    snap = roll({"session_id": session_id, "dice": [3, 3]})["snapshot"]
    state = {"puck": snap["puck"], "point": snap["point"]}
    return session_id, state


def test_insufficient_funds_rejected():
    sid, state = _place_setup()
    sess = SESSION_STORE.ensure(sid)
    player = sess["session"].player()
    assert player is not None
    player.bankroll = 5.0
    SessionBankrolls[sid] = 5.0
    with raises(ApiError) as e:
        apply_action(
            {
                "verb": "place",
                "args": {"box": 6, "amount": 12},
                "session_id": sid,
                "state": state,
            }
        )
    err = e.value
    assert err.code == ApiErrorCode.INSUFFICIENT_FUNDS
    assert "bankroll" in err.hint


def test_bankroll_deducts_deterministically():
    sid, state = _place_setup(seed=2718)
    sess = SESSION_STORE.ensure(sid)
    player = sess["session"].player()
    assert player is not None
    player.bankroll = 100.0
    SessionBankrolls[sid] = 100.0
    res = apply_action(
        {
            "verb": "place",
            "args": {"box": 6, "amount": 12},
            "session_id": sid,
            "state": state,
        }
    )
    after = float(res["snapshot"]["bankroll_after"])
    assert pytest.approx(after, rel=0, abs=1e-9) == 88.0
    assert pytest.approx(SessionBankrolls[sid]) == 88.0
    assert pytest.approx(player.bankroll) == 88.0


def test_table_rule_block_error_envelope_consistency():
    try:
        raise ApiError(
            ApiErrorCode.TABLE_RULE_BLOCK,
            "test block",
            {"session_id": "x", "hand_id": None, "roll_seq": None},
        )
    except ApiError as e:
        assert e.code == ApiErrorCode.TABLE_RULE_BLOCK
        assert isinstance(e.hint, str)
        assert "session_id" in e.at_state


def test_default_bankroll_if_unknown_session():
    sid = "newsession"
    assert get_bankroll(sid) == DEFAULT_START_BANKROLL


def test_buy_action_includes_vig_in_cost():
    sid, state = _place_setup(seed=1618)
    sess = SESSION_STORE.ensure(sid)
    player = sess["session"].player()
    assert player is not None
    player.bankroll = 200.0
    SessionBankrolls[sid] = 200.0
    res = apply_action(
        {
            "verb": "buy",
            "args": {"box": 4, "amount": 20},
            "session_id": sid,
            "state": state,
        }
    )
    effect = res["effect_summary"]
    assert effect["cash_required"] == pytest.approx(21.0)
    assert effect["vig"]["amount"] == pytest.approx(1.0)
    assert effect["vig"]["paid_on_win"] is False
    assert SessionBankrolls[sid] == pytest.approx(179.0)
    assert pytest.approx(player.bankroll) == pytest.approx(179.0)
