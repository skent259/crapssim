# Phase 5 · C1 — Come-Out & Point Cycle

This checkpoint adds true table rhythm to the API:
- Come-out rolls that land on 4,5,6,8,9,10 set the point and flip the puck to ON.
- When the puck is ON, rolling the point or a 7 ends the hand and returns to OFF.
- API emits `point_set`, `point_made`, `seven_out`, `hand_ended` with deterministic IDs.

No payouts or bet movements occur in this phase.

**Event hand ownership:** state-events (`point_made`, `seven_out`, `hand_ended`) are emitted with the *ending* hand_id. The response snapshot reflects the *current* state after transitions.
