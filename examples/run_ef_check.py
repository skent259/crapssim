
import os, sys
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path: sys.path.insert(0, REPO_ROOT)

from evo_engine import DEFAULTS
from evo_engine.population import run_one_generation
import json, os

def demo_genomes():
    return [
        {
            "id": "3pt_molly",
            "name": "3-Point Molly",
            "domain": "light",
            "base_unit": 10,
            "bankroll": 1000,
            "bets": [
                {"type": "pass_line", "amount": 10, "odds": "2x"},
                {"type": "come", "amount": 10, "odds": "2x", "max_concurrent": 2},
                {"type": "hardway", "targets": [6,8], "amount": 5},
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
                {"type": "field", "amount": 5},
                {"type": "yo", "amount": 1},
            ],
            "stop_rules": {"profit_target": 150, "loss_limit": -200, "max_rolls": 300},
        },
    ]


if __name__ == "__main__":
    import os, sys
    REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if REPO_ROOT not in sys.path: sys.path.insert(0, REPO_ROOT)
    from evo_engine.io.seeds import load_seed_genomes

    seeds_path = os.path.join(REPO_ROOT, "strategies", "seeds")
    genomes = load_seed_genomes(seeds_path) or demo_genomes()
    # Ensure basic IDs
    for i,g in enumerate(genomes):
        g.setdefault("id", g.get("name", f"genome_{i}").lower().replace(" ","_"))
        g.setdefault("bankroll", 1000)
        g.setdefault("base_unit", 10)

    from evo_engine import DEFAULTS
    from evo_engine.population import run_one_generation
    snap = run_one_generation(genomes, DEFAULTS, seed=0)

    outdir = os.path.join(os.path.dirname(__file__), "..", "runs")
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, "gen_0.json")
    from evo_engine.io.snapshot import write_snapshot
    write_snapshot(snap, outfile)
    print("Wrote", outfile)
    import json
    print(json.dumps({"table_cq": snap.table_cq, "main_pool": len(snap.main_pool), "danger_pool": len(snap.danger_pool)}, indent=2))
