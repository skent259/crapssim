# API Gauntlet (User View)

The Engine API includes an on-demand "gauntlet" GitHub Actions workflow that stress-tests roll sequences against both the API and the vanilla CrapsSim engine.

## What it does
- Runs the API sequence stress tests under a chosen Python version.
- Generates artifacts with journals, Markdown traces, and a parity report comparing API vs. vanilla outcomes.

## When to run
- Before shipping engine changes that affect bet handling or payouts.
- After updating the API layer to match new engine behavior.
- When validating parity for a release candidate.

## Where results appear
Download artifacts from the workflow run page. Investigate mismatches by comparing the JSON journals and Markdown traces for the affected scenarios.
