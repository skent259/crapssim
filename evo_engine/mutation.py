
import copy, random

def mutate_predictable(parent: dict, config: dict) -> dict:
    c = copy.deepcopy(parent)
    # small tweak to base unit or odds
    c['base_unit'] = max(1, float(c.get('base_unit', 10)) * random.choice([0.9,1.0,1.1]))
    return c

def mutate_wildcard50(parent: dict, config: dict) -> dict:
    c = copy.deepcopy(parent)
    if random.random() < 0.5 and c.get('bets'):
        # toggle come max_concurrent or odds
        for b in c['bets']:
            if b.get('type') in ('come','pass_line') and 'odds' in b:
                b['odds'] = f"{max(0,int(random.choice([0,1,2,3,4])))}x"
    else:
        c['base_unit'] = max(1, float(c.get('base_unit', 10)) * random.choice([0.8,1.2,1.5]))
    return c

def mutate_wildcard_chaos(parent: dict, config: dict) -> dict:
    c = copy.deepcopy(parent)
    # randomize bets order and maybe drop/add simple place bet
    random.shuffle(c.get('bets', []))
    if random.random() < 0.5:
        c.setdefault('bets', []).append({'type':'place','targets':[6,8],'amount':c.get('base_unit',10)})
    return c
