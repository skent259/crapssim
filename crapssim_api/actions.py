from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from .errors import ApiError, ApiErrorCode


def stub_handler(args: Dict[str, Any]) -> Dict[str, Any]:
    # No side effects: deterministic, verb-agnostic no-op
    return {
        "applied": True,
        "bankroll_delta": 0.0,
        "note": "stub: action accepted, no-op",
    }


VerbRegistry: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "pass_line": stub_handler,
    "dont_pass": stub_handler,
    "come": stub_handler,
    "dont_come": stub_handler,
    "place": stub_handler,
    "buy": stub_handler,
    "lay": stub_handler,
    "put": stub_handler,
    "hardway": stub_handler,
    "field": stub_handler,
    "horn": stub_handler,
    "world": stub_handler,
}


class TableView:
    def __init__(self, puck: str = "OFF", point: Optional[int] = None):
        # puck: "OFF" | "ON" | "MOVING" (adapter sentinel during resolve)
        self.puck = puck
        self.point = point


def check_timing(verb: str, table: TableView) -> None:
    if table.puck == "MOVING":
        raise ApiError(ApiErrorCode.ILLEGAL_TIMING, f"{verb} disallowed while dice are resolving")
    # Line bets only on come-out
    if verb in ("pass_line", "dont_pass") and table.puck == "ON":
        raise ApiError(ApiErrorCode.ILLEGAL_TIMING, f"{verb} only legal on come-out (puck OFF)")
    # Box bets only after point is set
    if verb in ("place", "buy", "lay", "put") and table.puck == "OFF":
        raise ApiError(ApiErrorCode.ILLEGAL_TIMING, f"{verb} only legal after point established (puck ON)")


def check_amount(verb: str, args: Dict[str, Any], place_increments: Dict[str, int]) -> None:
    amt = args.get("amount")
    if not isinstance(amt, (int, float)) or amt <= 0:
        raise ApiError(ApiErrorCode.ILLEGAL_AMOUNT, "bet amount must be a positive number")
    # For box-addressed verbs, validate increment by box number (string keys in caps)
    if verb in ("place", "buy", "lay", "put"):
        box = str(args.get("box"))
        inc = place_increments.get(box, None)
        if inc is None:
            # If box missing or unsupported, treat as bad args amount shape
            raise ApiError(ApiErrorCode.ILLEGAL_AMOUNT, f"missing/unsupported box '{box}' for {verb}")
        # Amount must be multiple of increment
        # Use integer math to avoid float modulo surprises
        if int(amt) != amt:
            # For simplicity in P3·C2, require whole-dollar chips
            raise ApiError(ApiErrorCode.ILLEGAL_AMOUNT, "amount must be whole dollars at this table")
        if int(amt) % int(inc) != 0:
            raise ApiError(
                ApiErrorCode.ILLEGAL_AMOUNT,
                f"amount ${int(amt)} not in valid increment of ${int(inc)} for box {box}",
            )


def check_limits(verb: str, args: Dict[str, Any], odds_policy: str, odds_max_x: int) -> None:
    amt = args.get("amount", 0)
    # Simple table cap placeholder to avoid outrageous inputs
    if amt and amt > 20000:
        raise ApiError(ApiErrorCode.LIMIT_BREACH, f"{verb} exceeds table cap")
    # Odds-related checks will land in P3·C3 when odds verbs are implemented.
    # Kept here for structure; no-op for now.
