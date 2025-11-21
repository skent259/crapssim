# Engine API Roadmap

## Purpose and guardrails
- Keep CrapsSim behavior authoritative; the API is a thin HTTP transport.
- Ship the API as an optional extra (`crapssim[api]`) so core users remain dependency-light.
- Avoid embedding analytics or orchestration logic; callers stay in control.

## Phase highlights
- **Phase 1 — HTTP surface & verbs**: Established FastAPI endpoints for sessions, actions, and rolls. Mirrored bet semantics without adding new logic.
- **Phase 2 — Compatibility & semantics**: Added Python 3.11–3.13 coverage, aligned error handling with engine codes, and documented push semantics and parity expectations.
- **Phase 3 — Packaging & extras**: Declared supported Python versions, introduced `api`/`dev`/`gauntlet` extras, and ensured CI installs match the optional dependency story.
- **Phase 4 — Determinism & replay tape**: Added session tape recording/export/import plus deterministic parity checks without altering engine decisions.
- **Phase 5 — State & metrics surfaces**: Exposed read-only session snapshots and metrics schemas versioned for external consumers.
- **Phase 6 — CI and compatibility polish**: Dedicated `api-engine-ci` workflow on Python 3.10–3.13, guarded optional imports, and kept FastAPI extras optional for engine-only installs.

## Forward-looking tracks
- Optional auth/rate-limiting for shared deployments (not scheduled).
- Additional observability hooks driven by researcher requests.
- Continued parity/stress coverage as new bet types or engine changes land.

## Phase 7-B — Docs reorganization
- Consolidated public docs under `crapssim_api/docs/` with a canonical README, overview, quickstart, install guide, verbs, determinism, and error contracts.
- Merged roadmap/bible/CI/gauntlet references into the `dev/` tree; archived legacy duplicates.
- Segregated generated stress/gauntlet reports under `dev/reports/` and tightened .gitignore to block ephemeral artifacts.

## Phase 7 — Docs Reorg & Cleanup
- Finalized the canonical doc layout split between public guides and maintainer notes under `docs/dev/`.
- Updated internal links to reference the new filenames (install, verbs, determinism, CI, testing) instead of legacy paths.
- Treated gauntlet and stress outputs as CI artifacts with `.gitignore` rules and cleaned the repo of committed runs.
