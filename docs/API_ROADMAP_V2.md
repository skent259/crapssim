# CrapsSim-Vanilla API — V2 Roadmap

This roadmap mirrors the intent documented at the repository root and keeps the
FastAPI addon story front-and-center for contributors reviewing the docs set.

## Design Principles
- Zero behavior changes to CrapsSim core.
- API is optional and lightweight.
- All analytics, decision logic, and statistics remain external.
- FastAPI and friends ship as an opt-in `crapssim[api]` extra.
- No new background services. Everything is synchronous and opt-in.

## Phase 1 — API Skeleton (Complete)
- Create isolated package `crapssim_api/`.
- Define errors, models, HTTP stubs.
- Health endpoint only.
- No core engine imports.

## Phase 2 — Capabilities Reflection
- `/capabilities` returns introspection of bet classes and table settings.
- `/schema` provides JSON schema for commands and responses.

## Phase 3 — State Snapshot
- `/state` returns point, bankrolls, dice, bets.
- Must use thin wrappers without engine-side logic.

## Phase 4 — Deterministic Control Surface
- `/start_session`
- `/apply_action` (place/remove/odds/set dice)
- `/step_roll`
- Must use existing legality checks.

## Phase 5 — Event Envelope (Pull Only)
- `/step_roll` returns dice + bet resolutions + deltas.

## Phase 6 — DX Polish
- `docs/API_OVERVIEW.md`
- `examples/api_client_min.py`
- Optional FastAPI autodocs if FastAPI installed.

## Phase 8 — Hardening & DX Polish
- Keep HTTP layer optional and extras-based.
- Ensure tests skip gracefully without FastAPI installed.
- Provide clear quickstart and roadmap documentation.

## Cross-Phase Guardrails
- No behavior changes to CrapsSim.
- API must remain fully optional.
- No new dependencies except via the `api` optional extra.

### Increment Policy Note
CrapsSim-Vanilla does not enforce increment correctness for bets (e.g., $7 on
Place 6). Increment validation is intentionally delegated to higher-level
orchestration layers such as CSC. API tests expecting increment rejection have
been updated to reflect the correct responsibility boundary.
