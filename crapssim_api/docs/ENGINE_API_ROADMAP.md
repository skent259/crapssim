# Engine API Roadmap

### Phase 3·C — CI & Packaging Validation

- Added a dedicated `api-engine-ci` GitHub Actions workflow.
- Runs API tests against Python 3.10–3.13 without touching core engine behavior.
- Installs the Engine API via editable extras (`crapssim_api[api,dev,gauntlet]`).
- Runs both the fast unit suite and the sequence/gauntlet stress suite.
- Keeps the Engine API optional: core users are unaffected unless they enable the workflow or install extras.

### Phase 4-B — Replay Tape Import/Export & Determinism Helpers

**Status:** Complete.

- Added an optional `record_tape` flag on `/session/start` so callers can opt in to deterministic session recording without changing engine behavior.
- Extended the in-memory session store to accumulate a `SessionTape` (metadata + ordered steps + final_state) using only the engine’s own responses as truth.
- Exposed `GET /session/{session_id}/tape` to export a replayable tape for a recorded session.
- Exposed `POST /session/replay` to drive a fresh engine instance from a `SessionTape` and report whether the replayed final state matches the recorded one.
- Introduced `SessionTape`, `SessionTapeStep`, `SessionTapeMetadata`, and `ReplayResult` types to formalize the determinism contract for external consumers (CSC, Evo, notebooks, etc.).
- Added an integration test that records a short session, exports its tape, replays it, and asserts deterministic equality of the final state.
