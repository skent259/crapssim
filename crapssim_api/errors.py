import json
from enum import Enum
from typing import Any, Dict, Optional

try:
    from fastapi import Request
except Exception:  # pragma: no cover

    class Request:  # minimal stub
        pass


try:
    from fastapi.responses import JSONResponse
except Exception:  # pragma: no cover

    class JSONResponse:  # minimal stub
        def __init__(self, *, status_code: int, content: Dict[str, Any]):
            self.status_code = status_code
            self.content = content
            self.body = json.dumps(content).encode()


class ApiErrorCode(str, Enum):
    BAD_ARGS = "BAD_ARGS"
    TABLE_RULE_BLOCK = "TABLE_RULE_BLOCK"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    UNSUPPORTED_BET = "UNSUPPORTED_BET"
    ILLEGAL_TIMING = "ILLEGAL_TIMING"
    ILLEGAL_AMOUNT = "ILLEGAL_AMOUNT"
    LIMIT_BREACH = "LIMIT_BREACH"
    INTERNAL = "INTERNAL"


class ApiError(Exception):
    def __init__(
        self,
        code: ApiErrorCode | str,
        hint: str,
        at_state: Optional[Dict[str, Any]] = None,
        *,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(hint)
        if isinstance(code, str) and code in ApiErrorCode._value2member_map_:
            self.code = ApiErrorCode(code)
        else:
            self.code = code
        self.hint = hint
        self.context = context or {}
        self.at_state = at_state or {
            "session_id": None,
            "hand_id": None,
            "roll_seq": None,
        }


def bad_args(hint: str) -> ApiError:
    return ApiError(ApiErrorCode.BAD_ARGS, hint)


def table_rule_block(hint: str) -> ApiError:
    return ApiError(ApiErrorCode.TABLE_RULE_BLOCK, hint)


def unsupported_bet(hint: str) -> ApiError:
    return ApiError(ApiErrorCode.UNSUPPORTED_BET, hint)


async def api_error_handler(request: Request, exc: ApiError):
    status_map = {
        ApiErrorCode.BAD_ARGS.value: 400,
        ApiErrorCode.TABLE_RULE_BLOCK.value: 409,
        ApiErrorCode.INSUFFICIENT_FUNDS.value: 409,
        ApiErrorCode.ILLEGAL_TIMING.value: 409,
        ApiErrorCode.ILLEGAL_AMOUNT.value: 422,
        ApiErrorCode.LIMIT_BREACH.value: 422,
        ApiErrorCode.UNSUPPORTED_BET.value: 422,
        ApiErrorCode.INTERNAL.value: 500,
    }
    code_value = exc.code.value if isinstance(exc.code, ApiErrorCode) else str(exc.code)
    status_code = status_map.get(code_value, 500)
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code_value,
            "hint": exc.hint,
            "at_state": exc.at_state,
            "context": exc.context,
        },
    )
