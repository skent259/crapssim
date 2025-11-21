# CrapsSim Engine API — Determinism & Replay Contract

This document describes how determinism works for the CrapsSim Engine API and how external tools (for example CSC, Evo, or research notebooks) can rely on it.

## What “Deterministic” Means Here

Given:

- the same CrapsSim engine version,
- the same initial table configuration,
- the same initial bankroll,
- the same seed, and
- the same sequence of dice rolls,

the API must produce the same sequence of game events and the same final bankroll and layout every time.

The Engine API does **not** introduce its own game logic. It only forwards requests to CrapsSim and returns structured responses. CrapsSim remains the single source of truth for rules, payouts, and push/lose/win semantics.

## Seed Lifecycle (High-Level)

At a high level:

1. A client starts a session with a seed (or a default if none is provided).
2. CrapsSim uses that seed to drive its RNG for dice rolls (or for any internal random decisions, if applicable).
3. Each roll is derived deterministically from the RNG state.
4. The Engine API exposes those rolls and outcomes but never mutates them.

Phase 4 will clarify:

- how seeds are accepted and recorded,
- how roll sequences are exposed for replay, and
- what parts of the response are guaranteed stable versus “implementation detail” metadata.

## Replay Tapes (Concept)

A **replay tape** is a minimal, portable representation of a session that can be used later to reproduce the same results.

Conceptually, a tape looks like:

```json
{
  "engine_version": "0.4.x",
  "table_config": { "...": "..." },
  "initial_bankroll": 250,
  "seed": 123456,
  "rolls": [[3, 4], [2, 2], [6, 1]]
}
```

Future phases will add endpoints that:
- export the tape for a finished or in-progress session, and
- import a tape for deterministic replay with no additional randomness.

The Engine API will only marshal this data; CrapsSim remains responsible for applying the rolls and determining outcomes.

## Guaranteed vs. Non-Guaranteed Fields

The following are expected to be stable under a fixed version of CrapsSim and the Engine API:
- per-roll dice results (order and values),
- per-roll outcome classification (win/lose/push as defined by CrapsSim),
- bankroll trajectory over the session,
- final bankroll and layout, including which bets remain.

The following are not guaranteed to be stable and may evolve over time:
- human-readable status strings or error messages,
- ordering of non-critical metadata fields,
- internal identifiers that are not part of the public API schema.

Consumers who need determinism should base their comparisons on:
- bankroll,
- bets and amounts,
- dice sequences,
- result codes (OK / error + error code),
- and any explicit, versioned fields in the API types.

## Cross-Version Considerations

Determinism is guaranteed within a compatible version band:
- Same CrapsSim engine version,
- Same CrapsSim Engine API version,
- Same Python minor version (validated via CI).

A future-breaking engine change may alter edge-case behavior or payout details. When that happens:
- The engine version will change.
- The API will surface that version so clients can gate against it.
- Deterministic replay is expected only when the original and replay environments match in version and configuration.

## How External Tools Should Use This

External tools (CSC, Evo, notebooks, etc.) should:
1. Record:
   - engine and API version,
   - seed,
   - table configuration,
   - initial bankroll,
   - roll sequence (or tape).
2. Treat the Engine API as a deterministic function given those inputs.
3. Use replay tapes to:
   - debug specific runs,
   - compare engine behavior across environments,
   - demonstrate reproducibility in research and analysis.

Later phases will define the concrete JSON schemas for tapes and endpoints to export/import them. This document captures the contract and expectations that those endpoints must satisfy.

## Replay Tape Determinism — Phase 4 Completion

The API now guarantees deterministic behavior across Python versions when seeds are consistent and replay tapes are enabled. A replay tape logs every inbound command and outbound event, allowing bit-for-bit reproduction of an entire session.

Replaying a tape bypasses randomness entirely. If a tape is loaded, the API issues events exactly as recorded, ensuring stable comparison across engine releases.

Tapes remain optional for end users. Only developers and researchers need them. Standard sessions use the seed-based RNG path.
