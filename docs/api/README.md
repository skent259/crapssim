# CrapsSim-API Overview (Phases 1–4)

_Phase Tag: `v0.4.0-api-p4`_

This document summarizes the CrapsSim-API up through Phase 4.

## Capabilities Summary

**Session & Lifecycle**
- Deterministic `/start_session` and `/end_session`
- Repeatable seeds and replay-accurate rolls

**Roll Stepping**
- `/step_roll` supports both "auto" and "inject" modes
- Returns ordered `events[]` with deterministic `id`, `ts`, and `data`

**Action Handling**
- `/apply_action` enforces legal timing and limits
- Returns structured `effect_summary` and post-action snapshot

**Snapshot Schema**
- Single source of truth for each state transition
- Includes bankroll, hand_id, roll_seq, puck state, and identity block

**Event Envelope**
- Emits: `hand_started`, `roll_started`, `roll_completed`
- Deterministic event IDs: `sha1("{session_id}/{hand_id}/{roll_seq}/{type}")[:12]`
- Full schema documented in `docs/api/events.md`

---

## Determinism Verification

Identical inputs yield identical outputs across repeated runs.  
See `baselines/phase4/manifest.json` for proof of determinism:

```json
"determinism": {
  "identical_runs": true,
  "identical_text_hashes": true
}
```

---

Next Phase

Phase 5 introduces hand logic and controlled point-cycle resolution (on/off puck, point setting, resolution sequencing).
