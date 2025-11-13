from __future__ import annotations

from typing import Any

from crapssim.bet import Buy, DontPass, Horn, Odds, PassLine, Place, Put, World
from crapssim.table import Table, TableSettings


def get_capabilities_payload() -> dict[str, Any]:
    """Return a lightweight capabilities payload for the HTTP API."""

    supported_bets = sorted(
        {
            cls.__name__
            for cls in (Buy, DontPass, Odds, PassLine, Place, Put, World, Horn)
        }
    )

    table_defaults: TableSettings = Table().settings  # type: ignore[assignment]
    buy_vig_on_win = bool(table_defaults.get("vig_paid_on_win", False))
    vig_rounding = str(table_defaults.get("vig_rounding", "nearest_dollar"))
    vig_floor_raw = table_defaults.get("vig_floor", 0.0)
    vig_floor = float(vig_floor_raw if isinstance(vig_floor_raw, (int, float)) else 0.0)

    capabilities: dict[str, Any] = {
        "bets": {
            "supported": supported_bets,
        },
        "table": {
            "buy_vig_on_win": buy_vig_on_win,
            "vig_rounding": vig_rounding,
            "vig_floor": vig_floor,
        },
    }
    return capabilities
