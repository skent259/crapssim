# CrapsSim-Vanilla HTTP API Overview

This document is a quick-start guide to the optional HTTP API that wraps
CrapsSim-Vanilla. The API lives in the `crapssim_api` package and is designed
to be a thin, opt-in layer on top of the core engine.

## 1. Installation

The core library does **not** require any HTTP dependencies.

To use the HTTP API, install FastAPI and a simple ASGI server (for example,
`uvicorn`):

```bash
pip install fastapi uvicorn

You can install these into the same environment where crapssim is installed.

2. Starting the API

The crapssim_api.http module exposes a small FastAPI application. A minimal
uvicorn launch command might look like:

uvicorn crapssim_api.http:create_app --factory --reload

This will start a development server on http://127.0.0.1:8000 by default.

3. Core Endpoints

GET /health

Returns a simple status payload:

{
  "status": "ok"
}

Use this to verify that the API is running.

GET /capabilities

Returns a JSON object describing what the current build of CrapsSim-Vanilla
supports. A typical response might look like:

{
  "bets": {
    "supported": ["Buy", "DontPass", "Odds", "PassLine", "Place", "Put", "World", "Horn"]
  },
  "table": {
    "buy_vig_on_win": true,
    "vig_rounding": "nearest_dollar",
    "vig_floor": 0.0
  }
}

Clients can use this to discover which bet types and basic vig/table settings
are available.

4. Design Notes
•The API exposes raw facts; it does not compute statistics such as ROI,
drawdown, or streaks.
•The HTTP layer does not change the behavior of the core engine. If you do not
start the server, nothing in your existing workflows changes.
•More advanced orchestration, analytics, and UI layers are expected to live in
external tools (for example, CSC or custom clients).

5. Example Client

See examples/api_client_min.py for a very small script that calls /health
and /capabilities against a running API instance.

---
