# CrapsSim Vanilla Engine Surface Stress Report

## Summary

* Total scenarios: **71**
* Successful actions: **40**
* Errors: **31**

## Scenario Results

| Scenario | Verb | Result | Error Code | Expected |
| --- | --- | --- | --- | --- |
| pass_line_basic_ok | pass_line | ok |  | ok |
| pass_line_zero_amount_error | pass_line | error | BAD_ARGS | error (BAD_ARGS) |
| dont_pass_basic_ok | dont_pass | ok |  | ok |
| dont_pass_insufficient_funds | dont_pass | error | INSUFFICIENT_FUNDS | error (INSUFFICIENT_FUNDS) |
| come_point_on_ok | come | ok |  | ok |
| come_point_off_error | come | error | TABLE_RULE_BLOCK | error (TABLE_RULE_BLOCK) |
| dont_come_point_on_ok | dont_come | ok |  | ok |
| dont_come_point_off_error | dont_come | error | TABLE_RULE_BLOCK | error (TABLE_RULE_BLOCK) |
| field_basic_ok | field | ok |  | ok |
| field_negative_amount_error | field | error | BAD_ARGS | error (BAD_ARGS) |
| any7_basic_ok | any7 | ok |  | ok |
| any7_insufficient_funds | any7 | error | INSUFFICIENT_FUNDS | error (INSUFFICIENT_FUNDS) |
| c_and_e_basic_ok | c&e | ok |  | ok |
| c_and_e_non_numeric_amount_error | c&e | error | BAD_ARGS | error (BAD_ARGS) |
| horn_basic_ok | horn | ok |  | ok |
| horn_zero_amount_error | horn | error | BAD_ARGS | error (BAD_ARGS) |
| world_basic_ok | world | ok |  | ok |
| world_insufficient_funds | world | error | INSUFFICIENT_FUNDS | error (INSUFFICIENT_FUNDS) |
| big6_basic_ok | big6 | ok |  | ok |
| big6_zero_amount_error | big6 | error | BAD_ARGS | error (BAD_ARGS) |
| big8_basic_ok | big8 | ok |  | ok |
| big8_insufficient_funds | big8 | error | INSUFFICIENT_FUNDS | error (INSUFFICIENT_FUNDS) |
| place_six_ok | place | ok |  | ok |
| place_invalid_number_error | place | error | BAD_ARGS | error (BAD_ARGS) |
| buy_four_ok | buy | ok |  | ok |
| buy_invalid_number_error | buy | error | BAD_ARGS | error (BAD_ARGS) |
| lay_eight_ok | lay | ok |  | ok |
| lay_invalid_number_error | lay | error | BAD_ARGS | error (BAD_ARGS) |
| put_eight_with_point_ok | put | ok |  | ok |
| put_point_off_error | put | error | TABLE_RULE_BLOCK | error (TABLE_RULE_BLOCK) |
| hardway_six_ok | hardway | ok |  | ok |
| hardway_invalid_number_error | hardway | error | BAD_ARGS | error (BAD_ARGS) |
| odds_pass_line_ok | odds | ok |  | ok |
| odds_missing_base_error | odds | error | TABLE_RULE_BLOCK | error (TABLE_RULE_BLOCK) |
| odds_invalid_base_error | odds | error | BAD_ARGS | error (BAD_ARGS) |
| two_basic_ok | two | ok |  | ok |
| two_negative_amount_error | two | error | BAD_ARGS | error (BAD_ARGS) |
| three_basic_ok | three | ok |  | ok |
| three_zero_amount_error | three | error | BAD_ARGS | error (BAD_ARGS) |
| yo_basic_ok | yo | ok |  | ok |
| yo_negative_amount_error | yo | error | BAD_ARGS | error (BAD_ARGS) |
| boxcars_basic_ok | boxcars | ok |  | ok |
| boxcars_zero_amount_error | boxcars | error | BAD_ARGS | error (BAD_ARGS) |
| any_craps_basic_ok | any_craps | ok |  | ok |
| any_craps_negative_amount_error | any_craps | error | BAD_ARGS | error (BAD_ARGS) |
| hop_basic_ok | hop | ok |  | ok |
| hop_bad_args_error | hop | error | BAD_ARGS | error (BAD_ARGS) |
| fire_basic_ok | fire | ok |  | ok |
| fire_zero_amount_error | fire | error | BAD_ARGS | error (BAD_ARGS) |
| all_basic_ok | all | ok |  | ok |
| all_negative_amount_error | all | error | BAD_ARGS | error (BAD_ARGS) |
| tall_basic_ok | tall | ok |  | ok |
| tall_zero_amount_error | tall | error | BAD_ARGS | error (BAD_ARGS) |
| small_basic_ok | small | ok |  | ok |
| small_negative_amount_error | small | error | BAD_ARGS | error (BAD_ARGS) |
| remove_bet_basic_ok | remove_bet | ok |  | ok |
| remove_bet_no_match_error | remove_bet | error | BAD_ARGS | error (BAD_ARGS) |
| reduce_bet_basic_ok | reduce_bet | ok |  | ok |
| reduce_bet_increase_error | reduce_bet | error | BAD_ARGS | error (BAD_ARGS) |
| clear_all_bets_basic_ok | clear_all_bets | ok |  | ok |
| clear_all_bets_noop_ok | clear_all_bets | ok |  | ok |
| clear_center_bets_basic_ok | clear_center_bets | ok |  | ok |
| clear_center_bets_noop_ok | clear_center_bets | ok |  | ok |
| clear_place_buy_lay_basic_ok | clear_place_buy_lay | ok |  | ok |
| clear_place_buy_lay_noop_ok | clear_place_buy_lay | ok |  | ok |
| clear_ats_bets_basic_ok | clear_ats_bets | ok |  | ok |
| clear_ats_bets_noop_ok | clear_ats_bets | ok |  | ok |
| clear_fire_bets_basic_ok | clear_fire_bets | ok |  | ok |
| clear_fire_bets_noop_ok | clear_fire_bets | ok |  | ok |
| set_odds_working_basic_ok | set_odds_working | ok |  | ok |
| set_odds_working_no_match_error | set_odds_working | error | BAD_ARGS | error (BAD_ARGS) |

