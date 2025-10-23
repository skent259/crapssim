# /apply_action (P3 · C1 — Stub)

Accepts an action `verb` with `args`, validates, and returns a deterministic no-op result.  
No bankroll updates or timing enforcement at this checkpoint.

## Request
```json
{ "verb": "place", "args": { "box": 6, "amount": 12 }, "session_id": "optional" }
```

## Response
```json
{
  "effect_summary": {
    "verb": "place",
    "args": {"box": 6, "amount": 12},
    "applied": true,
    "bankroll_delta": 0.0,
    "note": "stub: action accepted, no-op"
  },
  "snapshot": {
    "session_id": "stub-session",
    "identity": { "engine_api_version": "...", "capabilities_schema_version": 1 }
  }
}
```

## Errors
- `UNSUPPORTED_BET` — unknown verb
- `BAD_ARGS` — verb missing/empty or args not a dict
