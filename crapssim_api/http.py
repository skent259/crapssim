from __future__ import annotations

import json
import uuid

# ruff: noqa: E402
from typing import Any, Dict, List, Optional, Tuple

try:
    from fastapi import APIRouter, Body, FastAPI, HTTPException
    from fastapi.responses import JSONResponse, Response as FastAPIResponse

    HAVE_FASTAPI = True
except Exception:  # pragma: no cover - environment without fastapi
    HAVE_FASTAPI = False
    APIRouter = None  # type: ignore[assignment]
    FastAPI = None  # type: ignore[assignment]

    class HTTPException(Exception):  # type: ignore[override]
        def __init__(self, status_code: int, detail: str):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    def Body(default: Any = ..., **_: Any) -> Any:  # type: ignore[override]
        return default

    class Response:  # minimal stub
        def __init__(self, content: str, media_type: str):
            self.body = content.encode()
            self.media_type = media_type

    class JSONResponse(Response):  # minimal stub
        def __init__(self, content: Any, media_type: str = "application/json"):
            super().__init__(json.dumps(content), media_type)


if HAVE_FASTAPI:
    Response = FastAPIResponse  # type: ignore[assignment]


def _ensure_fastapi() -> None:
    if not HAVE_FASTAPI:
        raise RuntimeError(
            "FastAPI is not installed. Install the optional extras with "
            '`pip install "crapssim[api]"` to enable the HTTP API.'
        )


try:
    from pydantic import BaseModel, Field, ValidationInfo, field_validator
except ImportError:  # pragma: no cover - pydantic optional or v1 fallback
    try:
        from pydantic import BaseModel, Field, validator

        ValidationInfo = Dict[str, Any]  # type: ignore[assignment]

        def field_validator(field_name: str, *field_args: Any, **field_kwargs: Any):  # type: ignore[override]
            def decorator(func):
                return validator(field_name, *field_args, **field_kwargs)(func)

            return decorator

    except ImportError:  # pragma: no cover - no pydantic available

        class BaseModel:  # type: ignore[override]
            def __init__(self, **data: Any) -> None:
                for key, value in data.items():
                    setattr(self, key, value)

        def Field(default: Any = ..., **kwargs: Any) -> Any:  # type: ignore[override]
            return default

        ValidationInfo = Dict[str, Any]  # type: ignore[assignment]

        def field_validator(field_name: str, *field_args: Any, **field_kwargs: Any):  # type: ignore[override]
            def decorator(func):
                return func

            return decorator


class RollRequest(BaseModel):
    session_id: str
    dice: list[int] | None = None

    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("session_id must be a non-empty string")
        return v

    @field_validator("dice")
    @classmethod
    def validate_dice(cls, v: list[int] | None):
        if v is None:
            return v
        if not isinstance(v, list) or len(v) != 2:
            raise ValueError("dice must be [d1,d2]")
        if not all(isinstance(d, int) and 1 <= d <= 6 for d in v):
            raise ValueError("each die must be 1–6")
        return v


from .capabilities import get_capabilities_payload
from .errors import ApiError, ApiErrorCode, api_error_handler, bad_args, unsupported_bet
from .events import (
    build_event,
    build_hand_ended,
    build_point_made,
    build_point_set,
    build_seven_out,
)
from .session_store import SESSION_STORE
from .session import Session
from .types import (
    Capabilities,
    ReplayResult,
    SessionMetricsResponse,
    SessionStateResponse,
    SessionTape,
    SessionTapeMetadata,
    SessionTapeStep,
    StartSessionRequest,
    StartSessionResponse,
    TableSpec,
)
from .verbs import (
    SUPPORTED_VERBS,
    apply_bet_management,
    build_bet,
    compute_required_cash,
    describe_vig,
    is_bet_management_verb,
    is_bet_placement_verb,
)
from .version import CAPABILITIES_SCHEMA_VERSION, ENGINE_API_VERSION, get_identity

if HAVE_FASTAPI:
    router = APIRouter()
else:  # pragma: no cover - FastAPI optional
    router = None

ENGINE_VERSION_STRING = ENGINE_API_VERSION
API_VERSION_STRING = ENGINE_API_VERSION
DETERMINISM_CONTRACT_VERSION = "v1.0"
STATE_SCHEMA_VERSION = "1.0"
METRICS_SCHEMA_VERSION = "1.0"

DEFAULT_VIG_SETTINGS: Dict[str, Any] = {
    "vig_rounding": "nearest_dollar",
    "vig_floor": 0.0,
    "vig_paid_on_win": False,
}


