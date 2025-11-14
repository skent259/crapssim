import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

try:
    from fastapi.testclient import TestClient
except ModuleNotFoundError:  # pragma: no cover - optional fastapi
    TestClient = None  # type: ignore[assignment]


@pytest.mark.skipif(TestClient is None, reason="fastapi not installed")
def test_capabilities_contract() -> None:
    from crapssim_api.http import create_app

    app = create_app()
    client = TestClient(app)

    r_health = client.get("/health")
    assert r_health.status_code == 200
    health_body = r_health.json()
    assert health_body.get("status") == "ok"

    r_caps = client.get("/capabilities")
    assert r_caps.status_code == 200
    caps = r_caps.json()

    assert "bets" in caps
    assert "supported" in caps["bets"]
    assert isinstance(caps["bets"]["supported"], list)
    assert "PassLine" in caps["bets"]["supported"]

    assert "table" in caps
    table = caps["table"]
    assert "buy_vig_on_win" in table
    assert "vig_rounding" in table
    assert "vig_floor" in table
