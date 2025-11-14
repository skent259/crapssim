"""
Minimal example client for the CrapsSim HTTP API.

This script assumes:

- the FastAPI app is running locally, e.g.:

    uvicorn crapssim_api.http:app --reload

- the API implements the endpoints used below:
    - GET  /health
    - GET  /capabilities
    - POST /session/start
    - POST /session/apply_action
    - POST /session/roll

The goal is to demonstrate end-to-end usage:
    1. check health
    2. read capabilities
    3. start a seeded session
    4. place a simple Pass Line bet
    5. roll once and print the result
"""

from __future__ import annotations

import json
from typing import Any, Dict

import httpx

BASE_URL = "http://127.0.0.1:8000"


def pretty(label: str, payload: Any) -> None:
    print(f"\n=== {label} ===")
    print(json.dumps(payload, indent=2, sort_keys=True))


def get_health(client: httpx.Client) -> Dict[str, Any]:
    resp = client.get("/health")
    resp.raise_for_status()
    data = resp.json()
    pretty("health", data)
    return data


def get_capabilities(client: httpx.Client) -> Dict[str, Any]:
    resp = client.get("/capabilities")
    resp.raise_for_status()
    data = resp.json()
    pretty("capabilities", data)
    return data


def start_session(client: httpx.Client, seed: int = 12345) -> str:
    payload: Dict[str, Any] = {
        "seed": seed,
        "profile_id": "default",
    }
    resp = client.post("/session/start", json=payload)
    resp.raise_for_status()
    data = resp.json()
    pretty("session/start", data)

    # The exact path to session id is defined by the API schema.
    # Adjust this if your schema differs.
    session = data.get("session") or data
    session_id = session.get("id") or session.get("session_id")
    if not session_id:
        raise RuntimeError(f"Could not find session id in response: {data}")
    return str(session_id)


def apply_passline_bet(client: httpx.Client, session_id: str, amount: int = 10) -> None:
    payload: Dict[str, Any] = {
        "session_id": session_id,
        "actions": [
            {
                "type": "place_bet",
                "bet": "PassLine",
                "amount": amount,
                "player_id": 0,
            }
        ],
    }
    resp = client.post("/session/apply_action", json=payload)
    resp.raise_for_status()
    data = resp.json()
    pretty("session/apply_action (PassLine)", data)


def roll_once(client: httpx.Client, session_id: str) -> None:
    payload: Dict[str, Any] = {
        "session_id": session_id,
        # Optionally include explicit dice for deterministic testing:
        # "dice": [3, 4],
    }
    resp = client.post("/session/roll", json=payload)
    resp.raise_for_status()
    data = resp.json()
    pretty("session/roll", data)


def main() -> None:
    with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
        get_health(client)
        get_capabilities(client)

        session_id = start_session(client, seed=4242)
        print(f"\nSession started with id: {session_id}")

        apply_passline_bet(client, session_id, amount=10)
        roll_once(client, session_id)


if __name__ == "__main__":
    main()
