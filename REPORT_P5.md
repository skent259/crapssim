# REPORT_P5

## Deliverables
- Session wrapper: ✅
- TapeWriter / TapeReader: ✅
- Minimal event constructors: ✅
- HTTP session endpoints (optional): ✅
- Tests added under tests/api/: ✅
- Roadmap updated: ✅

## Test Summary
```
PYTHONPATH=. pytest -q
3944 passed, 9 skipped in 5.29s
```
- Fixed `/session/roll` to parse `dice` from JSON body using FastAPI `Body(...)`, so tests posting `{"dice":[4,3]}` now see deterministic dice.

## Samples
```json
{
  "start": {"type": "run_started"},
  "roll": {
    "type": "roll",
    "roll_id": 1,
    "dice": [2, 3],
    "before": {"point": null, "bets": [], "bankroll": 1000.0, "shooter": 1},
    "after": {"point": 5, "bets": [], "bankroll": 1000.0, "shooter": 1}
  }
}
```

## File Summary
- Added `crapssim_api/session.py`
- Added `crapssim_api/tape.py`
- Updated `crapssim_api/events.py`
- Updated `crapssim_api/http.py`
- Added API tests under `tests/api/`
- Updated `ROADMAP_API_V2.md`
- Added `REPORT_P5.md`
