"""Optional FastAPI application for the CrapsSim API."""
from __future__ import annotations

from importlib import reload
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - typing helper only
    from fastapi import FastAPI


def _require_fastapi() -> "FastAPI":
    """Import FastAPI lazily, raising a helpful error when unavailable."""
    try:
        from fastapi import FastAPI  # type: ignore[import-not-found]
    except Exception as exc:  # pragma: no cover - exercised via tests
        raise RuntimeError(
            "FastAPI is not installed. Install with `pip install crapssim[api]` "
            "to use the optional FastAPI app."
        ) from exc
    return FastAPI


def create_app() -> "FastAPI":
    """Create a FastAPI app exposing the existing HTTP routes."""
    FastAPI = _require_fastapi()
    from . import http

    router = getattr(http, "router", None)
    if router is None:
        # Re-import the HTTP module now that FastAPI is available. This mirrors
        # the module's behavior when FastAPI was missing the first time it was
        # imported, ensuring the real router is created when possible.
        http_module = reload(http)
        router = getattr(http_module, "router", None)

    if router is None:
        raise RuntimeError("FastAPI router is unavailable; cannot create app.")

    app = FastAPI(title="CrapsSim API", version="0.1.0")
    app.include_router(router)
    return app


def main() -> None:
    """Run the optional FastAPI app using uvicorn."""
    try:
        import uvicorn  # type: ignore[import-not-found]
    except Exception as exc:  # pragma: no cover - exercised via tests
        raise RuntimeError(
            "uvicorn is not installed. Install with `pip install crapssim[api]` "
            "to run the FastAPI app."
        ) from exc

    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":  # pragma: no cover - module CLI pattern
    main()
