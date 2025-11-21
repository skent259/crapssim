# Metrics Surface (Design)

Phase 5 also introduces a read-only metrics endpoint that exposes authoritative bankroll and performance statistics. As with the session snapshot, the API is a serializer only; all numbers originate from the engine’s native counters.

## Endpoint Concept

- Read-only metrics for a single session (e.g., `GET /session/<id>/metrics`).
- Values are taken directly from engine-tracked counters. No derived or reinterpreted figures.
- Intended consumers:
  - **CSC:** bankroll/drawdown/risk rules.
  - **Evo:** fitness and experiment summaries.
  - **Researchers:** reproducible statistics tied to deterministic runs.

## Target Schema

Fields marked as **future extension** require additional engine tracking; they remain optional until the engine provides them.

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

- **Bankroll and ROI:** pulled from the engine’s bankroll ledger. `roi` is only populated when start bankroll is non-zero; no API-side guard rails beyond the engine’s math.
- **Roll and hand counters:** surfaced from existing session/hand tracking. If the engine does not distinguish come-out rolls, `comeout` remains zero until the engine exposes it in a future phase.
- **Outcome counters and points:** forwarded from engine-provided tallies. If PSO tracking is absent, `pso_count` is deferred as a future extension rather than inferred.
- **Per-bet metrics:** enumerated from engine-maintained statistics by bet type. The API must not cluster or re-label bet families; it forwards the engine’s identifiers.
- **Determinism metadata:** mirrors the determinism contract version associated with the session so metrics snapshots align with replay tapes and seeds.

## Non-ownership of Rules

- The metrics surface does **not** define craps rules or outcome semantics.
- It does **not** decide what constitutes a PSO, a point, or a push; it only reports the engine’s own counters for those concepts.
- Consumers that need bespoke roll classification must derive it from raw events or replays, not from this endpoint.

## Versioning & Evolution

- **`metrics_schema` starts at "1.0".** Clients must tolerate additional fields and treat missing optional fields as absent data rather than errors.
- **Additive change model.** New metrics are appended; existing fields keep their meaning. Renames or semantic shifts require a schema version bump and clear release notes.
- **Compatibility expectations.** Deterministic runs (seed or tape) should yield identical metrics for a given engine version. Replay tapes override RNG to ensure metrics reproduce across upgrades so long as tape format compatibility holds.

## Future Implementation Notes (Phase 5·B/5·C)

- Add serializers that emit these counters directly from engine state without computation in the API layer.
- Back metrics with CI checks comparing serialized output to engine-reported statistics for the same session/tape.
- Expand schemas only when the engine supplies the necessary counters; avoid API-side aggregation beyond the engine’s native reporting.
