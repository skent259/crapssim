## Phase 2 — Compatibility & Semantics

This phase introduces Python 3.11–3.13 compatibility, dependency cleanup,
and correct API-side push detection without introducing any game logic.

The API now reflects engine push outcomes either through explicit engine signals
or through lifecycle-based detection logic. No rules are inferred and the engine
remains the authoritative source of truth.

Error handling has also been aligned with CrapsSim v4.0 semantics, ensuring all
API error codes faithfully mirror core engine behavior.

**Status:** Phase 2 implementation is complete. The API now runs clean under
Python 3.10–3.13, forwards engine error codes faithfully, and reports pushes
without embedding any craps rules in the API layer.

## Phase 3 — Python Support & Packaging Hardening

**Goal:** Make the CrapsSim Engine API installable and honest about its environment. Clearly document supported Python versions, dependency groups, and how to install and use the API as an optional extension to CrapsSim.

### P3·A — Design & Documentation Plan (this phase)

- Clarify the intended Python version support window (targeting 3.10–3.13).
- Describe the separation between:
  - Core CrapsSim engine users (no API required).
  - Engine + API users (`crapssim_api` as an optional wrapper).
- Define dependency groups conceptually:
  - Core engine dependencies (unchanged).
  - API runtime dependencies (FastAPI, Pydantic, uvicorn, typing-extensions).
  - Future dev/test extras (pytest, HTTP client libraries, etc.).
- Document the intended installation story:
  - Engine-only installs should not be forced to pull API dependencies.
  - API should be installable via an extra or clearly documented instructions.
- Avoid any code or CI changes in this phase; this is planning and documentation only.

### P3·B — Metadata & INSTALLING Wiring (planned)

- Update packaging metadata (`pyproject.toml` / `setup.cfg` under `crapssim_api/`) so that:
  - Supported Python versions are explicitly declared.
  - API dependencies are grouped under a clearly named extra (e.g. `api`).
- Add or refine an INSTALLING guide that explains:
  - Engine-only vs engine+API installation paths.
  - How to run API tests locally using the same install method as CI.

### P3·C — CI Alignment & Sanity Checks (planned)

- Ensure CI runs a minimal API test suite across the declared Python versions.
- Align the manual “gauntlet” workflow with the documented install flow.
- Confirm that documentation, metadata, and CI behavior all match the same Python support and dependency story.

### Phase 3·B — Packaging & Extras Implemented

- Added pyproject.toml / setup.cfg under crapssim_api/.
- Declared Python support for 3.10–3.13.
- Added API runtime dependencies.
- Added `[api]`, `[dev]`, and `[gauntlet]` extras.
- Updated INSTALLING guide with real commands.
- Ensured the Engine API is fully optional and does not affect core engine users.

### Phase 4 — Session State & Determinism Contracts ✔ COMPLETE

**One-liner:** Guarantee deterministic, replay-safe sessions (seed → dice → outcomes) across API and vanilla engines, including replay-tape export/import and cross-Python reproducibility.

**Highlights:**
- Determinism contract documented and versioned.
- Replay tape export/import implemented and validated for full-session replays.
- CI verifies deterministic behavior across supported Python versions (3.11–3.13) using stress and replay suites.

**Non-goals:**
- No new betting logic in the API.
- No changes to engine rules or payouts.
- No strategy or policy logic; the API remains a thin wrapper around CrapsSim.
