# Engine API CI Notes

## Core workflow
- `.github/workflows/api-engine-ci.yml` triggers on pushes/PRs touching `crapssim_api/**` and on manual dispatch.
- Matrix: Python 3.10–3.13.
- Installs via editable extras: `pip install -e .` then `pip install -e ./crapssim_api[api,dev,gauntlet]`.
- Runs API unit tests and the sequence stress suite.

## Gauntlet workflow
- `.github/workflows/crapsim_api_gauntlet.yml` remains manual (`workflow_dispatch`).
- Executes deep sequence parity checks with the same Python window.
- Uploads artifacts (journals, Markdown traces, parity summaries) for download; no artifacts are committed to the repo.
- Use these outputs to investigate mismatches before changing engine wiring.

## Maintenance tips
- Keep optional dependencies guarded so lint/unit runs succeed even when FastAPI/Pydantic are absent.
- Align docs and examples with the current extras story; CI should mirror the documented install commands.
- Treat gauntlet artifacts as ephemeral; they belong in build outputs, not source control.
