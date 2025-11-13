# CrapsSim API — Design Philosophy & Maintenance Intent

This document captures the intent behind the `crapssim_api` package so future contributors can keep changes aligned with the original goals.

---

## Core Principles

1. **Vanilla First**

The `crapssim` engine is the primary artifact. It owns:

- table rules
- bet legality
- payouts
- randomness and seeding

The API layer must **never** change core behavior as a side effect. If a change is required in engine behavior, it should be made in `crapssim` first, with tests, and only then surfaced via the API.

2. **Optional and Lightweight**

The API is an **optional add-on**, not a runtime requirement.

- Core install: `pip install crapssim`
- API install: `pip install "crapssim[api]"`

If a user never imports `crapssim_api`, nothing in their existing workflows should break or slow down. The API should introduce:

- no background threads by default
- no long-running processes unless explicitly started
- no extra global state beyond what is needed to manage sessions

3. **Dumb I/O, Smart Callers**

The HTTP layer should return **raw facts** about what just happened at the table:

- dice rolled
- bets placed and resolved
- bankroll before/after
- hand / point state

It should *not* compute:

- ROI
- drawdown
- streak metrics
- “best” strategies

Those belong in downstream tools (for example, CrapsSim-Control, notebooks, or other consumer apps). Keeping the API “dumb” avoids double-implementing analytics and keeps the engine focused.

4. **Clear Contracts**

Public API contracts should be:

- documented in tests (under `tests/api/`)
- reflected in small, focused doc files in this folder
- stable across minor changes where practical

Breaking changes to endpoints, payload shapes, or version tags should be deliberate and called out in release notes or docs.

---

## Module Roles

- `http.py`  
  Hosts the FastAPI router and request handlers. Responsible for:
  - validating inputs at the HTTP boundary
  - mapping requests to engine calls
  - serialising engine outputs to JSON

  It should not embed engine logic itself.

- `session_store.py`  
  Maintains session-scoped state (tables, hands, points). It is intentionally simple and in-memory. If more advanced storage is needed (e.g. Redis), it should be added as a separate integration.

- `hand_state.py`  
  Encapsulates rules for hand and point state transitions. This keeps “hand bookkeeping” logic away from the HTTP wiring and makes it easier to evolve.

- `version.py`  
  Central authority for engine API version tags and schema version IDs. Tests rely on these values; they should not be changed casually.

- `determinism.py`, `rng.py`, `state.py`  
  Reserved for **future determinism and snapshot tooling**. At present, they are not wired into the HTTP surface and must not be imported from runtime paths until they are fully designed and tested.

---

## Maintenance Expectations

- Keep changes **small and local**. Avoid refactors that span the core engine and the API in one step.
- Prefer adding tests in `tests/api/` that encode expectations for new endpoints or fields.
- When in doubt:
  - favor explicit, boring code over clever abstractions
  - leave a short comment explaining why a decision was made
- Treat the API as a **thin adapter** over the engine, not as a second engine.

If a future maintainer wants to expand the API (for example, to add more endpoints, determinism tools, or richer snapshots), they should first check this file and the tests, and keep new work consistent with these principles.

If an older API philosophy / roadmap doc already exists at the repo root, you may incorporate any extra details from it after this content block, but do not delete or modify the text above.
