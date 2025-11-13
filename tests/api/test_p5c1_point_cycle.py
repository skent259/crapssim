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


def _roll(session_id, dice):
    r = client.post("/step_roll", json={"session_id": session_id, "mode": "inject", "dice": dice})
    assert r.status_code == 200
    return r.json()


def test_point_set_from_off():
    j = _roll("pc1", [2, 2])  # total 4
    assert j["puck"] == "ON" and j["point"] == 4
    types = [e["type"] for e in j["events"]]
    assert "point_set" in types


def test_naturals_do_not_set_point_on_comeout():
    j = _roll("pc2", [3, 4])  # 7
    assert j["puck"] == "OFF" and j["point"] is None
    types = [e["type"] for e in j["events"]]
    assert "point_set" not in types

    j = _roll("pc2", [5, 6])  # 11
    assert j["puck"] == "OFF" and j["point"] is None


def test_craps_do_not_set_point_on_comeout():
    for d in ([1, 1], [1, 2], [6, 6]):  # 2,3,12
        j = _roll("pc3", d)
        assert j["puck"] == "OFF" and j["point"] is None


def test_point_made_ends_hand_and_increments_hand_id():
    s = "pc4"
    a = _roll(s, [3, 1])  # 4 sets point
    assert a["puck"] == "ON" and a["point"] == 4
    pre_hand = a["hand_id"]

    b = _roll(s, [2, 2])  # hit the point
    assert b["puck"] == "OFF" and b["point"] is None
    assert b["hand_id"] == pre_hand + 1
    types = [e["type"] for e in b["events"]]
    assert "point_made" in types and "hand_ended" in types


def test_seven_out_ends_hand_and_increments_hand_id():
    s = "pc5"
    a = _roll(s, [3, 1])  # 4 sets point
    pre_hand = a["hand_id"]
    b = _roll(s, [4, 3])  # 7-out
    assert b["puck"] == "OFF" and b["point"] is None
    assert b["hand_id"] == pre_hand + 1
    types = [e["type"] for e in b["events"]]
    assert "seven_out" in types and "hand_ended" in types


def test_event_hand_id_belongs_to_ending_hand():
    s = "pc6"
    a = _roll(s, [3, 1])  # set 4
    pre_hand = a["hand_id"]
    b = _roll(s, [2, 2])  # make point
    # The 'hand_ended' event should reference pre_hand, while snapshot is next hand
    ended = [e for e in b["events"] if e["type"] == "hand_ended"][0]
    assert ended["hand_id"] == pre_hand
    assert b["hand_id"] == pre_hand + 1
