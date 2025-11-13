# CrapsSim-Vanilla API — Design Intent

The optional HTTP addon exists to expose a thin control surface over the core
engine without changing how simulations run locally. The core `crapssim`
package stays dependency-light and importable without FastAPI, while
`crapssim_api` provides a convenient FastAPI wrapper for teams that want HTTP
hooks.

## Responsibility Split

1. **CrapsSim-Vanilla (core engine)**
   - Owns dice, bets, table rules, payout math, and legality.
   - Has no dependency on FastAPI, uvicorn, or pydantic.
   - Must remain usable as a pure Python library.

2. **`crapssim_api` (optional HTTP layer)**
   - Owns the FastAPI routes, request/response schemas, and helper utilities.
   - Imports FastAPI/pydantic only when the `api` extra is installed.
   - Mirrors the engine’s behavior rather than adding new table logic.

3. **External tools (e.g. CSC, Node-RED flows, dashboards)**
   - Own orchestration, analytics, simulations, and user interfaces.
   - Consume the API’s events, capabilities, and command endpoints.
   - Remain responsible for statistics such as ROI, drawdown, or streaks.

## Maintenance Intent

- Keep HTTP dependencies optional and lazily imported.
- Prefer additive evolution of endpoints; breaking changes require migration
  notes and tests.
- Core engine changes should not be driven by API ergonomics.
- Maintainers uninterested in the HTTP layer can ignore it by skipping the
  optional extras; engine development proceeds independently.

## Optional Extras Philosophy

- The published wheel exposes an `api` extra (`pip install crapssim[api]`).
- Base installs (`pip install crapssim`) run the simulator without FastAPI
  present.
- Tests under `tests/api/` skip cleanly when FastAPI or pydantic are missing.
- The FastAPI entrypoint is discoverable via documentation but never started
  automatically.
