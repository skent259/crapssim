# Phase 5 Kickoff — Hand State Machine (Scaffolds Only)

This checkpoint introduces a centralized hand-state ledger (puck/point/hand_id) exposed in snapshots, without altering core engine behavior.

## What changed
- Added `HandState` (`puck`, `point`, `hand_id`)
- Added `SessionStore` for adapter-level session tracking
- Wired `/step_roll` and `/start_session` to read hand fields from the ledger

## What did NOT change
- No automatic point setting/clearing
- No puck transitions
- No payouts or bet travel

These behaviors will be implemented with explicit, reviewable steps in subsequent P5 checkpoints.
