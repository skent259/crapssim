# CrapsSim-Vanilla API — Phase Mini-Roadmap (Active Phase: 2)

**Purpose**  
This page summarizes the **current** phase plan and status. It is **overwritten** on every phase kickoff checkpoint (**C0**) to reflect the latest phase scope and targets.

**Phase:** 2 — Session Lifecycle & Capabilities  
**Schema Version (capabilities):** 1 (in effect; may bump only if schema changes)  
**Engine API Version (target tag at phase end):** v0.1.0-api-phase2

---

## Checkpoints (Phase 2)

- **P2·C1 — Session Lifecycle Endpoints**  
  Implement `POST /start_session` and `POST /end_session`.  
  - Accept `{spec, seed, idempotency_key?}` on start.  
  - Return `{session_id, snapshot}` (using stub identity from Phase 1).  
  - Echo `{spec, seed}` in responses.  
  - Minimal `report_min` on end (hands, rolls, start/end bankroll).

- **P2·C2 — Capabilities Endpoint & Spec Ingestion**  
  Implement `GET /capabilities` and validate a table **spec** passed at session start.  
  - Report: bet families; legal increments; odds limits (incl. 3-4-5); Buy/Lay vig policy (rounding/floor/timing); Field pays; prop catalog.
  - Include `why_unsupported` for any omitted feature.  
  - Spec accepted by `/start_session` must mirror capability keys.

- **P2·C3 — Capability Truth Tests**  
  Add tests that assert parity between declared capabilities and actual engine behavior (legal targets, increments, limits).  
  - Include negative tests for unsupported features → `why_unsupported`.

- **P2·C4 — Docs: Lifecycle Overview**  
  Add `docs/API_LIFECYCLE.md` describing session start/end, capabilities contract, and spec ingestion examples.  
  - Update README with a short link.

---

## Status

| Checkpoint | Status  | Notes |
|------------|---------|-------|
| P2·C0      | ✅ Done | Phase 2 kicked off; roadmap overwritten; changelog appended. |
| P2·C1      | ☐ Todo  |  |
| P2·C2      | ☐ Todo  |  |
| P2·C3      | ☐ Todo  |  |
| P2·C4      | ☐ Todo  |  |

**Next up:** P2·C1 — Session Lifecycle Endpoints

_Last updated: (auto-populated by commit time)_
