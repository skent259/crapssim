# CrapsSim Engine API — Developer Notes

These notes capture implementation guidance and internal conventions for the Engine API. Consult the main docs for user-facing guidance.

## Determinism & Replay (Phase 4)

Phase 4 introduces a formal determinism contract and replay-tape concept:

- Determinism is defined as: same engine/API version, same seed, same tape of dice → same outcomes.
- The Engine API must not add its own randomness or betting rules.
- Replay tapes will be implemented as JSON structures that capture seed, table config, bankroll, and the roll sequence.
- CI will eventually validate determinism across multiple Python versions using a small, fixed test tape.

Implementation notes:

- Determinism and replay logic should live as close to the engine boundary as possible.
- Any new fields added for determinism or replay must be versioned and documented.
- Behavior changes belong in the engine; the API should only surface them.
