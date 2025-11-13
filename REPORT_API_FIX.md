# API Fix Report

## Modified Tests
- `tests/api/test_events_envelope.py`
- `tests/api/test_p5c0_scaffold.py`
- `tests/api/test_p5c1_point_cycle.py`
- `tests/api/test_step_roll_scaffold.py`
- `tests/test_version_identity.py`

All updated tests now skip when `fastapi.testclient` is unavailable (including when FastAPI itself or its HTTP client dependencies are missing).

## Optional FastAPI Handling
- `crapssim_api.http` lazily imports FastAPI objects and provides a minimal ASGI stub whenever FastAPI is absent.
- `crapssim_api.errors` now ships lightweight stubs for `Request` and `JSONResponse` so the package imports cleanly without FastAPI.

## Import Verification Without FastAPI
- Manual import check confirmed `crapssim_api.errors` and `crapssim_api.http` load successfully without FastAPI installed.

## Pytest Results
- `PYTHONPATH=. pytest -q`
  - Status: **fails** because `tests/unit/test_api_router.py::test_bad_increment` currently expects engine-side increment enforcement that the baseline core engine does not provide. All API-related suites either pass or skip when FastAPI tooling is unavailable.
