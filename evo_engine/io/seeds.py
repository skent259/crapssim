
import os, json, glob, yaml

def load_seed_genomes(path: str) -> list[dict]:
    seeds = []
    if not os.path.isdir(path):
        return seeds
    for fn in glob.glob(os.path.join(path, "*.yaml")) + glob.glob(os.path.join(path, "*.yml")):
        try:
            with open(fn, "r") as f:
                data = yaml.safe_load(f) or {}
                data.setdefault("id", os.path.splitext(os.path.basename(fn))[0])
                seeds.append(data)
        except Exception:
            continue
    for fn in glob.glob(os.path.join(path, "*.json")):
        try:
            with open(fn, "r") as f:
                data = json.load(f) or {}
                data.setdefault("id", os.path.splitext(os.path.basename(fn))[0])
                seeds.append(data)
        except Exception:
            continue
    return seeds
