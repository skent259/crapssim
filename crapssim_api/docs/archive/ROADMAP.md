# CrapsSim Engine API — Roadmap & Phase Narrative

## Phase 1 — HTTP Surface & Verbs
- Established FastAPI surface for creating sessions, applying actions, and rolling dice.
- Mirrored CrapsSim bet semantics without adding business logic in the API.

## Phase 2 — Compatibility & Semantics (Complete)
- Added Python 3.11–3.13 compatibility and dependency cleanup.
- Corrected API-side push detection while deferring all rulings to the engine.
- Aligned error handling with CrapsSim v4.0 codes to keep the API a transparent transport layer.

## Phase 3 — Packaging & Extras (Complete)
- Declared supported Python versions and extras in `pyproject.toml` / `setup.cfg` under `crapssim_api/`.
- Documented engine-only vs. engine+API installs; kept HTTP dependencies optional via `[api]`, `[dev]`, and `[gauntlet]` extras.
- Ensured CI installs and exercises the API without impacting core engine users.

## Phase 4 — Session Determinism & Replay Tape (Complete)
- Documented determinism contract and added replay tape export/import for full-session reproduction.
- Validated deterministic parity across supported Python versions via stress and replay suites.
- Kept the API logic-free: tapes record engine outputs and are re-applied without altering decisions.

## Phase 5 — Session State & Metrics Surfaces (Complete)
- Exposed read-only session snapshots and metrics tailored for CSC/Evo and research workflows.
- Versioned state/metrics schemas so clients can track changes without guessing.
- Ensured snapshots serialize engine truth only—no inference or reconciliation in the API layer.

## Future Ideas
- Optional auth and rate-limiting for shared deployments (not planned yet).
- Additional observability hooks if researchers request more granular traces.

For deeper design artifacts and historical reports, see [`dev/`](dev/README.md).
