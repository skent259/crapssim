# Action Legality & Timing (Phase 3 · C2)

The adapter validates actions before they reach the engine.

## Timing Windows
- **Line bets** (`pass_line`, `dont_pass`) — only on come-out (`puck = OFF`).
- **Box bets** (`place`, `buy`, `lay`, `put`) — only after point is established (`puck = ON`).
- Any action during resolve (`puck = MOVING`) is rejected.

## Amounts & Increments
- Box-addressed bets must match table increments from `/capabilities.increments.place`
  (e.g., 6/8 by $6; 4/5/9/10 by $5).
- Whole-dollar enforcement at this checkpoint.

## Limits
- Rejected if amount exceeds table cap (placeholder policy).
- Odds-specific checks arrive in P3 · C3.

## Errors
| Code | HTTP | Meaning |
|------|------|---------|
| `ILLEGAL_TIMING` | 409 | Not allowed in current state |
| `ILLEGAL_AMOUNT` | 422 | Violates minimum/increment |
| `LIMIT_BREACH` | 422 | Exceeds table/odds limits |
| `UNSUPPORTED_BET` | 422 | Unknown or disabled verb |
