### P2·C2 — Capabilities & Table Spec
- Added GET /capabilities returning supported bets, odds, increments, commission, and flags.
- Added POST /start_session echoing spec and normalized capabilities.
- Added type definitions (Capabilities, TableSpec, StartSessionRequest/Response).
- Added example + smoke tests.

## 0.2.0-api.p2 — Phase 2 Baseline
- Sessions + Capabilities + Error Envelope complete.
- Added baseline smoke and determinism fingerprint tools.
- Version surfaced as 0.2.0-api.p2 in responses.
