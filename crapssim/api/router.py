from __future__ import annotations

from typing import Any

from crapssim.api import commands
from crapssim.api.contract import EngineCommand, EngineResult
from crapssim.api.errors import BAD_ARGUMENTS, INTERNAL, err
from crapssim.table import Table


def _coerce_amount(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError("amount must be numeric")


def route(adapter: Any, table: Table, cmd: EngineCommand) -> EngineResult:
    verb = cmd.get("verb")
    if verb is None and "name" in cmd:
        verb = cmd.get("name")

    try:
        if verb == "add_bet":
            return commands.add_bet(table, cmd.get("type", ""), cmd.get("number"), _coerce_amount(cmd.get("amount", 0.0)))
        if verb == "remove_bet":
            return commands.remove_bet(table, cmd.get("type", ""), cmd.get("number"))
        if verb == "press_bet":
            return commands.press_bet(table, cmd.get("type", ""), cmd.get("number"), _coerce_amount(cmd.get("amount", 0.0)))
        if verb == "regress_bet":
            return commands.regress_bet(table, cmd.get("type", ""), cmd.get("number"), _coerce_amount(cmd.get("amount", 0.0)))
        if verb == "set_dice":
            d1, d2 = cmd.get("d1"), cmd.get("d2")
            if d1 is None or d2 is None:
                return {"success": False, "error": err(BAD_ARGUMENTS, "set_dice requires d1 and d2")}
            return commands.set_dice(table, int(d1), int(d2))
        if verb == "roll":
            return commands.roll_once(table)
        if verb == "clear_all":
            return commands.clear_all(table)
        return {"success": False, "error": err(BAD_ARGUMENTS, f"Unknown verb '{verb}'")}
    except ValueError as ve:
        if "amount must be numeric" in str(ve):
            return {"success": False, "error": err(BAD_ARGUMENTS, str(ve))}
        return {"success": False, "error": err(INTERNAL, "router failure", exception=str(ve))}
    except Exception as ex:  # pragma: no cover - defensive
        return {"success": False, "error": err(INTERNAL, "router failure", exception=str(ex))}
