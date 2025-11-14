# CrapsSim HTTP API — Quickstart

This document shows how to:

- install CrapsSim with the HTTP API extras
- start the FastAPI app
- create a session with a seed
- place a simple bet via the API
- roll the dice and read the results

The goal is to make it easy to poke the API with `curl` or a small client and see what comes back.

---

## 1. Install with API extras

From the repo root:

```bash
pip install -e .[api]

This should install the core library plus the HTTP layer and its dependencies (FastAPI, Pydantic, Uvicorn, HTTP client tools, etc.).

If you see an error about [api] extras, verify that your local environment is using the repo’s pyproject.toml / setup.cfg and that you are in the project root when running the command.

⸻

2. Start the HTTP app

Assuming the FastAPI application object is exposed as app in crapssim_api.http, you can launch it with uvicorn:

uvicorn crapssim_api.http:app --reload

This will start the server on http://127.0.0.1:8000 by default. You should now be able to hit the health endpoint:

curl http://127.0.0.1:8000/health

Expected output (shape, not exact values):

{
  "status": "ok",
  "engine_api_version": "v2",
  "capabilities_schema_version": "v1"
}

The actual version strings are defined in crapssim_api.version.

⸻

3. Start a session

To start a new craps session via HTTP, POST to the session start endpoint. The exact schema is defined by the Pydantic models in crapssim_api.http, but a minimal request usually looks like:

curl -X POST http://127.0.0.1:8000/session/start \
  -H "Content-Type: application/json" \
  -d '{
    "seed": 12345,
    "profile_id": "default"
  }'

Typical response shape:

{
  "session": {
    "id": "session-uuid-or-token",
    "seed": 12345,
    "profile_id": "default"
  },
  "engine": {
    "engine_api_version": "v2"
  }
}

Key points:
•seed is optional but recommended for reproducibility.
•profile_id is optional and may be used to select a table/profile config depending on how the API is wired.
•The session.id value is required for subsequent /session/apply_action and /session/roll calls.

See API_SEEDS_AND_SESSIONS.md for more detail on how seeds behave.

⸻

4. Place a simple bet

To place one or more actions against a session, call the apply-action endpoint. The exact schema is defined in the API’s request models; a simple pattern is:

curl -X POST http://127.0.0.1:8000/session/apply_action \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-uuid-or-token",
    "actions": [
      {
        "type": "place_bet",
        "bet": "PassLine",
        "amount": 10,
        "player_id": 0
      }
    ]
  }'

Typical response shape:

{
  "session_id": "session-uuid-or-token",
  "effects": [
    {
      "type": "place_bet",
      "status": "ok",
      "bet": {
        "bet_type": "PassLine",
        "amount": 10
      }
    }
  ],
  "errors": []
}

If the bet is illegal (bad increment, wrong timing, insufficient funds, etc.), the response will include error entries. See API_ERRORS_AND_CONTRACT.md for details on error codes and meanings.

⸻

5. Roll the dice

To advance the game by one roll, use the roll endpoint. The request can either:
•let the engine roll randomly, or
•supply explicit dice (for deterministic testing).

Minimal random roll:

curl -X POST http://127.0.0.1:8000/session/roll \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-uuid-or-token"
  }'

With explicit dice (if supported by the current schema):

curl -X POST http://127.0.0.1:8000/session/roll \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-uuid-or-token",
    "dice": [3, 4]
  }'

Typical response shape:

{
  "session_id": "session-uuid-or-token",
  "roll": {
    "dice": [3, 4],
    "total": 7,
    "roll_index": 1
  },
  "hand": {
    "point": 0,
    "phase": "come_out",
    "hand_index": 1
  },
  "bankrolls": {
    "players": [
      {
        "player_id": 0,
        "bankroll": 990
      }
    ]
  },
  "events": [
    {
      "type": "roll_resolved",
      "details": "..."
    }
  ]
}

•The exact keys and event shapes are defined in the Pydantic response models.
•If you provide dice, the engine should honor those values for that roll.
•If you omit dice, the engine uses its RNG, seeded per session.

⸻

6. Capabilities and health

Two helpful read-only endpoints:

# Health check
curl http://127.0.0.1:8000/health

# Capabilities (supported bets, table rules, etc.)
curl http://127.0.0.1:8000/capabilities

/capabilities returns structured data about what the underlying CrapsSim engine supports:
•bet types
•increments
•odds rules
•table configuration

This is useful for validating client behavior or building UIs that adapt to the table’s capabilities.

⸻

7. Where to go next
•For error codes, see: API_ERRORS_AND_CONTRACT.md
•For seeds and deterministic behavior, see: API_SEEDS_AND_SESSIONS.md
•For a minimal Python client example, see: crapssim_api/examples/api_client_min.py

All of the above are designed to keep the HTTP API:
•a thin, optional skin over CrapsSim,
•with no extra stats or analytics,
•and a clear, documented contract for external tools like CSC or other clients.

---
