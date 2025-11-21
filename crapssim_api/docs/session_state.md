# Session State Snapshot (Design + Phase 5·B implementation)

Phase 5 introduces a read-only surface for capturing the authoritative state of a running CrapsSim session. The API only serializes what the engine already tracks; it does not derive, reconcile, or reinterpret anything. Phase 5·B wires up the first live implementation based on the fields the engine currently exposes.

## Endpoint Concept

- Exposes a snapshot of a single session (e.g., `GET /session/<id>/state`).
- Read-only: no mutations, decisions, or reconciliation logic.
- All values are lifted directly from the core engine structures that already own the truth.
- Intended for CSC/Evo monitoring, research notebooks, and debugging tooling to observe in-flight sessions.

## Target Schema

This schema is a design target for the first public version. Fields that require additional engine access are marked as **future/optional** and remain `null`/absent until the engine exposes them.

```yaml
state_schema: "1.0"
session_id: str
seed: int | null

determinism_contract: "v1.0"
tape_loaded: bool

bankroll: float
point: int | null
roll_index: int        # rolls in this session
hand_index: int        # hands/shooters in this session

last_roll:
  total: int | null
  dice: [int, int] | null
  resolved: bool

bets:                   # unresolved active bets only
  - type: str           # engine bet type key ("PassLine", "Place", etc.)
    number: int | null  # box number if applicable
    amount: float
    working: bool | null
    odds_amount: float | null

ats:
  small_hits: int
  tall_hits: int
  all_complete: bool
  small_complete: bool
  tall_complete: bool

fire:
  points_made: [int]    # ordered list of distinct points made, if tracked

table:
  max_odds: str | null  # optional, if we can read table config
```

## Source of Truth per Field Group

- **Session identity and determinism metadata** (`session_id`, `seed`, `determinism_contract`, `tape_loaded`): pulled directly from the session store and determinism contract wiring. Phase 5·B hard-codes the determinism contract to `"v1.0"` alongside the stored seed and tape status.
- **Bankroll and progression counters** (`bankroll`, `roll_index`, `hand_index`): read directly from the engine session/hand state objects that already track bankroll and roll/hand progression.
- **Point** (`point`): surfaced exactly as the engine tracks the current point (or `null` if off). The API does not deduce point state from bets or history.
- **Last roll** (`last_roll.total`, `last_roll.dice`, `last_roll.resolved`): serialized from the latest roll record the engine already stores. Dice pairs are present when a roll has occurred in this session; otherwise the field remains `null`.
- **Bets** (`bets` array, with `type`, `number`, `amount`, `working`, `odds_amount`): enumerated from the engine’s active layout. No reclassification or normalization; the API forwards the engine’s identifiers and amounts as-is.
- **ATS/FIRE progress** (`ats`, `fire`): currently `null` placeholders; the engine does not track these yet.
- **Table configuration** (`table.max_odds`): populated from the engine table settings when available. Additional table config remains future/optional.

## Versioning & Compatibility

- **`state_schema` starts at "1.0".** Consumers must read this version and treat unknown/additional fields as optional.
- **Additive evolution only.** New fields can be appended; existing names and meanings must remain stable. Renames require a schema version bump and compatibility note.
- **Determinism alignment.** When a replay tape is loaded, the snapshot must reflect the exact tape-driven state; when running from a seed, snapshots are deterministic within an engine version but may change if the underlying engine behavior evolves.
- **Consumer guidance.** CSC/Evo clients should gate their parsers on `state_schema` and prefer feature detection for optional fields rather than strict field lists.

## Example (Phase 5·B)

```json
{
  "state_schema": "1.0",
  "session_id": "abc12345",
  "seed": 42,
  "determinism_contract": "v1.0",
  "tape_loaded": false,
  "bankroll": 985.0,
  "point": null,
  "roll_index": 0,
  "hand_index": 1,
  "last_roll": null,
  "bets": [
    {"type": "PassLine", "number": null, "amount": 15.0}
  ],
  "ats": null,
  "fire": null,
  "table": {"max_odds": {"4": 3, "5": 4, "6": 5, "8": 5, "9": 4, "10": 3}}
}
```
