# CrapsSim-Vanilla API Roadmap (CSC Adapter)

**Objective**  
Expose a minimal, deterministic HTTP API on top of CrapsSim-Vanilla that CSC (and other controllers) can drive. Core math remains untouched. The API is an **adapter**: small, stable JSON contracts; deterministic by construction; truthful capabilities.

**Final Deliverable (PR title)**  
_Add deterministic HTTP API adapter for CrapsSim-Vanilla (v0.1.0-api)._

---

## Phase 1 — API Scaffolding & Determinism Contract
**Goal:** Framework + versioning + seeded determinism.

- **P1·C1 — Adapter skeleton**: `crapssim_api/{http.py,state.py,rng.py,errors.py,events.py}`
- **P1·C2 — Determinism harness**: seeded RNG wrapper; action/roll tape recorder; reproducibility test
- **P1·C3 — Version & schema**: `engine_api.version`, `capabilities.schema_version`
- **P1·C4 — Baseline conformance**: identical outputs for identical `{spec, seed, tape}`; tag `v0.1.0-api-phase1`

**Exit:** Determinism proven; constants surfaced; core untouched.

---

## Phase 2 — Session Lifecycle + Capabilities
**Goal:** Start/end sessions and report truthful capabilities.

- **P2·C1 — `/start_session` + `/end_session`**: accept `{spec, seed}`; return `{session_id, snapshot}`
- **P2·C2 — `/capabilities`**: bet families, increments/limits, odds policy (3-4-5), commission modes/rounding/floors, field pays, prop catalog
- **P2·C3 — Identity & idempotency**: echo `{spec, seed}`; idempotency key on mutating calls
- **P2·C4 — Docs**: `docs/API_LIFECYCLE.md`; tag `v0.1.0-api-phase2`

**Exit:** Stable session lifecycle; truthful capabilities JSON.

---

## Phase 3 — Actions, Legality, Errors
**Goal:** CSC verbs with timing/legality enforcement and machine-readable errors.

- **P3·C1 — Action registry**: `POST /apply_action` maps verbs → engine ops (`place|buy|lay|put|pass_line|dont_pass|come|dont_come|odds|hardway|field|prop|big6|big8|horn|world`)
- **P3·C2 — Legality**: increments, limits, timing windows (odds require base; no mid-resolve pulls)
- **P3·C3 — Errors**: `{code, hint, at_state}` with codes: `ILLEGAL_TIMING, ILLEGAL_AMOUNT, UNSUPPORTED_BET, LIMIT_BREACH, INSUFFICIENT_FUNDS, TABLE_RULE_BLOCK, BAD_ARGS`
- **P3·C4 — Tests**: timing rejections; insufficient funds; increments/limits
- **P3·C5 — Docs**: verbs + error catalog; tag `v0.1.0-api-phase3`

**Exit:** Safe, deterministic actions; clear errors.

---

## Phase 4 — Roll Stepping & Event Journal
**Goal:** Atomic toss resolution with ordered events and single source-of-truth snapshot.

- **P4·C1 — `/step_roll`**: `{"mode":"auto"}` (seed RNG) or `{"mode":"inject","dice":[d1,d2]}`
- **P4·C2 — Event schema**: `hand_started, puck_on/off, point_set, bet_placed, bet_traveled, bet_resolved{payout,commission}, payment, seven_out, hand_ended`
- **P4·C3 — Snapshot generator**: stable JSON for puck/point/dice/bankroll/bets/flags/identity
- **P4·C4 — Tests**: point cycles, seven-outs, event ordering
- **P4·C5 — Docs**: `docs/API_SNAPSHOT.md`; tag `v0.1.0-api-phase4`

**Exit:** Events + snapshots consistent across endpoints.

---

## Phase 5 — Tape Export/Import & Replay
**Goal:** Deterministic replay with hashing.

- **P5·C1 — `GET /export_tape`**: `{actions, rolls, run_hash, tape_hash, capabilities_hash}`
- **P5·C2 — `POST /import_tape`**: re-run and verify parity
- **P5·C3 — Tests**: bit-for-bit equality on replay
- **P5·C4 — Docs**: `docs/API_REPLAY.md`; tag `v0.1.0-api-phase5`

**Exit:** Replay parity verified.

---

## Phase 6 — Docs, Conformance Suite, Release Candidate
**Goal:** Professional docs + self-test battery.

- **P6·C1 — Commission docs**: `GET /docs/commission` with worked examples (on_win vs on_bet + ceil + floor)
- **P6·C2 — Conformance mini-suite**: payouts (Place/Buy/Lay/Odds incl. 3-4-5), field/hardways, timing rejections, rounding ties, replay parity
- **P6·C3 — Docs polish**: `docs/API_OVERVIEW.md`, endpoint inventory, schema examples
- **P6·C4 — Tag & PR**: `v0.1.0-api` and submit adapter PR

**Exit:** Conformance green; adapter isolated; core untouched.

---

## Guardrails
- **Zero core mutations** — all API code in `crapssim_api/`
- **Deterministic by construction** — seed + tape; injected dice supported
- **Small reversible phases** — each tagged; easy rollback
- **Truthful capabilities** — no promises the engine can’t keep
- **Out of scope remains out** — strategies/DSL/risk/journals stay in CSC

---

## Minimal Endpoint Inventory (MVP)
- `POST /start_session`  
- `POST /end_session`  
- `GET /capabilities`  
- `POST /apply_action`  
- `POST /step_roll`  
- *(Pre-GA)* `GET /export_tape`, `POST /import_tape`

