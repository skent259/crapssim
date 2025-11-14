import pytest
from pytest import raises

from crapssim_api.errors import ApiError, ApiErrorCode
from crapssim_api.http import apply_action, roll, start_session
from crapssim_api.session_store import SESSION_STORE


def _start_session(seed: int = 314) -> str:
    return start_session({"seed": seed})["session_id"]


def _establish_point(session_id: str, dice: tuple[int, int] = (3, 3)) -> None:
    roll({"session_id": session_id, "dice": [dice[0], dice[1]]})


def test_insufficient_funds_rejected() -> None:
    session_id = _start_session()
    sess = SESSION_STORE.ensure(session_id)
    player = sess["session"].player()
    assert player is not None
    player.bankroll = 5.0

    with raises(ApiError) as exc:
        apply_action(
            {"verb": "pass_line", "args": {"amount": 10}, "session_id": session_id}
        )

    err = exc.value
    assert err.code is ApiErrorCode.INSUFFICIENT_FUNDS
    assert "bankroll" in err.hint
    assert player.bankroll == pytest.approx(5.0)


def test_bankroll_snapshot_matches_engine() -> None:
    session_id = _start_session(seed=2718)
    sess = SESSION_STORE.ensure(session_id)
    player = sess["session"].player()
    assert player is not None

    result = apply_action(
        {"verb": "pass_line", "args": {"amount": 10}, "session_id": session_id}
    )

    snapshot = result["snapshot"]
    assert snapshot["bankroll_after"] == f"{player.bankroll:.2f}"
    assert any(bet["type"] == "PassLine" for bet in snapshot["bets"])
    assert player.bankroll == pytest.approx(990.0)


def test_buy_action_includes_vig_in_cost() -> None:
    session_id = _start_session(seed=1618)
    _establish_point(session_id)
    sess = SESSION_STORE.ensure(session_id)
    player = sess["session"].player()
    assert player is not None
    player.bankroll = 200.0

    result = apply_action(
        {"verb": "buy", "args": {"box": 4, "amount": 20}, "session_id": session_id}
    )

    effect = result["effect_summary"]
    assert effect["cash_required"] == pytest.approx(21.0)
    assert effect["vig"]["amount"] == pytest.approx(1.0)
    assert effect["vig"]["paid_on_win"] is False
    assert player.bankroll == pytest.approx(179.0)
    assert result["snapshot"]["bankroll_after"] == f"{player.bankroll:.2f}"


def test_table_rule_block_error_includes_state() -> None:
    session_id = _start_session(seed=2024)
    apply_action(
        {"verb": "pass_line", "args": {"amount": 10}, "session_id": session_id}
    )
    _establish_point(session_id)

    with raises(ApiError) as exc:
        apply_action(
            {"verb": "pass_line", "args": {"amount": 5}, "session_id": session_id}
        )

    err = exc.value
    assert err.code is ApiErrorCode.TABLE_RULE_BLOCK
    assert err.at_state["session_id"] == session_id
    assert err.at_state["hand_id"] is not None
