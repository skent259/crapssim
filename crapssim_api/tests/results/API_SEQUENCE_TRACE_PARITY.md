# CrapsSim API — Sequence Trace Parity (API vs Vanilla)

## Summary

- Total scenarios: 12
- Perfect matches: 12
- Mismatches: 0

## Scenario Parity

| Scenario | Result | Error Code | Bankroll (API) | Bankroll (Vanilla) | Bets Match? | Status |
| --- | --- | --- | --- | --- | --- | --- |
| bet_management_cycle_sequence | ok |  | 361.00 | 361.00 | ✅ | ✅ |
| come_and_odds_hit_sequence | ok |  | 300.00 | 300.00 | ✅ | ✅ |
| dont_come_sequence_with_error | ok |  | 215.00 | 215.00 | ✅ | ✅ |
| dont_pass_with_odds_win | ok |  | 290.00 | 290.00 | ✅ | ✅ |
| field_and_props_chain | ok |  | 204.00 | 204.00 | ✅ | ✅ |
| hardway_hit_break_rebet_sequence | ok |  | 370.00 | 370.00 | ✅ | ✅ |
| mixed_success_and_failure_actions | ok |  | 130.00 | 130.00 | ✅ | ✅ |
| odds_without_base_error | error | TABLE_RULE_BLOCK | 250.00 | 250.00 | ✅ | ✅ |
| pass_line_with_odds_hit_sequence | ok |  | 310.00 | 310.00 | ✅ | ✅ |
| place_chain_with_seven_out | ok |  | 246.00 | 246.00 | ✅ | ✅ |
| press_6_8_then_buy_4_sequence | ok |  | 214.00 | 214.00 | ✅ | ✅ |
| prop_bets_resolution_cycle | ok |  | 464.00 | 464.00 | ✅ | ✅ |

All scenarios matched across API and vanilla harnesses.