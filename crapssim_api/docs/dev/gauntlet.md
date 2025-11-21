# Engine API Gauntlet (Maintainers)

The gauntlet is a manual GitHub Actions workflow that exercises deep roll-by-roll parity between the Engine API and the vanilla CrapsSim harness.

## Workflow summary
- File: `.github/workflows/crapsim_api_gauntlet.yml`
- Trigger: `workflow_dispatch`
- Python: 3.10–3.13
- Installs: editable engine + `crapssim_api[api,dev,gauntlet]`
- Suites: sequence stress/parity tests that emit journals and Markdown traces

## Artifacts
Each run uploads an artifact containing:
- API-side and vanilla journals (JSON)
- Markdown traces per scenario
- Parity summary indicating mismatches

Artifacts are intentionally not committed—download them from the run page when investigating regressions.

## When to run
- After engine changes that touch bet handling, payouts, or error codes
- Before tagging API releases or merging large routing changes
- When expanding the verb surface to ensure parity holds

## Triage tips
- Start with the parity report to spot failing scenarios.
- Compare API vs. vanilla journals for mismatching cases.
- Adjust API wiring rather than engine rules; the engine remains authoritative.
