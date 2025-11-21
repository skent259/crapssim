# HTTP Verb Reference

All wagering and management actions flow through `POST /apply_action` with a payload such as:

```json
{
  "session_id": "<8-char id returned from /session/start>",
  "verb": "pass_line",
  "args": {"amount": 10}
}
```

Responses include an `effect_summary` and an updated session snapshot. Unless noted, `amount` values are positive dollars enforced by the engine’s table rules. Management verbs only accept the arguments listed for each entry.

## Line and odds verbs

| Verb | Args | Engine mapping | Error codes |
| --- | --- | --- | --- |
| `pass_line` | `{amount}` | `PassLine(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `dont_pass` | `{amount}` | `DontPass(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `come` | `{amount}` | `Come(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `dont_come` | `{amount}` | `DontCome(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `put` | `{amount, number}` | `Put(number, amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `odds` | `{amount, base, number?, working?}` | `Odds(base_type, point, amount, always_working=working)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS`, `TABLE_RULE_BLOCK` |

### Example
```json
{"verb": "odds", "args": {"base": "pass_line", "amount": 20}}
```

## Place / buy / lay / big

| Verb | Args | Engine mapping | Error codes |
| --- | --- | --- | --- |
| `place` | `{amount, number}` | `Place(number, amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `buy` | `{amount, number}` | `Buy(number, amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `lay` | `{amount, number}` | `Lay(number, amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `big6` | `{amount}` | `Big6(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `big8` | `{amount}` | `Big8(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |

### Example
```json
{"verb": "place", "args": {"number": 6, "amount": 30}}
```

## Field and props

| Verb | Args | Engine mapping | Error codes |
| --- | --- | --- | --- |
| `field` | `{amount}` | `Field(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `any7` | `{amount}` | `Any7(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `c&e` | `{amount}` | `CAndE(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `horn` | `{amount}` | `Horn(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `world` | `{amount}` | `World(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `any_craps` | `{amount}` | `AnyCraps(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `two` | `{amount}` | `Two(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `three` | `{amount}` | `Three(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `yo` | `{amount}` | `Yo(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `boxcars` | `{amount}` | `Boxcars(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |

### Example
```json
{"verb": "horn", "args": {"amount": 5}}
```

## Hardways, hops, and specialty sidebets

| Verb | Args | Engine mapping | Error codes |
| --- | --- | --- | --- |
| `hardway` | `{amount, number}` | `HardWay(number, amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `hop` | `{amount, result:[d1,d2]}` | `Hop((d1, d2), amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `fire` | `{amount}` | `Fire(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `all` | `{amount}` | `All(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `tall` | `{amount}` | `Tall(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `small` | `{amount}` | `Small(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |

### Example
```json
{"verb": "hop", "args": {"result": [2, 2], "amount": 2}}
```

## Bet management verbs

| Verb | Args | Engine mapping | Error codes |
| --- | --- | --- | --- |
| `remove_bet` | `{type, number?}` | Remove matching bets if `is_removable` | `BAD_ARGS`, `TABLE_RULE_BLOCK` |
| `reduce_bet` | `{type, number?, new_amount}` | Replace existing amount with `new_amount` | `BAD_ARGS`, `TABLE_RULE_BLOCK` |
| `clear_all_bets` | `{}` | Remove every removable bet | `BAD_ARGS` |
| `clear_center_bets` | `{}` | Remove center action (`Field`, props, hops, ATS/Fire) | `BAD_ARGS` |
| `clear_place_buy_lay` | `{}` | Remove `Place`, `Buy`, `Lay` | `BAD_ARGS` |
| `clear_ats_bets` | `{}` | Remove `All`/`Tall`/`Small` | `BAD_ARGS` |
| `clear_fire_bets` | `{}` | Remove `Fire` | `BAD_ARGS` |
| `set_odds_working` | `{base, number, working}` | Toggle `Odds.always_working` for a base/number | `BAD_ARGS`, `TABLE_RULE_BLOCK` |

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

Refer to [`examples/api_client_min.py`](../examples/api_client_min.py) for a scripted walkthrough that chains these calls together.
