# CrapsSim API — Roll-by-Roll Sequence Trace (Vanilla)

## Summary

- Total scenarios: 12
- Successful (final result ok): 11
- With errors: 1

## Scenario: press_6_8_then_buy_4_sequence

- Initial bankroll: 250.00
- Initial bets: PassLine: $15

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | comeout_point_four | 2+2 | (none) | 235.00 → 235.00 | PassLine: $15 |
| 1 | hit_six_and_press | 4+2 | place 6:30 ok; place 8:30 ok | 235.00 → 175.00 | PassLine: $15; Place 6: $30; Place 8: $30 |
| 2 | buy_four | — | buy 4:25 ok | 175.00 → 149.00 | Buy 4: $25; PassLine: $15; Place 6: $30; Place 8: $30 |
| 3 | resolve_place_eight | 6+2 | (none) | 149.00 → 214.00 | Buy 4: $25; PassLine: $15; Place 6: $30 |
| 4 | seven_out | 3+4 | (none) | 214.00 → 214.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 214.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```

## Scenario: pass_line_with_odds_hit_sequence

- Initial bankroll: 250.00
- Initial bets: PassLine: $15

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | comeout_point_five | 4+1 | (none) | 235.00 → 235.00 | PassLine: $15 |
| 1 | add_pass_odds | — | odds 30 pass_line ok | 235.00 → 205.00 | Odds 5: $30; PassLine: $15 |
| 2 | point_hit | 3+2 | (none) | 205.00 → 310.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 310.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```

## Scenario: place_chain_with_seven_out

- Initial bankroll: 250.00
- Initial bets: PassLine: $10

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | comeout_point_eight | 6+2 | (none) | 240.00 → 240.00 | PassLine: $10 |
| 1 | place_numbers | — | place 6:18 ok; place 5:15 ok | 240.00 → 207.00 | PassLine: $10; Place 5: $15; Place 6: $18 |
| 2 | hit_place_six | 5+1 | (none) | 207.00 → 246.00 | PassLine: $10; Place 5: $15 |
| 3 | seven_out | 3+4 | (none) | 246.00 → 246.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 246.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```

## Scenario: mixed_success_and_failure_actions

- Initial bankroll: 80.00
- Initial bets: PassLine: $15

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | comeout_point_six | 4+2 | (none) | 65.00 → 65.00 | PassLine: $15 |
| 1 | place_six_success | — | place 6:30 ok | 65.00 → 35.00 | PassLine: $15; Place 6: $30 |
| 2 | place_eight_insufficient | — | place 8:60 error (INSUFFICIENT_FUNDS) | 35.00 → 35.00 | PassLine: $15; Place 6: $30 |
| 3 | point_hit | 5+1 | (none) | 35.00 → 130.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 130.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```

## Scenario: hardway_hit_break_rebet_sequence

- Initial bankroll: 200.00
- Initial bets: (none)

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | establish_hardways | — | hardway 6:10 ok; hardway 8:10 ok | 200.00 → 180.00 | HardWay 6: $10; HardWay 8: $10 |
| 1 | hard_six_hits | 3+3 | (none) | 180.00 → 280.00 | HardWay 8: $10 |
| 2 | rebet_hard_six | — | hardway 6:10 ok | 280.00 → 270.00 | HardWay 6: $10; HardWay 8: $10 |
| 3 | easy_six_breaks | 4+2 | (none) | 270.00 → 270.00 | HardWay 8: $10 |
| 4 | hard_eight_hits | 4+4 | (none) | 270.00 → 370.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 370.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```

## Scenario: field_and_props_chain

- Initial bankroll: 150.00
- Initial bets: (none)

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | enter_field_and_any7 | — | field 25 ok; any7 5 ok | 150.00 → 120.00 | Any7: $5; Field: $25 |
| 1 | seven_roll | 2+5 | (none) | 120.00 → 145.00 | (none) |
| 2 | horn_and_world | — | horn 16 ok; world 5 ok | 145.00 → 124.00 | Horn: $16; World: $5 |
| 3 | horn_three | 1+2 | (none) | 124.00 → 204.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 204.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```

## Scenario: dont_pass_with_odds_win

- Initial bankroll: 250.00
- Initial bets: DontPass: $20

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | comeout_point_ten | 6+4 | (none) | 230.00 → 230.00 | DontPass: $20 |
| 1 | add_dont_pass_odds | — | odds 40 dont_pass ok | 230.00 → 190.00 | DontPass: $20; Odds 10: $40 |
| 2 | seven_out | 3+4 | (none) | 190.00 → 290.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 290.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```

## Scenario: come_and_odds_hit_sequence

- Initial bankroll: 250.00
- Initial bets: PassLine: $10

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | comeout_point_nine | 5+4 | (none) | 240.00 → 240.00 | PassLine: $10 |
| 1 | come_bet_moves | — | come 15 ok | 240.00 → 225.00 | Come: $15; PassLine: $10 |
| 2 | come_bet_travels | 3+2 | (none) | 225.00 → 225.00 | Come 5: $15; PassLine: $10 |
| 3 | add_odds_to_come | — | odds 5:30 come ok | 225.00 → 195.00 | Come 5: $15; Odds 5: $30; PassLine: $10 |
| 4 | resolve_come_number | 4+1 | (none) | 195.00 → 300.00 | PassLine: $10 |
| 5 | seven_out | 3+4 | (none) | 300.00 → 300.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 300.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```

