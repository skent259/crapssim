#!/usr/bin/env python3
import os, sys, argparse, datetime, json, random

# --- ensure repo root on sys.path ---
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from evo_engine import DEFAULTS
from evo_engine.population import run_one_generation, select_parents, produce_offspring
from evo_engine.io.snapshot import write_snapshot
from evo_engine.io.seeds import load_seed_genomes

# -----------------------------
# CLI
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--gens", type=int, default=5, help="Number of generations")
parser.add_argument("--pop", type=int, default=40, help="Population size")
parser.add_argument("--seed", type=int, default=123, help="Base RNG seed")
parser.add_argument("--out", type=str, default="runs", help="Output folder name (under repo root)")
parser.add_argument("--resume", action="store_true", help="Resume if folder already exists")
parser.add_argument("--report", action="store_true", help="Print EF table each generation")
parser.add_argument("--xbreed", action="store_true", help="Enable crossbreeding (if engine supports it via config)")
parser.add_argument("--xbreed-rate", type=float, default=0.15, help="Crossbreed rate (0..1)")
parser.add_argument("--no-anneal", action="store_true", help="Disable mutation annealing")
args = parser.parse_args()

# safety fallbacks if flags drift
args.out = getattr(args, "out", "runs")
args.report = getattr(args, "report", False)
args.xbreed = getattr(args, "xbreed", False)
args.xbreed_rate = float(getattr(args, "xbreed_rate", 0.15))
args.no_anneal = getattr(args, "no_anneal", False)

# Per-run config toggles (engine will ignore unknowns harmlessly)
DEFAULTS["crossbreed"] = {"enable": bool(args.xbreed), "rate": float(args.xbreed_rate)}
DEFAULTS["anneal_enable"] = not bool(args.no_anneal)

# -----------------------------
# Output directory
# -----------------------------
if args.resume:
    outdir = os.path.join(REPO_ROOT, args.out)
else:
    base = os.path.join(REPO_ROOT, args.out)
    if os.path.exists(base):
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        outdir = f"{base}_{ts}"
    else:
        outdir = base
os.makedirs(outdir, exist_ok=True)
print(f"[INFO] Results will be written to: {outdir}")

# -----------------------------
# Helpers
# -----------------------------
def _pad_to_size(genomes, size):
    """Pad/trim a genome list to the requested size by sampling."""
    if not genomes:
        return genomes
    if len(genomes) >= size:
        return genomes[:size]
    out = list(genomes)
    while len(out) < size:
        out.append(random.choice(genomes))
    return out

def _top_rows_from_snapshot(snapshot, k=10):
    """Extract top rows for reporting from PopulationSnapshot dict."""
    rows = []
    def pull(pool):
        for item in pool:
            g = item.get("genome", {})
            s = item.get("stats", {})
            rows.append({
                "ef": float(s.get("ef", 0.0)),
                "profit": float(s.get("profit", 0.0)),
                "rolls": int(s.get("rolls_survived", s.get("rolls", 0))),
                "danger": 1 if bool(s.get("danger_zone", False)) else 0,
                "name": f"{g.get('id', 'unknown')}/{g.get('name', '')}".strip("/"),
            })
    pull(snapshot.get("main_pool", []))
    pull(snapshot.get("danger_pool", []))
    rows.sort(key=lambda r: (r["ef"], r["profit"]), reverse=True)
    return rows[:k]

# -----------------------------
# Init population (from seeds)
# -----------------------------
seed_genomes = load_seed_genomes(os.path.join(REPO_ROOT, "strategies", "seeds"))
if not seed_genomes:
    raise SystemExit("No seeds found. Add YAMLs under strategies/seeds/ or check seeds loader.")

genomes = _pad_to_size(seed_genomes, int(args.pop))
start_gen = 0

# -----------------------------
# Main loop
# -----------------------------
for gen in range(start_gen, start_gen + int(args.gens)):
    # Lock RNG seed per generation for reproducibility
    random.seed(int(args.seed) + gen)

    # Run generation
    snap = run_one_generation(genomes, DEFAULTS, seed=(int(args.seed) + gen))

    # Report
    if args.report:
        rows = _top_rows_from_snapshot(snap, k=10)
        print("EF    Profit   Rolls  Danger  ID/Name")
        for r in rows:
            print(f"{r['ef']:.3f}\t{int(r['profit']):+4}\t{r['rolls']:5}\t{r['danger']}\t{r['name']}")

    # Save snapshot JSON
    outfile = os.path.join(outdir, f"gen_{gen}.json")
    write_snapshot(snap, outfile)
    main_ct = len(snap.get("main_pool", []))
    dang_ct = len(snap.get("danger_pool", []))
    cq = snap.get("table_cq", "?")
    print(f"Wrote {outfile} | table_cq={cq} | main={main_ct} danger={dang_ct}")

    # Select parents and produce offspring for next gen
    parents = select_parents(snap, DEFAULTS)
    parent_genomes = [(p["genome"] if isinstance(p, dict) and "genome" in p else p) for p in parents]
    genomes = produce_offspring(parent_genomes, DEFAULTS, gen=gen)

# Write a tiny summary file (lightweight; not dependent on extra helpers)
summary_path = os.path.join(outdir, "summary.json")
summary = {
    "outdir": outdir,
    "gens": int(args.gens),
    "pop": int(args.pop),
    "seed": int(args.seed),
    "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
    "config": {
        "anneal_enable": bool(DEFAULTS.get("anneal_enable", False)),
        "crossbreed": DEFAULTS.get("crossbreed", {}),
    },
}
with open(summary_path, "w") as f:
    json.dump(summary, f, indent=2)
print(f"[INFO] Summary written to: {summary_path}")
