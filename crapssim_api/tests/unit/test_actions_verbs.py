from __future__ import annotations

import pytest

from crapssim.bet import All, AnyCraps, Boxcars, Fire, Hop, Small, Tall, Three, Two, Yo
from crapssim.table import Table

from crapssim_api.actions import SUPPORTED_VERBS, build_bet
from crapssim_api.errors import ApiError, ApiErrorCode


@pytest.fixture
def table_and_player():
    table = Table()
    player = table.add_player(bankroll=1000)
    return table, player


@pytest.mark.parametrize(
    ("verb", "bet_cls"),
    [
        ("two", Two),
        ("three", Three),
        ("yo", Yo),
        ("boxcars", Boxcars),
        ("any_craps", AnyCraps),
        ("fire", Fire),
        ("all", All),
        ("tall", Tall),
        ("small", Small),
    ],
)
def test_simple_amount_only_verbs(table_and_player, verb: str, bet_cls):
    table, player = table_and_player
    bet = build_bet(verb, {"amount": 25}, table=table, player=player)
    assert isinstance(bet, bet_cls)
    assert bet.amount == pytest.approx(25.0)


def test_hop_builds_with_result(table_and_player):
    table, player = table_and_player
    bet = build_bet("hop", {"amount": 12, "result": [5, 2]}, table=table, player=player)
    assert isinstance(bet, Hop)
    assert bet.result == (2, 5)
    assert bet.amount == pytest.approx(12.0)


@pytest.mark.parametrize(
    "result",
    [None, [5], [1, 9], ["a", 2]],
)
def test_hop_rejects_bad_results(table_and_player, result):
    table, player = table_and_player
    with pytest.raises(ApiError) as excinfo:
        args = {"amount": 5}
        if result is not None:
            args["result"] = result
        build_bet("hop", args, table=table, player=player)
    assert excinfo.value.code == ApiErrorCode.BAD_ARGS


def test_supported_verbs_include_new_entries():
    expected = {
        "two",
        "three",
        "yo",
        "boxcars",
        "any_craps",
        "hop",
        "fire",
        "all",
        "tall",
        "small",
    }
    assert expected.issubset(SUPPORTED_VERBS)