## Scenario: dont_come_sequence_with_error

- Initial bankroll: 180.00
- Initial bets: DontPass: $15

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | comeout_point_nine | 6+3 | (none) | 165.00 → 165.00 | DontPass: $15 |
| 1 | dont_come_bet | — | dont_come 20 ok | 165.00 → 145.00 | DontCome: $20; DontPass: $15 |
| 2 | dont_come_travel | 2+2 | (none) | 145.00 → 145.00 | DontCome 4: $20; DontPass: $15 |
| 3 | invalid_odds_attempt | — | odds 25 dont_come error (TABLE_RULE_BLOCK) | 145.00 → 145.00 | DontCome 4: $20; DontPass: $15 |
| 4 | seven_out | 3+4 | (none) | 145.00 → 215.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 215.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```

## Scenario: odds_without_base_error

- Initial bankroll: 250.00
- Initial bets: (none)

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | odds_without_passline | — | odds 25 pass_line error (TABLE_RULE_BLOCK) | 250.00 → 250.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 250.0,
    "bets": [],
    "error_code": "TABLE_RULE_BLOCK",
    "result": "error"
  }
}
```

## Scenario: prop_bets_resolution_cycle

- Initial bankroll: 360.00
- Initial bets: PassLine: $15

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | load_prop_suite | — | fire 5 ok; all 5 ok; tall 5 ok; small 5 ok | 345.00 → 325.00 | All: $5; Fire: $5; PassLine: $15; Small: $5; Tall: $5 |
| 1 | comeout_point_six | 3+3 | (none) | 325.00 → 325.00 | All: $5; Fire: $5; PassLine: $15; Small: $5; Tall: $5 |
| 2 | enter_hop_and_world | — | world 10 ok; horn 16 ok; hop 10 result=[2, 4] ok | 325.00 → 289.00 | All: $5; Fire: $5; Hop: $10; Horn: $16; PassLine: $15; Small: $5; Tall: $5; World: $10 |
| 3 | point_made_with_hop | 2+4 | (none) | 289.00 → 479.00 | All: $5; Fire: $5; Small: $5; Tall: $5 |
| 4 | re_establish_pass_line | — | pass_line 15 ok | 479.00 → 464.00 | All: $5; Fire: $5; PassLine: $15; Small: $5; Tall: $5 |
| 5 | new_point_five | 3+2 | (none) | 464.00 → 464.00 | All: $5; Fire: $5; PassLine: $15; Small: $5; Tall: $5 |
| 6 | seven_out_clears_props | 4+3 | (none) | 464.00 → 464.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 464.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```

## Scenario: bet_management_cycle_sequence

- Initial bankroll: 320.00
- Initial bets: PassLine: $15; Place 6: $30; Place 8: $30

| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |
| ------ | ----- | ---- | ------- | ------------------------ | ----------- |
| 0 | comeout_point_six | 4+2 | (none) | 245.00 → 310.00 | PassLine: $15; Place 8: $30 |
| 1 | establish_odds_and_come | — | odds 30 pass_line ok; come 15 ok | 310.00 → 265.00 | Come: $15; Odds 6: $30; PassLine: $15; Place 8: $30 |
| 2 | come_moves_to_five | 3+2 | (none) | 265.00 → 265.00 | Come 5: $15; Odds 6: $30; PassLine: $15; Place 8: $30 |
| 3 | add_come_odds_and_toggle_off | — | odds 5:30 come ok; set_odds_working come working=False ok | 265.00 → 235.00 | Come 5: $15; Odds 5: $30; Odds 6: $30; PassLine: $15; Place 8: $30 |
| 4 | reduce_and_remove_place | — | reduce_bet new_amount=18 type=place ok; remove_bet type=place ok | 235.00 → 265.00 | Come 5: $15; Odds 5: $30; Odds 6: $30; PassLine: $15 |
| 5 | hit_point_six | 5+1 | (none) | 265.00 → 361.00 | Come 5: $15; Odds 5: $30 |
| 6 | toggle_come_odds_on | — | set_odds_working come working=True ok | 361.00 → 361.00 | Come 5: $15; Odds 5: $30 |
| 7 | seven_out_resolves | 4+3 | (none) | 361.00 → 361.00 | (none) |
| 8 | rebuild_single_place | — | place 8:18 ok | 361.00 → 343.00 | Place 8: $18 |
| 9 | clear_remaining_layout | — | clear_all_bets ok | 343.00 → 361.00 | (none) |

```json
{
  "final_state": {
    "bankroll": 361.0,
    "bets": [],
    "error_code": null,
    "result": "ok"
  }
}
```
