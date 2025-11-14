# API Test Notes

### RNG & Seed Behavior

- `/session/start` accepts an optional `seed` parameter.
- The seed is applied once when the session is created; subsequent `/session/roll` calls do **not** re-seed the RNG.
- Within a session, each call to `/session/roll` advances the RNG, producing a sequence of dice outcomes.
- Fixed/forced dice (if enabled) are opt-in and do not affect the default RNG path.
- The API test suite includes `tests/api/test_rng_sanity.py` to guard against regressions (e.g., accidental "same roll every time" behavior).
