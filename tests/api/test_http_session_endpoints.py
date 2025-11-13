import pytest

try:
    from crapssim_api.http import app
    from fastapi.testclient import TestClient
    fast = True
except Exception:
    fast = False


@pytest.mark.skipif(not fast, reason="FastAPI not installed")
def test_http_session_endpoints():
    client = TestClient(app)
    r = client.post("/session/start")
    assert r.json()["ok"] is True

    r2 = client.post("/session/roll", json={"dice":[4,3]})
    assert r2.json()["event"]["dice"] == [4,3]

    r3 = client.get("/session/state")
    assert r3.json()["ok"] is True


