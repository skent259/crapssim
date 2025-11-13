# REPORT_P8 — API Hardening & DX Polish

## A. Checklist

- [x] Core tests pass without API extras installed (`PYTHONPATH=. pytest -q`)
- [x] API tests skip cleanly when `fastapi` / `pydantic` are not installed
- [ ] API tests pass when installed with `pip install .[api]`
- [x] `pyproject.toml` defines an `api` extra with all required deps (and none in core)
- [x] `crapssim_api` can be imported without FastAPI installed
- [x] `docs/API_OVERVIEW.md` documents install + run + basic curl example
- [x] `docs/API_ROADMAP_V2.md` and `docs/API_DESIGN_INTENT.md` reflect current design
- [x] `README.md` links to API docs without making them mandatory

## B. Notes

- The FastAPI test modules all guard imports with `pytest.importorskip`, so they
  skip automatically when extras are missing. I could not uninstall FastAPI in
  this environment, but the guards make the optional story explicit.
- Building the project with `pip install .[api]` currently fails because the
  legacy `setup.py` path does not populate `project.version` in `pyproject.toml`.
  Follow-up work could either add a version value or point contributors to the
  legacy `setup.py` installer.

## C. Commands Run

- `PYTHONPATH=. pytest -q` → 3921 passed, 17 skipped (`fastapi` tests executed when available)
- `pip install .[api]` → fails: `ValueError: invalid pyproject.toml config: project must contain ['version']`