BASE_CAPABILITIES: Capabilities = {
    "schema_version": CAPABILITIES_SCHEMA_VERSION,
    "bets": {
        "line": ["pass_line", "dont_pass", "come", "dont_come", "odds", "put"],
        "place": ["place_4", "place_5", "place_6", "place_8", "place_9", "place_10"],
        "buy": ["buy_4", "buy_5", "buy_6", "buy_8", "buy_9", "buy_10"],
        "lay": ["lay_4", "lay_5", "lay_6", "lay_8", "lay_9", "lay_10"],
        "big": ["big6", "big8"],
        "field": {"pays": {"2": "double", "12": "double"}},
        "hardways": {"break_on": "seven_or_easy"},
        "props": [
            "any7",
            "c&e",
            "horn",
            "world",
            "two",
            "three",
            "yo",
            "boxcars",
            "any_craps",
            "hop",
        ],
        "fire": ["fire"],
        "small_tall_all": ["small", "tall", "all"],
    },
    "increments": {
        "place": {"4": 5, "5": 5, "6": 6, "8": 6, "9": 5, "10": 5},
    },
    "odds_limits": {"policy": "3-4-5", "max_x": 20},
    "vig": {
        "buy": {
            "rate_bips": 500,
            "rounding": "nearest_dollar",
            "floor": 0.0,
            "paid_on_win": False,
        },
        "lay": {
            "rate_bips": 500,
            "rounding": "nearest_dollar",
            "floor": 0.0,
            "paid_on_win": False,
        },
    },
    "working_flags": {"comeout_odds_work": False, "place_work_comeout": False},
    "why_unsupported": {},
    "bet_management": [
        "remove_bet",
        "reduce_bet",
        "clear_all_bets",
        "clear_center_bets",
        "clear_place_buy_lay",
        "clear_ats_bets",
        "clear_fire_bets",
        "set_odds_working",
    ],
}


def _resolve_vig_settings(spec: TableSpec) -> Dict[str, Any]:
    settings: Dict[str, Any] = dict(DEFAULT_VIG_SETTINGS)
    vig_spec = spec.get("vig", {})
    candidate: Dict[str, Any] | None = None
    if isinstance(vig_spec, dict):
        if "buy" in vig_spec and isinstance(vig_spec["buy"], dict):
            candidate = vig_spec["buy"]
        elif "lay" in vig_spec and isinstance(vig_spec["lay"], dict):
            candidate = vig_spec["lay"]
        else:
            candidate = vig_spec
    if candidate:
        rounding = candidate.get("rounding")
        if isinstance(rounding, str):
            settings["vig_rounding"] = rounding
        floor = candidate.get("floor")
        if isinstance(floor, (int, float)):
            settings["vig_floor"] = float(floor)
        paid = candidate.get("paid_on_win")
        if isinstance(paid, bool):
            settings["vig_paid_on_win"] = paid
    return settings


def _apply_vig_settings_to_caps(
    caps: Dict[str, Any], vig_settings: Dict[str, Any]
) -> Dict[str, Any]:
    if "vig" not in caps:
        return caps
    vig_caps = {}
    for bet_name, rule in caps["vig"].items():
        if isinstance(rule, dict):
            updated = dict(rule)
            updated["rounding"] = vig_settings["vig_rounding"]
            updated["floor"] = vig_settings["vig_floor"]
            updated["paid_on_win"] = vig_settings["vig_paid_on_win"]
            vig_caps[bet_name] = updated
    caps = dict(caps)
    caps["vig"] = vig_caps
    return caps


def _json_dumps(value: Any) -> str:
    return json.dumps(value, separators=(", ", ": "))


def _json_response(payload: Any) -> Response:
    return Response(content=_json_dumps(payload), media_type="application/json")


def _get_session_or_404(session_id: str) -> Dict[str, Any]:
    session = getattr(SESSION_STORE, "_s", {}).get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Unknown session_id")
    return session


def _normalize_action_payload(
    action_payload: Dict[str, Any], session_id: str
) -> Dict[str, Any]:
    if not isinstance(action_payload, dict):
        raise bad_args("each action must be a mapping")

    payload = dict(action_payload)
    payload.setdefault("session_id", session_id)
    payload.setdefault("args", {})

    if "args" not in action_payload:
        args = {
            k: v for k, v in payload.items() if k not in ("verb", "session_id", "args")
        }
        payload["args"] = args

    return payload


def _record_tape_step(
    session_data: Dict[str, Any], dice: Tuple[int, int], actions: List[dict]
) -> None:
    steps: List[SessionTapeStep] = list(session_data.get("tape_steps", []))
    step_index = len(steps)
    steps.append({"step_index": step_index, "dice": dice, "actions": list(actions)})
    session_data["tape_steps"] = steps


def _normalize_state_for_tape(state: dict, session_id: Optional[str] = None) -> dict:
    normalized = dict(state or {})
    if session_id is not None:
        normalized["session_id"] = session_id
    events = []
    for ev in normalized.get("events", []):
        if isinstance(ev, dict):
            ev_copy = {k: v for k, v in ev.items() if k not in ("id", "ts")}
            events.append(ev_copy)
    normalized["events"] = events
    return normalized


def _capabilities_dict() -> Dict[str, Any]:
    resp = get_capabilities()
    return json.loads(resp.body.decode())


def create_app(*, strict: bool = False):
    if not HAVE_FASTAPI or router is None:  # pragma: no cover - FastAPI optional
        raise RuntimeError(
            "FastAPI is not installed. Install CrapsSim with the API extra: "
            "pip install crapssim[api]"
        )

    app = FastAPI(title="CrapsSim API")
    app.add_exception_handler(ApiError, api_error_handler)
    app.include_router(router)
    return app


def health() -> dict[str, str]:
    return {"status": "ok"}


