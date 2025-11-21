import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from crapssim_api.http import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)


def _start_session(client: TestClient, seed: int = 1234) -> str:
    resp = client.post("/session/start", json={"seed": seed})
    assert resp.status_code == 200
    payload = resp.json()
    return payload["session_id"]


def _place_pass_line(client: TestClient, session_id: str, amount: float = 15.0) -> None:
    resp = client.post(
        "/apply_action",
        json={"session_id": session_id, "verb": "pass_line", "args": {"amount": amount}},
    )
    assert resp.status_code == 200


def test_session_state_snapshot(client: TestClient):
    session_id = _start_session(client)
    _place_pass_line(client, session_id, amount=15.0)

    resp = client.get(f"/session/{session_id}/state")
    assert resp.status_code == 200
    state = resp.json()

    assert state["session_id"] == session_id
    assert state["state_schema"] == "1.0"
    assert state["bankroll"] == pytest.approx(985.0)
    assert state["roll_index"] == 0
    assert state["hand_index"] == 1
    assert state["last_roll"] is None

    assert any(bet["type"] == "PassLine" for bet in state["bets"])
    for bet in state["bets"]:
        assert set(bet.keys()) >= {"type", "number", "amount"}

    assert state["point"] is None
    assert state["determinism_contract"] == "v1.0"


def test_invalid_session_state_returns_404(client: TestClient):
    resp = client.get("/session/does-not-exist/state")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Unknown session_id"
