import pytest
from fastapi.testclient import TestClient
from crapssim_api.http import router

app = None
for r in [router]:
    if hasattr(r, "routes"):
        from fastapi import FastAPI
        app = FastAPI()
        app.include_router(r)
        break
client = TestClient(app)


def test_inject_valid_dice_reflected():
    body = {"session_id": "s1", "mode": "inject", "dice": [3, 4]}
    res = client.post("/step_roll", json=body)
    data = res.json()
    assert res.status_code == 200
    assert data["dice"] == [3, 4]
    assert data["roll_seq"] == 1


def test_inject_rejects_out_of_range():
    body = {"session_id": "s2", "mode": "inject", "dice": [0, 7]}
    r = client.post("/step_roll", json=body)
    assert r.status_code == 422


def test_auto_determinism_same_seed():
    body = {"session_id": "seedtest", "mode": "auto"}
    res1 = client.post("/step_roll", json=body).json()
    res2 = client.post("/step_roll", json=body).json()
    assert res1["dice"] == res2["dice"]
    assert res1["roll_seq"] + 1 == res2["roll_seq"]


def test_no_state_mutations_yet():
    body = {"session_id": "stable", "mode": "auto"}
    r = client.post("/step_roll", json=body)
    snap = r.json()
    assert snap["bankroll_after"] == "1000.00"
    assert snap["point"] is None
