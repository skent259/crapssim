# REPORT_P7 — Optional FastAPI App Wrapper

## Summary

- Added `crapssim_api.fastapi_app` module with a `create_app()` factory and `main()` entrypoint.
- FastAPI and uvicorn are optional and only required when using the app or CLI entrypoint.
- Existing HTTP router from `crapssim_api.http` is reused; no changes to core engine or router logic.

## Compliance Checklist

- [x] FastAPI imports are lazy and guarded behind a clear RuntimeError message.
- [x] Optional `[project.optional-dependencies].api` extra added with `fastapi` and `uvicorn`.
- [x] `create_app()` reuses the existing HTTP router.
- [x] New tests added under `tests/api/test_fastapi_app.py`.
- [x] Tests skip gracefully when FastAPI/uvicorn are not installed.
- [x] Core engine behavior unchanged when API extras are not used.

## Testing

Commands run:

- `PYTHONPATH=. pytest -q`

Results:

- `PYTHONPATH=. pytest -q` — 3921 passed, 17 skipped (FastAPI tests skipped if extras unavailable)

Notes:

- When FastAPI is not installed, `tests/api/test_fastapi_app.py` is skipped via `pytest.importorskip`/`skipif` guards.
- No changes to existing test expectations outside the new file.
