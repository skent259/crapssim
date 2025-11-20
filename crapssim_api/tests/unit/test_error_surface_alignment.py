from pytest import raises

from crapssim_api.errors import ApiError, ApiErrorCode
from crapssim_api.http import apply_action, start_session


def _session_id(seed: int = 777) -> str:
    return start_session({"seed": seed})["session_id"]


def test_amount_must_be_positive() -> None:
    session_id = _session_id()

    with raises(ApiError) as exc:
        apply_action(
            {
                "verb": "place",
                "args": {"amount": 0, "number": 6},
                "session_id": session_id,
            }
        )

    assert exc.value.code is ApiErrorCode.BAD_ARGS


def test_amount_must_be_numeric() -> None:
    session_id = _session_id(778)

    with raises(ApiError) as exc:
        apply_action(
            {
                "verb": "place",
                "args": {"amount": "ten", "number": 8},
                "session_id": session_id,
            }
        )

    assert exc.value.code is ApiErrorCode.BAD_ARGS


def test_invalid_number_rejected() -> None:
    session_id = _session_id(779)

    with raises(ApiError) as exc:
        apply_action(
            {
                "verb": "place",
                "args": {"amount": 25, "number": 2},
                "session_id": session_id,
            }
        )

    assert exc.value.code is ApiErrorCode.BAD_ARGS


def test_odds_require_point() -> None:
    session_id = _session_id(780)

    with raises(ApiError) as exc:
        apply_action(
            {
                "verb": "odds",
                "args": {"amount": 10, "base": "pass_line"},
                "session_id": session_id,
            }
        )

    assert exc.value.code is ApiErrorCode.TABLE_RULE_BLOCK


def test_remove_bet_requires_match() -> None:
    session_id = _session_id(781)

    with raises(ApiError) as exc:
        apply_action(
            {
                "verb": "remove_bet",
                "args": {"type": "place", "number": 8},
                "session_id": session_id,
            }
        )

    assert exc.value.code is ApiErrorCode.BAD_ARGS


def test_reduce_bet_requires_existing_action() -> None:
    session_id = _session_id(782)

    with raises(ApiError) as exc:
        apply_action(
            {
                "verb": "reduce_bet",
                "args": {"type": "place", "number": 5, "new_amount": 15},
                "session_id": session_id,
            }
        )

    assert exc.value.code is ApiErrorCode.BAD_ARGS
