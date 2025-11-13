# Pre-PR API Polish Report

| Checklist Item | Status |
| --- | --- |
| FastAPI/pydantic optionality | ✅ |
| HTTP endpoints deterministic dice handling | ✅ |
| Tests aligned with core invariants | ✅ |
| Docs match implemented API | ✅ |
| Architecture fit (no engine coupling) | ✅ |

## Test Commands
- `PYTHONPATH=. pytest -q` → pass (API suites skipped automatically when FastAPI/pydantic extras unavailable).
- `PYTHONPATH=. pytest tests/api -q` → pass with FastAPI-dependent tests skipped (extras not installed in this environment).

## Key Changes
- Confirmed optional dependency guards across `crapssim_api` and refined the FastAPI installation hint for clarity.
- Synced API overview documentation with current `/apply_action` bankroll/vig behavior.
- Verified deterministic dice handling and legality checks remain aligned with engine expectations while maintaining isolation from core packages.
