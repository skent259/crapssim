import pytest

pytest.importorskip("pydantic")

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    FastAPI = None  # type: ignore[assignment]
    TestClient = None  # type: ignore[assignment]

from crapssim_api.http import router  # reuse the existing router


@pytest.mark.skipif(
    FastAPI is None or TestClient is None, reason="FastAPI not installed"
)
def test_replay_tape_round_trip():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    # 1) Start a session with tape recording enabled.
    start_resp = client.post(
        "/session/start",
        json={
            "seed": 12345,
            "record_tape": True,
            "table_spec": {},
            "initial_bankroll": 250.0,
        },
    )
    assert start_resp.status_code == 200
    start_payload = start_resp.json()
    session_id = start_payload["session_id"]

    # 2) Drive a small deterministic sequence of actions + rolls.
    step_resp = client.post(
        f"/session/{session_id}/step",
        json={
            "dice": [3, 2],
            "actions": [
                {"verb": "pass_line", "amount": 10},
            ],
        },
    )
    assert step_resp.status_code == 200

    step_resp = client.post(
        f"/session/{session_id}/step",
        json={
            "dice": [4, 1],
            "actions": [],
        },
    )
    assert step_resp.status_code == 200

    final_state = step_resp.json()["state"]

    # 3) Export the tape.
    tape_resp = client.get(f"/session/{session_id}/tape")
    assert tape_resp.status_code == 200
    tape = tape_resp.json()

    assert tape["final_state"]  # final_state captured
    assert tape["steps"], "tape should contain at least one step"

    # 4) Replay the tape via the new endpoint.
    replay_resp = client.post("/session/replay", json=tape)
    assert replay_resp.status_code == 200
    replay = replay_resp.json()

    assert replay["deterministic"] is True
    assert replay["mismatch_step"] is None
    assert replay["original_final_state"] == tape["final_state"]
    assert replay["replay_final_state"] == tape["final_state"]
    assert replay["replay_final_state"] == final_state
