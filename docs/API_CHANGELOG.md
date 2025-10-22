# CrapsSim-Vanilla API — Checkpoint Changelog (Append-Only)

This changelog records **what changed at each checkpoint**. It is append-only and ordered newest-first within each phase.

---
## Phase 1 — API Scaffolding & Determinism Contract

### P1·C2 — Determinism Harness
- Added crapssim_api/determinism.py with seed+tape+replay and short run hash.
- Enhanced crapssim_api/rng.py to support optional recorder for RNG call logging.
- Added tests validating same-seed same-tape parity, mismatch detection, and replay.

_(Commit: pending (5e6565d210bb4d456d677d3d54c1f37c268ce83c); Date: 2025-10-22 18:09:48 UTC)_


### P1·C1 — Adapter Skeleton
- Created crapssim_api package with __init__.py, http.py, state.py, rng.py, errors.py, events.py.
- Added skeleton tests (import, ASGI app callable, error codes, RNG determinism).
- Zero core engine changes; dependency-free fallback for ASGI.

_(Commit: pending (59f9bcb4ecd2c97ec08906692e0803dff8549e46); Date: 2025-10-22 17:04:44 UTC)_


### P1·C0 — Phase Mini-Roadmap & Changelog Scaffolding
- Created docs/API_PHASE_STATUS.md (overwritten by every C0).
- Created docs/API_CHANGELOG.md (append-only, checkpoint log).
- Added tools/api_checkpoint.py helper to manage C0 overwrites and changelog appends.

_(Commit: a00946a6d9c11e022eb3cfaedb383b9f149fc54f; Date: 2025-10-22 16:34:11 UTC)_

