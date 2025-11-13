# CrapsSim-Vanilla API — Design Intent

This document captures the design philosophy and maintenance intent for the
`crapssim_api` package that wraps CrapsSim-Vanilla.

## Responsibility Split

We deliberately separate responsibilities across three layers:

1. **CrapsSim-Vanilla (core engine)**
   - Owns: dice, bets, table rules, payout math, and legality.
   - Does **not** own: HTTP, long-running services, analytics, or strategy policy.
   - Must remain usable as a pure Python library with no extra dependencies.

2. **`crapssim_api` (optional HTTP API layer)**
   - Owns: a thin HTTP surface and convenience utilities for external tools.
   - Provides: endpoints for health, capabilities, and a minimal command surface.
   - Does **not** change core engine behavior or introduce table-side policy.
   - May depend on `fastapi` and `uvicorn`, but only as optional extras.
   - Must not be imported automatically by `crapssim` core modules.

3. **External tools (e.g. CSC, Node-RED flows, custom UIs)**
   - Own: orchestration, analytics, simulations, and user interfaces.
   - Consume: the API’s events, capabilities, and command endpoints.
   - Are responsible for computing statistics (ROI, drawdown, streaks, etc.).

## Key Principles

- **No bloat in the engine.** The core `crapssim` package should remain small and focused on craps math and table behavior.
- **Dumb I/O, smart clients.** The API should expose raw facts (events, state, capabilities) and let callers compute whatever summaries they need.
- **Optional HTTP.** The library must work without `fastapi`. Importing `crapssim` or `crapssim_api` must not fail if HTTP dependencies are missing.
- **Clear contracts.** API types (enums, dataclasses, error codes) should express intent clearly and be easy to consume from other languages and tools.
- **Stable surface.** Once the API is public, breaking changes should be rare and documented, with migration notes.

## Maintenance Intent

- Changes to `crapssim_api` should:
  - Be small and self-contained.
  - Prefer additive evolution over breaking changes.
  - Include tests that codify the API contract (shape of JSON, error codes, etc.).
- Changes to `crapssim` core should not be driven by API convenience alone.
  The engine’s primary goal is correctness and usability as a standalone library.
