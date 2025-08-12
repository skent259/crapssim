#!/usr/bin/env python3
import os
import sys
import json
import argparse
import datetime
from statistics import mean

# Ensure repo root is on sys.path so "evo_engine" is importable
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from evo_engine import DEFAULTS
from evo_engine.population import (
    run_one_generation,
    select_parents,
    produce_offspring,
)
from evo_engine.io.snapshot import write_snapshot, read_snapshot
from evo_engine.io.seeds import load_seed_genomes


def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")


def _fallback_toy_seeds() -> list[dict]:
    # Minimal legal seeds so the loop can run even if seeds/ is empty
    return [
        {
            "id": "toy_pass",
            "name": "Toy Pass",
            "domain": "light",
            "bankroll": DEFAULTS.get("starting_bankroll", 1000),
            "base_unit": DEFAULTS.get("base_unit", 10),
            "bets": [{"type": "pass_line", "amount": DEFAULTS.get("base_unit", 10), "odds": "2x"}],
            "stop_rules": {"profit_target": 150, "loss_limit": -200, "max_rolls": 300},
            "lineage": {"parent_id": None, "generation": 0},
        },
        {
            "id": "toy_dont",
            "name": "Toy Don’t",
            "domain": "dark",
            "bankroll": DEFAULTS.get("starting_bankroll", 1000),
            "base_unit": DEFAULTS.get("base_unit", 10),
            "bets": [{"type": "dont_pass", "amount": DEFAULTS.get("base_unit", 10), "odds": "2x"}],
            "stop_rules": {"profit_target": 150, "loss_limit": -200, "max_rolls": 300},
            "lineage": {"parent_id": None, "generation": 0},
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gens", type=int, default=5, help="Number of generations to run")
    parser.add_argument("--pop", type=int, default=40, help="Population size target per generation")
    parser.add_argument("--seed", type=int, default=123, help="Base random seed")
    parser.add_argument("--out", type=str, default="runs", help="Output folder name (under repo root)")
    parser.add_argument("--resume", action="store_true", help="Resume from the last gen_*.json in --out")
    parser.add_argument("--report", action="store_true", help="Print a top-10 EF table each generation")
    args = parser.parse_args()

    # Resolve output directory
    base_outdir = os.path.join(REPO_ROOT, args.out)
    if args.resume:
        outdir = base_outdir
    else:
        outdir = base_outdir
        if os.path.exists(outdir):
            outdir = f"{outdir}_{_timestamp()}"
    os.makedirs(outdir, exist_ok=True)
    print(f"[INFO] Results will be written to: {outdir}")

    # Manifest (lightweight)
    manifest = {
        "started_at": datetime.datetime.utcnow().isoformat() + "Z",
        "defaults": DEFAULTS,
        "cmd": " ".join(sys.argv),
        "seeds_dir": os.path.join(REPO_ROOT, "strategies", "seeds"),
    }
    with open(os.path.join(outdir, "manifest.json"), "w") as mf:
        json.dump(manifest, mf, indent=2)

    # CSV
    csv_path = os.path.join(outdir, "ef_gen.csv")
    if not (args.resume and os.path.exists(csv_path)):
        with open(csv_path, "w") as cf:
            cf.write("generation,genome_id,name,domain,ef,profit,rolls,variance,table_cq,danger\n")

    # Load seeds
    seeds_dir = os.path.join(REPO_ROOT, "strategies", "seeds")
    genomes = load_seed_genomes(seeds_dir)
    if not genomes:
        genomes = _fallback_toy_seeds()

    # If resuming, pick up from last snapshot and produce offspring as next input
    start_gen = 0
    if args.resume:
        existing = [f for f in os.listdir(outdir) if f.startswith("gen_") and f.endswith(".json")]
        if existing:
            last = max(int(f.split("_")[1].split(".")[0]) for f in existing)
            snap = read_snapshot(os.path.join(outdir, f"gen_{last}.json"))
            parents = select_parents(snap, DEFAULTS)
            genomes = produce_offspring(parents, DEFAULTS)
            start_gen = last + 1
            print(f"[INFO] Resuming from gen_{last}.json → starting at generation {start_gen}")

    # Evolution loop
    cq_series: list[int] = []
    ef_all: list[float] = []
    best_ef: float | None = None
    worst_ef: float | None = None

    gens = int(args.gens)
    pop_target = int(args.pop)

    # If initial population smaller than target, pad via offspring of selves
    if len(genomes) < pop_target:
        from evo_engine.mutation import mutate_predictable
        # reproduce to meet target size
        while len(genomes) < pop_target:
            genomes.append(mutate_predictable(genomes[len(genomes) % max(1, len(genomes))], DEFAULTS))
        genomes = genomes[:pop_target]

    for gen in range(start_gen, gens):
        # Deterministic seed per gen for rollset
        seed_for_gen = args.seed + gen

        snap = run_one_generation(genomes, DEFAULTS, seed=seed_for_gen)
        cq_series.append(int(snap.table_cq))

        # Write snapshot
        outfile = os.path.join(outdir, f"gen_{gen}.json")
        write_snapshot(snap, outfile)

        # CSV append and EF tracking
        with open(csv_path, "a") as cf:
            for item in (snap.main_pool + snap.danger_pool):
                s = item["stats"]
                g = item["genome"]
                ef = float(s.get("ef", 0.0))
                ef_all.append(ef)
                best_ef = ef if best_ef is None else max(best_ef, ef)
                worst_ef = ef if worst_ef is None else min(worst_ef, ef)
                cf.write(
                    f"{gen},{g.get('id')},{g.get('name')},{g.get('domain')},"
                    f"{ef},{s.get('profit')},{s.get('rolls_survived')},"
                    f"{s.get('variance_score')},{s.get('table_cq')},{int(s.get('danger_zone'))}\n"
                )

        # Optional console report
        if args.report:
            top = sorted((snap.main_pool + snap.danger_pool), key=lambda x: x["stats"]["ef"], reverse=True)[:10]
            print("EF    Profit   Rolls  Danger  ID/Name")
            for it in top:
                s = it["stats"]
                g = it["genome"]
                print(f"{s['ef']:.3f} {s['profit']:+7.0f}  {s['rolls_survived']:5d}    {int(s['danger_zone'])}    {g.get('id','?')}/{g.get('name','?')}")

        # Select parents and produce next gen (keeps elites + mutated children)
        parents = select_parents(snap, DEFAULTS)

        # Ensure we always have something to breed
        if not parents:
            parents = (snap.main_pool or snap.danger_pool)[:]
            parents = parents[:max(1, int(len(parents) * 0.5))]

        parent_genomes = [
    (p["genome"] if isinstance(p, dict) and "genome" in p else p)
    for p in parents
]

        genomes = produce_offspring(parent_genomes, DEFAULTS)

        # Size control
        if len(genomes) > pop_target:
            genomes = genomes[:pop_target]
        elif len(genomes) < pop_target:
            # pad with copies of elites
            while len(genomes) < pop_target:
                genomes.append(parent_genomes[len(genomes) % max(1, len(parent_genomes))])

        print(
            f"Wrote {outfile} | table_cq={snap.table_cq} | main={len(snap.main_pool)} danger={len(snap.danger_pool)}"
        )

    # Summary.json
    summary = {
        "generations": gens,
        "population": pop_target,
        "avg_table_cq": mean(cq_series) if cq_series else None,
        "best_ef_score": best_ef,
        "worst_ef_score": worst_ef,
        "total_strategies_evaluated": len(ef_all),
        "finished_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    summary_path = os.path.join(outdir, "summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[INFO] Summary written to: {summary_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
