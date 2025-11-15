# HTTP Verb Reference

All wagering and management actions flow through the `POST /apply_action` endpoint. Each request uses the same envelope:

```json
{
  "session_id": "<8-char id returned from /session/start>",
  "verb": "pass_line",
  "args": {"amount": 10}
}
```

Responses include the effect summary and an updated snapshot:

```json
{
  "effect_summary": {
    "verb": "pass_line",
    "applied": true,
    "bankroll_delta": -10.0,
    "note": "applied via engine"
  },
  "snapshot": {
    "bankroll_after": "990.00",
    "bets": [...]
  }
}
```

Unless otherwise stated, `amount` values are in dollars and must respect the table limits enforced by the vanilla engine. Bets that require a `number` expect standard box numbers (4,5,6,8,9,10). Management verbs never accept `amount` and only take the arguments listed below.

## Core line bets

| Verb | Required args | Notes |
| --- | --- | --- |
| `pass_line` | `{"amount": int}` | Come-out bet that wins on 7/11, loses on 2/3/12. |
| `dont_pass` | `{"amount": int}` | Come-out bet that wins on 2/3, pushes on 12. |
| `come` | `{"amount": int}` | Moves to the rolled number as a point. |
| `dont_come` | `{"amount": int}` | Travels to the rolled number as a lay. |
| `put` | `{"amount": int, "number": int}` | Places a direct line bet on the specified box number. |
| `odds` | `{"base": "pass_line"/"dont_pass"/"come"/"dont_come", "amount": int}` | Adds odds behind an existing base bet. |

### Example

```json
{"verb": "odds", "args": {"base": "pass_line", "amount": 20}}
```

## Place / Buy / Lay / Big bets

| Verb | Required args | Notes |
| --- | --- | --- |
| `place` | `{"number": int, "amount": int}` | Standard place bet on 4,5,6,8,9,10. |
| `buy` | `{"number": int, "amount": int}` | Pay vig on win; vig rounded per table settings. |
| `lay` | `{"number": int, "amount": int}` | Lay against a number; vig paid up front. |
| `big6` | `{"amount": int}` | Even-money bet on 6. |
| `big8` | `{"amount": int}` | Even-money bet on 8. |

### Example

```json
{"verb": "place", "args": {"number": 6, "amount": 30}}
```

## Field, prop, and center bets

| Verb | Required args | Notes |
| --- | --- | --- |
| `field` | `{"amount": int}` | Wins on 2,3,4,9,10,11,12 (2/12 pay double). |
| `any7` | `{"amount": int}` | One-roll bet on any seven. |
| `any_craps` | `{"amount": int}` | One-roll bet on 2,3,12. |
| `two` | `{"amount": int}` | Yo-leven style single-number prop (also see `three`, `yo`, `boxcars`). |
| `three` | `{"amount": int}` | One-roll bet on 3. |
| `yo` | `{"amount": int}` | One-roll bet on 11. |
| `boxcars` | `{"amount": int}` | One-roll bet on 12. |
| `c&e` | `{"amount": int}` | Split prop covering craps + yo. |
| `horn` | `{"amount": int}` | Splits action on 2/3/11/12. |
| `world` | `{"amount": int}` | Horn plus any-seven protection. |

### Example

```json
{"verb": "horn", "args": {"amount": 5}}
```

## Hardways and hops

| Verb | Required args | Notes |
| --- | --- | --- |
| `hardway` | `{"number": 4/6/8/10, "amount": int}` | Wins on the hard combination, loses on easy or seven. |
| `hop` | `{"dice": [int, int], "amount": int}` | One-roll hop bet on exact dice. |

### Example

```json
{"verb": "hop", "args": {"dice": [2, 2], "amount": 2}}
```

## Fire & All/Tall/Small

| Verb | Required args | Notes |
| --- | --- | --- |
| `fire` | `{"amount": int}` | Tracks unique points made for the shooter. |
| `all` | `{"amount": int}` | Part of the All/Tall/Small feature. |
| `tall` | `{"amount": int}` | Part of the All/Tall/Small feature. |
| `small` | `{"amount": int}` | Part of the All/Tall/Small feature. |

### Example

```json
{"verb": "fire", "args": {"amount": 5}}
```

## Bet management verbs

| Verb | Required args | Notes |
| --- | --- | --- |
| `remove_bet` | `{"bet_id": str}` | Removes a single bet by identifier returned in snapshots. |
| `reduce_bet` | `{"bet_id": str, "amount": int}` | Reduce an existing bet while keeping it active. |
| `clear_all_bets` | `{}` | Removes every removable bet from the layout. |
| `clear_center_bets` | `{}` | Clears horn/prop/field wagers. |
| `clear_place_buy_lay` | `{}` | Clears place/buy/lay bets. |
| `clear_ats_bets` | `{}` | Clears All/Tall/Small wagers. |
| `clear_fire_bets` | `{}` | Clears Fire bets. |
| `set_odds_working` | `{"working": bool}` | Toggles whether odds work on the come-out. |

### Example

```json
{"verb": "clear_all_bets", "args": {}}
```

Management verbs report `bets_before` and `bets_after` arrays so clients can confirm the layout change.

## Session endpoints

- `POST /session/start` — returns a new session identifier and initial snapshot. Accepts optional `seed` and table configuration.
- `POST /session/roll` — advance the session with automatic dice or a supplied pair via the `dice` array.
- `POST /step_roll` — convenience endpoint used by parity tests for deterministic roll scripts.
- `POST /end_session` — currently returns a minimal report placeholder.

Refer to the [example client](../examples/api_client_min.py) for a scripted walkthrough that chains these calls together.
