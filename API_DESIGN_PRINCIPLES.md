# CrapsSim API — Design Philosophy & Long-Term Maintenance Intent

This document defines the purpose, philosophy, and future expectations for
the CrapsSim-Vanilla API. It exists to ensure that future contributors and
automated agents understand the boundaries and intent.

## Purpose
Provide a minimal, optional interface layer to allow external tools (e.g., CSC,
web UIs, research tools) to control and observe CrapsSim.

## Philosophy
- CrapsSim core is the authoritative engine.
- API must never alter CrapsSim behavior.
- API should add convenience without adding logic.
- All analytics, risk, decision-making, and statistics must remain external.

## What the API Must Never Do
- Must never compute statistics (ROI, EV, streaks, drawdown, etc.).
- Must never override legality.
- Must never introduce timing, threading, or background services.
- Must never require FastAPI.

## Optional FastAPI Policy
- The API must import cleanly without fastapi installed.
- If fastapi is present, HTTP endpoints become available.
- If fastapi is absent, files still import and tests pass.

## Maintenance Intent
- Keep API surface stable and backward-compatible.
- Keep code footprint small.
- Add new endpoints only when they expose existing engine behavior.
- No new dependencies without explicit opt-in.
