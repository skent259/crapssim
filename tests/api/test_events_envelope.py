import pytest

try:
    from fastapi import FastAPI
except Exception:  # pragma: no cover
    FastAPI = None

try:
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    TestClient = None

from crapssim_api.http import router
from crapssim_api.events import make_event_id

if TestClient is None or FastAPI is None:
    pytest.skip("fastapi not installed", allow_module_level=True)

app = FastAPI()
if router is not None:
    app.include_router(router)
client = TestClient(app)


def test_event_order_and_types():
    r = client.post("/step_roll", json={"session_id": "evt1", "mode": "inject", "dice": [2, 3]})
    assert r.status_code == 200
    ev = r.json()["events"]
    types = [e["type"] for e in ev]
    assert types[:3] == ["hand_started", "roll_started", "roll_completed"]
    assert types[3:] == ["point_set"]


def test_event_ids_are_deterministic():
    a = make_event_id("abc", 1, 1, "roll_completed")
    b = make_event_id("abc", 1, 1, "roll_completed")
    assert a == b and len(a) == 12


def test_event_fields_required():
    r = client.post("/step_roll", json={"session_id": "evt2", "mode": "inject", "dice": [4, 4]})
    e = r.json()["events"][0]
    for key in [
        "type",
        "id",
        "ts",
        "hand_id",
        "roll_seq",
        "bankroll_before",
        "bankroll_after",
        "data",
    ]:
        assert key in e


def test_roll_started_mode_reflects_request():
    r = client.post("/step_roll", json={"session_id": "evt3", "mode": "inject", "dice": [1, 6]})
    evs = r.json()["events"]
    mode_event = next(e for e in evs if e["type"] == "roll_started")
    assert mode_event["data"]["mode"] == "inject"


def test_bankroll_fields_consistent():
    r = client.post("/step_roll", json={"session_id": "evt4", "mode": "auto"})
    e = r.json()["events"][0]
    assert e["bankroll_before"] == e["bankroll_after"] == "1000.00"
