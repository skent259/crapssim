from __future__ import annotations

from typing import Any, Dict, List

from crapssim.bet import (
    All,
    Any7,
    AnyCraps,
    Big6,
    Big8,
    Boxcars,
    Buy,
    CAndE,
    Come,
    DontCome,
    DontPass,
    Field,
    Fire,
    HardWay,
    Hop,
    Horn,
    Lay,
    Odds,
    PassLine,
    Place,
    Put,
    Small,
    Tall,
    Three,
    Two,
    World,
    Yo,
)
from crapssim.table import Table, TableSettings

from .actions import SUPPORTED_VERBS
_VERB_CAPABILITIES: Dict[str, Dict[str, Any]] = {
    "pass_line": {"args": ["amount"]},
    "dont_pass": {"args": ["amount"]},
    "come": {"args": ["amount"]},
    "dont_come": {"args": ["amount"]},
    "put": {"args": ["amount", "number"]},
    "odds": {
        "args": ["amount", "base", "number?", "working?"],
        "constraints": {"base": ["pass_line", "dont_pass", "come", "dont_come", "put"]},
    },
    "place": {
        "args": ["amount", "number"],
        "constraints": {"number": [4, 5, 6, 8, 9, 10]},
    },
    "buy": {
        "args": ["amount", "number"],
        "constraints": {"number": [4, 5, 6, 8, 9, 10]},
    },
    "lay": {
        "args": ["amount", "number"],
        "constraints": {"number": [4, 5, 6, 8, 9, 10]},
    },
    "big6": {"args": ["amount"]},
    "big8": {"args": ["amount"]},
    "field": {"args": ["amount"]},
    "any7": {"args": ["amount"]},
    "any_craps": {"args": ["amount"]},
    "two": {"args": ["amount"]},
    "three": {"args": ["amount"]},
    "yo": {"args": ["amount"]},
    "boxcars": {"args": ["amount"]},
    "c&e": {"args": ["amount"]},
    "horn": {"args": ["amount"]},
    "world": {"args": ["amount"]},
    "hardway": {
        "args": ["amount", "number"],
        "constraints": {"number": [4, 6, 8, 10]},
    },
    "hop": {
        "args": ["amount", "result"],
        "constraints": {"result": "[die1, die2] each 1-6"},
    },
    "fire": {"args": ["amount"]},
    "all": {"args": ["amount"]},
    "tall": {"args": ["amount"]},
    "small": {"args": ["amount"]},
    "remove_bet": {"args": ["type", "number?"]},
    "reduce_bet": {"args": ["type", "number?", "new_amount"]},
    "clear_all_bets": {"args": []},
    "clear_center_bets": {"args": []},
    "clear_place_buy_lay": {"args": []},
    "clear_ats_bets": {"args": []},
    "clear_fire_bets": {"args": []},
    "set_odds_working": {"args": ["base", "number", "working"]},
}


def _supported_bets() -> List[str]:
    bet_classes = (
        All,
        Any7,
        AnyCraps,
        Big6,
        Big8,
        Boxcars,
        Buy,
        CAndE,
        Come,
        DontCome,
        DontPass,
        Field,
        Fire,
        HardWay,
        Hop,
        Horn,
        Lay,
        Odds,
        PassLine,
        Place,
        Put,
        Small,
        Tall,
        Three,
        Two,
        World,
        Yo,
    )
    return sorted({cls.__name__ for cls in bet_classes})


def get_capabilities_payload() -> dict[str, Any]:
    """Return a lightweight capabilities payload for the HTTP API."""

    supported_bets = _supported_bets()

    table_defaults: TableSettings = Table().settings  # type: ignore[assignment]
    buy_vig_on_win = bool(table_defaults.get("vig_paid_on_win", False))
    vig_rounding = str(table_defaults.get("vig_rounding", "nearest_dollar"))
    vig_floor_raw = table_defaults.get("vig_floor", 0.0)
    vig_floor = float(vig_floor_raw if isinstance(vig_floor_raw, (int, float)) else 0.0)

    capabilities: dict[str, Any] = {
        "bets": {"supported": supported_bets},
        "verbs": {verb: _VERB_CAPABILITIES.get(verb, {}) for verb in SUPPORTED_VERBS},
        "table": {
            "buy_vig_on_win": buy_vig_on_win,
            "vig_rounding": vig_rounding,
            "vig_floor": vig_floor,
        },
    }
    return capabilities
