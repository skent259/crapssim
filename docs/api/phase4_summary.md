# Phase 4 Summary — Roll Flow & Event Envelope

**Tag:** `v0.4.0-api-p4`

Phase 4 delivered deterministic roll stepping and a structured event stream:
- `/step_roll` supports `"auto"` and `"inject"` modes.
- `events[]` includes `hand_started`, `roll_started`, `roll_completed` with deterministic IDs and stable ordering.
- Determinism verified across 3 consecutive runs; artifacts recorded in `baselines/phase4/`.

See `baselines/phase4/manifest.json` for totals and determinism checks.
