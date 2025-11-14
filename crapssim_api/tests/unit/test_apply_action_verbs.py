import pytest

from crapssim_api.http import apply_action, roll, start_session
from crapssim_api.session_store import SESSION_STORE


VERB_CASES = [
    ("pass_line", {"amount": 10}, "PassLine", False),
    ("dont_pass", {"amount": 10}, "DontPass", False),
    ("come", {"amount": 10}, "Come", True),
    ("dont_come", {"amount": 10}, "DontCome", True),
    ("place", {"box": 6, "amount": 12}, "Place", True),
    ("buy", {"box": 4, "amount": 20}, "Buy", True),
    ("lay", {"box": 4, "amount": 20}, "Lay", True),
    ("put", {"box": 6, "amount": 30}, "Put", True),
    ("hardway", {"number": 6, "amount": 5}, "HardWay", False),
    ("field", {"amount": 5}, "Field", False),
    ("any7", {"amount": 5}, "Any7", False),
    ("c&e", {"amount": 5}, "CAndE", False),
    ("horn", {"amount": 4}, "Horn", False),
    ("world", {"amount": 5}, "World", False),
    ("big6", {"amount": 5}, "Big6", False),
    ("big8", {"amount": 5}, "Big8", False),
]


def _prepare_session(needs_point: bool, seed: int) -> str:
    session_id = start_session({"seed": seed})["session_id"]
    if needs_point:
        roll({"session_id": session_id, "dice": [3, 3]})
    return session_id


@pytest.mark.parametrize("index,case", list(enumerate(VERB_CASES)))
def test_supported_verbs_place_bets(index, case) -> None:
    verb, args, expected_type, needs_point = case
    seed = 700 + index
    session_id = _prepare_session(needs_point, seed)

    result = apply_action({"verb": verb, "args": dict(args), "session_id": session_id})
    effect = result["effect_summary"]
    assert effect["applied"] is True

    snapshot = result["snapshot"]
    assert any(bet["type"] == expected_type for bet in snapshot["bets"])

    sess = SESSION_STORE.ensure(session_id)
    player = sess["session"].player()
    assert player is not None


def test_odds_bet_attaches_to_pass_line() -> None:
    session_id = start_session({"seed": 901})["session_id"]
    apply_action(
        {"verb": "pass_line", "args": {"amount": 10}, "session_id": session_id}
    )
    roll({"session_id": session_id, "dice": [3, 3]})

    result = apply_action(
        {
            "verb": "odds",
            "args": {"base": "pass_line", "amount": 30},
            "session_id": session_id,
        }
    )

    snapshot = result["snapshot"]
    assert any(bet["type"] == "Odds" for bet in snapshot["bets"])
    effect = result["effect_summary"]
    assert effect["applied"] is True