def healthz() -> Response:
    identity = get_identity()
    payload = {"status": "ok", **identity}
    return _json_response(payload)


def get_capabilities() -> Response:
    payload: Dict[str, Any] = {
        "engine_api": {"version": ENGINE_API_VERSION},
        "capabilities": BASE_CAPABILITIES,
        "summary": get_capabilities_payload(),
    }
    return _json_response(payload)


def _http_capabilities() -> Dict[str, Any]:
    return get_capabilities_payload()


if router is not None:  # pragma: no cover - FastAPI optional
    router.get("/health")(health)
    router.get("/healthz")(healthz)
    router.get("/capabilities")(_http_capabilities)


def _coerce_start_session_payload(
    payload: StartSessionRequest | BaseModel | Dict[str, Any],
) -> Dict[str, Any]:
    """Return a plain mapping for the start session request."""

    if isinstance(payload, BaseModel):  # pragma: no branch - pydantic model
        if hasattr(payload, "model_dump"):
            data = payload.model_dump()  # type: ignore[assignment]
        elif hasattr(payload, "dict"):
            data = payload.dict()  # type: ignore[assignment]
        else:  # pragma: no cover - defensive fallback
            data = dict(payload.__dict__)
        return dict(data)

    if isinstance(payload, dict):
        return dict(payload)

    raise bad_args("start_session payload must be a mapping")


def _coerce_roll_payload(
    payload: RollRequest | BaseModel | Dict[str, Any] | None,
) -> Dict[str, Any]:
    if payload is None:
        raise bad_args("roll payload must be provided")

    if isinstance(payload, BaseModel):  # pragma: no branch - pydantic model
        if hasattr(payload, "model_dump"):
            data = payload.model_dump()  # type: ignore[assignment]
        elif hasattr(payload, "dict"):
            data = payload.dict()  # type: ignore[assignment]
        else:  # pragma: no cover - defensive fallback
            data = dict(payload.__dict__)
        return dict(data)

    if isinstance(payload, dict):
        return dict(payload)

    raise bad_args("roll payload must be a mapping")


class StartSessionResult(dict):
    """Dictionary-like result that retains a JSON encoded body for legacy callers."""

    body: bytes

    def __init__(self, payload: StartSessionResponse):
        super().__init__(payload)
        self.body = _json_dumps(payload).encode()


def start_session(
    payload: StartSessionRequest | BaseModel | Dict[str, Any],
) -> StartSessionResult:
    """Core callable used by tests and the FastAPI layer."""

    request_data = _coerce_start_session_payload(payload)
    spec_value = request_data.get("spec", request_data.get("table_spec", {}))
    if not isinstance(spec_value, dict):
        raise bad_args("spec must be a mapping")
    spec: TableSpec = spec_value

    seed_value = request_data.get("seed", 0)
    if isinstance(seed_value, bool) or not isinstance(seed_value, int):
        raise bad_args("seed must be int")
    seed = seed_value

    initial_bankroll_value = request_data.get("initial_bankroll")
    if initial_bankroll_value is None:
        initial_bankroll = 1000.0
    elif isinstance(initial_bankroll_value, (int, float)):
        initial_bankroll = float(initial_bankroll_value)
    else:  # pragma: no cover - invalid bankroll type
        raise bad_args("initial_bankroll must be numeric")

    record_tape = bool(request_data.get("record_tape", False))

    vig_settings = _resolve_vig_settings(spec)
    caps = _apply_vig_settings_to_caps(dict(BASE_CAPABILITIES), vig_settings)
    if spec.get("enabled_buylay") is False:
        caps = dict(caps)
        caps["bets"] = dict(caps["bets"])
        caps["bets"]["buy"] = []
        caps["bets"]["lay"] = []
        if "vig" in caps:
            caps["vig"] = dict(caps["vig"])
            caps["vig"].pop("buy", None)
            caps["vig"].pop("lay", None)
        caps["why_unsupported"] = dict(caps["why_unsupported"])
        caps["why_unsupported"]["buy"] = "disabled_by_spec"
        caps["why_unsupported"]["lay"] = "disabled_by_spec"

    session_id = str(uuid.uuid4())[:8]
    session_state = SESSION_STORE.create(session_id, seed=seed)
    session_state["settings"] = dict(vig_settings)
    session_state["table_spec"] = dict(spec)
    session_state["initial_bankroll"] = initial_bankroll
    session_state["record_tape"] = record_tape
    session_state["tape_steps"] = []  # type: ignore[assignment]
    session_state["tape_metadata"] = {
        "engine_version": ENGINE_VERSION_STRING,
        "api_version": API_VERSION_STRING,
        "seed": seed,
        "table_spec": dict(spec),
        "initial_bankroll": initial_bankroll,
    }
    hand = session_state["hand"]
    hand_fields = hand.to_snapshot_fields()
    session_obj = session_state["session"]
    table = session_state.get("table")
    player = session_obj.player()
    if player is None and table is not None:
        table.add_player(bankroll=initial_bankroll, strategy=None, name="API Player")
        player = session_obj.player()
    if player is not None:
        player.bankroll = float(initial_bankroll)
    snapshot_state = session_obj.snapshot()
    bankroll_after = float(snapshot_state.get("bankroll", 0.0))

    snapshot: Dict[str, Any] = {
        "identity": {
            "engine_version": ENGINE_API_VERSION,
            "table_profile": spec.get("table_profile", "vanilla-default"),
            "seed": seed,
            "engine_api_version": ENGINE_API_VERSION,
            "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
        },
        "capabilities": caps,
        "session_id": session_id,
        **hand_fields,
        "roll_seq": session_state["roll_seq"],
        "dice": session_state["last_dice"],
        "bankroll_after": f"{bankroll_after:.2f}",
        "events": [],
        "bets": snapshot_state.get("bets", []),
    }

    response: StartSessionResponse = {
        "session_id": session_id,
        "snapshot": snapshot,
    }
    return StartSessionResult(response)


