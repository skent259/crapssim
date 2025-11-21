import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from crapssim_api.http import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)


def _start_session(client: TestClient, bankroll: float = 1000.0) -> str:
    resp = client.post("/session/start", json={"initial_bankroll": bankroll, "seed": 111})
    assert resp.status_code == 200
    payload = resp.json()
    return payload["session_id"]


def _place_pass_line(client: TestClient, session_id: str, amount: float = 10.0) -> None:
    resp = client.post(
        "/apply_action",
        json={"session_id": session_id, "verb": "pass_line", "args": {"amount": amount}},
    )
    assert resp.status_code == 200


def _roll(client: TestClient, session_id: str, dice: list[int]) -> None:
    resp = client.post("/session/roll", json={"session_id": session_id, "dice": dice})
    assert resp.status_code == 200


def test_session_metrics_summary(client: TestClient):
    session_id = _start_session(client, bankroll=1000.0)
    _place_pass_line(client, session_id, amount=10.0)

    _roll(client, session_id, [3, 3])
    _roll(client, session_id, [2, 4])

    resp = client.get(f"/session/{session_id}/metrics")
    assert resp.status_code == 200
    metrics = resp.json()

    bankroll = metrics["bankroll"]
    assert bankroll["start"] == pytest.approx(1000.0)
    assert bankroll["current"] == pytest.approx(1010.0)
    assert bankroll["net"] == pytest.approx(10.0)
    assert bankroll["roi"] == pytest.approx(0.01)

    assert metrics["metrics_schema"] == "1.0"
    assert metrics["rolls"]["total"] == 2
    assert metrics["hands"]["total"] == 2
    assert metrics["hands"]["completed"] == 1
    assert metrics["determinism_contract"] == "v1.0"
    assert metrics["by_bet_type"] == []


def test_state_and_metrics_are_observers_only(client: TestClient):
    session_id = _start_session(client, bankroll=750.0)
    _place_pass_line(client, session_id, amount=25.0)

    state_before = client.get(f"/session/{session_id}/state").json()
    metrics_before = client.get(f"/session/{session_id}/metrics").json()

    state_after = client.get(f"/session/{session_id}/state").json()
    metrics_after = client.get(f"/session/{session_id}/metrics").json()

    assert state_before["bankroll"] == state_after["bankroll"]
    assert state_before["bets"] == state_after["bets"]

    assert metrics_before["bankroll"]["current"] == metrics_after["bankroll"]["current"]
    assert metrics_before["rolls"]["total"] == metrics_after["rolls"]["total"]


def test_invalid_session_metrics_returns_404(client: TestClient):
    resp = client.get("/session/invalid/metrics")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Unknown session_id"
