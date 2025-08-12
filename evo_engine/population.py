
from __future__ import annotations
from typing import List, Dict, Any
from dataclasses import dataclass
from evo_engine.rollsets import generate_roll_set, compute_table_cq, validate_table_cq
from evo_engine.adapters.crapssim_adapter import run_strategy_with_crapssim
from evo_engine.scoring import variance_score, ef_main, ef_danger, in_danger
from evo_engine.stats import StrategyStats
from typing import List, Dict, Any

def _annealed_mix(config: dict, gen: int) -> dict:
    if not config.get('anneal_enable', False):
        return {
            'predictables_pct': config.get('predictables_pct', 0.6),
            'wildcard50_pct':  config.get('wildcard50_pct', 0.25),
            'wildcardChaos_pct': config.get('wildcardChaos_pct', 0.15),
        }
    g0 = int(config.get('anneal_start_gen', 0))
    g1 = int(config.get('anneal_end_gen', 20))
    if gen <= g0:
        t = 0.0
    elif gen >= g1:
        t = 1.0
    else:
        t = (gen - g0) / max(1, (g1 - g0))
    start = {
        'predictables_pct': config.get('predictables_pct', 0.6),
        'wildcard50_pct':  config.get('wildcard50_pct', 0.25),
        'wildcardChaos_pct': config.get('wildcardChaos_pct', 0.15),
    }
    end = config.get('anneal_floor', {'predictables_pct':0.75,'wildcard50_pct':0.2,'wildcardChaos_pct':0.05})
    return {k: (start[k]*(1-t) + end.get(k, start[k])*t) for k in start}

from evo_engine.util import category_fit_bonus

@dataclass
class PopulationSnapshot:
    generation: int
    roll_set_id: str
    table_cq: int
    main_pool: list[dict]
    danger_pool: list[dict]
    hall_of_shame: list[dict]
    hall_of_fame: list[dict]

def run_one_generation(genomes: List[Dict[str,Any]], config: Dict[str,Any], seed: int) -> PopulationSnapshot:
    roll_set = generate_roll_set(num_shooters=25, seed=seed)
    cq = compute_table_cq(roll_set)
    main_pool, danger_pool = [], []
    hall_fame, hall_shame = [], []
    for g in genomes:
        stats: StrategyStats = run_strategy_with_crapssim(g, roll_set, config)
        v = variance_score(stats.bankroll_curve, config.get('starting_bankroll', 1000.0))
        stats.variance_score = v; stats.table_cq = cq
        ef_fn = ef_danger if in_danger(v, config.get('danger_variance_threshold',0.75)) else ef_main
        stats.danger_zone = ef_fn is ef_danger
        cb = category_fit_bonus(g)
        stats.ef = ef_fn(stats.rolls_survived, stats.profit, v, category_fit_bonus=cb,
                         start_bankroll=config.get('starting_bankroll',1000.0),
                         max_rolls_cap=config.get('max_rolls_cap',2000))
        item = {"genome": g, "stats": stats.__dict__}
        (danger_pool if stats.danger_zone else main_pool).append(item)
    if main_pool: hall_fame.append(max(main_pool, key=lambda x:x['stats']['ef']))
    if main_pool + danger_pool: hall_shame.append(min(main_pool + danger_pool, key=lambda x:x['stats']['ef']))
    return PopulationSnapshot(generation=seed, roll_set_id=f"seed_{seed}", table_cq=cq,
                              main_pool=main_pool, danger_pool=danger_pool,
                              hall_of_shame=hall_shame, hall_of_fame=hall_fame)

def select_parents(snapshot: PopulationSnapshot, config: Dict[str,Any]) -> List[Dict[str,Any]]:
    mp = snapshot.main_pool
    if not mp: return []
    elites = sorted(mp, key=lambda x:x['stats']['ef'], reverse=True)
    k = max(1, int(len(elites) * config.get('elite_keep_pct', 0.2)))
    return [e['genome'] for e in elites[:k]]



def produce_offspring(parents: List[Dict[str,Any]], config: Dict[str,Any], gen: int | None = None) -> List[Dict[str,Any]]:
    from evo_engine.mutation import mutate_predictable, mutate_wildcard50, mutate_wildcard_chaos
    if not parents:
        return []
    size = max(len(parents), int(config.get('population_size', 10)))
    mix = _annealed_mix(config, int(gen or 0))
    n_pred = max(0, int(size * mix['predictables_pct']))
    n_w50  = max(0, int(size * mix['wildcard50_pct']))
    n_wc   = max(0, int(size * mix['wildcardChaos_pct']))
    children: List[Dict[str,Any]] = []
    elites_keep = max(1, int(size * config.get('elite_keep_pct', 0.1)))
    elites = parents[:elites_keep]
    children.extend(elites)
    import random
    for _ in range(n_pred):
        children.append(mutate_predictable(random.choice(parents), config))
    for _ in range(n_w50):
        children.append(mutate_wildcard50(random.choice(parents), config))
    for _ in range(n_wc):
        children.append(mutate_wildcard_chaos(random.choice(parents), config))
    xcfg = config.get('crossbreed', {'enable': False, 'rate': 0.15})
    children = _maybe_crossbreed(children, bool(xcfg.get('enable', False)), float(xcfg.get('rate', 0.15)))
    while len(children) < size:
        children.append(random.choice(parents))
    return children[:size]


def _maybe_crossbreed(genomes: list[dict], enable: bool, rate: float = 0.15) -> list[dict]:
    if not enable or len(genomes) < 2:
        return genomes
    from evo_engine.mutation import crossover_one_point
    import random
    out = genomes[:]
    pairs = max(1, int(len(genomes) * rate))
    for _ in range(pairs):
        a, b = random.sample(genomes, 2)
        out.append(crossover_one_point(a, b))
    return out
