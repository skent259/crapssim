import pytest

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    FastAPI = None  # type: ignore[assignment]
    TestClient = None  # type: ignore[assignment]

from crapssim_api.http import router

if (
    FastAPI is None or TestClient is None or router is None
):  # pragma: no cover - optional deps
    pytest.skip("fastapi not installed", allow_module_level=True)

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def _start_session(seed: int = 424242):
    resp = client.post("/session/start", json={"seed": seed})
    assert resp.status_code == 200
    data = resp.json()
    return data["session_id"], data["snapshot"]


def _place_pass_line(session_id: str, state: dict[str, object]) -> dict:
    payload = {
        "session_id": session_id,
        "verb": "pass_line",
        "args": {"amount": 10},
        "state": state,
    }
    resp = client.post("/apply_action", json=payload)
    assert resp.status_code == 200
    return resp.json()


def _roll(session_id: str, dice: list[int]) -> dict:
    resp = client.post("/session/roll", json={"session_id": session_id, "dice": dice})
    assert resp.status_code == 200
    return resp.json()["snapshot"]


def _to_float(value):
    if isinstance(value, str):
        return float(value)
    return float(value)


def test_api_pass_line_bet_lifecycle():
    session_id, snap0 = _start_session()
    state = {"puck": snap0["puck"], "point": snap0["point"]}

    apply_resp = _place_pass_line(session_id, state)
    effect = apply_resp["effect_summary"]
    assert effect["applied"] is True
    assert effect["verb"] == "pass_line"
    assert effect["bankroll_delta"] == pytest.approx(-10.0)

    snapshot_after_bet = apply_resp["snapshot"]
    bankroll_after_bet = _to_float(snapshot_after_bet["bankroll_after"])
    assert bankroll_after_bet == pytest.approx(990.0)
    assert any(bet["type"] == "PassLine" for bet in snapshot_after_bet["bets"])

    snap_point = _roll(session_id, [3, 3])
    assert snap_point["point"] == 6
    assert snap_point["puck"] == "ON"
    assert any(bet["type"] == "PassLine" for bet in snap_point["bets"])
    assert _to_float(snap_point["bankroll_after"]) == pytest.approx(bankroll_after_bet)

    snap_resolve = _roll(session_id, [2, 4])
    assert snap_resolve["puck"] == "OFF"
    assert snap_resolve["point"] is None
    assert snap_resolve["bets"] == []
    assert _to_float(snap_resolve["bankroll_after"]) == pytest.approx(1010.0)
