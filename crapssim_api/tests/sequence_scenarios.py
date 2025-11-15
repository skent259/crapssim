"""Sequence scenario definitions for CrapsSim API multi-step testing."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Tuple, TypedDict

NormalizedBet = TypedDict(
    "NormalizedBet",
    {
        "type": str,
        "number": Optional[int],
        "amount": float,
    },
)


class SequenceAction(TypedDict):
    """Single action within a sequence step."""

    verb: str
    args: Dict[str, Any]


class SequenceStep(TypedDict, total=False):
    """Single step consisting of optional roll and actions."""

    label: str
    dice: Tuple[int, int] | None
    actions: List[SequenceAction]


class SequenceExpectation(TypedDict, total=False):
    """Expected final state for a sequence."""

    final_bankroll: Optional[float]
    expected_result: Literal["ok", "error"]
    error_code: Optional[str]
    bets_after: List[NormalizedBet]


class SequenceScenario(TypedDict, total=False):
    """Scenario describing a full multi-step sequence."""

    label: str
    initial_bankroll: float
    initial_bets: List[SequenceAction]
    steps: List[SequenceStep]
    expect: SequenceExpectation
    seed_offset: int


DEFAULT_BANKROLL = 250.0


SEQUENCE_SCENARIOS: List[SequenceScenario] = [
    {
        "label": "press_6_8_then_buy_4_sequence",
        "initial_bankroll": 250.0,
        "initial_bets": [
            {"verb": "pass_line", "args": {"amount": 15}},
        ],
        "steps": [
            {"label": "comeout_point_four", "dice": (2, 2), "actions": []},
            {
                "label": "hit_six_and_press",
                "dice": (4, 2),
                "actions": [
                    {"verb": "place", "args": {"amount": 30, "number": 6}},
                    {"verb": "place", "args": {"amount": 30, "number": 8}},
                ],
            },
            {
                "label": "buy_four",
                "dice": None,
                "actions": [
                    {"verb": "buy", "args": {"amount": 25, "number": 4}},
                ],
            },
            {"label": "resolve_place_eight", "dice": (6, 2), "actions": []},
            {"label": "seven_out", "dice": (3, 4), "actions": []},
        ],
        "expect": {
            "final_bankroll": 214.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
    {
        "label": "pass_line_with_odds_hit_sequence",
        "initial_bankroll": DEFAULT_BANKROLL,
        "initial_bets": [
            {"verb": "pass_line", "args": {"amount": 15}},
        ],
        "steps": [
            {"label": "comeout_point_five", "dice": (4, 1), "actions": []},
            {
                "label": "add_pass_odds",
                "dice": None,
                "actions": [
                    {"verb": "odds", "args": {"base": "pass_line", "amount": 30}},
                ],
            },
            {"label": "point_hit", "dice": (3, 2), "actions": []},
        ],
        "expect": {
            "final_bankroll": 310.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
    {
        "label": "place_chain_with_seven_out",
        "initial_bankroll": DEFAULT_BANKROLL,
        "initial_bets": [
            {"verb": "pass_line", "args": {"amount": 10}},
        ],
        "steps": [
            {"label": "comeout_point_eight", "dice": (6, 2), "actions": []},
            {
                "label": "place_numbers",
                "dice": None,
                "actions": [
                    {"verb": "place", "args": {"amount": 18, "number": 6}},
                    {"verb": "place", "args": {"amount": 15, "number": 5}},
                ],
            },
            {"label": "hit_place_six", "dice": (5, 1), "actions": []},
            {"label": "seven_out", "dice": (3, 4), "actions": []},
        ],
        "expect": {
            "final_bankroll": 246.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
    {
        "label": "mixed_success_and_failure_actions",
        "initial_bankroll": 80.0,
        "initial_bets": [
            {"verb": "pass_line", "args": {"amount": 15}},
        ],
        "steps": [
            {"label": "comeout_point_six", "dice": (4, 2), "actions": []},
            {
                "label": "place_six_success",
                "dice": None,
                "actions": [
                    {"verb": "place", "args": {"amount": 30, "number": 6}},
                ],
            },
            {
                "label": "place_eight_insufficient",
                "dice": None,
                "actions": [
                    {"verb": "place", "args": {"amount": 60, "number": 8}},
                ],
            },
            {"label": "point_hit", "dice": (5, 1), "actions": []},
        ],
        "expect": {
            "final_bankroll": 130.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
    {
        "label": "hardway_hit_break_rebet_sequence",
        "initial_bankroll": 200.0,
        "initial_bets": [],
        "steps": [
            {
                "label": "establish_hardways",
                "dice": None,
                "actions": [
                    {"verb": "hardway", "args": {"amount": 10, "number": 6}},
                    {"verb": "hardway", "args": {"amount": 10, "number": 8}},
                ],
            },
            {"label": "hard_six_hits", "dice": (3, 3), "actions": []},
            {
                "label": "rebet_hard_six",
                "dice": None,
                "actions": [
                    {"verb": "hardway", "args": {"amount": 10, "number": 6}},
                ],
            },
            {"label": "easy_six_breaks", "dice": (4, 2), "actions": []},
            {"label": "hard_eight_hits", "dice": (4, 4), "actions": []},
        ],
        "expect": {
            "final_bankroll": 370.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
    {
        "label": "field_and_props_chain",
        "initial_bankroll": 150.0,
        "initial_bets": [],
        "steps": [
            {
                "label": "enter_field_and_any7",
                "dice": None,
                "actions": [
                    {"verb": "field", "args": {"amount": 25}},
                    {"verb": "any7", "args": {"amount": 5}},
                ],
            },
            {"label": "seven_roll", "dice": (2, 5), "actions": []},
            {
                "label": "horn_and_world",
                "dice": None,
                "actions": [
                    {"verb": "horn", "args": {"amount": 16}},
                    {"verb": "world", "args": {"amount": 5}},
                ],
            },
            {"label": "horn_three", "dice": (1, 2), "actions": []},
        ],
        "expect": {
            "final_bankroll": 204.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
    {
        "label": "dont_pass_with_odds_win",
        "initial_bankroll": DEFAULT_BANKROLL,
        "initial_bets": [
            {"verb": "dont_pass", "args": {"amount": 20}},
        ],
        "steps": [
            {"label": "comeout_point_ten", "dice": (6, 4), "actions": []},
            {
                "label": "add_dont_pass_odds",
                "dice": None,
                "actions": [
                    {"verb": "odds", "args": {"base": "dont_pass", "amount": 40}},
                ],
            },
            {"label": "seven_out", "dice": (3, 4), "actions": []},
        ],
        "expect": {
            "final_bankroll": 290.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
    {
        "label": "come_and_odds_hit_sequence",
        "initial_bankroll": DEFAULT_BANKROLL,
        "initial_bets": [
            {"verb": "pass_line", "args": {"amount": 10}},
        ],
        "steps": [
            {"label": "comeout_point_nine", "dice": (5, 4), "actions": []},
            {
                "label": "come_bet_moves",
                "dice": None,
                "actions": [
                    {"verb": "come", "args": {"amount": 15}},
                ],
            },
            {"label": "come_bet_travels", "dice": (3, 2), "actions": []},
            {
                "label": "add_odds_to_come",
                "dice": None,
                "actions": [
                    {
                        "verb": "odds",
                        "args": {"base": "come", "amount": 30, "number": 5},
                    },
                ],
            },
            {"label": "resolve_come_number", "dice": (4, 1), "actions": []},
            {"label": "seven_out", "dice": (3, 4), "actions": []},
        ],
        "expect": {
            "final_bankroll": 300.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
    {
        "label": "dont_come_sequence_with_error",
        "initial_bankroll": 180.0,
        "initial_bets": [
            {"verb": "dont_pass", "args": {"amount": 15}},
        ],
        "steps": [
            {"label": "comeout_point_nine", "dice": (6, 3), "actions": []},
            {
                "label": "dont_come_bet",
                "dice": None,
                "actions": [
                    {"verb": "dont_come", "args": {"amount": 20}},
                ],
            },
            {"label": "dont_come_travel", "dice": (2, 2), "actions": []},
            {
                "label": "invalid_odds_attempt",
                "dice": None,
                "actions": [
                    {"verb": "odds", "args": {"base": "dont_come", "amount": 25}},
                ],
            },
            {"label": "seven_out", "dice": (3, 4), "actions": []},
        ],
        "expect": {
            "final_bankroll": 215.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
    {
        "label": "odds_without_base_error",
        "initial_bankroll": DEFAULT_BANKROLL,
        "initial_bets": [],
        "steps": [
            {
                "label": "odds_without_passline",
                "dice": None,
                "actions": [
                    {"verb": "odds", "args": {"base": "pass_line", "amount": 25}},
                ],
            },
        ],
        "expect": {
            "final_bankroll": 250.0,
            "expected_result": "error",
            "error_code": "TABLE_RULE_BLOCK",
            "bets_after": [],
        },
    },
    {
        "label": "prop_bets_resolution_cycle",
        "initial_bankroll": 360.0,
        "initial_bets": [
            {"verb": "pass_line", "args": {"amount": 15}},
        ],
        "steps": [
            {
                "label": "load_prop_suite",
                "dice": None,
                "actions": [
                    {"verb": "fire", "args": {"amount": 5}},
                    {"verb": "all", "args": {"amount": 5}},
                    {"verb": "tall", "args": {"amount": 5}},
                    {"verb": "small", "args": {"amount": 5}},
                ],
            },
            {"label": "comeout_point_six", "dice": (3, 3), "actions": []},
            {
                "label": "enter_hop_and_world",
                "dice": None,
                "actions": [
                    {"verb": "world", "args": {"amount": 10}},
                    {"verb": "horn", "args": {"amount": 16}},
                    {"verb": "hop", "args": {"amount": 10, "result": [2, 4]}},
                ],
            },
            {"label": "point_made_with_hop", "dice": (2, 4), "actions": []},
            {
                "label": "re_establish_pass_line",
                "dice": None,
                "actions": [
                    {"verb": "pass_line", "args": {"amount": 15}},
                ],
            },
            {"label": "new_point_five", "dice": (3, 2), "actions": []},
            {"label": "seven_out_clears_props", "dice": (4, 3), "actions": []},
        ],
        "expect": {
            "final_bankroll": 464.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
    {
        "label": "bet_management_cycle_sequence",
        "initial_bankroll": 320.0,
        "initial_bets": [
            {"verb": "pass_line", "args": {"amount": 15}},
            {"verb": "place", "args": {"amount": 30, "number": 6}},
            {"verb": "place", "args": {"amount": 30, "number": 8}},
        ],
        "steps": [
            {"label": "comeout_point_six", "dice": (4, 2), "actions": []},
            {
                "label": "establish_odds_and_come",
                "dice": None,
                "actions": [
                    {"verb": "odds", "args": {"base": "pass_line", "amount": 30}},
                    {"verb": "come", "args": {"amount": 15}},
                ],
            },
            {"label": "come_moves_to_five", "dice": (3, 2), "actions": []},
            {
                "label": "add_come_odds_and_toggle_off",
                "dice": None,
                "actions": [
                    {
                        "verb": "odds",
                        "args": {"base": "come", "amount": 30, "number": 5},
                    },
                    {
                        "verb": "set_odds_working",
                        "args": {"base": "come", "number": 5, "working": False},
                    },
                ],
            },
            {
                "label": "reduce_and_remove_place",
                "dice": None,
                "actions": [
                    {
                        "verb": "reduce_bet",
                        "args": {"type": "place", "number": 8, "new_amount": 18},
                    },
                    {"verb": "remove_bet", "args": {"type": "place", "number": 8}},
                ],
            },
            {"label": "hit_point_six", "dice": (5, 1), "actions": []},
            {
                "label": "toggle_come_odds_on",
                "dice": None,
                "actions": [
                    {
                        "verb": "set_odds_working",
                        "args": {"base": "come", "number": 5, "working": True},
                    },
                ],
            },
            {"label": "seven_out_resolves", "dice": (4, 3), "actions": []},
            {
                "label": "rebuild_single_place",
                "dice": None,
                "actions": [
                    {"verb": "place", "args": {"amount": 18, "number": 8}},
                ],
            },
            {
                "label": "clear_remaining_layout",
                "dice": None,
                "actions": [
                    {"verb": "clear_all_bets", "args": {}},
                ],
            },
        ],
        "expect": {
            "final_bankroll": 361.0,
            "expected_result": "ok",
            "error_code": None,
            "bets_after": [],
        },
    },
]
