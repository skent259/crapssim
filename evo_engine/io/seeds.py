
import os, json, glob, yaml
def load_seed_genomes(path:str)->list[dict]:
    seeds=[]; 
    if not os.path.isdir(path): return seeds
    for fn in glob.glob(os.path.join(path,'*.yml'))+glob.glob(os.path.join(path,'*.yaml')):
        try:
            with open(fn,'r') as f:
                d=yaml.safe_load(f) or {}; d.setdefault('id', os.path.splitext(os.path.basename(fn))[0]); seeds.append(d)
        except Exception: pass
    for fn in glob.glob(os.path.join(path,'*.json')):
        try:
            with open(fn,'r') as f:
                d=json.load(f) or {}; d.setdefault('id', os.path.splitext(os.path.basename(fn))[0]); seeds.append(d)
        except Exception: pass
    return seeds
