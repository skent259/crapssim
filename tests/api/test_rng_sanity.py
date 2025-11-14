import pytest

pytest.importorskip("pydantic")

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    FastAPI = None  # type: ignore[assignment]
    TestClient = None  # type: ignore[assignment]

from crapssim_api.http import router

if FastAPI is None or TestClient is None or router is None:  # pragma: no cover - optional deps
    pytest.skip("fastapi not installed", allow_module_level=True)

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def _start_session(seed: int) -> str:
    resp = client.post("/session/start", json={"seed": seed})
    assert resp.status_code == 200
    return resp.json()["session_id"]


def _roll_sequence(session_id: str, n: int) -> list[tuple[int, int]]:
    results: list[tuple[int, int]] = []
    for _ in range(n):
        resp = client.post("/session/roll", json={"session_id": session_id})
        assert resp.status_code == 200
        snap = resp.json()["snapshot"]
        results.append(tuple(int(v) for v in snap["dice"]))
    return results


def test_rolls_advance_within_session():
    session_id = _start_session(seed=12345)
    dice_pairs = _roll_sequence(session_id, 10)

    assert len(set(dice_pairs)) > 1, f"All rolls were identical: {dice_pairs}"
    for d1, d2 in dice_pairs:
        assert 1 <= d1 <= 6
        assert 1 <= d2 <= 6


def test_same_seed_restarts_deterministic_sequence():
    seed = 777
    first = _roll_sequence(_start_session(seed), 6)
    second = _roll_sequence(_start_session(seed), 6)
    assert first == second
