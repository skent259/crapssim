# CrapsSim API Surface Stress Report

## Summary

* Total scenarios: **35**
* Successful actions: **17**
* Errors: **18**

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
  }
]
```
