# Engine API Bible

This living note captures the intent behind the `crapssim_api` package so future contributors keep changes aligned with the original goals.

## Core principles
1. **Vanilla first**: CrapsSim remains the single source of truth for rules, payouts, and randomness. The API must never alter engine behavior.
2. **Optional and lightweight**: The HTTP layer is an opt-in extra (`crapssim[api]`) with no background services or mandatory dependencies for core users.
3. **Dumb I/O, smart callers**: The API returns raw facts—dice, bets, bankroll deltas, hand state—while analytics and strategy stay in downstream tools.
4. **Clear contracts**: Public payloads are documented in tests and docs, with deliberate signaling for breaking changes.

## Module roles
- `http.py`: FastAPI router, request validation, and transport-only mappings to engine calls.
- `session_store.py`: In-memory session state; swap for external storage only via explicit integration work.
- `hand_state.py`: Hand and point bookkeeping separated from HTTP wiring.
- `version.py`: Central authority for Engine API version tags and schema IDs used by tests and clients.

## Phase narrative snapshot
- **Phase 3 — Python support & packaging**: Documented Python targets, kept core installs dependency-light, and aligned docs/metadata/CI on optional extras.
- **Phase 4 — Replay tape & determinism**: Added tape recording/export/import plus parity validation while leaving engine rulings untouched.

## Docs consolidation note
Phase 7-B reorganized docs to keep public guidance small and canonical, archived legacy duplicates, and moved deep design artifacts into `crapssim_api/docs/dev/` for maintainers.
