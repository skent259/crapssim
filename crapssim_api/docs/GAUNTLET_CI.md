# API Gauntlet CI Job

The CrapsSim Engine API includes a stress-test "gauntlet" that can be run as a
manual GitHub Actions workflow. It exercises a suite of roll-by-roll sequences
against both the API and the vanilla CrapsSim engine, and compares final
bankroll and layout state for parity.

## What the job does

- Runs the API sequence stress tests under a chosen Python version.
- Generates artifacts containing:
  - API-side journals (JSON)
  - Vanilla engine journals (JSON)
  - Markdown traces summarizing each scenario
  - A parity report showing which scenarios matched

The gauntlet does **not** run on every push by default. It is intended as a
deeper, on-demand validation tool for engine or API changes.

## When to run it

- Before making breaking changes to the CrapsSim engine that affect bet
  handling, resolution, or error codes.
- After updating the Engine API layer to match new engine behavior.
- When validating that API + engine parity holds across a new release.

## Interpreting results

- A run with all scenarios marked as matching indicates that bankroll and
  final-layout parity is preserved between API and vanilla.
- Any mismatches should be investigated by:
  - Inspecting the JSON journals for API vs vanilla
  - Reviewing the corresponding Markdown traces
  - Adjusting the Engine API wiring, not the core engine logic
