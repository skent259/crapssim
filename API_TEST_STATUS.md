## P7 — Contract & Fingerprint Fixes

- Date: 2025-11-14
- Branch: API
- Changes:
  - Aligned `crapssim_api.http.start_session` callable signature and behavior with API tests.
  - Added `tools/api_fingerprint.py` to emit engine/capabilities version JSON.
- Commands:
  - PYTHONPATH=. pytest -q
  - PYTHONPATH=. pytest tests/api -q
  - PYTHONPATH=. pytest tests/integration -q
- Result: ✅ All tests passing.
