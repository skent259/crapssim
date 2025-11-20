# Push Reporting in CrapsSim API

The API does not implement game logic. CrapsSim engine remains the sole
authority for all win/lose/push outcomes.

The API reports push outcomes using the following rules:

1. If the engine provides an explicit push signal, the API forwards it exactly.
2. If the engine returns a no-change bet resolution that corresponds to a
   legitimate push scenario, the API marks the result as `is_push = true`.
3. No game rules are encoded in the API. All detection is based strictly on:
   - engine deltas,
   - bet lifecycle, and
   - resolution structures.

This preserves engine truthfulness while enabling higher-level consumers
(e.g., CSC or Node-RED pipelines) to distinguish pushes reliably.
