# Session State Snapshot (Design)

Phase 5 introduces a read-only surface for capturing the authoritative state of a running CrapsSim session. The API only serializes what the engine already tracks; it does not derive, reconcile, or reinterpret anything.

## Endpoint Concept

- Exposes a snapshot of a single session (e.g., `GET /session/<id>/state`).
- Read-only: no mutations, decisions, or reconciliation logic.
- All values are lifted directly from the core engine structures that already own the truth.
- Intended for CSC/Evo monitoring, research notebooks, and debugging tooling to observe in-flight sessions.

## Target Schema

This schema is a design target for the first public version. Fields that require additional engine access are marked as **future/optional** and must not be fabricated by the API.

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

- **Session identity and determinism metadata** (`session_id`, `seed`, `determinism_contract`, `tape_loaded`): pulled directly from the session store and determinism contract wiring introduced in Phase 4. No reinterpretation or inferred flags.
- **Bankroll and progression counters** (`bankroll`, `roll_index`, `hand_index`): read directly from the engine session/hand state objects that already track bankroll and roll/hand progression.
- **Point** (`point`): surfaced exactly as the engine tracks the current point (or `null` if off). The API must not deduce point state from bets or history.
- **Last roll** (`last_roll.total`, `last_roll.dice`, `last_roll.resolved`): serialized from the latest roll record the engine already stores. If the engine does not retain dice pairs, this field remains `null` until the engine supplies it in Phase 5·B/5·C.
- **Bets** (`bets` array, with `type`, `number`, `amount`, `working`, `odds_amount`): enumerated from the engine’s active layout. No reclassification or normalization; the API forwards the engine’s identifiers and amounts as-is.
- **ATS/FIRE progress** (`ats`, `fire`): pulled from the engine’s side-bet tracking structures. If a field is not present in the engine state, it must remain omitted or `null` rather than inferred.
- **Table configuration** (`table.max_odds`): only populated if the engine exposes this configuration without computation. Otherwise, it is marked as future/optional.

## Versioning & Compatibility

- **`state_schema` starts at "1.0".** Consumers must read this version and treat unknown/additional fields as optional.
- **Additive evolution only.** New fields can be appended; existing names and meanings must remain stable. Renames require a schema version bump and compatibility note.
- **Determinism alignment.** When a replay tape is loaded, the snapshot must reflect the exact tape-driven state; when running from a seed, snapshots are deterministic within an engine version but may change if the underlying engine behavior evolves.
- **Consumer guidance.** CSC/Evo clients should gate their parsers on `state_schema` and prefer feature detection for optional fields rather than strict field lists.

## Future Implementation Notes (Phase 5·B/5·C)

- Add explicit serializers that walk the engine state and emit this shape without adding business logic.
- Wire CI checks to compare snapshots against direct engine queries to prevent drift between API serialization and engine truth.
- Extend the schema only after the engine exposes the corresponding data; the API must not synthesize placeholders.
