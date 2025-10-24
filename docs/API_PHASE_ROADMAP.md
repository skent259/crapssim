# Phase 4 — Event & Roll Flow Framework

**Goal:** Extend the API to handle roll stepping and event sequencing while maintaining determinism.

## Checkpoints
| ID | Title | Status | Summary |
|:--:|:------|:-------|:---------|
| P4·C0 | Docs Kickoff + Baseline Sync | ✅ Implemented | Tag fix, re-baseline, update docs. |
| P4·C1 | Roll Stepping Endpoint Scaffold | ✅ Implemented | Basic deterministic dice and state ledger |
| P4·C2 | Event Stream Envelope | ✅ Implemented | Emits hand_started, roll_started, roll_completed |
| P4·C3 | State Machine Integration | ⏳ Pending | Connect roll/results with session state. |
| P4·C4 | Baseline & Tag | ⏳ Pending | Capture v0.4.0-api-p4. |
| P4·C5 | Finalize Phase 4 baseline and prep release | ✅ Complete | Tag v0.4.0-api-p4 pushed |
| P5·C0 | Hand State scaffolds (puck/point/hand_id) wired into snapshot; no behavior change | ✅ Implemented |
| P5·C1 | Implement come-out & point cycle transitions (ON/OFF, hand end) | ✅ Implemented |
