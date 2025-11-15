"""Minimal HTTP client demo for CrapsSim.

Run this script with a local server listening on ``http://127.0.0.1:8000``::

    uvicorn crapssim_api.http:app --reload

The walkthrough starts a session, establishes a point with fixed dice, adds odds and a place bet, resolves the hand, and shows
the layout clearing verbs. It also demonstrates how errors are returned from the API.
"""

from __future__ import annotations

from typing import Any, Dict

import requests

BASE_URL = "http://127.0.0.1:8000"


def _print_header(title: str) -> None:
    print("\n" + title)
    print("-" * len(title))


def _print_bets(bets: list[Dict[str, Any]]) -> None:
    if not bets:
        print("  Bets: none")
        return

    print("  Bets:")
    for bet in bets:
        parts = [bet.get("type", "?")]
        number = bet.get("number")
        base = bet.get("base")
        if number not in (None, ""):
            parts.append(f"number={number}")
        if base:
            parts.append(f"base={base}")
        amount = float(bet.get("amount", 0.0))
        parts.append(f"amount=${amount:0.2f}")
        print("    - " + ", ".join(parts))


def _print_transition(label: str, before: float, after: float, bets: list[Dict[str, Any]]) -> float:
    _print_header(label)
    print(f"  Bankroll: before ${before:0.2f} → after ${after:0.2f}")
    _print_bets(bets)
    return after


def start_session(client: requests.Session, *, seed: int = 4242) -> tuple[str, float]:
    resp = client.post(f"{BASE_URL}/session/start", json={"seed": seed})
    resp.raise_for_status()
    payload = resp.json()
    snapshot = payload["snapshot"]
    session_id = payload["session_id"]
    bankroll = float(snapshot["bankroll_after"])
    _print_transition("Session started", bankroll, bankroll, snapshot.get("bets", []))
    return session_id, bankroll


def apply_action(
    client: requests.Session, session_id: str, verb: str, args: Dict[str, Any], bankroll: float
) -> tuple[float, Dict[str, Any]]:
    resp = client.post(
        f"{BASE_URL}/apply_action", json={"session_id": session_id, "verb": verb, "args": args}
    )
    resp.raise_for_status()
    payload = resp.json()
    snapshot = payload["snapshot"]
    after = float(snapshot["bankroll_after"])
    new_bankroll = _print_transition(
        f"Applied {verb}", bankroll, after, snapshot.get("bets", [])
    )
    return new_bankroll, payload


def roll_once(
    client: requests.Session, session_id: str, dice: list[int], bankroll: float, label: str
) -> float:
    resp = client.post(
        f"{BASE_URL}/session/roll", json={"session_id": session_id, "dice": dice}
    )
    resp.raise_for_status()
    snapshot = resp.json()["snapshot"]
    after = float(snapshot["bankroll_after"])
    return _print_transition(label, bankroll, after, snapshot.get("bets", []))


def main() -> None:
    with requests.Session() as client:
        client.headers.update({"Accept": "application/json"})

        session_id, bankroll = start_session(client, seed=2025)

        bankroll, _ = apply_action(client, session_id, "pass_line", {"amount": 10}, bankroll)

        bankroll = roll_once(
            client,
            session_id,
            dice=[3, 2],
            bankroll=bankroll,
            label="Come-out roll (point established)",
        )

        bankroll, _ = apply_action(
            client, session_id, "odds", {"base": "pass_line", "amount": 20}, bankroll
        )

        bankroll, _ = apply_action(
            client, session_id, "place", {"number": 6, "amount": 30}, bankroll
        )

        bankroll = roll_once(
            client,
            session_id,
            dice=[2, 3],
            bankroll=bankroll,
            label="Point made (bets resolved)",
        )

        bankroll, _ = apply_action(client, session_id, "clear_all_bets", {}, bankroll)

        # Demonstrate structured error payloads.
        error_resp = client.post(
            f"{BASE_URL}/apply_action",
            json={"session_id": session_id, "verb": "pass_line", "args": {"amount": 5000}},
        )
        _print_header("Intentional error")
        print(f"  HTTP status: {error_resp.status_code}")
        try:
            print(f"  Body: {error_resp.json()}")
        except ValueError:
            print(f"  Raw body: {error_resp.text}")


if __name__ == "__main__":
    main()
