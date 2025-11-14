# API Bet Wiring Diagnosis

## Summary
- Investigated the FastAPI `/apply_action` endpoint and the session roll pipeline to understand how bets flow from HTTP requests into the vanilla CrapsSim engine.
- Replaced the stubbed action handlers with real engine wiring so every supported verb creates the corresponding `crapssim.bet` instance.
- Normalised bankroll reporting so the API always reflects `Session.player().bankroll`, making the engine the single source of truth.
- Removed reliance on client-supplied state hints; the engine now determines timing and legality for every action.

## Root Cause
- `crapssim_api.http.apply_action` previously delegated to stub handlers (`VerbRegistry`) that returned success without mutating the engine table or player, so bets never reached the CrapsSim engine.
- Session snapshots used in `/session/roll` were built from a lightweight `HandState` structure with hard-coded bankroll values (`"1000.00"`), ignoring the actual table/player bankroll and bet layout.

Affected paths:
- `crapssim_api/http.py::apply_action`
- `crapssim_api/http.py::step_roll`
- `crapssim_api/session_store.py::_new_state`

## Changes Made
- Wired `/apply_action` directly to the live `Session`, instantiating real bet objects for each supported verb.
- Ensured session creation stores a `Session` instance with a default player so bets have a target bankroll.
- Updated roll snapshots to use engine snapshots for bankroll, bets, and dice outcomes.
- Added comprehensive tests covering bankroll accounting, legality propagation, and verb coverage.

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
- Consider consolidating duplicated state between `HandState` and the engine snapshot to avoid divergence.
- Additional table management verbs (removals, working toggles) remain future work.
