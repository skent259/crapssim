# Optional CrapsSim HTTP API Overview

## Intro

`crapssim_api` is an optional, lightweight HTTP wrapper around the core
CrapsSim engine. You can run every simulation entirely locally without it; the
API only exists to expose simple "handles" for tools such as CSC automations,
Node-RED flows, or custom dashboards. By design the server stays low-bloat—there
is no extra analytics layer, no background schedulers, and no new game
logic—just straightforward request/response I/O around the simulator state.

## Installation / Extras

The base `crapssim` package installs only the core engine. To enable the HTTP
surface and its tests you need the optional FastAPI stack. Install the published
extras together with a lightweight ASGI server:

```bash
pip install "crapssim[api]"
```

The `[api]` extra bundles the API dependencies (FastAPI, pydantic, uvicorn). You
may also install the individual packages manually if you prefer. Without these
extras the core engine continues to work, but the HTTP app and its tests are
unavailable.

## Starting the Server

The HTTP application is exposed via an app factory. Launch it with any ASGI
server that supports FastAPI. Typical development commands:

```bash
uvicorn crapssim_api.fastapi_app:create_app --factory --reload

# or

python -m crapssim_api.fastapi_app
```

Unless you pass different parameters, uvicorn binds to `http://127.0.0.1:8000`.
The API is opt-in: nothing starts automatically, and the core simulator runs as
usual unless you launch the server yourself.

## Endpoint Overview

| Method | Path | Purpose | Auth |
| --- | --- | --- | --- |
| GET | `/health` | Basic liveness probe that returns `{ "status": "ok" }`. | none |
| GET | `/healthz` | Liveness plus identity metadata from `crapssim_api.version.get_identity()`. | none |
| GET | `/capabilities` | Exposes the engine capability payload used by clients to discover supported bets and limits. | none |
| POST | `/start_session` | Creates a deterministic session snapshot and returns a `session_id` plus table state and capability data. | none |
| POST | `/end_session` | Stub session end hook that currently reports `{"hands": 0, "rolls": 0}`. | none |
| POST | `/apply_action` | Validates a betting verb/arguments pair against table rules and echoes the effect summary (no actual bankroll math yet). | none |
| POST | `/step_roll` | Advances a session by one roll in `auto` or `inject` mode and streams the resulting events/snapshot. | none |
| POST | `/session/start` | Starts the simplified in-memory `Session` helper used by the `/session/*` testing routes. | none |
| POST | `/session/roll` | Performs a roll on the helper session, optionally with injected dice, and returns the resulting event. | none |
| GET | `/session/state` | Returns the helper session snapshot produced by `Session.snapshot()`. | none |
| POST | `/session/stop` | Stops the helper session and releases its resources. | none |

## Example Usage (curl)

Check that the server is up:

```bash
curl http://127.0.0.1:8000/health
```

Start a deterministic session and capture the returned `session_id`:

```bash
curl -X POST http://127.0.0.1:8000/start_session \
  -H "content-type: application/json" \
  -d '{"spec": {"table_profile": "vanilla-default"}, "seed": 42}'
```

Advance the session once with automatic dice, then inject a specific roll:

```bash
curl -X POST http://127.0.0.1:8000/step_roll \
  -H "content-type: application/json" \
  -d '{"session_id": "<session_id>", "mode": "auto"}'

curl -X POST http://127.0.0.1:8000/step_roll \
  -H "content-type: application/json" \
  -d '{"session_id": "<session_id>", "mode": "inject", "dice": [3, 4]}'
```

Fetch the lightweight capability summary for client-side introspection:

```bash
curl http://127.0.0.1:8000/capabilities
```

For the helper session routes, first create an in-memory session and then poll
its state:

```bash
curl -X POST http://127.0.0.1:8000/session/start
curl http://127.0.0.1:8000/session/state
```

## Python Client Example (TestClient)

```python
try:
    from fastapi.testclient import TestClient
except ImportError as exc:  # pragma: no cover - FastAPI optional
    raise SystemExit(
        "Install the optional API extras to run this snippet: pip install \"crapssim[api]\""
    ) from exc

from crapssim_api.http import create_app

app = create_app()
client = TestClient(app)

health = client.get("/health").json()
print(health)

start = client.post("/start_session", json={"spec": {}, "seed": 0}).json()
print(start["session_id"])

roll = client.post(
    "/step_roll",
    json={"session_id": start["session_id"], "mode": "auto"},
).json()
print(roll["dice"], roll["events"][-1])
```

## Design Philosophy / Constraints

The optional HTTP layer never mutates the underlying CrapsSim engine—it wraps
existing objects and exposes their state. The API does not calculate analytics
such as ROI, drawdown, or streaks; callers remain responsible for higher-level
statistics. Keeping the surface area "dumb" ensures that external tools own
presentation and analysis while the simulator stays the single source of truth
for craps rules and hand evolution. The routes aim to be stable enough for
automation, yet thin enough that all substantive game logic continues to live in
`crapssim` proper.
