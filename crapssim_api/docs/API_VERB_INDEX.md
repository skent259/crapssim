# API Verb Index (v0.4.x alignment)

This index mirrors the CrapsSim engine bet classes and management hooks
currently exposed through the HTTP API. Each verb is passed to
`POST /apply_action` with an `args` payload matching the shapes below.
Error codes follow the shared API enums: `BAD_ARGS`,
`INSUFFICIENT_FUNDS`, and `TABLE_RULE_BLOCK`.

## Line and odds verbs

| Verb | Args | Engine mapping | Error codes |
| --- | --- | --- | --- |
| `pass_line` | `{amount}` | `PassLine(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `dont_pass` | `{amount}` | `DontPass(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `come` | `{amount}` | `Come(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `dont_come` | `{amount}` | `DontCome(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `put` | `{amount, number}` | `Put(number, amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `odds` | `{amount, base, number?, working?}` | `Odds(base_type, point, amount, always_working=working)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS`, `TABLE_RULE_BLOCK` |

## Place / buy / lay / big

| Verb | Args | Engine mapping | Error codes |
| --- | --- | --- | --- |
| `place` | `{amount, number}` | `Place(number, amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `buy` | `{amount, number}` | `Buy(number, amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `lay` | `{amount, number}` | `Lay(number, amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `big6` | `{amount}` | `Big6(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `big8` | `{amount}` | `Big8(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |

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

## Hardways, hops, and specialty sidebets

| Verb | Args | Engine mapping | Error codes |
| --- | --- | --- | --- |
| `hardway` | `{amount, number}` | `HardWay(number, amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `hop` | `{amount, result:[d1,d2]}` | `Hop((d1, d2), amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `fire` | `{amount}` | `Fire(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `all` | `{amount}` | `All(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `tall` | `{amount}` | `Tall(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |
| `small` | `{amount}` | `Small(amount)` | `BAD_ARGS`, `INSUFFICIENT_FUNDS` |

## Bet management verbs

| Verb | Args | Operation | Error codes |
| --- | --- | --- | --- |
| `remove_bet` | `{type, number?}` | Remove matching bets if `is_removable` | `BAD_ARGS`, `TABLE_RULE_BLOCK` |
| `reduce_bet` | `{type, number?, new_amount}` | Replace existing amount with `new_amount` | `BAD_ARGS`, `TABLE_RULE_BLOCK` |
| `clear_all_bets` | `{}` | Remove every removable bet | `BAD_ARGS` |
| `clear_center_bets` | `{}` | Remove center action (`Field`, props, hops, ATS/Fire) | `BAD_ARGS` |
| `clear_place_buy_lay` | `{}` | Remove `Place`, `Buy`, `Lay` | `BAD_ARGS` |
| `clear_ats_bets` | `{}` | Remove `All`/`Tall`/`Small` | `BAD_ARGS` |
| `clear_fire_bets` | `{}` | Remove `Fire` | `BAD_ARGS` |
| `set_odds_working` | `{base, number, working}` | Toggle `Odds.always_working` for a base/number | `BAD_ARGS`, `TABLE_RULE_BLOCK` |

### Notes

- `BAD_ARGS` covers malformed payloads (non-numeric amounts, missing
  required fields, invalid numbers), while `INSUFFICIENT_FUNDS` surfaces
  when bankroll is below the combined action cost.
- `TABLE_RULE_BLOCK` is returned when a request violates table state
  (for example, adding odds without a resolved base point or attempting
  to modify a locked bet).
