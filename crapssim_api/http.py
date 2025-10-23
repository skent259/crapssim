from __future__ import annotations

import json
import uuid
from typing import Any, Dict

import random

from fastapi import APIRouter, FastAPI
from fastapi.responses import Response
from pydantic import BaseModel, Field, ValidationInfo, field_validator

from .actions import VerbRegistry
from .actions import (
    TableView,
    apply_bankroll_delta,
    check_amount,
    check_funds,
    check_limits,
    check_timing,
    get_bankroll,
)
from .errors import ApiError, api_error_handler, bad_args, table_rule_block, unsupported_bet
from .events import build_event
from .types import Capabilities, StartSessionRequest, StartSessionResponse, TableSpec
from .version import CAPABILITIES_SCHEMA_VERSION, ENGINE_API_VERSION, get_identity

app = FastAPI(title="CrapsSim API")

router = APIRouter()

# Session roll ledger
SessionRolls: dict[str, dict[str, Any]] = {}

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
    "commission": {
        "buy": {"mode": "on_win", "rate_bips": 500, "rounding": "nearest_dollar"},
        "lay": {"mode": "on_win", "rate_bips": 500, "rounding": "nearest_dollar"},
    },
    "working_flags": {"comeout_odds_work": False, "place_work_comeout": False},
    "why_unsupported": {
        "fire": "not implemented in vanilla",
        "small_tall_all": "not implemented in vanilla",
    },
}


def _json_dumps(value: Any) -> str:
    return json.dumps(value, separators=(", ", ": "))


def _json_response(payload: Any) -> Response:
    return Response(content=_json_dumps(payload), media_type="application/json")


def _capabilities_dict() -> Dict[str, Any]:
    resp = get_capabilities()
    return json.loads(resp.body.decode())


def create_app() -> FastAPI:
    app.add_exception_handler(ApiError, api_error_handler)
    return app


@app.get("/healthz")
def healthz() -> Response:
    identity = get_identity()
    payload = {"status": "ok", **identity}
    return _json_response(payload)


@app.get("/capabilities")
def get_capabilities() -> Response:
    payload: Dict[str, Any] = {
        "engine_api": {"version": ENGINE_API_VERSION},
        "capabilities": BASE_CAPABILITIES,
    }
    return _json_response(payload)


@app.post("/start_session")
def start_session(body: StartSessionRequest) -> Response:
    spec: TableSpec = body.get("spec", {})
    seed = body.get("seed", 0)
    if not isinstance(seed, int):
        raise bad_args("seed must be int")

    caps = dict(BASE_CAPABILITIES)
    if spec.get("enabled_buylay") is False:
        caps = dict(caps)
        caps["bets"] = dict(caps["bets"])
        caps["bets"]["buy"] = []
        caps["bets"]["lay"] = []
        caps["why_unsupported"] = dict(caps["why_unsupported"])
        caps["why_unsupported"]["buy"] = "disabled_by_spec"
        caps["why_unsupported"]["lay"] = "disabled_by_spec"

    response: StartSessionResponse = {
        "session_id": str(uuid.uuid4())[:8],
        "snapshot": {
            "identity": {
                "engine_version": ENGINE_API_VERSION,
                "table_profile": spec.get("table_profile", "vanilla-default"),
                "seed": seed,
            },
            "capabilities": caps,
        },
    }
    return _json_response(response)


@app.post("/end_session")
def end_session():
    return {"report_min": {"hands": 0, "rolls": 0}}


@app.post("/apply_action")
def apply_action(req: dict):
    verb = req.get("verb")
    args = req.get("args", {})
    session_id = req.get("session_id", "stub-session")

    if not isinstance(verb, str) or not verb:
        raise bad_args("verb must be a non-empty string")
    if verb not in VerbRegistry:
        raise unsupported_bet(f"verb '{verb}' not recognized")
    if not isinstance(args, dict):
        raise bad_args("args must be a dictionary")

    # ----- legality context ---------------------------------------------------
    caps = _capabilities_dict()["capabilities"]
    place_increments = {str(k): int(v) for k, v in caps.get("increments", {}).get("place", {}).items()}
    odds_limits = caps.get("odds_limits", {"policy": "3-4-5", "max_x": 20})
    odds_policy = str(odds_limits.get("policy", "3-4-5"))
    odds_max_x = int(odds_limits.get("max_x", 20))

    # Allow tests/clients to pass a minimal state hint; default puck OFF (come-out)
    # Example: {"state": {"puck": "ON", "point": 6}}
    state = req.get("state", {})
    puck = state.get("puck", "OFF")
    point = state.get("point", None)
    table = TableView(puck=puck, point=point)

    # ----- legality checks ----------------------------------------------------
    check_timing(verb, table)
    check_amount(verb, args, place_increments)
    check_limits(verb, args, odds_policy, odds_max_x)

    amt = args.get("amount", 0)
    if isinstance(amt, (int, float)) and amt > 0:
        # Verify funds and deduct for deterministic ledger tracking
        check_funds(session_id, amt)
        apply_bankroll_delta(session_id, -amt)

    # ----- dispatch (still no-op stub) ---------------------------------------
    result = VerbRegistry[verb](args)
    result_note = result.get("note", "")
    if result_note.startswith("stub:"):
        # clarify that legality passed
        result["note"] = "validated (legal, stub execution)"

    return {
        "effect_summary": {
            "verb": verb,
            "args": args,
            **result,
        },
        "snapshot": {
            "session_id": session_id,
            "bankroll_after": get_bankroll(session_id),
            "identity": {
                "engine_api_version": ENGINE_API_VERSION,
                "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
            },
            # expose minimal table view echo for client tracing
            "puck": table.puck,
            "point": table.point,
        },
    }


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
        if values.data.get("mode") == "inject":
            if not isinstance(v, list) or len(v) != 2:
                raise ValueError("dice must be [d1,d2]")
            if not all(isinstance(d, int) and 1 <= d <= 6 for d in v):
                raise ValueError("each die must be 1–6")
        return v


@router.post("/step_roll")
def step_roll(req: StepRollRequest):
    session_id = req.session_id
    entry = SessionRolls.get(
        session_id, {"roll_seq": 0, "hand_id": 1, "last_dice": None}
    )
    roll_seq = entry["roll_seq"] + 1
    hand_id = entry["hand_id"]

    # deterministic RNG seed
    rng_seed = hash(session_id) & 0xFFFFFFFF
    rnd = random.Random(rng_seed + roll_seq)
    if req.mode == "inject":
        assert req.dice is not None
        d1, d2 = req.dice
    elif entry.get("last_dice"):
        d1, d2 = entry["last_dice"]
    else:
        d1, d2 = rnd.randint(1, 6), rnd.randint(1, 6)

    entry.update({"roll_seq": roll_seq, "last_dice": (d1, d2)})
    SessionRolls[session_id] = entry

    bankroll_before = "1000.00"
    bankroll_after = bankroll_before

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
            {"dice": [d1, d2]},
        )
    )

    snapshot = {
        "session_id": session_id,
        "hand_id": hand_id,
        "roll_seq": roll_seq,
        "dice": [d1, d2],
        "puck": "OFF",
        "point": None,
        "bankroll_after": bankroll_after,
        "events": events,
        "identity": {
            "engine_api_version": ENGINE_API_VERSION,
            "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
        },
    }
    return snapshot


app.include_router(router)
