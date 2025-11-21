# Docs Reorg & Gauntlet Cleanup Status

## Summary

- Verified Engine API docs layout matches the canonical structure.
- Updated internal links to point at the new filenames/paths.
- Removed committed gauntlet/stress artifacts and moved them to CI-only.
- Finalized .gitignore rules for gauntlet output.

## Structure Snapshot

- Public docs:
  - docs/README.md
  - docs/overview.md
  - docs/quickstart.md
  - docs/installation.md
  - docs/status.md
  - docs/verbs.md
  - docs/errors.md
  - docs/determinism.md
  - docs/session_state.md
  - docs/metrics.md
  - docs/push_semantics.md
  - docs/gauntlet_user.md
- Dev docs:
  - docs/dev/roadmap.md
  - docs/dev/bible.md
  - docs/dev/ci_notes.md
  - docs/dev/compat_plan.md
  - docs/dev/testing.md
  - docs/dev/bet_wiring.md
  - docs/dev/seeds_sessions.md
  - docs/dev/gauntlet.md
- Gauntlet artifacts:
  - All previous stress/parity/tape/journal outputs removed from the repo.
  - Future outputs are expected to be CI artifacts only.

## Notes

- Legacy installation and roadmap docs are archived under docs/archive/ for reference.
