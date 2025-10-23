from enum import Enum
from typing import Any, Dict, Optional

from fastapi import Request
from fastapi.responses import JSONResponse


class ApiErrorCode(str, Enum):
    BAD_ARGS = "BAD_ARGS"
    TABLE_RULE_BLOCK = "TABLE_RULE_BLOCK"
    UNSUPPORTED_BET = "UNSUPPORTED_BET"
    INTERNAL = "INTERNAL"


class ApiError(Exception):
    def __init__(self, code: ApiErrorCode, hint: str, at_state: Optional[Dict[str, Any]] = None):
        super().__init__(hint)
        self.code = code
        self.hint = hint
        self.at_state = at_state or {"session_id": None, "hand_id": None, "roll_seq": None}


def bad_args(hint: str) -> ApiError:
    return ApiError(ApiErrorCode.BAD_ARGS, hint)


def table_rule_block(hint: str) -> ApiError:
    return ApiError(ApiErrorCode.TABLE_RULE_BLOCK, hint)


def unsupported_bet(hint: str) -> ApiError:
    return ApiError(ApiErrorCode.UNSUPPORTED_BET, hint)


async def api_error_handler(request: Request, exc: ApiError):
    status_map = {
        ApiErrorCode.BAD_ARGS: 400,
        ApiErrorCode.TABLE_RULE_BLOCK: 409,
        ApiErrorCode.UNSUPPORTED_BET: 422,
        ApiErrorCode.INTERNAL: 500,
    }
    return JSONResponse(
        status_code=status_map.get(exc.code, 500),
        content={"code": exc.code, "hint": exc.hint, "at_state": exc.at_state},
    )