def roll(
    payload: RollRequest | BaseModel | Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    data = _coerce_roll_payload(payload)

    session_id_value = data.get("session_id")
    if not isinstance(session_id_value, str) or not session_id_value.strip():
        raise bad_args("session_id must be non-empty string")
    session_id = session_id_value

    dice_value = data.get("dice")
    dice: list[int] | None
    if dice_value is None:
        dice = None
    else:
        if not isinstance(dice_value, list) or len(dice_value) != 2:
            raise bad_args("dice must be [d1,d2]")
        dice = [int(dice_value[0]), int(dice_value[1])]
        if not all(1 <= d <= 6 for d in dice):
            raise bad_args("dice must be between 1 and 6")

    mode = "inject" if dice is not None else "auto"
    step_req = StepRollRequest(session_id=session_id, mode=mode, dice=dice)
    snapshot = step_roll(step_req)
    return {"snapshot": snapshot}


def _build_session_state_response(session_id: str) -> SessionStateResponse:
    session_state = _get_session_or_404(session_id)
    session_obj: Session | None = session_state.get("session")
    table = session_state.get("table")
    hand = session_state.get("hand")

    if session_obj is None:
        session_obj = Session(table=session_state.get("table"))
        session_state["session"] = session_obj
    if table is None and session_obj is not None:
        table = session_obj.table
        session_state["table"] = table

    player = session_obj.player() if session_obj is not None else None

    point_value = None
    if table is not None:
        point_value = getattr(getattr(table, "point", None), "number", None)

    table_settings = getattr(table, "settings", {}) if table is not None else {}
    table_section = None
    if isinstance(table_settings, dict):
        max_odds = table_settings.get("max_odds")
        if max_odds is not None:
            table_section = {"max_odds": max_odds}

    response: SessionStateResponse = {
        "state_schema": STATE_SCHEMA_VERSION,
        "session_id": session_id,
        "seed": session_state.get("seed"),
        "determinism_contract": DETERMINISM_CONTRACT_VERSION,
        "tape_loaded": bool(session_state.get("tape_steps")),
        "bankroll": float(getattr(player, "bankroll", 0.0)) if player else 0.0,
        "point": point_value,
        "roll_index": session_state.get("roll_seq"),
        "hand_index": getattr(hand, "hand_id", None),
        "last_roll": _serialize_last_roll(session_state, table) if table else None,
        "bets": _serialize_bets(player) if player else [],
        "ats": None,
        "fire": None,
        "table": table_section,
    }

    return response


def _build_session_metrics_response(session_id: str) -> SessionMetricsResponse:
    session_state = _get_session_or_404(session_id)
    session_obj: Session | None = session_state.get("session")
    player = session_obj.player() if session_obj is not None else None
    hand = session_state.get("hand")

    start_bankroll = float(session_state.get("initial_bankroll", 0.0))
    current_bankroll = float(getattr(player, "bankroll", 0.0)) if player else 0.0
    net = current_bankroll - start_bankroll
    roi = net / start_bankroll if start_bankroll else None

    roll_total = session_state.get("roll_seq")
    hand_total = getattr(hand, "hand_id", None)

    response: SessionMetricsResponse = {
        "metrics_schema": METRICS_SCHEMA_VERSION,
        "session_id": session_id,
        "bankroll": {
            "start": start_bankroll,
            "current": current_bankroll,
            "net": net,
            "roi": roi,
        },
        "rolls": {"total": roll_total, "comeout": None, "point_resolutions": None},
        "hands": {
            "total": hand_total,
            "completed": (hand_total - 1) if isinstance(hand_total, int) else None,
        },
        "outcomes": {"wins": None, "losses": None, "pushes": None},
        "points": {"made": None, "seven_outs": None, "pso_count": None},
        "by_bet_type": [],
        "determinism_contract": DETERMINISM_CONTRACT_VERSION,
    }

    return response


if router is not None:  # pragma: no cover - FastAPI optional

    def _start_session_http(body: Dict[str, Any] = Body(...)) -> Response:
        return _json_response(start_session(body))

    router.post("/session/start")(_start_session_http)
    router.post("/start_session")(_start_session_http)

    def _roll_http(body: RollRequest = Body(...)) -> Response:
        return _json_response(roll(body))

    router.post("/session/roll")(_roll_http)

    def _session_state_http(session_id: str) -> Response:
        return _json_response(_build_session_state_response(session_id))

    router.get("/session/{session_id}/state")(_session_state_http)

    def _session_metrics_http(session_id: str) -> Response:
        return _json_response(_build_session_metrics_response(session_id))

    router.get("/session/{session_id}/metrics")(_session_metrics_http)


def end_session():
    return {"report_min": {"hands": 0, "rolls": 0}}


if router is not None:  # pragma: no cover - FastAPI optional
    router.post("/end_session")(end_session)


def _at_state(session_id: str, session_state: Dict[str, Any]) -> Dict[str, Any]:
    hand = session_state.get("hand")
    hand_id = getattr(hand, "hand_id", None)
    return {
        "session_id": session_id,
        "hand_id": hand_id,
        "roll_seq": session_state.get("roll_seq"),
    }


def _player_signature(player: Any) -> list[tuple[str, int | None, float]]:
    signature: list[tuple[str, int | None, float]] = []
    for bet in getattr(player, "bets", []):
        signature.append(
            (
                bet.__class__.__name__,
                getattr(bet, "number", None),
                float(getattr(bet, "amount", 0.0)),
            )
        )
    return signature


def _serialize_bets(player: Any) -> list[dict]:
    bets: list[dict] = []
    for bet in getattr(player, "bets", []):
        entry: dict[str, Any] = {
            "type": bet.__class__.__name__,
            "number": getattr(bet, "number", None),
            "amount": float(getattr(bet, "amount", 0.0)),
        }

        working = getattr(bet, "working", None)
        if working is not None:
            entry["working"] = bool(working)

        odds = getattr(bet, "odds", None)
        if odds is not None:
            try:
                entry["odds_amount"] = float(getattr(odds, "amount", odds))
            except Exception:  # pragma: no cover - defensive
                pass

        bets.append(entry)
    return bets


def _serialize_last_roll(session_state: Dict[str, Any], table: Any) -> dict | None:
    last_roll_value = getattr(table, "last_roll", None)
    last_dice_value = session_state.get("last_dice")
    dice_values = None
    if last_dice_value is not None:
        try:
            dice_values = [int(last_dice_value[0]), int(last_dice_value[1])]
        except Exception:  # pragma: no cover - defensive
            dice_values = None

    if last_roll_value is None and dice_values is None:
        return None

    return {
        "total": last_roll_value,
        "dice": dice_values,
        "resolved": None,
    }


def apply_action(req: dict):
    verb = req.get("verb")
    args = req.get("args", {})
    session_id = req.get("session_id")

    if not isinstance(verb, str) or not verb:
        raise bad_args("verb must be a non-empty string")
    if verb not in SUPPORTED_VERBS:
        raise unsupported_bet(f"verb '{verb}' not recognized")
    if not isinstance(args, dict):
        raise bad_args("args must be a dictionary")
    if not isinstance(session_id, str) or not session_id.strip():
        raise bad_args("session_id must be provided")

    session_state = SESSION_STORE.ensure(session_id)
    table_settings = session_state.setdefault("settings", dict(DEFAULT_VIG_SETTINGS))
    session_obj: Session | None = session_state.get("session")
    table = session_state.get("table")

    if session_obj is None:
        if table is None:
            table = SESSION_STORE.ensure(session_id)["table"]
        session_obj = Session(table=table)
        session_state["session"] = session_obj

    assert session_obj is not None

    if table is None:
        table = session_obj.table
        session_state["table"] = table

    vig_rounding = table_settings.get("vig_rounding")
    if isinstance(vig_rounding, str):
        table.settings["vig_rounding"] = vig_rounding
    vig_floor = table_settings.get("vig_floor")
    if isinstance(vig_floor, (int, float)):
        table.settings["vig_floor"] = float(vig_floor)
    vig_paid_on_win = table_settings.get("vig_paid_on_win")
    if isinstance(vig_paid_on_win, bool):
        table.settings["vig_paid_on_win"] = vig_paid_on_win

    player = session_obj.player()
    if player is None:
        table.add_player(bankroll=1000, strategy=None, name="API Player")
        player = session_obj.player()

    if player is None:  # pragma: no cover - defensive
        raise ApiError(
            ApiErrorCode.INTERNAL,
            "session player unavailable",
            at_state=_at_state(session_id, session_state),
        )

    bankroll_before = float(player.bankroll)

    if is_bet_placement_verb(verb):
        signature_before = _player_signature(player)

        bet = build_bet(verb, args, table=table, player=player)
        required_cash = compute_required_cash(player, bet)

        if required_cash > bankroll_before + 1e-9:
            raise ApiError(
                ApiErrorCode.INSUFFICIENT_FUNDS,
                f"bankroll ${bankroll_before:.2f} < required ${required_cash:.2f}",
                at_state=_at_state(session_id, session_state),
            )

        player.add_bet(bet)

        bankroll_after = float(player.bankroll)
        signature_after = _player_signature(player)

        applied = (
            bankroll_after != bankroll_before or signature_after != signature_before
        )
        if not applied:
            raise ApiError(
                ApiErrorCode.TABLE_RULE_BLOCK,
                "engine rejected action",
                at_state=_at_state(session_id, session_state),
            )

        bankroll_delta = bankroll_after - bankroll_before
        vig_info = describe_vig(bet, table)

        effect_summary: Dict[str, Any] = {
            "verb": verb,
            "args": args,
            "applied": True,
            "bankroll_delta": bankroll_delta,
            "note": "applied via engine",
        }

        if vig_info is not None:
            effect_summary["vig"] = vig_info
        if required_cash > 0:
            effect_summary["cash_required"] = required_cash

    elif is_bet_management_verb(verb):
        mgmt_result = apply_bet_management(session_obj, verb, args)
        if mgmt_result.get("result") != "ok":
            error_code_value = (
                mgmt_result.get("error_code") or ApiErrorCode.BAD_ARGS.value
            )
            hint = mgmt_result.get("error_hint", "bet management action failed")
            context = mgmt_result.get("error_context")
            context_value = context if isinstance(context, dict) else {}
            raise ApiError(
                error_code_value,
                hint,
                at_state=_at_state(session_id, session_state),
                context=context_value,
            )

        bankroll_after = float(mgmt_result["bankroll_after"])
        bankroll_delta = bankroll_after - float(mgmt_result["bankroll_before"])
        effect_summary = {
            "verb": verb,
            "args": args,
            "applied": bool(mgmt_result.get("changed")),
            "bankroll_delta": bankroll_delta,
            "note": "applied via bet management",
            "bets_before": mgmt_result["bets_before"],
            "bets_after": mgmt_result["bets_after"],
        }
    else:  # pragma: no cover - defensive
        raise ApiError(
            ApiErrorCode.UNSUPPORTED_BET,
            f"verb '{verb}' not recognized",
            at_state=_at_state(session_id, session_state),
        )

    snapshot_state = session_obj.snapshot()
    bankroll_value = f"{float(snapshot_state.get('bankroll', bankroll_after)):.2f}"

    return {
        "effect_summary": effect_summary,
        "snapshot": {
            "session_id": session_id,
            "bankroll_after": bankroll_value,
            "identity": {
                "engine_api_version": ENGINE_API_VERSION,
                "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
            },
            "puck": "ON" if table.point.status == "On" else "OFF",
            "point": table.point.number,
            "bets": snapshot_state.get("bets", []),
        },
    }


if router is not None:  # pragma: no cover - FastAPI optional
    router.post("/apply_action")(apply_action)


class StepRollRequest(BaseModel):
    session_id: str
    mode: str = Field(..., description="auto or inject")
    dice: list[int] | None = None

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        if v not in ("auto", "inject"):
            raise ValueError("mode must be 'auto' or 'inject'")
        return v

    @field_validator("dice")
    @classmethod
    def validate_dice(cls, v: list[int] | None, values: ValidationInfo):
        mode_value = None
        if hasattr(values, "data"):
            mode_value = values.data.get("mode")  # type: ignore[attr-defined]
        elif isinstance(values, dict):
            mode_value = values.get("mode")
        if mode_value == "inject":
            if not isinstance(v, list) or len(v) != 2:
                raise ValueError("dice must be [d1,d2]")
            if not all(isinstance(d, int) and 1 <= d <= 6 for d in v):
                raise ValueError("each die must be 1–6")
        return v


def step_roll(req: StepRollRequest):
    session_id = req.session_id
    sess = SESSION_STORE.ensure(session_id)
    hand = sess["hand"]
    session_obj: Session = sess["session"]
    table = session_obj.table
    sess["table"] = table
    roll_seq = sess["roll_seq"] + 1
    sess["roll_seq"] = roll_seq
    hand_id = hand.hand_id

    dice_override: list[int] | None
    if req.mode == "inject":
        assert req.dice is not None
        dice_override = [int(req.dice[0]), int(req.dice[1])]
    else:
        dice_override = None

    event = session_obj.step_roll(dice_override)
    dice_values = [int(v) for v in event.get("dice", (0, 0))]
    sess["last_dice"] = tuple(dice_values)

    before_snapshot = event.get("before", {})
    after_snapshot = event.get("after", {})
    bankroll_before = f"{float(before_snapshot.get('bankroll', 0.0)):.2f}"
    bankroll_after = f"{float(after_snapshot.get('bankroll', 0.0)):.2f}"

    events = []
    if roll_seq == 1:
        events.append(
            build_event(
                session_id,
                hand_id,
                roll_seq,
                "hand_started",
                bankroll_before,
                bankroll_after,
                {},
            )
        )

    events.append(
        build_event(
            session_id,
            hand_id,
            roll_seq,
            "roll_started",
            bankroll_before,
            bankroll_after,
            {"mode": req.mode},
        )
    )
    is_push = bool(event.get("is_push", False))

    events.append(
        build_event(
            session_id,
            hand_id,
            roll_seq,
            "roll_completed",
            bankroll_before,
            bankroll_after,
            {"dice": dice_values, "is_push": is_push},
        )
    )

    pre_hand_id = hand_id
    state_evs = hand.on_roll((dice_values[0], dice_values[1]))

    for ev in state_evs:
        et = ev["type"]
        data = ev.get("data", {})
        if et == "point_set":
            events.append(
                build_point_set(
                    session_id,
                    pre_hand_id,
                    roll_seq,
                    bankroll_before,
                    bankroll_after,
                    data["point"],
                )
            )
        elif et == "point_made":
            events.append(
                build_point_made(
                    session_id,
                    pre_hand_id,
                    roll_seq,
                    bankroll_before,
                    bankroll_after,
                    data["point"],
                )
            )
        elif et == "seven_out":
            events.append(
                build_seven_out(
                    session_id,
                    pre_hand_id,
                    roll_seq,
                    bankroll_before,
                    bankroll_after,
                )
            )
        elif et == "hand_ended":
            events.append(
                build_hand_ended(
                    session_id,
                    pre_hand_id,
                    roll_seq,
                    bankroll_before,
                    bankroll_after,
                    data.get("end_reason", "unknown"),
                )
            )

    snap_state = hand.to_snapshot_fields()
    snapshot = {
        "session_id": session_id,
        "hand_id": snap_state["hand_id"],
        "roll_seq": roll_seq,
        "dice": dice_values,
        "puck": snap_state["puck"],
        "point": snap_state["point"],
        "bankroll_after": bankroll_after,
        "events": events,
        "identity": {
            "engine_api_version": ENGINE_API_VERSION,
            "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
        },
        "bets": after_snapshot.get("bets", []),
        "is_push": is_push,
    }
    return snapshot


def session_step(session_id: str, body: Dict[str, Any] = Body(...)) -> Response:
    payload = dict(body or {})
    actions_value = payload.get("actions", [])
    if actions_value is None:
        actions_value = []
    if not isinstance(actions_value, list):
        raise bad_args("actions must be a list")

    normalized_actions: List[Dict[str, Any]] = []
    for action_payload in actions_value:
        normalized = _normalize_action_payload(action_payload, session_id)
        normalized_actions.append(normalized)
        apply_action(normalized)

    dice_value = payload.get("dice")
    roll_payload: Dict[str, Any] = {
        "session_id": session_id,
        "mode": "inject" if dice_value is not None else "auto",
    }
    if dice_value is not None:
        roll_payload["dice"] = dice_value

    roll_req = StepRollRequest(**roll_payload)
    state = step_roll(roll_req)

    sess = SESSION_STORE.ensure(session_id)
    actions_for_tape = [dict(a) for a in actions_value]
    if sess.get("record_tape"):
        dice_tuple = (
            (
                int(dice_value[0]),
                int(dice_value[1]),
            )
            if dice_value is not None
            else (
                int(state["dice"][0]),
                int(state["dice"][1]),
            )
        )
        _record_tape_step(sess, dice_tuple, actions_for_tape)

    sess["final_state"] = dict(state)
    sess["last_snapshot"] = dict(state)

    return _json_response({"state": state})


def _state_signature(
    state: Dict[str, Any],
) -> Tuple[str, Tuple[Tuple[str | None, int | None, float], ...]]:
    bankroll = str(state.get("bankroll_after") or state.get("bankroll") or "")
    bets = []
    for bet in state.get("bets", []):
        if isinstance(bet, dict):
            bets.append(
                (
                    bet.get("type"),
                    bet.get("number"),
                    float(bet.get("amount", 0.0)),
                )
            )
    bets_signature = tuple(sorted(bets))
    return bankroll, bets_signature


def _create_table_from_spec(
    *,
    table_spec: dict,
    seed: Optional[int],
    initial_bankroll: Optional[float] = None,
    session_label: Optional[str] = None,
) -> Tuple[str, Any]:
    session_id = session_label or str(uuid.uuid4())[:8]
    if session_label is not None:
        try:
            getattr(SESSION_STORE, "_s", {}).pop(session_id, None)
        except Exception:  # pragma: no cover - defensive
            pass
    session_state = SESSION_STORE.create(
        session_id, seed=seed if seed is not None else 0
    )
    session_state["settings"] = dict(_resolve_vig_settings(table_spec))
    session_state["table_spec"] = dict(table_spec)
    session_state["initial_bankroll"] = (
        float(initial_bankroll)
        if initial_bankroll is not None
        else float(session_state.get("initial_bankroll", 1000.0))
    )
    session_state["record_tape"] = False
    session_state["tape_steps"] = []  # type: ignore[assignment]
    table = session_state["table"]
    setattr(table, "_api_session_id", session_id)

    session_obj: Session = session_state["session"]
    player = session_obj.player()
    if player is None:
        table.add_player(
            bankroll=session_state["initial_bankroll"], strategy=None, name="API Player"
        )
        player = session_obj.player()
    if player is not None:
        player.bankroll = float(session_state["initial_bankroll"])

    return session_id, table


def _apply_action(table: Any, action_payload: Dict[str, Any]) -> Dict[str, Any]:
    session_id = getattr(table, "_api_session_id", None)
    if session_id is None:
        raise bad_args("table missing session context")
    normalized = _normalize_action_payload(action_payload, session_id)
    return apply_action(normalized)


def _roll_dice(table: Any, d1: int, d2: int) -> Dict[str, Any]:
    session_id = getattr(table, "_api_session_id", None)
    req = StepRollRequest(session_id=session_id, mode="inject", dice=[int(d1), int(d2)])
    snapshot = step_roll(req)
    sess = SESSION_STORE.ensure(session_id)
    sess["last_snapshot"] = dict(snapshot)
    sess["final_state"] = dict(snapshot)
    return snapshot


def _summarize_table_state(table: Any) -> dict:
    session_id = getattr(table, "_api_session_id", None)
    if session_id is None:
        return {}
    sess = SESSION_STORE.ensure(session_id)
    if "final_state" in sess:
        return dict(sess.get("final_state") or {})
    last_snapshot = sess.get("last_snapshot")
    if isinstance(last_snapshot, dict):
        return dict(last_snapshot)

    hand = sess.get("hand")
    session_obj: Session | None = sess.get("session")
    if hand is None or session_obj is None:
        return {}
    snap_state = hand.to_snapshot_fields()
    snapshot_state = session_obj.snapshot()
    bankroll_after = f"{float(snapshot_state.get('bankroll', 0.0)):.2f}"
    dice_values = list(sess.get("last_dice") or [])
    return {
        "session_id": session_id,
        "hand_id": snap_state.get("hand_id"),
        "roll_seq": sess.get("roll_seq"),
        "dice": dice_values,
        "puck": snap_state.get("puck"),
        "point": snap_state.get("point"),
        "bankroll_after": bankroll_after,
        "events": [],
        "identity": {
            "engine_api_version": ENGINE_API_VERSION,
            "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
        },
        "bets": snapshot_state.get("bets", []),
        "is_push": False,
    }


def _find_first_mismatch_step(
    tape: SessionTape, table_spec: dict, seed: Optional[int], original_final_state: dict
) -> Optional[int]:
    initial_bankroll = tape.get("metadata", {}).get("initial_bankroll")
    session_id, table = _create_table_from_spec(
        table_spec=table_spec,
        seed=seed,
        initial_bankroll=initial_bankroll,
        session_label=f"{tape.get('session_id', 'tape')}-mismatch",
    )
    _ = session_id
    target_signature = _state_signature(original_final_state)
    last_step_index: Optional[int] = None
    last_signature: Optional[
        Tuple[str, Tuple[Tuple[str | None, int | None, float], ...]]
    ] = None
    for step in tape.get("steps", []):
        for action_payload in step.get("actions", []):
            _apply_action(table, action_payload)
        snapshot = _roll_dice(table, step["dice"][0], step["dice"][1])
        last_signature = _state_signature(snapshot)
        last_step_index = int(step.get("step_index", step["step_index"]))
    if last_signature is not None and last_signature != target_signature:
        return last_step_index
    return None


def export_session_tape(session_id: str) -> SessionTape:
    session = getattr(SESSION_STORE, "_s", {}).get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Unknown session_id")

    if not session.get("record_tape"):
        raise HTTPException(
            status_code=400, detail="Tape recording was not enabled for this session"
        )

    metadata: SessionTapeMetadata = {**session.get("tape_metadata", {})}
    steps: list[SessionTapeStep] = list(session.get("tape_steps", []))
    final_state: dict = dict(session.get("final_state") or {})

    return {
        "session_id": session_id,
        "metadata": metadata,
        "steps": steps,
        "final_state": final_state,
    }


def replay_session_tape(tape: SessionTape) -> ReplayResult:
    meta = tape.get("metadata", {})
    table_spec = meta.get("table_spec", {})
    seed = meta.get("seed")
    initial_bankroll = meta.get("initial_bankroll")

    _, table = _create_table_from_spec(
        table_spec=table_spec,
        seed=seed,
        initial_bankroll=initial_bankroll,
        session_label=tape.get("session_id"),
    )

    last_snapshot: dict = {}
    for step in tape.get("steps", []):
        for action_payload in step.get("actions", []):
            _apply_action(table, action_payload)
        d1, d2 = step.get("dice", (0, 0))
        last_snapshot = _roll_dice(table, d1, d2)

    if not last_snapshot:
        last_snapshot = _summarize_table_state(table)

    replay_state = dict(last_snapshot)

    original_final = dict(tape.get("final_state") or {})
    normalized_original = _normalize_state_for_tape(
        original_final, tape.get("session_id")
    )
    normalized_replay = _normalize_state_for_tape(replay_state, tape.get("session_id"))

    deterministic = normalized_replay == normalized_original
    mismatch_step: Optional[int] = None

    if not deterministic:
        mismatch_step = _find_first_mismatch_step(
            tape, table_spec, seed, normalized_original
        )

    replay_return_state = dict(replay_state)
    if tape.get("session_id"):
        replay_return_state["session_id"] = tape["session_id"]
    if deterministic and original_final.get("events"):
        replay_return_state["events"] = original_final.get("events", [])
    original_return_state = original_final if original_final else normalized_original

    return {
        "deterministic": deterministic,
        "mismatch_step": mismatch_step,
        "original_final_state": original_return_state,
        "replay_final_state": replay_return_state,
    }


if router is not None:  # pragma: no cover - FastAPI optional
    router.post("/step_roll")(step_roll)
    router.post("/session/{session_id}/step")(session_step)
    router.get("/session/{session_id}/tape")(export_session_tape)
    router.post("/session/replay")(replay_session_tape)


try:  # pragma: no cover - FastAPI optional
    app = create_app(strict=True)
except RuntimeError:
    app = None  # type: ignore[assignment]
