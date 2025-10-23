## 0.2.0-api.p2 — Phase 2 Baseline Finalized
- Added standardized API error contract with envelope {code,hint,at_state}.
- Corrected /capabilities increments payload and odds limits shape.
- Implemented /end_session stub returning minimal report.
- Added docs/api/errors.md and adapter error tests.

## 0.3.0-api.p3 — Phase 3 Actions & Legality Kickoff
- Initialized Phase 3 documentation and scaffolds.
- No behavior changes; groundwork for `/apply_action` begins.

### P3 · C1 — Action Schema & Dispatch Stub
- Added `/apply_action` endpoint with unified verb/args request and effect summary response.
- Introduced `VerbRegistry` and a deterministic no-op stub handler.
- Returns error envelopes for unknown verbs and malformed arguments.

### P3 · C2 — Timing & Legality Core
- `/apply_action` enforces timing windows (come-out vs point-on).
- Validates amount increments from `/capabilities`.
- Adds error codes: ILLEGAL_TIMING, ILLEGAL_AMOUNT, LIMIT_BREACH.
- No bankroll/payout math yet; returns deterministic no-op on legal actions.

### P3 · C3 — Error Codes Expansion & State Awareness
- Added INSUFFICIENT_FUNDS and TABLE_RULE_BLOCK error codes.
- Introduced SessionBankrolls for per-session bankroll tracking.
- `/apply_action` now validates and deducts bankroll deterministically.
- All errors now use standardized envelope and consistent HTTP codes.
