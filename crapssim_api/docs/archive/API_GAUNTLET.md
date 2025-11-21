# CrapsSim Engine API Gauntlet

This document describes the "API Gauntlet" — a manual CI workflow that runs the
CrapsSim Engine API stress and sequence parity tests and publishes their logs
as downloadable artifacts.

## What it does

The gauntlet workflow:

1. Checks out the repo and sets up the same Python environment as the main test CI.
2. Installs the engine and API test dependencies.
3. Runs:
   - `crapssim_api/tests/test_api_surface_stress.py`
   - `crapssim_api/tests/test_api_sequence_parity.py`
4. Collects the Markdown / JSON / CSV outputs written under:
   - `crapssim_api/tests/results/`
5. Uploads those files as a GitHub Actions artifact.

No result files are committed to the repo; they are treated as build artifacts only.

## When to run it

Use the gauntlet when:

- Rebasing the CrapsSim Engine API branch onto a new CrapsSim release.
- Verifying that upstream engine changes did not break the API verb behavior.
- Performing a deep sanity check before tagging a new API version.

It is not intended to run on every push; it is a manual, on-demand check.

## How to run it

1. Push your branch with any API-related changes.
2. In GitHub, go to **Actions** → **CrapsSim Engine API Gauntlet**.
3. Click **Run workflow**, select the desired branch, and confirm.

Once the workflow finishes:

1. Open the workflow run.
2. Scroll to the **Artifacts** section.
3. Download the artifact named `crapsim-api-gauntlet-<SHA>`.

Inside the artifact you should see files like:

- `API_SURFACE_STRESS.md`
- `API_SEQUENCE_TRACE_API.md`
- `API_SEQUENCE_TRACE_VANILLA.md`
- `API_SEQUENCE_TRACE_PARITY.md`
- Any supporting JSON/CSV journals the tests emit.

These files contain the roll-by-roll traces and parity reports comparing the API
behavior against the vanilla engine harness.

## Notes

- The gauntlet is read-only with respect to source; it only writes into
  `crapssim_api/tests/results/`.
- If new API tests are added later (e.g., additional stress suites), they can
  also emit into `crapssim_api/tests/results/` and will be picked up by the
  artifact upload step.
