#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
import random
import json
import time
# Ensure repo root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from evo_engine import (
    DEFAULTS,
    initialize_population,
    evaluate_population,
    select_parents,
    produce_offspring,
    compute_summary,
)

# Repo root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# -----------------------------
# Argparse
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--gens", type=int, default=5, help="Number of generations to run")
parser.add_argument("--pop", type=int, default=40, help="Population size")
parser.add_argument("--seed", type=int, default=123, help="Base random seed")
parser.add_argument("--out", type=str, default="runs", help="Output folder name")
parser.add_argument("--resume", action="store_true", help="Resume from existing folder")
parser.add_argument("--report", action="store_true", help="Print EF table each generation")
parser.add_argument("--xbreed", action="store_true", help="Enable crossbreeding (one-point crossover)")
parser.add_argument("--xbreed-rate", type=float, default=0.15, help="Crossbreed rate (0..1)")
parser.add_argument("--no-anneal", action="store_true", help="Disable mutation annealing")
args = parser.parse_args()

# Safety fallback in case args drift
args.out = getattr(args, "out", "runs")
args.resume = getattr(args, "resume", False)
args.report = getattr(args, "report", False)
args.xbreed = getattr(args, "xbreed", False)
args.xbreed_rate = float(getattr(args, "xbreed_rate", 0.15))
args.no_anneal = getattr(args, "no_anneal", False)

# Per-run config toggles
DEFAULTS["crossbreed"] = {"enable": bool(args.xbreed), "rate": float(args.xbreed_rate)}
DEFAULTS["anneal_enable"] = not bool(args.no_anneal)

# -----------------------------
# Output directory
# -----------------------------
if not args.resume:
    outdir = os.path.join(REPO_ROOT, args.out)
    if os.path.exists(outdir):
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        outdir = f"{outdir}_{ts}"
else:
    outdir = os.path.join(REPO_ROOT, args.out)

os.makedirs(outdir, exist_ok=True)
print(f"[INFO] Results will be written to: {outdir}")

# -----------------------------
# Main Evolution Loop
# -----------------------------
def main():
    random.seed(args.seed)

    # Init population
    if not args.resume:
        genomes = initialize_population(args.pop, DEFAULTS)
        start_gen = 0
    else:
        # resume mode
        with open(os.path.join(outdir, "gen_latest.json")) as f:
            genomes = json.load(f)
        start_gen = int(genomes[0].get("gen", 0)) + 1

    for gen in range(start_gen, start_gen + args.gens):
        # Evaluate
        evaluated = evaluate_population(genomes, DEFAULTS)

        # Report
        if args.report:
            print("EF    Profit   Rolls  Danger  ID/Name")
            for strat in evaluated[:10]:
                ef = strat.get("ef", 0)
                profit = strat.get("profit", 0)
                rolls = strat.get("rolls", 0)
                danger = strat.get("danger", 0)
                name = strat.get("id", "unknown")
                print(f"{ef:.3f}\t{profit:+4}\t{rolls:4}\t{danger}\t{name}")

        # Save generation results
        gen_file = os.path.join(outdir, f"gen_{gen}.json")
        with open(gen_file, "w") as f:
            json.dump(evaluated, f, indent=2)
        print(f"Wrote {gen_file}")

        # Update symlink/latest marker
        latest_file = os.path.join(outdir, "gen_latest.json")
        with open(latest_file, "w") as f:
            json.dump(evaluated, f, indent=2)

        # Parent selection
        parents = select_parents(evaluated, DEFAULTS)

        # Produce offspring
        parent_genomes = [p["genome"] for p in parents]
        genomes = produce_offspring(parent_genomes, DEFAULTS, gen=gen)

    # Final summary
    summary = compute_summary(outdir)
    with open(os.path.join(outdir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[INFO] Summary written to: {os.path.join(outdir, 'summary.json')}")

if __name__ == "__main__":
    sys.exit(main())
