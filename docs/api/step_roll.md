# /step_roll — Roll Stepping Endpoint (Phase 4 · C1)

Implements deterministic dice rolling and injection modes.

## Request Examples
```json
{ "session_id": "abc123", "mode": "auto" }

{ "session_id": "abc123", "mode": "inject", "dice": [5, 5] }

Response (Scaffold)

{
  "session_id": "abc123",
  "hand_id": 1,
  "roll_seq": 1,
  "dice": [5, 5],
  "puck": "OFF",
  "point": null,
  "bankroll_after": "1000.00",
  "events": [],
  "identity": { "engine_api_version": "0.3.1-api-p3-sync" }
}
```

## Notes
- "auto" uses deterministic RNG based on session_id.
- "inject" lets the caller specify dice for deterministic replay.
- No bet resolution or payouts occur at this phase.
- Events are empty; they will be populated in Phase 4 · C2.
