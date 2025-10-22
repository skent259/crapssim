from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ApiErrorCode(str, Enum):
    ILLEGAL_TIMING = "ILLEGAL_TIMING"
    ILLEGAL_AMOUNT = "ILLEGAL_AMOUNT"
    UNSUPPORTED_BET = "UNSUPPORTED_BET"
    LIMIT_BREACH = "LIMIT_BREACH"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    TABLE_RULE_BLOCK = "TABLE_RULE_BLOCK"
    BAD_ARGS = "BAD_ARGS"
    INTERNAL = "INTERNAL"


@dataclass
class ApiError(Exception):
    code: ApiErrorCode
    hint: str = ""
    at_state: dict | None = None

    def to_dict(self) -> dict:
        out = {"code": self.code.value, "hint": self.hint}
        if self.at_state is not None:
            out["at_state"] = self.at_state
        return out
