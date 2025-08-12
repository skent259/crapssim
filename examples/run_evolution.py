
import os, json, sys, time, sys, json
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
    
    parser.add_argument("--out", type=str, default="runs", help="Output directory (default: runs)")
    parser.add_argument("--resume", action="store_true", help="Resume from last gen_*.json in --out")
    parser.add_argument("--report", action="store_true", help="Print a brief top-10 EF table per gen")
args = parser.parse_args()

    outdir = os.path.join(REPO_ROOT, args.out)

    
    # Output handling
    ts = time.strftime("%Y-%m-%d_%H%M%S")
    if os.path.exists(outdir) and not args.resume:
        outdir = f"{outdir}_{ts}"
    os.makedirs(outdir, exist_ok=True)

    # manifest
    manifest = {"cmd": " ".join(sys.argv), "defaults": DEFAULTS}
    with open(os.path.join(outdir, "manifest.json"), "w") as mf:
        json.dump(manifest, mf, indent=2)

    # CSV init
    csv_path = os.path.join(outdir, "ef_gen.csv")
    if not os.path.exists(csv_path) or not args.resume:
        with open(csv_path, "w") as cf:
            cf.write("generation,genome_id,name,domain,ef,profit,rolls,variance,table_cq,danger\n")

    # SUMMARY_INIT
    summary = {"gens": [], "best": {"ef": -1e9}, "worst": {"ef": 1e9}, "hall_fame": 0, "hall_shame": 0}
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
        genomes = produce_offspring(parents, DEFAULTS)

        # CSV_APPEND
        with open(csv_path, "a") as cf:
            for item in (snap.main_pool + snap.danger_pool):
                s = item["stats"]; gnm = item["genome"]
                cf.write(f"{gen},{gnm.get('id')},{gnm.get('name')},{gnm.get('domain')},{s['ef']},{s['profit']},{s['rolls_survived']},{s['variance_score']},{s['table_cq']},{int(s['danger_zone'])}\n")

        if args.report:
            top = sorted((snap.main_pool + snap.danger_pool), key=lambda x: x["stats"]["ef"], reverse=True)[:10]
            print("EF    Profit  Rolls  D  Name/ID")
            for it in top:
                s=it["stats"]; g=it["genome"]
                print(f"{s['ef']:.3f} {s['profit']:+.0f}   {s['rolls_survived']:4d}  {int(s['danger_zone'])} {g.get('name') or g.get('id')}")

        # summary accumulators
        all_stats = [it["stats"] for it in (snap.main_pool + snap.danger_pool)]
        if all_stats:
            best = max(all_stats, key=lambda s: s["ef"])
            worst = min(all_stats, key=lambda s: s["ef"])
            if best["ef"] > summary["best"]["ef"]:
                summary["best"] = {"ef": best["ef"], "profit": best["profit"], "rolls": best["rolls_survived"], "generation": gen}
            if worst["ef"] < summary["worst"]["ef"]:
                summary["worst"] = {"ef": worst["ef"], "profit": worst["profit"], "rolls": worst["rolls_survived"], "generation": gen}
            summary["gens"].append({"gen": gen, "table_cq": snap.table_cq, "main": len(snap.main_pool), "danger": len(snap.danger_pool)})

# write summary.json
with open(os.path.join(outdir, "summary.json"), "w") as sf:
    json.dump(summary, sf, indent=2)
