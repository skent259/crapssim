"""API-backed sequence harness for CrapsSim."""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pytest

from crapssim_api.http import SESSION_STORE, create_app
from crapssim_api.session import Session

from .sequence_harness_common import (
    API_JSON_PATH,
    API_REPORT_PATH,
    ActionResult,
    SequenceJournalEntry,
    SequenceRunConfig,
    ensure_results_dir,
    normalize_bets,
    write_json,
    write_sequence_report,
)
from .sequence_scenarios import SEQUENCE_SCENARIOS


def _require_test_client():
    pytest.importorskip("fastapi")
    pytest.importorskip("pydantic")
    from fastapi.testclient import TestClient  # type: ignore import-not-found

    return TestClient


def _ensure_player(session: Session):
    session._ensure_player()  # noqa: SLF001 - harness access
    player = session.player()
    if player is None:  # pragma: no cover - defensive
        raise RuntimeError("session player unavailable")
    return player


def _start_session(client: Any, seed: int) -> tuple[str, Session]:
    response = client.post("/session/start", json={"seed": seed})
    response.raise_for_status()
    payload = response.json()
    session_id = payload["session_id"]
    state = SESSION_STORE.ensure(session_id)
    session_obj: Session = state["session"]
    return session_id, session_obj


def _apply_initial_state(
    client: Any,
    session_id: str,
    session_obj: Session,
    *,
    bankroll: float,
    initial_bets: List[Dict[str, Any]],
) -> None:
    player = _ensure_player(session_obj)
    player.bets.clear()
    player.bankroll = float(bankroll)

    for bet in initial_bets:
        verb = bet["verb"]
        args = bet.get("args", {}) or {}
        payload = {"verb": verb, "args": args, "session_id": session_id}
        resp = client.post("/apply_action", json=payload)
        resp.raise_for_status()


def _apply_action(client: Any, session_id: str, action: Dict[str, Any]) -> ActionResult:
    verb = action["verb"]
    args = dict(action.get("args", {}) or {})
    payload = {"verb": verb, "args": args, "session_id": session_id}
    response = client.post("/apply_action", json=payload)

    if response.status_code == 200:
        return {"verb": verb, "args": dict(args), "result": "ok", "error_code": None}

    error_code: str | None
    try:
        error_code = response.json().get("code")
    except ValueError:  # pragma: no cover - defensive
        error_code = None
    return {"verb": verb, "args": dict(args), "result": "error", "error_code": error_code}


def _inject_roll(client: Any, session_id: str, dice: Tuple[int, int]) -> None:
    payload = {"session_id": session_id, "dice": [int(dice[0]), int(dice[1])]}
    response = client.post("/session/roll", json=payload)
    response.raise_for_status()


def run_api_sequence_harness(config: SequenceRunConfig | None = None) -> List[SequenceJournalEntry]:
    pytest.importorskip("fastapi")
    pytest.importorskip("pydantic")
    TestClient = _require_test_client()
    app = create_app()
    client = TestClient(app)

    cfg = config or SequenceRunConfig()
    journal: List[SequenceJournalEntry] = []

    ensure_results_dir()

    for index, scenario in enumerate(SEQUENCE_SCENARIOS):
        seed = cfg.seed_base + scenario.get("seed_offset", index)
        session_id, session_obj = _start_session(client, seed)
        initial_bankroll = float(scenario.get("initial_bankroll", 250.0))
        initial_bets = list(scenario.get("initial_bets", []))
        _apply_initial_state(
            client,
            session_id,
            session_obj,
            bankroll=initial_bankroll,
            initial_bets=initial_bets,
        )

        player = _ensure_player(session_obj)

        initial_snapshot = session_obj.snapshot()
        normalized_initial_bets = normalize_bets(initial_snapshot.get("bets", []))

        steps: List[Dict[str, Any]] = []
        last_result = "ok"
        last_error: str | None = None

        for step_index, step in enumerate(scenario.get("steps", [])):
            before_snapshot = session_obj.snapshot()
            before_bankroll = float(before_snapshot.get("bankroll", 0.0))
            before_bets = normalize_bets(before_snapshot.get("bets", []))

            dice = step.get("dice")
            if dice is not None:
                _inject_roll(client, session_id, (int(dice[0]), int(dice[1])))
                last_result = "ok"
                last_error = None

            actions = step.get("actions", []) or []
            action_results: List[ActionResult] = []
            for action in actions:
                result = _apply_action(client, session_id, action)
                action_results.append(result)
                last_result = result["result"]
                last_error = result.get("error_code")

            after_snapshot = session_obj.snapshot()
            after_bankroll = float(after_snapshot.get("bankroll", 0.0))
            after_bets = normalize_bets(after_snapshot.get("bets", []))

            steps.append(
                {
                    "index": step_index,
                    "label": step.get("label", f"step_{step_index}"),
                    "dice": [int(dice[0]), int(dice[1])] if dice is not None else None,
                    "before_bankroll": before_bankroll,
                    "after_bankroll": after_bankroll,
                    "bets_before": before_bets,
                    "bets_after": after_bets,
                    "actions": action_results,
                }
            )

        final_snapshot = session_obj.snapshot()
        final_bankroll = float(final_snapshot.get("bankroll", 0.0))
        final_bets = normalize_bets(final_snapshot.get("bets", []))

        journal.append(
            {
                "scenario": scenario["label"],
                "seed": seed,
                "initial_bankroll": initial_bankroll,
                "initial_bets": normalized_initial_bets,
                "steps": steps,
                "final_state": {
                    "bankroll": final_bankroll,
                    "bets": final_bets,
                    "result": last_result,
                    "error_code": last_error,
                },
            }
        )

        player.bets.clear()

    write_json(API_JSON_PATH, journal)
    write_sequence_report(
        API_REPORT_PATH, journal, title="CrapsSim API — Roll-by-Roll Sequence Trace"
    )
    return journal
