# CrapsSim Engine API — Determinism & Replay Contract

This document outlines how determinism works for the CrapsSim Engine API and how external tools (CSC, Evo, research notebooks) can rely on it.

## Seed-Based Determinism vs. Replay Tapes

- **Seeded sessions**: A client provides a seed (or accepts a default). The engine’s RNG produces dice in a deterministic order. Given the same engine/API version, table configuration, bankroll, and seed, you should see the same rolls, outcomes, and bankroll trajectory. This is the default path for day-to-day use.
- **Replay tapes**: A recorded sequence of inputs and engine-emitted events. Loading a tape bypasses RNG entirely and replays the captured dice and outcomes. Tapes are optional and aimed at research, debugging, and compatibility audits.

The Engine API never injects game logic; it forwards requests to CrapsSim and returns its structured responses. CrapsSim remains the single source of truth for rules, payouts, and push/lose/win semantics. Tapes simply record and reapply those engine decisions.

## Seed Lifecycle (High-Level)

1. A client starts a session with a seed (or a default if none is provided).
2. CrapsSim uses that seed to drive its RNG for dice rolls (or any internal randomness).
3. Each roll is derived deterministically from the RNG state.
4. The Engine API exposes those rolls and outcomes but never mutates them.

## Replay Tapes (Concept)

A **replay tape** is a portable representation of a session that can be used later to reproduce the same results.

```json
{
  "engine_version": "0.4.x",
  "table_config": { "...": "..." },
  "initial_bankroll": 250,
  "seed": 123456,
  "rolls": [[3, 4], [2, 2], [6, 1]]
}
```

Exporting a tape captures the recorded dice and outcomes; importing a tape drives a fresh engine instance with no additional randomness. When a tape is present, it takes precedence over seeds for reproduction.

## Guaranteed vs. Non-Guaranteed Fields

Stable under a fixed engine/API version:
- per-roll dice results (order and values),
- per-roll outcome classification (win/lose/push as defined by CrapsSim),
- bankroll trajectory over the session,
- final bankroll and layout, including which bets remain.

Not guaranteed to be stable and may evolve over time:
- human-readable status strings or error messages,
- ordering of non-critical metadata fields,
- internal identifiers that are not part of the public API schema.

Consumers who need determinism should base comparisons on bankroll, bets/amounts, dice sequences, result codes, and versioned API fields.

## Cross-Version Considerations

Determinism is guaranteed within a compatible version band:
- Same CrapsSim engine version,
- Same CrapsSim Engine API version,
- Same Python minor version (validated via CI).

When the engine changes, expect deterministic parity only when the original and replay environments match in version and configuration.

## Replay Tape Determinism — Phase 4 Completion

The API guarantees deterministic behavior across supported Python versions when seeds are consistent and replay tapes are enabled. A replay tape logs every inbound command and outbound event, allowing bit-for-bit reproduction of an entire session. Loading a tape issues events exactly as recorded, ensuring stable comparisons across engine releases so long as tape compatibility holds.

Tapes remain optional for end users. Only developers and researchers need them. Standard sessions use the seed-based RNG path.

## How Session Snapshots and Metrics Fit In (Phase 5 Design)

- **Seed vs. tape precedence:** A session started with a seed and no tape is deterministic within a specific engine/API version. Loading a replay tape overrides RNG entirely and must reproduce the recorded dice and outcomes, even across engine updates as long as the tape format remains compatible.
- **Read-only views:** Session state snapshots and metrics surfaces serialize the engine’s live truth. They do not introduce inference, policy, or reconciliation logic.
- **Consistency expectations:**
  - With a seed-only session, snapshots and metrics are stable for a given engine version but can change if engine behavior legitimately evolves.
  - With a loaded tape, snapshots and metrics must match the recorded sequence and outcomes exactly, enabling cross-version regression checks as long as tape compatibility holds.
- **Capture points:** Snapshots and metrics may be taken at any time during a session. Exporting a tape and replaying it should yield identical snapshot/metric outputs at the same roll/hand indices.
- **Source-of-truth reminder:** The core engine remains authoritative. The API is a transport/serialization layer that must not attempt to “fix” or recalculate anything during snapshot or metric emission.

## See also
- [Docs index](index.md)
- [Developer stress and gauntlet tests](dev/testing.md)
