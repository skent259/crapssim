# CrapsSim-Vanilla API Roadmap

This document tracks a minimal, engine-first API that exposes state and hooks without adding extra services or changing game behavior. The API is designed so other projects (e.g., CSC) can observe and drive simulations deterministically while keeping Vanilla focused on legal bet resolution.

---

## Principles

- **Engine-only**: No network/server code inside Vanilla by default.
- **Determinism**: Given the same specs and dice, outcomes match.
- **Low overhead**: Simple dataclasses, no heavy deps.
- **Dumb I/O**: Emit raw state deltas; consumers compute analytics.

---

## Phase 1 — Engine Contract & Internal Event Bus (this PR)

**Goal:** Define typed contracts (`EngineState`, `EngineCommand`, `EngineResult`) and a minimal synchronous `EventBus`.  
**No behavior changes.** No wiring into the engine yet.

**Deliverables:**
- `crapssim/api/contract.py` — dataclasses & `EngineContract` protocol
- `crapssim/api/events.py` — minimal in-process `EventBus`
- `tests/unit/test_api_contract.py` — structural tests
- `REPORT_P1.md` — verification notes

---

## Phase 2 — Engine Adapter & Snapshot Mapping

**Goal:** Implement a thin adapter that maps current `Table`/`Dice`/`Player` state into `EngineState`.  
Add lightweight emit points (e.g., after roll resolution) using `EventBus`.  
**Behavior remains unchanged.**

**Deliverables:** adapter module, snapshot mapper, unit tests, `REPORT_P2.md`.

---

## Phase 3 — Command Path (Deterministic Apply)

**Goal:** Support a minimal set of commands (`roll`, `bet`, `remove`) routed through the adapter with legality checks delegated to existing engine paths.  
Add tests proving replay parity (live vs scripted).

**Deliverables:** command router, parity tests, `REPORT_P3.md`.

---

## Phase 4 — Tape Export/Import

**Goal:** Add a stable “tape” (JSONL) for states/commands enabling reproducible replays.  
No external services.

**Deliverables:** tape writer/reader, tests, `REPORT_P4.md`.

---

## Phase 5 — Capability Surface & Error Codes

**Goal:** Provide a discoverable capability map and explicit error codes/messages for rejected commands.  
No logic changes—only structured reporting.

**Deliverables:** capability query, error enums, tests, `REPORT_P5.md`.

---

## Phase 2 — Engine Adapter & Snapshot Mapping

**Goal:** Implement a thin adapter that maps current `Table`/`Dice`/`Player` state into `EngineState`, and emit events using `EventBus`.  
No command routing or networking yet.

**Deliverables**
- `crapssim/api/adapter.py` — EngineAdapter implementing EngineContract
- `crapssim/api/hooks.py` — minimal hook emitter
- `tests/unit/test_api_adapter.py` — deterministic snapshot and event tests
- `REPORT_P2.md` — verification notes

## Phase 3 — Command Routing & Legality Gate (in-process)

**What:** A minimal router that accepts structured commands, validates legality/timing/funds using vanilla logic, applies them, and returns a fresh snapshot.  
**No networking. No new services.**

**Verbs (v1):** `add_bet`, `remove_bet`, `press_bet`, `regress_bet` (may be UNSUPPORTED), `set_dice` (debug only), `roll`, `clear_all` (test convenience).

**Result:** Each command returns `{ success, error?, state }`. Errors use stable codes: `ILLEGAL_BET`, `BAD_INCREMENT`, `INSUFFICIENT_FUNDS`, `NOT_FOUND`, `FORBIDDEN`, `UNSUPPORTED`, `BAD_ARGUMENTS`, `INTERNAL`.

**Guarantees:** No changes to bet math; the router delegates to existing Table/Player/Bet behaviors. Fixed-dice is gated behind `debug.allow_fixed_dice`.
