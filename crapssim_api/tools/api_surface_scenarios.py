"""Scenario definitions for CrapsSim API surface stress testing."""
from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class ScenarioState(TypedDict, total=False):
    rolls_before: List[tuple[int, int]]
    existing_bets: List[Dict[str, Any]]
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


VERB_CATALOG: Dict[str, Dict[str, Any]] = {
    "pass_line": {"engine_bet": "PassLine"},
    "dont_pass": {"engine_bet": "DontPass"},
    "come": {"engine_bet": "Come"},
    "dont_come": {"engine_bet": "DontCome"},
    "field": {"engine_bet": "Field"},
    "any7": {"engine_bet": "Any7"},
    "c&e": {"engine_bet": "CAndE"},
    "horn": {"engine_bet": "Horn"},
    "world": {"engine_bet": "World"},
    "big6": {"engine_bet": "Big6"},
    "big8": {"engine_bet": "Big8"},
    "place": {"engine_bet": "Place"},
    "buy": {"engine_bet": "Buy"},
    "lay": {"engine_bet": "Lay"},
    "put": {"engine_bet": "Put"},
    "hardway": {"engine_bet": "HardWay"},
    "odds": {"engine_bet": "Odds"},
}


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
]


__all__ = ["VERB_CATALOG", "SCENARIOS", "Scenario", "ScenarioExpectation", "ScenarioState"]
