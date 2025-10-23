# API Error Contract

All endpoints return machine-readable envelopes for errors.

```json
{
  "code": "BAD_ARGS",
  "hint": "seed must be int",
  "at_state": { "session_id": null, "hand_id": null, "roll_seq": null }
}
```

| Code | HTTP | Meaning |
| --- | --- | --- |
| BAD_ARGS | 400 | Schema or type mismatch |
| TABLE_RULE_BLOCK | 409 | Table configuration prohibits action |
| INSUFFICIENT_FUNDS | 409 | Bankroll too low for attempted action |
| UNSUPPORTED_BET | 422 | Bet family not implemented |
| INTERNAL | 500 | Unexpected server error |

## Examples

- Non-int seed ⇒ 400 BAD_ARGS
- Enabling fire prop when unsupported ⇒ 422 UNSUPPORTED_BET
- Odds limit > 20 ⇒ 409 TABLE_RULE_BLOCK

Use these consistently for all mutating calls.
