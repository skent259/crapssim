from crapssim_api.version import ENGINE_API_VERSION, CAPABILITIES_SCHEMA_VERSION, get_identity
from crapssim_api.http import create_app


def test_constants_types():
    assert isinstance(ENGINE_API_VERSION, str)
    assert isinstance(CAPABILITIES_SCHEMA_VERSION, int)
    ident = get_identity()
    assert ident["engine_api_version"] == ENGINE_API_VERSION
    assert ident["capabilities_schema_version"] == CAPABILITIES_SCHEMA_VERSION


def test_healthz_reports_identity():
    app = create_app()
    if hasattr(app, "openapi_url"):  # FastAPI path
        from fastapi.testclient import TestClient
        client = TestClient(app)
        r = client.get("/healthz")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert data["engine_api_version"] == ENGINE_API_VERSION
        assert data["capabilities_schema_version"] == CAPABILITIES_SCHEMA_VERSION
    else:
        # Minimal ASGI fallback responds with plain text
        # Simulate minimal scope to ensure callable
        assert callable(app)
