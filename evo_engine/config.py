  
DEFAULTS = {
  "population_size": 10,
  "elite_keep_pct": 0.2,
  "predictables_pct": 0.6,
  "wildcard50_pct": 0.2,
  "wildcardChaos_pct": 0.2,
  "danger_variance_threshold": 0.75,
  "danger_cull_after_gens": 8,
  "tablecq_range": (40, 90),
  "starting_bankroll": 1000.0,
  "base_unit": 10.0,
  "max_rolls_cap": 500,
  "population_size": 200,
  "elite_keep_pct": 0.08,

    # mutation mix at “midpoint”; we’ll anneal toward calmer later
    "predictables_pct": 0.60,
    "wildcard50_pct": 0.25,
    "wildcardChaos_pct": 0.15,

    # annealing schedule (linear)
    "anneal_enable": True,
    "anneal_start_gen": 0,
    "anneal_end_gen": 20,           # by this gen, chill the chaos
    "anneal_floor": {               # minimum mix by end_gen
        "predictables_pct": 0.75,
        "wildcard50_pct": 0.20,
        "wildcardChaos_pct": 0.05,
    },
}
