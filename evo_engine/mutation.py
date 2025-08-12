
from __future__ import annotations
import copy, random, uuid
from typing import Dict, Any, List

def _mut_id() -> str:
    return str(uuid.uuid4())[:8]

def _mut_boost(val: float, lo: float, hi: float) -> float:
    return float(max(lo, min(hi, val)))

def mutate_predictable(parent: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    c = copy.deepcopy(parent)
    # Gentle nudge on base_unit and odds multipliers (if present)
    c['id'] = f"{parent.get('id','strat')}_pred_{_mut_id()}"
    c.setdefault('lineage', {}).update({'parent_id': parent.get('id'), 'generation': parent.get('lineage',{}).get('generation',0)+1})
    bu = float(c.get('base_unit', config.get('base_unit', 10.0)))
    c['base_unit'] = round(_mut_boost(bu * random.choice([0.9, 1.0, 1.1]), 1.0, bu*2), 2)
    for b in c.get('bets', []):
        if 'odds' in b and isinstance(b['odds'], (int, float, str)):
            # odds can be "2x" strings or ints
            if isinstance(b['odds'], str) and b['odds'].endswith('x'):
                n = int(b['odds'][:-1])
                n = max(0, min(5, n + random.choice([-1,0,1])))
                b['odds'] = f"{n}x"
            else:
                n = int(b.get('odds', 0))
                n = max(0, min(5, n + random.choice([-1,0,1])))
                b['odds'] = n
    return c

def mutate_wildcard50(parent: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    c = copy.deepcopy(parent)
    c['id'] = f"{parent.get('id','strat')}_w50_{_mut_id()}"
    c.setdefault('lineage', {}).update({'parent_id': parent.get('id'), 'generation': parent.get('lineage',{}).get('generation',0)+1})
    # 50% chance to add or remove a bet; otherwise tweak base_unit/amounts more aggressively
    if random.random() < 0.5:
        # Add a random simple bet or remove one
        if random.random() < 0.5:
            # Add
            c.setdefault('bets', [])
            choice = random.choice(['field','any7','yo','boxcars','aces','ace_deuce','place','hardway'])
            if choice == 'place':
                c['bets'].append({'type':'place', 'targets': random.sample([4,5,6,8,9,10], k=2), 'amount': c.get('base_unit',10)})
            elif choice == 'hardway':
                c['bets'].append({'type':'hardway', 'targets': random.sample([4,6,8,10], k=1), 'amount': max(1, c.get('base_unit',10)/2)})
            else:
                c['bets'].append({'type': choice, 'amount': max(1, c.get('base_unit',10)/2)})
        else:
            # Remove a random bet if any
            if c.get('bets'):
                idx = random.randrange(len(c['bets']))
                del c['bets'][idx]
    else:
        # Tweak amounts
        for b in c.get('bets', []):
            if 'amount' in b:
                b['amount'] = round(_mut_boost(float(b['amount'])*random.choice([0.8,0.9,1.1,1.25]), 1.0, 10_000.0), 2)
        c['base_unit'] = round(_mut_boost(float(c.get('base_unit',10))*random.choice([0.8,1.2,1.5]), 1.0, 10_000.0), 2)
    return c

def mutate_wildcard_chaos(parent: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    c = copy.deepcopy(parent)
    c['id'] = f"{parent.get('id','strat')}_wcx_{_mut_id()}"
    c.setdefault('lineage', {}).update({'parent_id': parent.get('id'), 'generation': parent.get('lineage',{}).get('generation',0)+1})
    # Shuffle, add and remove multiple bets, randomize odds/base_unit hard
    random.shuffle(c.get('bets', []))
    # Add 0-3 random prop/hardway/place
    for _ in range(random.randint(0,3)):
        choice = random.choice(['field','any7','yo','boxcars','aces','ace_deuce','place','hardway'])
        if choice == 'place':
            c.setdefault('bets', []).append({'type':'place', 'targets': random.sample([4,5,6,8,9,10], k=2), 'amount': c.get('base_unit',10)})
        elif choice == 'hardway':
            c.setdefault('bets', []).append({'type':'hardway', 'targets': random.sample([4,6,8,10], k=1), 'amount': max(1, c.get('base_unit',10)/2)})
        else:
            c.setdefault('bets', []).append({'type': choice, 'amount': max(1, c.get('base_unit',10)/2)})
    # Remove up to 2 random bets if any
    for _ in range(min(2, len(c.get('bets', [])))):
        if c.get('bets') and random.random() < 0.5:
            del c['bets'][random.randrange(len(c['bets']))]
    # Randomize base_unit bigger swings
    c['base_unit'] = round(_mut_boost(float(c.get('base_unit',10))*random.choice([0.5,0.75,1.25,1.5,2.0]), 1.0, 50_000.0), 2)
    # Odds randomization
    for b in c.get('bets', []):
        if 'odds' in b:
            n = random.choice([0,1,2,3,4,5])
            b['odds'] = f"{n}x"
    return c


def crossover_one_point(a: dict, b: dict) -> dict:
    import copy, random, uuid
    from evo_engine.util import normalize_genome
    child = copy.deepcopy(a)
    child["id"] = f"xb_{str(uuid.uuid4())[:8]}"
    bets_a = a.get("bets", []) or []
    bets_b = b.get("bets", []) or []
    if not bets_a and not bets_b:
        return child
    cut_a = random.randrange(len(bets_a)+1) if bets_a else 0
    cut_b = random.randrange(len(bets_b)+1) if bets_b else 0
    child["bets"] = (bets_a[:cut_a] + bets_b[cut_b:]) or (bets_a or bets_b)
    child["base_unit"] = int(round((a.get("base_unit",10)+b.get("base_unit",10))/2))
    child, _notes = normalize_genome(child)
    return child
