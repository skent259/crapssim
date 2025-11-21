# Developer Docs

This folder hosts maintainer-facing references for the Engine API along with generated stress/parity reports.

## References
- [roadmap](roadmap.md) — phase summaries and future tracks
- [bible](bible.md) — design principles and module roles
- [compatibility plan](compat_plan.md) — Python/package alignment notes
- [testing](testing.md) — stress and gauntlet workflow details
- [bet wiring](bet_wiring.md) — notes on engine/API bet mapping
- [seeds & sessions](seeds_sessions.md) — determinism and session behavior
- [gauntlet](gauntlet.md) — maintainer view of the manual gauntlet workflow

## Reports
Generated stress/parity outputs live under `dev/reports/`. Regenerate them via the stress harnesses in `crapssim_api/tests/`; they are not needed for routine usage.
