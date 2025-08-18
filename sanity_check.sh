#!/usr/bin/env bash
set -e

# Clean up any old run dirs
rm -rf runs_sanity

# Run a quick 2-generation sanity check with small population
. .venv/bin/activate
python examples/run_evolution.py \
    --gens 2 \
    --pop 10 \
    --seed 42 \
    --out runs_sanity \
    --report

echo "✅ Sanity check complete. See runs_sanity/summary.json for results."
