# Engine API Stress & Gauntlet Tests

These notes describe the parity and stress tooling for the CrapsSim Engine API. The suites drive the HTTP verbs across many scenarios, compare results against the vanilla engine, and validate determinism assumptions.

## What the suites cover

- **API surface stress**: High-volume verb and sequence coverage for error handling and bet management. See [`crapssim_api/tests/stress/test_api_sequences.py`](../../tests/stress/test_api_sequences.py) and [`crapssim_api/tests/stress/test_sequence_parity.py`](../../tests/stress/test_sequence_parity.py).
- **Vanilla vs. API parity**: Paired runs against the HTTP surface and the in-process engine to ensure bankroll and final layout stay aligned. Scenarios and harness helpers live in [`crapssim_api/tests/stress/test_vanilla_sequences.py`](../../tests/stress/test_vanilla_sequences.py) and [`crapssim_api/tests/sequence_harness_api.py`](../../tests/sequence_harness_api.py).
- **Determinism and replay**: Coverage for seeds, injected dice, and tape replay lives alongside the stress modules to confirm reproducible outcomes before and after tape import.

These suites are aimed at maintainers, integrators, and researchers. Ordinary API users do not need to run them to use the package.

## Gauntlet workflow

A manual GitHub Actions workflow (`.github/workflows/crapsim_api_gauntlet.yml`) runs the stress suites across selected Python versions. It produces downloadable artifacts containing:

- API-side and vanilla-engine journals (JSON)
- Markdown traces summarizing each scenario
- A parity report indicating which scenarios matched

Trigger the workflow in GitHub Actions when validating engine parity, investigating determinism regressions, or before publishing changes that affect API wiring. The workflow does not run on every push by default.

## Artifacts and inspection

After a gauntlet run completes, download the artifacts from the workflow summary page. Inspect the JSON journals to compare step-by-step engine decisions, and review the Markdown traces for a human-readable timeline of each scenario.

## Local execution

Developers can run the same suites locally:

```bash
PYTHONPATH=. pytest -q crapssim_api/tests/stress
```

This covers the stress modules only; running `pytest -q crapssim_api/tests` executes the full API suite. Either way, the tests depend on the engine’s truth and do not alter CrapsSim behavior.
