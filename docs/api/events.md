# Event Envelope — Phase 4 · C2

Defines the structure of `events[]` emitted by `/step_roll`.

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Event category (`hand_started`, `roll_started`, `roll_completed`) |
| `id` | string | Deterministic SHA1 hash (12 chars) |
| `ts` | ISO8601 string | UTC timestamp |
| `hand_id` | int | Current hand number |
| `roll_seq` | int | Current roll sequence |
| `bankroll_before` | string | Bankroll before roll |
| `bankroll_after` | string | Bankroll after roll |
| `data` | object | Event-specific payload |

### Emitted Types (C2)
- **hand_started** – emitted once per session on first roll.  
- **roll_started** – emitted each `/step_roll` call with `{mode}`.  
- **roll_completed** – emitted each call with `{dice}`.

### Determinism
Event IDs are deterministic:  
`sha1("{session_id}/{hand_id}/{roll_seq}/{type}")[:12]`

### Example Response
```json
{
  "events": [
    {"type":"hand_started","id":"4a2e1d9f3c5a","ts":"2025-10-23T15:00:00Z","hand_id":1,"roll_seq":1,"bankroll_before":"1000.00","bankroll_after":"1000.00","data":{}},
    {"type":"roll_started","id":"e3c9bf012b44","ts":"2025-10-23T15:00:00Z","hand_id":1,"roll_seq":1,"bankroll_before":"1000.00","bankroll_after":"1000.00","data":{"mode":"auto"}},
    {"type":"roll_completed","id":"a0c7c54b8c31","ts":"2025-10-23T15:00:00Z","hand_id":1,"roll_seq":1,"bankroll_before":"1000.00","bankroll_after":"1000.00","data":{"dice":[3,4]}}
  ]
}
```
