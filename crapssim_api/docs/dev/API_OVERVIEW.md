# CrapsSim API Overview (`crapssim_api`)

This package provides an **optional HTTP API layer** on top of the core `crapssim` engine. It is designed as a small, additive convenience for tools like CrapsSim-Control (CSC) and other external clients that want to drive the engine over HTTP, without changing how the core engine works.

The intent is:

- Keep `crapssim` as the **source of truth** for rules, payouts, and table behavior.
- Make the API **opt-in** and lightweight.
- Avoid adding analytics or “smart” features that belong in downstream tools.

If you never import `crapssim_api` or install the `api` extra, nothing about the core engine changes.

---

## Installation

The API layer is exposed as an **optional extra**. To install the core engine only:

```bash
pip install crapssim

To install the engine plus the HTTP API dependencies (FastAPI / Pydantic and friends):

pip install "crapssim[api]"

The extra is named api so it remains clearly separated from the core runtime.

⸻

High-Level Structure

The main modules in the API package are:
•crapssim_api.http
FastAPI application and route handlers. Exposes session management and roll stepping over HTTP.
•crapssim_api.session_store
In-memory store for sessions. Keeps track of the underlying Table instances and associated hand/point state.
•crapssim_api.hand_state
Tracks hand/point transitions and emits “hand state” information that is surfaced in HTTP responses.
•crapssim_api.version
Central place for engine API version tags and schema/version metadata returned from HTTP endpoints.

There are also a few future-facing modules (see below) that are not yet wired into the HTTP surface but are kept in the tree to reserve the design and namespace.

⸻

FastAPI Usage (Basic Example)

After installing with the api extra, you can create and run an application like this:

from fastapi import FastAPI
from crapssim_api.http import get_router

app = FastAPI()
app.include_router(get_router())

Then run it with your favorite ASGI server (for example, uvicorn):

uvicorn myapp:app --reload

The router includes endpoints for:
•starting sessions
•applying actions (bets, removals, etc.)
•stepping rolls (optionally with fixed dice)
•querying basic capabilities and version metadata

The exact endpoint and payload contracts are described in the tests under crapssim_api/tests/ and in the dedicated API documentation files in this folder.

⸻

Design Philosophy (Short Version)
•Additive only:
The API does not modify the core bet logic, table behavior, or public crapssim interfaces.
•Dumb I/O:
The API returns raw facts (bankroll, bets, dice outcomes, hand state). It does not compute higher-level statistics like ROI, drawdown, or risk metrics. Those are left to downstream tools.
•Optional dependencies:
HTTP-related dependencies are only required when the api extra is installed. Core users are not forced to bring in FastAPI, Pydantic, or any HTTP stack.

For a fuller discussion of design intent and maintenance expectations, see API_DESIGN_PHILOSOPHY.md in this same folder.

---
