"""Scenario definitions for CrapsSim API surface stress testing."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple, TypedDict

from crapssim_api import actions as api_actions


class ScenarioPreActionRequired(TypedDict):
    verb: str


class ScenarioPreAction(ScenarioPreActionRequired, total=False):
    args: Dict[str, Any]


class ScenarioSetupStep(TypedDict, total=False):
    dice: Tuple[int, int] | None
    actions: List[ScenarioPreAction]


class ScenarioState(TypedDict, total=False):
    rolls_before: List[Tuple[int, int]]
    existing_bets: List[ScenarioPreAction]
    setup_steps: List[ScenarioSetupStep]
    bankroll: float


class ScenarioExpectation(TypedDict):
    result: str
    error_code: str | None


class Scenario(TypedDict):
    label: str
    verb: str
    args: Dict[str, Any]
    pre_state: ScenarioState
    expect: ScenarioExpectation


def _build_verb_catalog() -> Dict[str, Dict[str, Any]]:
    catalog: Dict[str, Dict[str, Any]] = {}
    for verb in sorted(api_actions.SUPPORTED_VERBS):
        metadata: Dict[str, Any] = {}
        bet_cls = api_actions._BET_MANAGEMENT_TYPE_MAP.get(verb)
        if bet_cls is not None:
            metadata["engine_bet"] = bet_cls.__name__
        elif api_actions.is_bet_management_verb(verb):
            metadata["engine_bet"] = None
        catalog[verb] = metadata
    return catalog


VERB_CATALOG: Dict[str, Dict[str, Any]] = _build_verb_catalog()


DEFAULT_BANKROLL = 250.0


SCENARIOS: List[Scenario] = [
    {
        "label": "pass_line_basic_ok",
        "verb": "pass_line",
        "args": {"amount": 10},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "pass_line_zero_amount_error",
        "verb": "pass_line",
        "args": {"amount": 0},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "dont_pass_basic_ok",
        "verb": "dont_pass",
        "args": {"amount": 15},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "dont_pass_insufficient_funds",
        "verb": "dont_pass",
        "args": {"amount": 400},
        "pre_state": {"bankroll": 150.0},
        "expect": {"result": "error", "error_code": "INSUFFICIENT_FUNDS"},
    },
    {
        "label": "come_point_on_ok",
        "verb": "come",
        "args": {"amount": 20},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "rolls_before": [(3, 3)],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "come_point_off_error",
        "verb": "come",
        "args": {"amount": 15},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "TABLE_RULE_BLOCK"},
    },
    {
        "label": "dont_come_point_on_ok",
        "verb": "dont_come",
        "args": {"amount": 25},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "rolls_before": [(2, 2)],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "dont_come_point_off_error",
        "verb": "dont_come",
        "args": {"amount": 25},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "TABLE_RULE_BLOCK"},
    },
    {
        "label": "field_basic_ok",
        "verb": "field",
        "args": {"amount": 10},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "field_negative_amount_error",
        "verb": "field",
        "args": {"amount": -5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "any7_basic_ok",
        "verb": "any7",
        "args": {"amount": 5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "any7_insufficient_funds",
        "verb": "any7",
        "args": {"amount": 500},
        "pre_state": {"bankroll": 100.0},
        "expect": {"result": "error", "error_code": "INSUFFICIENT_FUNDS"},
    },
    {
        "label": "c_and_e_basic_ok",
        "verb": "c&e",
        "args": {"amount": 12},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "c_and_e_non_numeric_amount_error",
        "verb": "c&e",
        "args": {"amount": "ten"},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "horn_basic_ok",
        "verb": "horn",
        "args": {"amount": 16},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "horn_zero_amount_error",
        "verb": "horn",
        "args": {"amount": 0},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "world_basic_ok",
        "verb": "world",
        "args": {"amount": 20},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "world_insufficient_funds",
        "verb": "world",
        "args": {"amount": 600},
        "pre_state": {"bankroll": 150.0},
        "expect": {"result": "error", "error_code": "INSUFFICIENT_FUNDS"},
    },
    {
        "label": "big6_basic_ok",
        "verb": "big6",
        "args": {"amount": 18},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "big6_zero_amount_error",
        "verb": "big6",
        "args": {"amount": 0},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "big8_basic_ok",
        "verb": "big8",
        "args": {"amount": 18},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "big8_insufficient_funds",
        "verb": "big8",
        "args": {"amount": 500},
        "pre_state": {"bankroll": 120.0},
        "expect": {"result": "error", "error_code": "INSUFFICIENT_FUNDS"},
    },
    {
        "label": "place_six_ok",
        "verb": "place",
        "args": {"number": 6, "amount": 30},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "place_invalid_number_error",
        "verb": "place",
        "args": {"number": 2, "amount": 30},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "buy_four_ok",
        "verb": "buy",
        "args": {"number": 4, "amount": 25},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "buy_invalid_number_error",
        "verb": "buy",
        "args": {"number": 3, "amount": 25},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "lay_eight_ok",
        "verb": "lay",
        "args": {"number": 8, "amount": 60},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "lay_invalid_number_error",
        "verb": "lay",
        "args": {"number": 11, "amount": 40},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "put_eight_with_point_ok",
        "verb": "put",
        "args": {"number": 8, "amount": 35},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "rolls_before": [(3, 3)],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "put_point_off_error",
        "verb": "put",
        "args": {"number": 8, "amount": 35},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "TABLE_RULE_BLOCK"},
    },
    {
        "label": "hardway_six_ok",
        "verb": "hardway",
        "args": {"number": 6, "amount": 20},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "hardway_invalid_number_error",
        "verb": "hardway",
        "args": {"number": 5, "amount": 20},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "odds_pass_line_ok",
        "verb": "odds",
        "args": {"base": "pass_line", "amount": 30},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [{"verb": "pass_line", "args": {"amount": 15}}],
            "rolls_before": [(3, 3)],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "odds_missing_base_error",
        "verb": "odds",
        "args": {"base": "pass_line", "amount": 30},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "rolls_before": [(4, 2)],
        },
        "expect": {"result": "error", "error_code": "TABLE_RULE_BLOCK"},
    },
    {
        "label": "odds_invalid_base_error",
        "verb": "odds",
        "args": {"base": "foo", "amount": 30},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "two_basic_ok",
        "verb": "two",
        "args": {"amount": 5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "two_negative_amount_error",
        "verb": "two",
        "args": {"amount": -5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "three_basic_ok",
        "verb": "three",
        "args": {"amount": 5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "three_zero_amount_error",
        "verb": "three",
        "args": {"amount": 0},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "yo_basic_ok",
        "verb": "yo",
        "args": {"amount": 7},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "yo_negative_amount_error",
        "verb": "yo",
        "args": {"amount": -7},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "boxcars_basic_ok",
        "verb": "boxcars",
        "args": {"amount": 6},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "boxcars_zero_amount_error",
        "verb": "boxcars",
        "args": {"amount": 0},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "any_craps_basic_ok",
        "verb": "any_craps",
        "args": {"amount": 8},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "any_craps_negative_amount_error",
        "verb": "any_craps",
        "args": {"amount": -8},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "hop_basic_ok",
        "verb": "hop",
        "args": {"amount": 10, "result": [2, 3]},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "hop_bad_args_error",
        "verb": "hop",
        "args": {"amount": 10, "result": [2, 7]},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "fire_basic_ok",
        "verb": "fire",
        "args": {"amount": 5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "fire_zero_amount_error",
        "verb": "fire",
        "args": {"amount": 0},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "all_basic_ok",
        "verb": "all",
        "args": {"amount": 5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "all_negative_amount_error",
        "verb": "all",
        "args": {"amount": -5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "tall_basic_ok",
        "verb": "tall",
        "args": {"amount": 5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "tall_zero_amount_error",
        "verb": "tall",
        "args": {"amount": 0},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "small_basic_ok",
        "verb": "small",
        "args": {"amount": 5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "small_negative_amount_error",
        "verb": "small",
        "args": {"amount": -5},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "remove_bet_basic_ok",
        "verb": "remove_bet",
        "args": {"type": "place", "number": 6},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "place", "args": {"number": 6, "amount": 30}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "remove_bet_no_match_error",
        "verb": "remove_bet",
        "args": {"type": "place", "number": 8},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "place", "args": {"number": 6, "amount": 30}},
            ],
        },
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "reduce_bet_basic_ok",
        "verb": "reduce_bet",
        "args": {"type": "place", "number": 6, "new_amount": 18},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "place", "args": {"number": 6, "amount": 30}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "reduce_bet_increase_error",
        "verb": "reduce_bet",
        "args": {"type": "place", "number": 6, "new_amount": 60},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "place", "args": {"number": 6, "amount": 30}},
            ],
        },
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
    {
        "label": "clear_all_bets_basic_ok",
        "verb": "clear_all_bets",
        "args": {},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "pass_line", "args": {"amount": 15}},
                {"verb": "place", "args": {"number": 6, "amount": 30}},
                {"verb": "hardway", "args": {"number": 6, "amount": 10}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "clear_all_bets_noop_ok",
        "verb": "clear_all_bets",
        "args": {},
        "pre_state": {"bankroll": DEFAULT_BANKROLL},
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "clear_center_bets_basic_ok",
        "verb": "clear_center_bets",
        "args": {},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "any7", "args": {"amount": 10}},
                {"verb": "horn", "args": {"amount": 16}},
                {"verb": "world", "args": {"amount": 20}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "clear_center_bets_noop_ok",
        "verb": "clear_center_bets",
        "args": {},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "place", "args": {"number": 6, "amount": 30}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "clear_place_buy_lay_basic_ok",
        "verb": "clear_place_buy_lay",
        "args": {},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "place", "args": {"number": 6, "amount": 30}},
                {"verb": "buy", "args": {"number": 4, "amount": 25}},
                {"verb": "lay", "args": {"number": 10, "amount": 60}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "clear_place_buy_lay_noop_ok",
        "verb": "clear_place_buy_lay",
        "args": {},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "field", "args": {"amount": 10}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "clear_ats_bets_basic_ok",
        "verb": "clear_ats_bets",
        "args": {},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "all", "args": {"amount": 5}},
                {"verb": "tall", "args": {"amount": 5}},
                {"verb": "small", "args": {"amount": 5}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "clear_ats_bets_noop_ok",
        "verb": "clear_ats_bets",
        "args": {},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "pass_line", "args": {"amount": 15}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "clear_fire_bets_basic_ok",
        "verb": "clear_fire_bets",
        "args": {},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "fire", "args": {"amount": 5}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "clear_fire_bets_noop_ok",
        "verb": "clear_fire_bets",
        "args": {},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "place", "args": {"number": 6, "amount": 30}},
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "set_odds_working_basic_ok",
        "verb": "set_odds_working",
        "args": {"base": "come", "number": 5, "working": True},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "pass_line", "args": {"amount": 15}},
            ],
            "rolls_before": [(3, 3)],
            "setup_steps": [
                {"actions": [{"verb": "come", "args": {"amount": 15}}]},
                {"dice": (2, 3), "actions": []},
                {
                    "actions": [
                        {
                            "verb": "odds",
                            "args": {"base": "come", "amount": 30, "number": 5},
                        }
                    ]
                },
            ],
        },
        "expect": {"result": "ok", "error_code": None},
    },
    {
        "label": "set_odds_working_no_match_error",
        "verb": "set_odds_working",
        "args": {"base": "come", "number": 6, "working": False},
        "pre_state": {
            "bankroll": DEFAULT_BANKROLL,
            "existing_bets": [
                {"verb": "pass_line", "args": {"amount": 15}},
            ],
            "rolls_before": [(4, 4)],
            "setup_steps": [
                {"actions": [{"verb": "come", "args": {"amount": 15}}]},
                {"dice": (3, 1), "actions": []},
            ],
        },
        "expect": {"result": "error", "error_code": "BAD_ARGS"},
    },
]


DEFINED_VERBS = {scenario["verb"] for scenario in SCENARIOS}
MISSING_VERBS = api_actions.SUPPORTED_VERBS - DEFINED_VERBS
if MISSING_VERBS:  # pragma: no cover - import time guard
    missing_list = ", ".join(sorted(MISSING_VERBS))
    raise RuntimeError(f"surface scenarios missing verbs: {missing_list}")


__all__ = [
    "VERB_CATALOG",
    "SCENARIOS",
    "Scenario",
    "ScenarioExpectation",
    "ScenarioState",
    "ScenarioPreAction",
    "ScenarioSetupStep",
]
