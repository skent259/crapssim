# API Branch Cleanup & Sync

## Summary

- Updated `main` from `upstream/main`.
- Rebuilt `api` as a clean branch on top of the new `main` by cherry-picking API commits only.
- Ensured only the following areas differ from `main`:
  - `crapssim_api/**`
  - `tests/api/**`
  - `crapssim_api/docs/API_ROADMAP_V2.md`
  - API-related report files.

## Tests

- `PYTHONPATH=. pytest tests/api -q`

Result: all passed (1 test run, 16 skipped).
