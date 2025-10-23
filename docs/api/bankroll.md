# Mock Bankroll Ledger (Phase 3 · C3)

The adapter maintains a deterministic bankroll ledger per `session_id`.

- Default bankroll: `$1000.00`
- Deducts bet amount when `/apply_action` accepts an action
- Rejects with `INSUFFICIENT_FUNDS` when bankroll too low
- No persistence or payout; resets with new session_id
- Used only for adapter-level validation and determinism
