# CrapsSim-Vanilla API — Phase Mini-Roadmap (Active Phase: 1)

**Purpose**  
This page summarizes the **current** phase plan and status. It is **overwritten** on every phase kickoff checkpoint (**C0**).

**Phase:** 1 — API Scaffolding & Determinism Contract  
**Schema Version (capabilities):** 1 (planned)  
**Engine API Version (target tag at phase end):** v0.1.0-api-phase1

---

## Checkpoints (Phase 1)

- **P1·C1 — Adapter Skeleton**  
  Create `crapssim_api/` with skeleton modules:
  `http.py`, `state.py`, `rng.py`, `errors.py`, `events.py`.

- **P1·C2 — Determinism Harness**  
  Seeded RNG wrapper; action/roll tape recorder; reproducibility test.

- **P1·C3 — Version & Schema**  
  Surface `engine_api.version` and `capabilities.schema_version`.

- **P1·C4 — Baseline Conformance**  
  Prove identical outputs for identical `{spec, seed, tape}`; tag `v0.1.0-api-phase1`.

---

## Status

| Checkpoint | Status  | Notes |
|------------|---------|-------|
| P1·C0      | ✅ Done | Roadmap + changelog scaffold created. |
| P1·C1      | ☐ Todo  |  |
| P1·C2      | ☐ Todo  |  |
| P1·C3      | ☐ Todo  |  |
| P1·C4      | ☐ Todo  |  |

**Next up:** P1·C1 — Adapter Skeleton

_Last updated: (auto-populated by commit time)_
