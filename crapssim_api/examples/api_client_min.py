"""Minimal HTTP client demo for CrapsSim.

See ``crapssim_api/docs/API_VERBS.md`` for verb documentation and
``crapssim_api/docs/dev/`` for deeper stress/sequence reports.

Run the FastAPI app locally (for example ``uvicorn crapssim_api.http:app --reload``)
before executing this script.
"""

from __future__ import annotations

import json
from typing import Any, Dict

import httpx

BASE_URL = "http://127.0.0.1:8000"


def pretty(label: str, payload: Any) -> None:
    print(f"\n=== {label} ===")
    print(json.dumps(payload, indent=2, sort_keys=True))


def start_session(client: httpx.Client, *, seed: int = 4242) -> Dict[str, Any]:
    resp = client.post("/session/start", json={"seed": seed})
    resp.raise_for_status()
    data = resp.json()
    pretty("session/start", data)
    return data


def apply_action(client: httpx.Client, session_id: str, verb: str, args: Dict[str, Any]) -> Dict[str, Any]:
    resp = client.post(
        "/apply_action",
        json={"session_id": session_id, "verb": verb, "args": args},
    )
    resp.raise_for_status()
    data = resp.json()
    summary = data.get("effect_summary", {})
    pretty(f"apply_action → {verb}", summary)
    return data


def roll_once(client: httpx.Client, session_id: str, dice: list[int]) -> Dict[str, Any]:
    resp = client.post("/session/roll", json={"session_id": session_id, "dice": dice})
    resp.raise_for_status()
    data = resp.json()
    pretty("session/roll", data)
    return data


def step_auto(client: httpx.Client, session_id: str) -> Dict[str, Any]:
    resp = client.post("/step_roll", json={"session_id": session_id, "mode": "auto"})
    resp.raise_for_status()
    snapshot = resp.json()
    pretty(
        "step_roll",
        {
            "bankroll_after": snapshot.get("bankroll_after"),
            "bets": snapshot.get("bets", []),
            "dice": snapshot.get("dice"),
        },
    )
    return snapshot


def handle_error(response: httpx.Response) -> None:
    details = {
        "status": response.status_code,
        "body": response.json(),
    }
    pretty("apply_action error", details)


def main() -> None:
    with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
        session_data = start_session(client, seed=2025)
        session_id = session_data.get("session_id")
        if not session_id:
            raise RuntimeError(f"Unexpected session payload: {session_data}")

        # Pass Line on the come-out roll
        apply_action(client, session_id, "pass_line", {"amount": 10})

        # Establish the point with deterministic dice
        roll_once(client, session_id, dice=[2, 2])

        # Add a Place bet and odds behind the Pass Line
        apply_action(client, session_id, "place", {"number": 6, "amount": 30})
        apply_action(client, session_id, "odds", {"base": "pass_line", "amount": 20})

        # Take an automatic roll and display bankroll/bets after the outcome
        step_auto(client, session_id)

        # Use a management verb to clear removable bets
        apply_action(client, session_id, "clear_all_bets", {})

        # Demonstrate error handling with an intentionally oversized bet
        resp = client.post(
            "/apply_action",
            json={"session_id": session_id, "verb": "pass_line", "args": {"amount": 5000}},
        )
        if resp.status_code >= 400:
            handle_error(resp)
        else:
            pretty("unexpected success", resp.json())


if __name__ == "__main__":
    main()
