# CrapsSim Engine API — Quickstart

This guide walks through starting the optional HTTP layer, opening a session, placing a couple of bets, rolling, and reading results. All rules and error semantics come directly from the CrapsSim engine; the API simply forwards decisions and returns structured JSON.

## 1. Install with API extras

From the repo root:

```bash
pip install -e .[api]
```

The API lives under `crapssim_api/` and is optional. Core CrapsSim users do not need to install these HTTP dependencies unless they want the FastAPI surface.

## 2. Start the HTTP app

Launch FastAPI via uvicorn:

```bash
uvicorn crapssim_api.http:app --reload
```

Visit `http://127.0.0.1:8000/health` to confirm the server is up and to see the reported Engine API version.

## 3. Start a session

Create a deterministic session by posting a seed:

```bash
curl -X POST http://127.0.0.1:8000/session/start \
  -H "Content-Type: application/json" \
  -d '{"seed": 12345, "profile_id": "default"}'
```

The response includes a `session.id` you will use for actions and rolls.

## 4. Place bets

Apply a simple Pass Line bet against that session:

```bash
curl -X POST http://127.0.0.1:8000/session/apply_action \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<session-id>", "verb": "pass_line", "args": {"amount": 10}}'
```

The API responds with an `effect_summary` and a snapshot of bankroll, bets, and puck/point. Bet legality and error codes are emitted by CrapsSim; see [`verbs.md`](verbs.md) and [`errors.md`](errors.md) for the full catalog.

## 5. Roll the dice

Advance the game with a roll:

```bash
curl -X POST http://127.0.0.1:8000/session/roll \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<session-id>"}'
```

You can also provide explicit dice for deterministic checks:

```bash
curl -X POST http://127.0.0.1:8000/session/roll \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<session-id>", "dice": [3, 4]}'
```

The response reports the roll, hand phase, bankroll, and emitted events. For deeper parity validation, see the stress suites referenced in [`dev/testing.md`](dev/testing.md).

## 6. Explore capabilities

Two read-only endpoints are handy for clients:

- `GET /health` — service status plus Engine API version.
- `GET /capabilities` — supported bet surface and increments, as reported by the underlying engine.

A minimal Python client lives at [`examples/api_client_min.py`](../examples/api_client_min.py) if you want to script these calls instead of using `curl`.
