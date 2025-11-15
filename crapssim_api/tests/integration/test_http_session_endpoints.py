import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

try:
    from crapssim_api.http import app
    from fastapi.testclient import TestClient
    fast = True
except Exception:
    fast = False


@pytest.mark.skipif(not fast, reason="FastAPI not installed")
def test_http_session_endpoints():
    client = TestClient(app)
    r = client.post("/session/start", json={"seed": 314})
    assert r.status_code == 200
    payload = r.json()
    session_id = payload["session_id"]
    assert payload["snapshot"]["identity"]["seed"] == 314

    r2 = client.post("/session/roll", json={"session_id": session_id, "dice":[4,3]})
    assert r2.status_code == 200
    assert r2.json()["snapshot"]["dice"] == [4, 3]

    r3 = client.post("/session/roll", json={"session_id": session_id})
    assert r3.status_code == 200
    snap = r3.json()["snapshot"]
    assert snap["session_id"] == session_id
    assert snap["roll_seq"] == 2


