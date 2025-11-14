from __future__ import annotations

import json
import uuid
from typing import Any, Dict

try:
    from fastapi import APIRouter, FastAPI, Body
    from fastapi.responses import Response as FastAPIResponse
except ModuleNotFoundError:  # pragma: no cover - environment without fastapi
    APIRouter = None  # type: ignore[assignment]
    FastAPI = None  # type: ignore[assignment]
    FastAPIResponse = None  # type: ignore[assignment]

    class Response:  # minimal stub
        def __init__(self, content: str, media_type: str):
            self.body = content.encode()
            self.media_type = media_type

else:  # pragma: no cover - FastAPI available
    Response = FastAPIResponse  # type: ignore[assignment]


def _ensure_fastapi() -> None:
    if FastAPI is None or APIRouter is None:
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


from crapssim.bet import _compute_vig, _vig_policy


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


from .actions import SUPPORTED_VERBS, build_bet, compute_required_cash, describe_vig
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
from .types import Capabilities, StartSessionRequest, StartSessionResponse, TableSpec
from .version import CAPABILITIES_SCHEMA_VERSION, ENGINE_API_VERSION, get_identity

if FastAPI is None:  # pragma: no cover - FastAPI optional

    class _StubApp:  # minimal ASGI fallback
        def __call__(
            self, scope: Any, receive: Any, send: Any
        ) -> None:  # pragma: no cover
            raise RuntimeError("FastAPI is not installed")

    _stub_app = _StubApp()
else:
    _stub_app = None

if APIRouter is not None:
    router = APIRouter()
else:  # pragma: no cover - FastAPI optional
    router = None

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
        "field": {"pays": {"2": "double", "12": "double"}},
        "hardways": {"break_on": "seven_or_easy"},
        "props": ["any7", "c&e", "horn", "world"],
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
    "why_unsupported": {
        "fire": "not implemented in vanilla",
        "small_tall_all": "not implemented in vanilla",
    },
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


def _capabilities_dict() -> Dict[str, Any]:
    resp = get_capabilities()
    return json.loads(resp.body.decode())


def create_app(*, strict: bool = False):
    if FastAPI is None or router is None:  # pragma: no cover - FastAPI optional
        if strict:
            _ensure_fastapi()
        assert _stub_app is not None
        return _stub_app  # type: ignore[return-value]

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
    spec_value = request_data.get("spec", {})
    if not isinstance(spec_value, dict):
        raise bad_args("spec must be a mapping")
    spec: TableSpec = spec_value

    seed_value = request_data.get("seed", 0)
    if isinstance(seed_value, bool) or not isinstance(seed_value, int):
        raise bad_args("seed must be int")
    seed = seed_value

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
    hand = session_state["hand"]
    hand_fields = hand.to_snapshot_fields()
    session_obj = session_state["session"]
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


if router is not None:  # pragma: no cover - FastAPI optional

    def _start_session_http(body: Dict[str, Any] = Body(...)) -> Response:
        return _json_response(start_session(body))

    router.post("/session/start")(_start_session_http)
    router.post("/start_session")(_start_session_http)

    def _roll_http(body: RollRequest = Body(...)) -> Response:
        return _json_response(roll(body))

    router.post("/session/roll")(_roll_http)


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

    applied = bankroll_after != bankroll_before or signature_after != signature_before
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
    events.append(
        build_event(
            session_id,
            hand_id,
            roll_seq,
            "roll_completed",
            bankroll_before,
            bankroll_after,
            {"dice": dice_values},
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
    }
    return snapshot


if router is not None:  # pragma: no cover - FastAPI optional
    router.post("/step_roll")(step_roll)


try:  # pragma: no cover - FastAPI optional
    app = create_app(strict=True)
except RuntimeError:
    app = None  # type: ignore[assignment]
