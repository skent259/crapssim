from __future__ import annotations

import json
import uuid
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.responses import Response

from .actions import VerbRegistry
from .errors import ApiError, api_error_handler, bad_args, table_rule_block, unsupported_bet
from .types import Capabilities, StartSessionRequest, StartSessionResponse, TableSpec
from .version import CAPABILITIES_SCHEMA_VERSION, ENGINE_API_VERSION, get_identity

app = FastAPI(title="CrapsSim API")

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

    result = VerbRegistry[verb](args)
    return {
        "effect_summary": {
            "verb": verb,
            "args": args,
            **result,
        },
        "snapshot": {
            "session_id": session_id,
            "identity": {
                "engine_api_version": ENGINE_API_VERSION,
                "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
            },
        },
    }
