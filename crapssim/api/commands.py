from __future__ import annotations

from typing import Dict, Optional, Type

from crapssim.api.contract import EngineCommand, EngineResult
from crapssim.api.errors import (
    BAD_ARGUMENTS,
    BAD_INCREMENT,
    FORBIDDEN,
    ILLEGAL_BET,
    INSUFFICIENT_FUNDS,
    INTERNAL,
    NOT_FOUND,
    UNSUPPORTED,
    err,
)
from crapssim.table import Table, TableUpdate


def _resolve_bet_class(name: str) -> Optional[Type]:
    try:
        import crapssim.bet as betmod
    except Exception:
        return None
    return getattr(betmod, name, None)


def _new_bet(bet_type: str, number: int | None, amount: float):
    cls = _resolve_bet_class(bet_type)
    if cls is None:
        return None
    try:
        return cls(number, amount) if number is not None else cls(amount)
    except TypeError:
        try:
            return cls(number, amount)
        except Exception:
            return None


def _layout_signature(table: Table) -> Dict[str, float]:
    player = table.players[0] if table.players else None
    if not player:
        return {}
    sig: Dict[str, float] = {}
    for bet in player.bets:
        key = (bet.__class__.__name__, getattr(bet, "number", None), getattr(bet, "_placed_key", None))
        sig[str(key)] = float(getattr(bet, "amount", 0.0))
    return sig


def _get_first_player(table: Table):
    if not table.players:
        table.add_player()
    return table.players[0]


def _snapshot(table: Table):
    adapter = getattr(table, "adapter", None)
    if adapter is None:
        raise RuntimeError("table has no adapter attached")
    return adapter.snapshot()


def add_bet(table: Table, bet_type: str, number: int | None, amount: float) -> EngineResult:
    if amount is None or amount < 0:
        return {"success": False, "error": err(BAD_ARGUMENTS, "amount must be >= 0")}

    bet = _new_bet(bet_type, number, amount)
    if bet is None:
        return {"success": False, "error": err(ILLEGAL_BET, f"Unknown or invalid bet type '{bet_type}'")}

    player = _get_first_player(table)
    before_sig = _layout_signature(table)
    before_bankroll = player.bankroll

    try:
        player.add_bet(bet)
    except ValueError as ve:
        msg = str(ve)
        lowered = msg.lower()
        if "increment" in lowered:
            return {"success": False, "error": err(BAD_INCREMENT, msg)}
        if "fund" in lowered or "bankroll" in lowered:
            return {"success": False, "error": err(INSUFFICIENT_FUNDS, msg)}
        return {"success": False, "error": err(ILLEGAL_BET, msg)}
    except Exception as ex:  # pragma: no cover - defensive
        return {"success": False, "error": err(INTERNAL, "add_bet failed", exception=str(ex))}

    after_sig = _layout_signature(table)
    after_bankroll = player.bankroll

    if after_sig == before_sig and abs(after_bankroll - before_bankroll) < 1e-9:
        # Nothing changed: treat as illegal bet.
        return {"success": False, "error": err(ILLEGAL_BET, "bet rejected by table rules")}

    return {"success": True, "state": _snapshot(table)}


def remove_bet(table: Table, bet_type: str, number: int | None) -> EngineResult:
    player = _get_first_player(table)
    found = None
    for bet in list(player.bets):
        if bet.__class__.__name__ != bet_type:
            continue
        bet_number = getattr(bet, "number", None)
        if number is None or bet_number == number:
            found = bet
            break

    if not found:
        desc = bet_type if number is None else f"{bet_type} {number}"
        return {"success": False, "error": err(NOT_FOUND, f"No bet found: {desc}")}

    try:
        player.remove_bet(found)
    except Exception as ex:  # pragma: no cover - defensive
        return {"success": False, "error": err(INTERNAL, "remove_bet failed", exception=str(ex))}

    return {"success": True, "state": _snapshot(table)}


def press_bet(table: Table, bet_type: str, number: int | None, amount: float) -> EngineResult:
    return add_bet(table, bet_type, number, amount)


def regress_bet(table: Table, bet_type: str, number: int | None, amount: float) -> EngineResult:  # noqa: ARG001
    return {"success": False, "error": err(UNSUPPORTED, "regress not supported by vanilla core")}


def set_dice(table: Table, d1: int, d2: int) -> EngineResult:
    if not table.settings.get("debug.allow_fixed_dice", False):
        return {"success": False, "error": err(FORBIDDEN, "fixed dice disabled")}

    try:
        TableUpdate.roll(table, fixed_outcome=[int(d1), int(d2)])
        TableUpdate.update_bets(table)
    except Exception as ex:  # pragma: no cover - defensive
        return {"success": False, "error": err(INTERNAL, "set_dice failed", exception=str(ex))}

    return {"success": True, "state": _snapshot(table)}


def roll_once(table: Table) -> EngineResult:
    try:
        TableUpdate.roll(table)
        TableUpdate.update_bets(table)
    except Exception as ex:  # pragma: no cover - defensive
        return {"success": False, "error": err(INTERNAL, "roll failed", exception=str(ex))}

    return {"success": True, "state": _snapshot(table)}


def clear_all(table: Table) -> EngineResult:
    try:
        player = _get_first_player(table)
        for bet in list(player.bets):
            player.remove_bet(bet)
    except Exception as ex:  # pragma: no cover - defensive
        return {"success": False, "error": err(INTERNAL, "clear_all failed", exception=str(ex))}

    return {"success": True, "state": _snapshot(table)}
