# Phase 3 Summary — Error Handling & Legality Layer

**Tag:** `v0.3.0-api-p3`

Phase 3 established the adapter’s legality and error model:
- Deterministic `/apply_action` with verb validation and legality enforcement (timing, increments, limits).
- Unified error envelope with expanded codes: `ILLEGAL_TIMING`, `ILLEGAL_AMOUNT`, `LIMIT_BREACH`, `INSUFFICIENT_FUNDS`, `TABLE_RULE_BLOCK`.
- Per-session mock bankroll ledger used for pre-action validation.
- Determinism verified across 3 consecutive test runs; baseline artifacts recorded under `baselines/phase3/`.

Refer to `baselines/phase3/manifest.json` for run totals and determinism hashes.
