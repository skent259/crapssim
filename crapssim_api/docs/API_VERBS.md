# CrapsSim API Betting Verbs

The `/apply_action` endpoint exposes a set of verbs that map directly to bet classes
provided by the underlying CrapsSim engine. Legality (timing, bankroll availability,
base-bet requirements, etc.) is enforced by the engine itself; the API validates only
request shape and surfaces the engine's decision.

| Verb | Required fields | Notes |
| ---- | --------------- | ----- |
| `pass_line` | `amount` | Come-out only. Places a `PassLine` bet. |
| `dont_pass` | `amount` | Come-out only. Places a `DontPass` bet. |
| `come` | `amount` | Requires point on. Places a `Come` bet. |
| `dont_come` | `amount` | Requires point on. Places a `DontCome` bet. |
| `place` | `amount`, `box`/`number` | Places a `Place` bet on 4/5/6/8/9/10. |
| `buy` | `amount`, `box`/`number` | Places a `Buy` bet with table vig policy. |
| `lay` | `amount`, `box`/`number` | Places a `Lay` bet with table vig policy. |
| `put` | `amount`, `box`/`number` | Places a flat `Put` bet while the point is on. |
| `hardway` | `amount`, `number` | Places a `HardWay` bet on 4/6/8/10. |
| `field` | `amount` | Places a one-roll `Field` bet. |
| `any7` | `amount` | Places an `Any7` one-roll proposition. |
| `c&e` | `amount` | Places a `CAndE` one-roll proposition. |
| `horn` | `amount` | Places a `Horn` one-roll proposition. |
| `world` | `amount` | Places a `World` one-roll proposition. |
| `big6` | `amount` | Places a `Big6` bet. |
| `big8` | `amount` | Places a `Big8` bet. |
| `odds` | `amount`, `base`, optional `number`, optional `working` | Adds an `Odds` bet behind `pass_line`, `dont_pass`, `come`, `dont_come`, or `put`. The engine requires the matching base bet to be present. |

Unsupported verbs produce an `UNSUPPORTED_BET` error with no side effects. Bets that the
engine rejects (for example, attempting odds without an established base bet) raise a
`TABLE_RULE_BLOCK` error and leave bankroll/bets unchanged.

The bankroll reported in `/apply_action` responses is taken directly from
`Session.player().bankroll`, making the engine the sole source of truth.
