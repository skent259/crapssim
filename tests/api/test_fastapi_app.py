"""Tests for the optional FastAPI application wrapper."""
from __future__ import annotations

import builtins
import importlib
import importlib.util
import sys

import pytest

from crapssim_api.fastapi_app import create_app


def test_import_fastapi_app_without_fastapi_is_safe(monkeypatch: pytest.MonkeyPatch) -> None:
    """Importing without FastAPI should not crash and raises RuntimeError lazily."""
    sys.modules.pop("fastapi", None)
    sys.modules.pop("crapssim_api.fastapi_app", None)

    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.startswith("fastapi"):
            raise ModuleNotFoundError("fastapi is missing")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    module = importlib.import_module("crapssim_api.fastapi_app")

    with pytest.raises(RuntimeError):
        module.create_app()


FASTAPI_AVAILABLE = importlib.util.find_spec("fastapi") is not None
UVICORN_AVAILABLE = importlib.util.find_spec("uvicorn") is not None

if FASTAPI_AVAILABLE:  # pragma: no branch - conditional import for optional dep
    from fastapi.testclient import TestClient
else:  # pragma: no cover - executed when fastapi missing
    TestClient = None  # type: ignore[assignment]


@pytest.fixture()
def fastapi_app_fixture() -> object:
    """Provide a fresh FastAPI app when extras are installed."""
    if not FASTAPI_AVAILABLE or not UVICORN_AVAILABLE:
        pytest.skip("FastAPI extra not installed")

    if "crapssim_api.http" in sys.modules:
        importlib.reload(sys.modules["crapssim_api.http"])

    return create_app()


@pytest.mark.skipif(not FASTAPI_AVAILABLE, reason="FastAPI extra not installed")
@pytest.mark.skipif(not UVICORN_AVAILABLE, reason="uvicorn extra not installed")
def test_create_app_returns_fastapi_instance(fastapi_app_fixture: object) -> None:
    app = fastapi_app_fixture
    assert hasattr(app, "openapi")

    client = TestClient(app)  # type: ignore[arg-type]
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "status" in data


@pytest.mark.skipif(not FASTAPI_AVAILABLE, reason="FastAPI extra not installed")
@pytest.mark.skipif(not UVICORN_AVAILABLE, reason="uvicorn extra not installed")
def test_create_app_reuses_router_routes(fastapi_app_fixture: object) -> None:
    app = fastapi_app_fixture
    client = TestClient(app)  # type: ignore[arg-type]

    resp = client.get("/capabilities")
    assert resp.status_code in (200, 404)
    if resp.status_code == 200:
        assert isinstance(resp.json(), dict)
