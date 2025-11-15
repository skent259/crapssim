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


def test_auto_roll_advances_rng():
    body = {"session_id": "seedtest", "mode": "auto"}
    rolls = []
    for _ in range(5):
        rolls.append(client.post("/step_roll", json=body).json())

    seq_values = [tuple(r["dice"]) for r in rolls]
    assert len(set(seq_values)) > 1, f"expected varied dice, got {seq_values}"
    assert [r["roll_seq"] for r in rolls] == list(range(1, 6))


def test_no_state_mutations_yet():
    body = {"session_id": "stable", "mode": "auto"}
    r = client.post("/step_roll", json=body)
    snap = r.json()
    assert snap["bankroll_after"] == "1000.00"
    if snap["puck"] == "ON":
        assert snap["point"] == sum(snap["dice"])
    else:
        assert snap["point"] is None
