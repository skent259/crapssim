## v0.2.0 — Compatibility & Push Semantics

This release finalizes Phase 2 of the CrapsSim Engine API roadmap.

- Added Python 3.11, 3.12, 3.13 support via metadata + typing_extensions.
- Added optional `api` dependency group for FastAPI deployments.
- Implemented push-aware API reporting with no game logic.
- Synchronized error codes with CrapsSim v4.0.
- Minor fixes to import paths and type definitions.

## Planned (Phase 4 — Session State & Determinism Contracts)

- Document determinism contract (seed → dice → outcomes) for Engine API consumers.
- Introduce replay tape concept for exporting/importing deterministic sessions.
- Add CI scaffolding to validate determinism across supported Python versions (3.10–3.13).
- Provide high-level guidance for CSC/Evo and research clients on how to rely on the Engine API for reproducible simulations.
