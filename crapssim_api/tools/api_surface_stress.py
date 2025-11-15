"""Run the CrapsSim API surface stress scenarios against the FastAPI layer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, List

import pytest

from crapssim_api.http import SESSION_STORE, create_app
from crapssim_api.session import Session

from .api_surface_scenarios import (
    SCENARIOS,
    Scenario,
    ScenarioPreAction,
    ScenarioSetupStep,
)

DEFAULT_JSON = Path("build/api_surface_api.json")
DEFAULT_MARKDOWN = Path("crapssim_api/docs/dev/API_SURFACE_STRESS_API.md")


def _require_test_client():
    pytest.importorskip("fastapi")
    pytest.importorskip("pydantic")
    from fastapi.testclient import TestClient  # type: ignore import-not-found

    return TestClient


def _ensure_player(session: Session) -> Any:
    session._ensure_player()  # noqa: SLF001 - harness needs direct access
    player = session.player()
    if player is None:  # pragma: no cover - defensive
        raise RuntimeError("session player unavailable")
    return player


def _normalize_bets(bets: Iterable[dict]) -> List[dict]:
    normalized: List[dict] = []
    for bet in bets:
        normalized.append(
            {
                "type": str(bet.get("type")),
                "number": bet.get("number"),
                "amount": float(bet.get("amount", 0.0)),
            }
        )
    normalized.sort(
        key=lambda item: (
            item["type"],
            item["number"] if item["number"] is not None else -1,
            item["amount"],
        )
    )
    return normalized


def _apply_pre_action(client: Any, session_id: str, action: ScenarioPreAction) -> None:
    verb = action["verb"]
    args = dict(action.get("args", {}) or {})
    response = client.post(
        "/apply_action",
        json={"verb": verb, "args": args, "session_id": session_id},
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"pre-state action {verb} failed: status={response.status_code}, body={response.text}"
        )


def _execute_setup_steps(
    client: Any, session_id: str, steps: Iterable[ScenarioSetupStep]
) -> None:
    for step in steps:
        for action in step.get("actions", []) or []:
            _apply_pre_action(client, session_id, action)
        dice = step.get("dice")
        if dice is not None:
            _inject_roll(client, session_id, (int(dice[0]), int(dice[1])))


def _inject_roll(client: Any, session_id: str, dice: tuple[int, int]) -> None:
    payload = {"session_id": session_id, "dice": [int(dice[0]), int(dice[1])]}
    response = client.post("/session/roll", json=payload)
    if response.status_code != 200:
        raise RuntimeError(
            f"failed to inject roll {dice}: status={response.status_code}, body={response.text}"
        )


def _run_single_scenario(client: Any, scenario: Scenario, seed: int) -> dict:
    start_payload = {"seed": seed}
    start_resp = client.post("/session/start", json=start_payload)
    start_resp.raise_for_status()
    start_data = start_resp.json()
    session_id = start_data["session_id"]

    session_state = SESSION_STORE.ensure(session_id)
    session_obj: Session = session_state["session"]
    player = _ensure_player(session_obj)
    player.bets.clear()

    bankroll = scenario["pre_state"].get("bankroll")
    if bankroll is not None:
        player.bankroll = float(bankroll)

    for action in scenario["pre_state"].get("existing_bets", []):
        _apply_pre_action(client, session_id, action)

    for dice in scenario["pre_state"].get("rolls_before", []):
        _inject_roll(client, session_id, tuple(dice))

    setup_steps = scenario["pre_state"].get("setup_steps", []) or []
    if setup_steps:
        _execute_setup_steps(client, session_id, setup_steps)

    before_snapshot = session_obj.snapshot()
    before_bankroll = float(before_snapshot.get("bankroll", 0.0))
    before_bets = _normalize_bets(before_snapshot.get("bets", []))

    payload = {
        "verb": scenario["verb"],
        "args": scenario["args"],
        "session_id": session_id,
    }
    response = client.post("/apply_action", json=payload)

    if response.status_code == 200:
        result = "ok"
        error_code = None
    else:
        result = "error"
        try:
            error_code = response.json().get("code")
        except ValueError:  # pragma: no cover - defensive
            error_code = None

    after_snapshot = session_obj.snapshot()
    after_bankroll = float(after_snapshot.get("bankroll", 0.0))
    after_bets = _normalize_bets(after_snapshot.get("bets", []))

    return {
        "scenario": scenario["label"],
        "verb": scenario["verb"],
        "args": scenario["args"],
        "result": result,
        "error_code": error_code,
        "before_bankroll": before_bankroll,
        "after_bankroll": after_bankroll,
        "bets_before": before_bets,
        "bets_after": after_bets,
    }


def _ensure_output_dirs(*paths: Path) -> None:
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, data: Any) -> None:
    _ensure_output_dirs(path)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_markdown(path: Path, journal: list[dict]) -> None:
    _ensure_output_dirs(path)
    total = len(journal)
    ok_count = sum(1 for entry in journal if entry["result"] == "ok")
    error_count = total - ok_count
    scenario_lookup = {scenario["label"]: scenario for scenario in SCENARIOS}

    lines = ["# CrapsSim API Surface Stress Report", ""]
    lines.append("## Summary")
    lines.append("")
    lines.append(f"* Total scenarios: **{total}**")
    lines.append(f"* Successful actions: **{ok_count}**")
    lines.append(f"* Errors: **{error_count}**")
    lines.append("")

    lines.append("## Scenario Results")
    lines.append("")
    lines.append("| Scenario | Verb | Result | Error Code | Expected |")
    lines.append("| --- | --- | --- | --- | --- |")
    for entry in journal:
        expected = scenario_lookup.get(entry["scenario"], {}).get("expect", {})
        expected_desc = expected.get("result")
        expected_code = expected.get("error_code")
        if expected_code:
            expected_desc = f"{expected_desc} ({expected_code})"
        lines.append(
            "| {scenario} | {verb} | {result} | {error_code} | {expected} |".format(
                scenario=entry["scenario"],
                verb=entry["verb"],
                result=entry["result"],
                error_code=entry["error_code"] or "",
                expected=expected_desc or "",
            )
        )
    lines.append("")

    lines.append("## Full Journal")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(journal, indent=2, sort_keys=True))
    lines.append("```")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    *,
    limit: int | None = None,
    json_path: Path = DEFAULT_JSON,
    markdown_path: Path = DEFAULT_MARKDOWN,
) -> list[dict]:
    TestClient = _require_test_client()
    app = create_app()
    client = TestClient(app)

    scenarios: Iterable[Scenario]
    if limit is not None:
        scenarios = SCENARIOS[:limit]
    else:
        scenarios = SCENARIOS

    journal: list[dict] = []
    for idx, scenario in enumerate(scenarios):
        seed = 10_000 + idx
        entry = _run_single_scenario(client, scenario, seed)
        journal.append(entry)

    _write_json(json_path, journal)
    _write_markdown(markdown_path, journal)
    return journal


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Run the CrapsSim API stress scenarios"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of scenarios to execute",
    )
    parser.add_argument(
        "--json", type=Path, default=DEFAULT_JSON, help="Path to write the JSON journal"
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        default=DEFAULT_MARKDOWN,
        help="Path to write the markdown report",
    )
    args = parser.parse_args()

    run(limit=args.limit, json_path=args.json, markdown_path=args.markdown)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
