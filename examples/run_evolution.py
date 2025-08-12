
import os, sys, json
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path: sys.path.insert(0, REPO_ROOT)

from evo_engine import DEFAULTS
from evo_engine.population import run_one_generation, select_parents, produce_offspring
from evo_engine.io.snapshot import write_snapshot
from evo_engine.io.seeds import load_seed_genomes

def load_genomes():
    seeds_path = os.path.join(REPO_ROOT, "strategies", "seeds")
    genomes = load_seed_genomes(seeds_path)
    if not genomes:
        # Fallback tiny demo
        genomes = [
            {
                "id": "3pt_molly",
                "name": "3-Point Molly",
                "domain": "light",
                "base_unit": 10,
                "bankroll": 1000,
                "bets": [
                    {"type": "pass_line", "amount": 10, "odds": "2x"},
                    {"type": "come", "amount": 10, "odds": "2x", "max_concurrent": 2},
                ],
                "stop_rules": {"profit_target": 150, "loss_limit": -200, "max_rolls": 300},
            },
            {
                "id": "contracruise",
                "name": "ContraCruise",
                "domain": "dark",
                "base_unit": 10,
                "bankroll": 1000,
                "bets": [
                    {"type": "dont_pass", "amount": 10, "odds": "2x"},
                    {"type": "place", "targets": [6,8], "amount": 5},
                ],
                "stop_rules": {"profit_target": 150, "loss_limit": -200, "max_rolls": 300},
            },
        ]
    # Normalize
    for i,g in enumerate(genomes):
        g.setdefault("id", g.get("name", f"genome_{i}").lower().replace(" ","_"))
        g.setdefault("bankroll", 1000)
        g.setdefault("base_unit", 10)
        g.setdefault("lineage", {"parent_id": None, "generation": 0})
    return genomes


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run evolutionary craps sim for N generations.")
    parser.add_argument("--gens", type=int, default=3, help="Number of generations to run")
    parser.add_argument("--pop", type=int, default=None, help="Population size override")
    parser.add_argument("--seed", type=int, default=0, help="Random seed / rollset seed")
    args = parser.parse_args()

    DEFAULTS["crossbreed"] = {"enable": bool(args.xbreed), "rate": float(args.xbreed_rate)}
    DEFAULTS["anneal_enable"] = not bool(args.no_anneal)

    outdir = os.path.join(REPO_ROOT, "runs")

    os.makedirs(outdir, exist_ok=True)

    genomes = load_genomes()
    if args.pop:
        DEFAULTS['population_size'] = int(args.pop)
    gens = int(args.gens)
    for gen in range(gens):
        snap = run_one_generation(genomes, DEFAULTS, seed=(args.seed + gen))
        outfile = os.path.join(outdir, f"gen_{gen}.json")
        write_snapshot(snap, outfile)
        print(f"Wrote {outfile} | table_cq={snap.table_cq} | main={len(snap.main_pool)} danger={len(snap.danger_pool)}")
        parents = select_parents(snap, DEFAULTS)
        genomes = produce_offspring(parents, DEFAULTS, gen=start_gen)
