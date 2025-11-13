from __future__ import annotations

from typing import Any, Dict

ILLEGAL_BET = "ILLEGAL_BET"
BAD_INCREMENT = "BAD_INCREMENT"
INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
NOT_FOUND = "NOT_FOUND"
FORBIDDEN = "FORBIDDEN"
UNSUPPORTED = "UNSUPPORTED"
BAD_ARGUMENTS = "BAD_ARGUMENTS"
INTERNAL = "INTERNAL"


def err(code: str, reason: str, **details: Any) -> Dict[str, Any]:
    e = {"code": code, "reason": reason}
    if details:
        e["details"] = details
    return e
