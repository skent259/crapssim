# CrapsSim HTTP API — Seeds and Sessions

This document explains how RNG seeds and sessions interact in the CrapsSim HTTP API.

The key idea: **seeds apply to sessions, not individual rolls**. Once a session is started with a seed, its sequence of random dice rolls is deterministic, but it still advances roll by roll like a normal game.

---

## 1. Session-level seeding

When you call `/session/start`, you may provide an optional `seed` field:

```json
{
  "seed": 12345,
  "profile_id": "default"
}

The API uses this seed to initialize the random number generator for that session. After that:
•each call to /session/roll that does not supply explicit dice will consume the next random outcome from that session’s RNG
•the sequence of random outcomes is deterministic for that session, given the same seed and the same sequence of actions

If you create another session with the same seed and the same behavior (same order of actions and rolls), you should get the same series of random rolls.

⸻

2. Roll-by-roll behavior

The engine does not reset the RNG between rolls.
•Roll 1 uses the first random sample derived from the seed.
•Roll 2 uses the next random sample.
•Roll N uses the N-th sample, and so on.

This prevents “Groundhog Day” behavior where the same roll repeats forever. Instead, the seed simply pins down one particular path through the space of possible sequences.

⸻

3. Explicit dice vs RNG

The roll endpoint typically supports two modes for dice:
1.Implicit/random dice (RNG-based):

{
  "session_id": "session-uuid-or-token"
}

In this case, the session’s RNG is used to generate dice for the roll.

2.Explicit dice (caller-provided):

{
  "session_id": "session-uuid-or-token",
  "dice": [3, 4]
}

In this case:
•the engine uses [3, 4] as the dice values for that roll
•the RNG for the session may either:
•skip advancement for this roll, or
•advance in a well-defined way (implementation detail)

The exact semantics (whether the RNG advances when explicit dice are supplied) are defined in the implementation, but the core contract is:
•if you provide dice, those values drive the game outcome for that roll
•if you omit dice, the RNG (seeded per session) is used

⸻

4. Reproducible experiments

For deterministic experiments, a typical workflow is:
1.Start a session with a given seed:

{
  "seed": 4242,
  "profile_id": "default"
}


2.Apply a known sequence of actions (bets, removals, etc.).
3.Call /session/roll the same number of times in the same order.

If you repeat the experiment with the same seed and the same sequence of actions, you should get:
•the same dice totals (when using RNG-based rolls)
•the same bankroll trajectories
•the same hand/point transitions

If you change the seed, you change the entire sequence.

⸻

5. Multiple sessions and seeds

Sessions are isolated:
•each session has its own RNG state
•seeding one session does not affect any others
•concurrent sessions with the same seed may still diverge if they take different actions or roll counts

This isolation is important for tools like CSC and other clients that may run many simulations side by side.

⸻

6. Practical tips
•For general play or interactive use, you can omit seed entirely and let the engine choose.
•For testing, baselines, or analysis, always specify a seed on /session/start.
•When using explicit dice (dice: [d1, d2]), keep in mind you are now responsible for the sequence; RNG seeding still matters for any rolls where dice is omitted.

The design goal is to keep deterministic workflows possible without changing how the craps engine itself behaves: the HTTP API supplies session-scoped seeding and optional explicit dice, but the core game logic remains the same.

---
