from __future__ import annotations
from typing import Dict, Any, List

import crapssim as craps
from crapssim.strategy import (
    BetPassLine,
    BetDontPass,
    BetPlace,
    PassLineOddsMultiplier,
    DontPassOddsMultiplier,
    ComeOddsMultiplier, 
    AggregateStrategy,
    CountStrategy,
)
from crapssim.strategy.single_bet import BetCome

from evo_engine.stats import StrategyStats
from evo_engine.lineage import new_lineage

def _odds_multiplier(odds: str|int, light: bool=True):
    if isinstance(odds, (int,float)):
        mult = int(odds)
    elif isinstance(odds, str) and odds.endswith("x"):
        mult = int(odds[:-1])
    else:
        mult = 0
    return PassLineOddsMultiplier(mult) if light else DontPassOddsMultiplier(mult)

def _build_strategy_from_genome(genome: Dict[str, Any]):
    ops: List = []
    base_unit = float(genome.get("base_unit", 10))
    for bet in genome.get("bets", []):
        btype = bet.get("type")
        if btype == "pass_line":
            amt = float(bet.get("amount", base_unit))
            ops.append(BetPassLine(amt))
            odds = bet.get("odds", 0)
            if odds:
                ops.append(_odds_multiplier(odds, light=True))
        elif btype == "come":
            amt = float(bet.get("amount", base_unit))
            maxc = int(bet.get("max_concurrent", 1))
            come_strat = CountStrategy(craps.bet.Come, maxc, BetCome(amt))
            ops.append(come_strat)
            odds = bet.get("odds", 0)
            if odds:
                # Pass line odds multiplier also applies to Come odds in this simplified mapping
                ops.append(_odds_multiplier(odds, light=True))
        elif btype == "dont_pass":
            amt = float(bet.get("amount", base_unit))
            ops.append(BetDontPass(amt))
            odds = bet.get("odds", 0)
            if odds:
                ops.append(_odds_multiplier(odds, light=False))
        elif btype == "place":
            # expects targets and amount per target
            targets = bet.get("targets", [])
            amount = float(bet.get("amount", base_unit))
            ops.append(BetPlace({int(t): amount for t in targets}))
        # NOTE: Lays/Hardways and other props can be added later
    if not ops:
        ops = [BetPassLine(base_unit)]
    if len(ops) == 1:
        return ops[0]
    return AggregateStrategy(*ops)

def run_strategy_with_crapssim(genome: dict, roll_set: dict, config: dict) -> StrategyStats:
    table = craps.Table()
    strategy = _build_strategy_from_genome(genome)
    table.add_player(bankroll=float(genome.get("bankroll", config.get("starting_bankroll", 1000.0))), strategy=strategy, name=genome.get("name","Genome"))
    player = table.players[0]

    bankroll_curve = [float(player.bankroll)]
    rolls_survived = 0
    # step through fixed dice to capture bankroll curve
    for i, roll in enumerate(roll_set.get("rolls", [])):
        craps.table.TableUpdate().run(table, dice_outcome=roll, verbose=False)
        bankroll_curve.append(float(player.bankroll))
        rolls_survived += 1
        # stop rules
        stop = genome.get("stop_rules", {})
        if stop:
            profit = float(player.bankroll) - float(genome.get("bankroll", config.get("starting_bankroll", 1000.0)))
            if profit >= float(stop.get("profit_target", 1e18)):
                break
            if profit <= float(stop.get("loss_limit", -1e18)):
                break
            if rolls_survived >= int(stop.get("max_rolls", 1e18)):
                break

    profit = float(player.bankroll) - float(genome.get("bankroll", config.get("starting_bankroll", 1000.0)))
    # Stats object will be filled further by population/scoring step
    return StrategyStats(
        id=str(genome.get("id", genome.get("name","genome"))),
        generation=int(genome.get("lineage", {}).get("generation", 0)),
        rolls_survived=int(rolls_survived),
        profit=float(profit),
        bankroll_curve=list(bankroll_curve),
        variance_score=0.0,
        ef=0.0,
        table_cq=0,
        danger_zone=False,
        hall_flags={"shame": False, "fame": False},
    )
