# CrapsSim API Betting Verbs

The `/apply_action` endpoint exposes a set of verbs that map directly to bet classes
provided by the underlying CrapsSim engine. Legality (timing, bankroll availability,
base-bet requirements, etc.) is enforced by the engine itself; the API validates only
request shape and surfaces the engine's decision.

### Added missing API bet verbs for full engine parity

The following bet types now have full API coverage: Two, Three, Yo, Boxcars, AnyCraps,
Hop, Fire, All, Tall, Small. Each verb maps directly to the corresponding CrapsSim
engine bet class.

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
| `two` | `amount` | Places a `Two` (snake eyes) one-roll proposition. |
| `three` | `amount` | Places a `Three` one-roll proposition. |
| `yo` | `amount` | Places a `Yo` (eleven) one-roll proposition. |
| `boxcars` | `amount` | Places a `Boxcars` (midnight) one-roll proposition. |
| `any_craps` | `amount` | Places an `AnyCraps` one-roll proposition. |
| `c&e` | `amount` | Places a `CAndE` one-roll proposition. |
| `horn` | `amount` | Places a `Horn` one-roll proposition. |
| `world` | `amount` | Places a `World` one-roll proposition. |
| `hop` | `amount`, `result=[d1,d2]` | Places a `Hop` bet on a specific dice outcome. |
| `big6` | `amount` | Places a `Big6` bet. |
| `big8` | `amount` | Places a `Big8` bet. |
| `fire` | `amount` | Places a `Fire` bet (requires new shooter per engine rules). |
| `all` | `amount` | Places an `All` ATS bet. |
| `tall` | `amount` | Places a `Tall` ATS bet. |
| `small` | `amount` | Places a `Small` ATS bet. |
| `odds` | `amount`, `base`, optional `number`, optional `working` | Adds an `Odds` bet behind `pass_line`, `dont_pass`, `come`, `dont_come`, or `put`. The engine requires the matching base bet to be present. |

Unsupported verbs produce an `UNSUPPORTED_BET` error with no side effects. Bets that the
engine rejects (for example, attempting odds without an established base bet) raise a
`TABLE_RULE_BLOCK` error and leave bankroll/bets unchanged.

The bankroll reported in `/apply_action` responses is taken directly from
`Session.player().bankroll`, making the engine the sole source of truth.
