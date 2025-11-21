# Metrics Surface (Design + Phase 5·B implementation)

Phase 5 also introduces a read-only metrics endpoint that exposes authoritative bankroll and performance statistics. As with the session snapshot, the API is a serializer only; all numbers originate from the engine’s native counters. Phase 5·B implements this surface using the counters available today.

## Endpoint Concept

- Read-only metrics for a single session (e.g., `GET /session/<id>/metrics`).
- Values are taken directly from engine-tracked counters. No derived or reinterpreted figures.
- Intended consumers:
  - **CSC:** bankroll/drawdown/risk rules.
  - **Evo:** fitness and experiment summaries.
  - **Researchers:** reproducible statistics tied to deterministic runs.

## Target Schema

Fields marked as **future extension** require additional engine tracking; they remain optional until the engine provides them. Outcome, point-detail, and per-bet metrics remain `null`/empty in Phase 5·B until the engine surfaces the raw values.

```yaml
metrics_schema: "1.0"
session_id: str

bankroll:
  start: float
  current: float
  net: float             # current - start
  roi: float | null      # net / start, if start > 0

rolls:
  total: int
  comeout: int
  point_resolutions: int

hands:
  total: int
  completed: int

outcomes:
  wins: int
  losses: int
  pushes: int

points:
  made: int
  seven_outs: int
  pso_count: int        # future extension if not already tracked

by_bet_type:
  - type: str
    wins: int
    losses: int
    pushes: int
    net: float

determinism_contract: "v1.0"
```

## Source of Truth

- **Bankroll and ROI:** pulled from the engine’s bankroll ledger alongside the API-recorded `initial_bankroll`. `roi` is only populated when start bankroll is non-zero.
- **Roll and hand counters:** surfaced from existing session/hand tracking. With the current engine, only roll totals and the current hand index are available; come-out and point-resolution counts stay `null` until the engine exposes them.
- **Outcome counters and points:** deferred until the engine provides explicit tallies; these fields remain `null`.
- **Per-bet metrics:** deferred; the API returns an empty list rather than inferring results.
- **Determinism metadata:** mirrors the determinism contract version associated with the session so metrics snapshots align with replay tapes and seeds.

## Non-ownership of Rules

- The metrics surface does **not** define craps rules or outcome semantics.
- It does **not** decide what constitutes a PSO, a point, or a push; it only reports the engine’s own counters for those concepts.
- Consumers that need bespoke roll classification must derive it from raw events or replays, not from this endpoint.

## Versioning & Evolution

- **`metrics_schema` starts at "1.0".** Clients must tolerate additional fields and treat missing optional fields as absent data rather than errors.
- **Additive change model.** New metrics are appended; existing fields keep their meaning. Renames or semantic shifts require a schema version bump and clear release notes.
- **Compatibility expectations.** Deterministic runs (seed or tape) should yield identical metrics for a given engine version. Replay tapes override RNG to ensure metrics reproduce across upgrades so long as tape format compatibility holds.

## Example (Phase 5·B)

```json
{
  "metrics_schema": "1.0",
  "session_id": "abc12345",
  "bankroll": {"start": 1000.0, "current": 1010.0, "net": 10.0, "roi": 0.01},
  "rolls": {"total": 2, "comeout": null, "point_resolutions": null},
  "hands": {"total": 1, "completed": 0},
  "outcomes": {"wins": null, "losses": null, "pushes": null},
  "points": {"made": null, "seven_outs": null, "pso_count": null},
  "by_bet_type": [],
  "determinism_contract": "v1.0"
}
```
