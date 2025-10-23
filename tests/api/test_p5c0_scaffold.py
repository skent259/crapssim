from fastapi import FastAPI
from fastapi.testclient import TestClient

from crapssim_api.http import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_step_roll_snapshot_contains_hand_fields():
    response = client.post(
        "/step_roll", json={"session_id": "hsc1", "mode": "inject", "dice": [2, 3]}
    )
    payload = response.json()
    assert "hand_id" in payload and "puck" in payload and "point" in payload
    assert payload["puck"] in ("ON", "OFF")
    assert payload["point"] in (None, 4, 5, 6, 8, 9, 10)


def test_p5c0_does_not_change_prior_behavior():
    first = client.post("/step_roll", json={"session_id": "hsc2", "mode": "auto"}).json()
    second = client.post("/step_roll", json={"session_id": "hsc2", "mode": "auto"}).json()

    assert first["puck"] == second["puck"] == "OFF"
    assert first["point"] is None and second["point"] is None
    assert second["roll_seq"] == first["roll_seq"] + 1


def test_session_store_isolation_by_session_id():
    a = client.post(
        "/step_roll", json={"session_id": "sA", "mode": "inject", "dice": [1, 1]}
    ).json()
    b = client.post(
        "/step_roll", json={"session_id": "sB", "mode": "inject", "dice": [6, 6]}
    ).json()

    assert a["session_id"] != b["session_id"]
    assert a["roll_seq"] == 1 and b["roll_seq"] == 1
