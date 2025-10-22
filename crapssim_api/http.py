from __future__ import annotations


def _minimal_asgi_app():
    # Dependency-free fallback ASGI app (HTTP 200 'OK' on /healthz)
    async def app(scope, receive, send):
        if scope["type"] != "http":
            await send({"type": "http.response.start", "status": 500, "headers": []})
            await send({"type": "http.response.body", "body": b"Unsupported scope"})
            return
        path = scope.get("path", "/")
        if path == "/healthz":
            body = b"ok"
            await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"text/plain")]})
            await send({"type": "http.response.body", "body": body})
        else:
            await send({"type": "http.response.start", "status": 404, "headers": []})
            await send({"type": "http.response.body", "body": b"not found"})

    return app


def create_app():
    """Return an ASGI app. Prefer FastAPI/Starlette if available, otherwise fallback."""
    try:
        from fastapi import FastAPI

        app = FastAPI(title="CrapsSim-Vanilla API (skeleton)", version="0.1.0-api.dev")

        @app.get("/healthz")
        def healthz():
            return {"status": "ok"}

        return app
    except Exception:
        # FastAPI not available; return minimal ASGI app
        return _minimal_asgi_app()


if __name__ == "__main__":
    # Best-effort local run if uvicorn is present
    try:
        import uvicorn  # type: ignore

        uvicorn.run(create_app(), host="127.0.0.1", port=8000)
    except Exception:
        print("Adapter skeleton ready. Install 'fastapi[all]' and 'uvicorn' to run locally.")
