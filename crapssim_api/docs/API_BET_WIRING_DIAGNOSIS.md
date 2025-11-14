# API Bet Wiring Diagnosis

## Summary
- Investigated the FastAPI `/apply_action` endpoint and the session roll pipeline to understand how bets flow from HTTP requests into the vanilla CrapsSim engine.
- Discovered that the API previously validated bet legality but never forwarded actions to the engine, leaving bankroll and bet state unchanged across rolls.
- Implemented targeted fixes so API bets now interact with the engine-backed session, persist through rolls, and resolve with bankroll updates.

## Root Cause
- `crapssim_api.http.apply_action` delegated to stub handlers (`VerbRegistry`) that returned success without mutating the engine table or player, so bets never reached the CrapsSim engine.
- Session snapshots used in `/session/roll` were built from a lightweight `HandState` structure with hard-coded bankroll values (`"1000.00"`), ignoring the actual table/player bankroll and bet layout.

Affected paths:
- `crapssim_api/http.py::apply_action`
- `crapssim_api/http.py::step_roll`
- `crapssim_api/session_store.py::_new_state`

## Changes Made
- Wired `apply_action` to the real `Session` object, synchronising bankroll ledgers and mapping supported verbs (pass line, place, buy, etc.) to CrapsSim bet classes.
- Ensured session creation stores a `Session` instance with a default player so bets have a target bankroll.
- Updated roll snapshots to use engine snapshots for bankroll, bets, and dice outcomes.
- Added comprehensive tests:
  - Updated unit tests for bankroll accounting and stub handling.
  - Added FastAPI end-to-end test covering bet placement, persistence, and resolution.

## How to Reproduce & Verify
- Run all tests (FastAPI optional):
  ```bash
  pytest -q
  ```
- To exercise the HTTP flow manually:
  ```bash
  uvicorn crapssim_api.http:app --reload
  ```
  Then POST to `/session/start`, `/apply_action`, and `/session/roll` with the sequences demonstrated in `tests/api/test_api_bet_flow.py`.

## Open Questions / Future Work
- The legality checks still rely on client-supplied state hints; future work could derive timing from the authoritative session state.
- Additional verbs (props, horn/world, odds) remain stubbed and would need engine mappings similar to the implemented bets.
- Consider consolidating duplicated state between `HandState` and the engine snapshot to avoid divergence.
