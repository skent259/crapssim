"""Tests for bet management helpers and verbs."""

import pytest

from crapssim.bet import All, Field, Fire, Horn, Odds, PassLine, Place, Small, Tall
from crapssim.table import Table

from crapssim_api.actions import apply_bet_management, build_bet, is_bet_management_verb
from crapssim_api.errors import ApiErrorCode
from crapssim_api.session import Session


@pytest.fixture()
def session() -> Session:
    table = Table()
    return Session(table=table)


def _ensure_player(session: Session):
    session._ensure_player()  # noqa: SLF001 - test helper access
    player = session.player()
    assert player is not None
    return player


def test_remove_bet_success(session: Session):
    player = _ensure_player(session)
    bet = build_bet(
        "place", {"amount": 60, "number": 6}, table=session.table, player=player
    )
    player.add_bet(bet)

    result = apply_bet_management(session, "remove_bet", {"type": "place", "number": 6})

    assert result["result"] == "ok"
    assert result["error_code"] is None
    assert result["bets_after"] == []
    assert pytest.approx(result["bankroll_after"], rel=1e-9) == pytest.approx(
        result["bankroll_before"] + 60.0, rel=1e-9
    )


def test_remove_bet_invalid_type(session: Session):
    result = apply_bet_management(session, "remove_bet", {"type": "unknown"})

    assert result["result"] == "error"
    assert result["error_code"] == ApiErrorCode.BAD_ARGS.value


def test_remove_bet_non_removable(session: Session):
    player = _ensure_player(session)
    bet = build_bet("pass_line", {"amount": 10}, table=session.table, player=player)
    player.add_bet(bet)
    session.table.point.number = 4

    result = apply_bet_management(session, "remove_bet", {"type": "pass_line"})

    assert result["result"] == "error"
    assert result["error_code"] == ApiErrorCode.BAD_ARGS.value
    # Bet remains on the felt
    assert len(player.bets) == 1


def test_reduce_bet_success(session: Session):
    player = _ensure_player(session)
    bet = build_bet(
        "place", {"amount": 60, "number": 6}, table=session.table, player=player
    )
    player.add_bet(bet)

    result = apply_bet_management(
        session,
        "reduce_bet",
        {"type": "place", "number": 6, "new_amount": 30},
    )

    assert result["result"] == "ok"
    assert result["error_code"] is None
    assert result["bets_after"] == [{"type": "Place", "number": 6, "amount": 30.0}]
    assert pytest.approx(result["bankroll_after"], rel=1e-9) == pytest.approx(
        result["bankroll_before"] + 30.0, rel=1e-9
    )


def test_reduce_bet_to_zero(session: Session):
    player = _ensure_player(session)
    bet = build_bet(
        "place", {"amount": 24, "number": 8}, table=session.table, player=player
    )
    player.add_bet(bet)

    result = apply_bet_management(
        session,
        "reduce_bet",
        {"type": "place", "number": 8, "new_amount": 0},
    )

    assert result["result"] == "ok"
    assert result["bets_after"] == []


def test_reduce_bet_increase_rejected(session: Session):
    player = _ensure_player(session)
    bet = build_bet(
        "place", {"amount": 30, "number": 5}, table=session.table, player=player
    )
    player.add_bet(bet)

    result = apply_bet_management(
        session,
        "reduce_bet",
        {"type": "place", "number": 5, "new_amount": 60},
    )

    assert result["result"] == "error"
    assert result["error_code"] == ApiErrorCode.BAD_ARGS.value
    # State unchanged
    assert player.bets[0].amount == pytest.approx(30.0)


def test_clear_all_bets(session: Session):
    player = _ensure_player(session)
    player.add_bet(
        build_bet("field", {"amount": 10}, table=session.table, player=player)
    )
    player.add_bet(
        build_bet(
            "place", {"amount": 30, "number": 4}, table=session.table, player=player
        )
    )
    pass_line = build_bet(
        "pass_line", {"amount": 15}, table=session.table, player=player
    )
    player.add_bet(pass_line)
    session.table.point.number = 6

    result = apply_bet_management(session, "clear_all_bets", {})

    assert result["result"] == "ok"
    assert len(player.bets) == 1
    assert isinstance(player.bets[0], PassLine)


def test_clear_specific_categories(session: Session):
    player = _ensure_player(session)
    player.add_bet(Field(5))
    player.add_bet(Horn(2))
    player.add_bet(Fire(1))
    player.add_bet(All(3))
    player.add_bet(Tall(3))
    player.add_bet(Small(3))
    player.add_bet(Place(6, 30))

    result_center = apply_bet_management(session, "clear_center_bets", {})
    assert result_center["result"] == "ok"
    assert all(bet["type"] != "Field" for bet in result_center["bets_after"])

    result_place = apply_bet_management(session, "clear_place_buy_lay", {})
    assert result_place["result"] == "ok"
    assert result_place["bets_after"] == []


def test_clear_ats_and_fire(session: Session):
    player = _ensure_player(session)
    player.add_bet(Fire(1))
    player.add_bet(All(2))
    player.add_bet(Tall(2))
    player.add_bet(Small(2))

    result_ats = apply_bet_management(session, "clear_ats_bets", {})
    assert result_ats["result"] == "ok"
    assert all(bet["type"] != "All" for bet in result_ats["bets_after"])

    result_fire = apply_bet_management(session, "clear_fire_bets", {})
    assert result_fire["result"] == "ok"
    assert result_fire["bets_after"] == []


def test_set_odds_working(session: Session):
    player = _ensure_player(session)
    base_bet = PassLine(10)
    player.add_bet(base_bet)
    session.table.point.number = 4
    odds_bet = Odds(PassLine, 4, 20)
    player.add_bet(odds_bet)

    result = apply_bet_management(
        session,
        "set_odds_working",
        {"base": "pass_line", "number": 4, "working": True},
    )

    assert result["result"] == "ok"
    updated = [bet for bet in player.bets if isinstance(bet, Odds) and bet.number == 4][
        0
    ]
    assert updated.always_working is True

    result_disable = apply_bet_management(
        session,
        "set_odds_working",
        {"base": "pass_line", "number": 4, "working": False},
    )

    assert result_disable["result"] == "ok"
    refreshed = [
        bet for bet in player.bets if isinstance(bet, Odds) and bet.number == 4
    ][0]
    assert refreshed.always_working is False


def test_set_odds_working_requires_match(session: Session):
    _ensure_player(session)

    result = apply_bet_management(
        session,
        "set_odds_working",
        {"base": "pass_line", "number": 6, "working": True},
    )

    assert result["result"] == "error"
    assert result["error_code"] == ApiErrorCode.BAD_ARGS.value


def test_management_verbs_registered():
    expected = {
        "remove_bet",
        "reduce_bet",
        "clear_all_bets",
        "clear_center_bets",
        "clear_place_buy_lay",
        "clear_ats_bets",
        "clear_fire_bets",
        "set_odds_working",
    }

    for verb in expected:
        assert is_bet_management_verb(verb)