## Full Journal

```json
[
  {
    "after_bankroll": 240.0,
    "args": {
      "amount": 10
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 10.0,
        "number": null,
        "type": "PassLine"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "pass_line_basic_ok",
    "verb": "pass_line"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 0
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "pass_line_zero_amount_error",
    "verb": "pass_line"
  },
  {
    "after_bankroll": 235.0,
    "args": {
      "amount": 15
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 15.0,
        "number": null,
        "type": "DontPass"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "dont_pass_basic_ok",
    "verb": "dont_pass"
  },
  {
    "after_bankroll": 150.0,
    "args": {
      "amount": 400
    },
    "before_bankroll": 150.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "INSUFFICIENT_FUNDS",
    "result": "error",
    "scenario": "dont_pass_insufficient_funds",
    "verb": "dont_pass"
  },
  {
    "after_bankroll": 230.0,
    "args": {
      "amount": 20
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 20.0,
        "number": null,
        "type": "Come"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "come_point_on_ok",
    "verb": "come"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 15
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "TABLE_RULE_BLOCK",
    "result": "error",
    "scenario": "come_point_off_error",
    "verb": "come"
  },
  {
    "after_bankroll": 225.0,
    "args": {
      "amount": 25
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 25.0,
        "number": null,
        "type": "DontCome"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "dont_come_point_on_ok",
    "verb": "dont_come"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 25
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "TABLE_RULE_BLOCK",
    "result": "error",
    "scenario": "dont_come_point_off_error",
    "verb": "dont_come"
  },
  {
    "after_bankroll": 240.0,
    "args": {
      "amount": 10
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 10.0,
        "number": null,
        "type": "Field"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "field_basic_ok",
    "verb": "field"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": -5
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "field_negative_amount_error",
    "verb": "field"
  },
  {
    "after_bankroll": 245.0,
    "args": {
      "amount": 5
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 5.0,
        "number": null,
        "type": "Any7"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "any7_basic_ok",
    "verb": "any7"
  },
  {
    "after_bankroll": 100.0,
    "args": {
      "amount": 500
    },
    "before_bankroll": 100.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "INSUFFICIENT_FUNDS",
    "result": "error",
    "scenario": "any7_insufficient_funds",
    "verb": "any7"
  },
  {
    "after_bankroll": 238.0,
    "args": {
      "amount": 12
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 12.0,
        "number": null,
        "type": "CAndE"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "c_and_e_basic_ok",
    "verb": "c&e"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": "ten"
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "c_and_e_non_numeric_amount_error",
    "verb": "c&e"
  },
  {
    "after_bankroll": 234.0,
    "args": {
      "amount": 16
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 16.0,
        "number": null,
        "type": "Horn"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "horn_basic_ok",
    "verb": "horn"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 0
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "horn_zero_amount_error",
    "verb": "horn"
  },
  {
    "after_bankroll": 230.0,
    "args": {
      "amount": 20
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 20.0,
        "number": null,
        "type": "World"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "world_basic_ok",
    "verb": "world"
  },
  {
    "after_bankroll": 150.0,
    "args": {
      "amount": 600
    },
    "before_bankroll": 150.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "INSUFFICIENT_FUNDS",
    "result": "error",
    "scenario": "world_insufficient_funds",
    "verb": "world"
  },
  {
    "after_bankroll": 232.0,
    "args": {
      "amount": 18
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 18.0,
        "number": 6,
        "type": "Big6"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "big6_basic_ok",
    "verb": "big6"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 0
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "big6_zero_amount_error",
    "verb": "big6"
  },
  {
    "after_bankroll": 232.0,
    "args": {
      "amount": 18
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 18.0,
        "number": 8,
        "type": "Big8"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "big8_basic_ok",
    "verb": "big8"
  },
  {
    "after_bankroll": 120.0,
    "args": {
      "amount": 500
    },
    "before_bankroll": 120.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "INSUFFICIENT_FUNDS",
    "result": "error",
    "scenario": "big8_insufficient_funds",
    "verb": "big8"
  },
  {
    "after_bankroll": 220.0,
    "args": {
      "amount": 30,
      "number": 6
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "place_six_ok",
    "verb": "place"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 30,
      "number": 2
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "place_invalid_number_error",
    "verb": "place"
  },
  {
    "after_bankroll": 224.0,
    "args": {
      "amount": 25,
      "number": 4
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 25.0,
        "number": 4,
        "type": "Buy"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "buy_four_ok",
    "verb": "buy"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 25,
      "number": 3
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "buy_invalid_number_error",
    "verb": "buy"
  },
  {
    "after_bankroll": 187.0,
    "args": {
      "amount": 60,
      "number": 8
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 60.0,
        "number": 8,
        "type": "Lay"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "lay_eight_ok",
    "verb": "lay"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 40,
      "number": 11
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "lay_invalid_number_error",
    "verb": "lay"
  },
  {
    "after_bankroll": 215.0,
    "args": {
      "amount": 35,
      "number": 8
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 35.0,
        "number": 8,
        "type": "Put"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "put_eight_with_point_ok",
    "verb": "put"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 35,
      "number": 8
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "TABLE_RULE_BLOCK",
    "result": "error",
    "scenario": "put_point_off_error",
    "verb": "put"
  },
  {
    "after_bankroll": 230.0,
    "args": {
      "amount": 20,
      "number": 6
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 20.0,
        "number": 6,
        "type": "HardWay"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "hardway_six_ok",
    "verb": "hardway"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 20,
      "number": 5
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "hardway_invalid_number_error",
    "verb": "hardway"
  },
  {
    "after_bankroll": 205.0,
    "args": {
      "amount": 30,
      "base": "pass_line"
    },
    "before_bankroll": 235.0,
    "bets_after": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Odds"
      },
      {
        "amount": 15.0,
        "number": null,
        "type": "PassLine"
      }
    ],
    "bets_before": [
      {
        "amount": 15.0,
        "number": null,
        "type": "PassLine"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "odds_pass_line_ok",
    "verb": "odds"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 30,
      "base": "pass_line"
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "TABLE_RULE_BLOCK",
    "result": "error",
    "scenario": "odds_missing_base_error",
    "verb": "odds"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 30,
      "base": "foo"
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "odds_invalid_base_error",
    "verb": "odds"
  },
  {
    "after_bankroll": 245.0,
    "args": {
      "amount": 5
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 5.0,
        "number": null,
        "type": "Two"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "two_basic_ok",
    "verb": "two"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": -5
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "two_negative_amount_error",
    "verb": "two"
  },
  {
    "after_bankroll": 245.0,
    "args": {
      "amount": 5
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 5.0,
        "number": null,
        "type": "Three"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "three_basic_ok",
    "verb": "three"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 0
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "three_zero_amount_error",
    "verb": "three"
  },
  {
    "after_bankroll": 243.0,
    "args": {
      "amount": 7
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 7.0,
        "number": null,
        "type": "Yo"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "yo_basic_ok",
    "verb": "yo"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": -7
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "yo_negative_amount_error",
    "verb": "yo"
  },
  {
    "after_bankroll": 244.0,
    "args": {
      "amount": 6
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 6.0,
        "number": null,
        "type": "Boxcars"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "boxcars_basic_ok",
    "verb": "boxcars"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 0
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "boxcars_zero_amount_error",
    "verb": "boxcars"
  },
  {
    "after_bankroll": 242.0,
    "args": {
      "amount": 8
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 8.0,
        "number": null,
        "type": "AnyCraps"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "any_craps_basic_ok",
    "verb": "any_craps"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": -8
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "any_craps_negative_amount_error",
    "verb": "any_craps"
  },
  {
    "after_bankroll": 240.0,
    "args": {
      "amount": 10,
      "result": [
        2,
        3
      ]
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 10.0,
        "number": null,
        "type": "Hop"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "hop_basic_ok",
    "verb": "hop"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 10,
      "result": [
        2,
        7
      ]
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "hop_bad_args_error",
    "verb": "hop"
  },
  {
    "after_bankroll": 245.0,
    "args": {
      "amount": 5
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 5.0,
        "number": null,
        "type": "Fire"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "fire_basic_ok",
    "verb": "fire"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 0
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "fire_zero_amount_error",
    "verb": "fire"
  },
  {
    "after_bankroll": 245.0,
    "args": {
      "amount": 5
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 5.0,
        "number": null,
        "type": "All"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "all_basic_ok",
    "verb": "all"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": -5
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "all_negative_amount_error",
    "verb": "all"
  },
  {
    "after_bankroll": 245.0,
    "args": {
      "amount": 5
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 5.0,
        "number": null,
        "type": "Tall"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "tall_basic_ok",
    "verb": "tall"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": 0
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "tall_zero_amount_error",
    "verb": "tall"
  },
  {
    "after_bankroll": 245.0,
    "args": {
      "amount": 5
    },
    "before_bankroll": 250.0,
    "bets_after": [
      {
        "amount": 5.0,
        "number": null,
        "type": "Small"
      }
    ],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "small_basic_ok",
    "verb": "small"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "amount": -5
    },
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "small_negative_amount_error",
    "verb": "small"
  },
  {
    "after_bankroll": 250.0,
    "args": {
      "number": 6,
      "type": "place"
    },
    "before_bankroll": 220.0,
    "bets_after": [],
    "bets_before": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "remove_bet_basic_ok",
    "verb": "remove_bet"
  },
  {
    "after_bankroll": 220.0,
    "args": {
      "number": 8,
      "type": "place"
    },
    "before_bankroll": 220.0,
    "bets_after": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "bets_before": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "remove_bet_no_match_error",
    "verb": "remove_bet"
  },
  {
    "after_bankroll": 232.0,
    "args": {
      "new_amount": 18,
      "number": 6,
      "type": "place"
    },
    "before_bankroll": 220.0,
    "bets_after": [
      {
        "amount": 18.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "bets_before": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "reduce_bet_basic_ok",
    "verb": "reduce_bet"
  },
  {
    "after_bankroll": 220.0,
    "args": {
      "new_amount": 60,
      "number": 6,
      "type": "place"
    },
    "before_bankroll": 220.0,
    "bets_after": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "bets_before": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "reduce_bet_increase_error",
    "verb": "reduce_bet"
  },
  {
    "after_bankroll": 250.0,
    "args": {},
    "before_bankroll": 195.0,
    "bets_after": [],
    "bets_before": [
      {
        "amount": 10.0,
        "number": 6,
        "type": "HardWay"
      },
      {
        "amount": 15.0,
        "number": null,
        "type": "PassLine"
      },
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "clear_all_bets_basic_ok",
    "verb": "clear_all_bets"
  },
  {
    "after_bankroll": 250.0,
    "args": {},
    "before_bankroll": 250.0,
    "bets_after": [],
    "bets_before": [],
    "error_code": null,
    "result": "ok",
    "scenario": "clear_all_bets_noop_ok",
    "verb": "clear_all_bets"
  },
  {
    "after_bankroll": 250.0,
    "args": {},
    "before_bankroll": 204.0,
    "bets_after": [],
    "bets_before": [
      {
        "amount": 10.0,
        "number": null,
        "type": "Any7"
      },
      {
        "amount": 16.0,
        "number": null,
        "type": "Horn"
      },
      {
        "amount": 20.0,
        "number": null,
        "type": "World"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "clear_center_bets_basic_ok",
    "verb": "clear_center_bets"
  },
  {
    "after_bankroll": 220.0,
    "args": {},
    "before_bankroll": 220.0,
    "bets_after": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "bets_before": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "clear_center_bets_noop_ok",
    "verb": "clear_center_bets"
  },
  {
    "after_bankroll": 250.0,
    "args": {},
    "before_bankroll": 131.0,
    "bets_after": [],
    "bets_before": [
      {
        "amount": 25.0,
        "number": 4,
        "type": "Buy"
      },
      {
        "amount": 60.0,
        "number": 10,
        "type": "Lay"
      },
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "clear_place_buy_lay_basic_ok",
    "verb": "clear_place_buy_lay"
  },
  {
    "after_bankroll": 240.0,
    "args": {},
    "before_bankroll": 240.0,
    "bets_after": [
      {
        "amount": 10.0,
        "number": null,
        "type": "Field"
      }
    ],
    "bets_before": [
      {
        "amount": 10.0,
        "number": null,
        "type": "Field"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "clear_place_buy_lay_noop_ok",
    "verb": "clear_place_buy_lay"
  },
  {
    "after_bankroll": 250.0,
    "args": {},
    "before_bankroll": 235.0,
    "bets_after": [],
    "bets_before": [
      {
        "amount": 5.0,
        "number": null,
        "type": "All"
      },
      {
        "amount": 5.0,
        "number": null,
        "type": "Small"
      },
      {
        "amount": 5.0,
        "number": null,
        "type": "Tall"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "clear_ats_bets_basic_ok",
    "verb": "clear_ats_bets"
  },
  {
    "after_bankroll": 235.0,
    "args": {},
    "before_bankroll": 235.0,
    "bets_after": [
      {
        "amount": 15.0,
        "number": null,
        "type": "PassLine"
      }
    ],
    "bets_before": [
      {
        "amount": 15.0,
        "number": null,
        "type": "PassLine"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "clear_ats_bets_noop_ok",
    "verb": "clear_ats_bets"
  },
  {
    "after_bankroll": 250.0,
    "args": {},
    "before_bankroll": 245.0,
    "bets_after": [],
    "bets_before": [
      {
        "amount": 5.0,
        "number": null,
        "type": "Fire"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "clear_fire_bets_basic_ok",
    "verb": "clear_fire_bets"
  },
  {
    "after_bankroll": 220.0,
    "args": {},
    "before_bankroll": 220.0,
    "bets_after": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "bets_before": [
      {
        "amount": 30.0,
        "number": 6,
        "type": "Place"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "clear_fire_bets_noop_ok",
    "verb": "clear_fire_bets"
  },
  {
    "after_bankroll": 190.0,
    "args": {
      "base": "come",
      "number": 5,
      "working": true
    },
    "before_bankroll": 190.0,
    "bets_after": [
      {
        "amount": 15.0,
        "number": 5,
        "type": "Come"
      },
      {
        "amount": 30.0,
        "number": 5,
        "type": "Odds"
      },
      {
        "amount": 15.0,
        "number": null,
        "type": "PassLine"
      }
    ],
    "bets_before": [
      {
        "amount": 15.0,
        "number": 5,
        "type": "Come"
      },
      {
        "amount": 30.0,
        "number": 5,
        "type": "Odds"
      },
      {
        "amount": 15.0,
        "number": null,
        "type": "PassLine"
      }
    ],
    "error_code": null,
    "result": "ok",
    "scenario": "set_odds_working_basic_ok",
    "verb": "set_odds_working"
  },
  {
    "after_bankroll": 220.0,
    "args": {
      "base": "come",
      "number": 6,
      "working": false
    },
    "before_bankroll": 220.0,
    "bets_after": [
      {
        "amount": 15.0,
        "number": 4,
        "type": "Come"
      },
      {
        "amount": 15.0,
        "number": null,
        "type": "PassLine"
      }
    ],
    "bets_before": [
      {
        "amount": 15.0,
        "number": 4,
        "type": "Come"
      },
      {
        "amount": 15.0,
        "number": null,
        "type": "PassLine"
      }
    ],
    "error_code": "BAD_ARGS",
    "result": "error",
    "scenario": "set_odds_working_no_match_error",
    "verb": "set_odds_working"
  }
]
```
