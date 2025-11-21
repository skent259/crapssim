# Engine API CI Notes

## Workflow

The Engine API uses a dedicated workflow:

- File: `.github/workflows/api-engine-ci.yml`
- Triggers:
  - `push` to `crapssim_api/**`
  - `pull_request` that touches the API folder or this workflow
  - `workflow_dispatch` (manual run)

For longer parity and trace coverage, a manual gauntlet workflow remains available:

- File: `.github/workflows/crapsim_api_gauntlet.yml`
- Trigger: `workflow_dispatch` (manual run)

## Python Versions

The workflow runs the Engine API tests against:

- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13

Core CrapsSim users are not affected; the workflow only exercises the API and its tests.

## Installation in CI

CI installs:

```bash
pip install -e .
pip install -e ./crapssim_api[api,dev,gauntlet]
```

This matches the packaging metadata declared under `crapssim_api/` and ensures the Engine API is fully optional but well-tested.

## Test Suites

CI runs:
- `crapssim_api/tests/` — fast unit tests for verbs, routing, and error handling.
- `crapssim_api/tests/stress/test_api_sequences.py` — sequence/gauntlet tests that compare API behavior against the vanilla engine harness.

The stress suite is designed to validate parity and safety, not to change any core engine logic.
