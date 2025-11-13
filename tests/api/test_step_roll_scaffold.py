import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

try:
    from fastapi import FastAPI
except Exception:  # pragma: no cover
    FastAPI = None

try:
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    TestClient = None

from crapssim_api.http import router

if TestClient is None or FastAPI is None:
    pytest.skip("fastapi not installed", allow_module_level=True)

app = FastAPI()
if router is not None:
    app.include_router(router)
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
    if snap["puck"] == "ON":
        assert snap["point"] == sum(snap["dice"])
    else:
        assert snap["point"] is None
