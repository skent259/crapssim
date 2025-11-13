# API Polish — Docs & Dormant Modules

## Checklist

- [x] API_OVERVIEW.md added under `crapssim_api/docs/`
- [x] API_DESIGN_PHILOSOPHY.md added under `crapssim_api/docs/`
- [x] Dormant determinism modules annotated with NOTE block
- [x] API-specific REPORT_*.md and roadmap docs moved under `crapssim_api/docs/`
- [x] References (if any) updated to the new doc paths
- [x] `pip install -e ".[api]"` succeeded locally
- [x] `pytest -q` run from repo root

## Validation Notes

- `pip install -e ".[api]"`: ⚠️
  - pip emitted "does not provide the extra 'api'" warning, but the install still completed successfully.
- `pytest -q`: ✅
