
from __future__ import annotations
from typing import Dict, Any, List

import crapssim as craps
from crapssim.strategy import (
    BetPassLine, BetDontPass, BetPlace,
    PassLineOddsMultiplier, DontPassOddsMultiplier, ComeOddsMultiplier,
    AggregateStrategy, CountStrategy,
)
from crapssim.strategy.single_bet import (
    BetHardWay, BetAny7, BetTwo, BetThree, BetYo, BetBoxcars, BetField
)
from evo_engine.stats import StrategyStats

def _odds_from_any(odds: str|int|float)->int:
    if isinstance(odds, (int, float)):
        return int(odds)
    if isinstance(odds, str) and odds.endswith("x"):
        return int(odds[:-1] or 0)
    return 0

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
                ops.append(PassLineOddsMultiplier(_odds_from_any(odds)))

        elif btype == "come":
            amt = float(bet.get("amount", base_unit))
            maxc = int(bet.get("max_concurrent", 1))
            come_strat = CountStrategy(craps.bet.Come, maxc, craps.bet.Come(amt))
            ops.append(come_strat)
            odds = bet.get("odds", 0)
            if odds:
                ops.append(ComeOddsMultiplier(_odds_from_any(odds)))

        elif btype == "dont_pass":
            amt = float(bet.get("amount", base_unit))
            ops.append(BetDontPass(amt))
            odds = bet.get("odds", 0)
            if odds:
                ops.append(DontPassOddsMultiplier(_odds_from_any(odds)))

        elif btype == "place":
            targets = bet.get("targets", [])
            amount = float(bet.get("amount", base_unit))
            ops.append(BetPlace({int(t): amount for t in targets}))

        elif btype == "hardway":
            # targets should be subset of [4,6,8,10]
            targets = [int(t) for t in bet.get("targets", []) if int(t) in (4,6,8,10)]
            amount = float(bet.get("amount", base_unit))
            for t in targets:
                ops.append(BetHardWay({t: amount}))

        elif btype == "field":
            amount = float(bet.get("amount", base_unit))
            ops.append(BetField(amount))

        elif btype == "any7":
            amount = float(bet.get("amount", base_unit))
            ops.append(BetAny7(amount))

        elif btype in ("yo","eleven","11"):
            amount = float(bet.get("amount", base_unit))
            ops.append(BetYo(amount))

        elif btype in ("boxcars","12"):
            amount = float(bet.get("amount", base_unit))
            ops.append(BetBoxcars(amount))

        elif btype in ("aces","2"):
            amount = float(bet.get("amount", base_unit))
            ops.append(BetTwo(amount))

        elif btype in ("ace_deuce","three","3"):
            amount = float(bet.get("amount", base_unit))
            ops.append(BetThree(amount))

        elif btype == "lay":
            # NOTE: The current engine does not provide an explicit Lay bet type.
            # We'll skip these gracefully for now; future: emulate via DC with odds.
            continue

        # else: ignore unknown bet types for now

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
    for i, roll in enumerate(roll_set.get("rolls", [])):
        craps.table.TableUpdate().run(table, dice_outcome=roll, verbose=False)
        bankroll_curve.append(float(player.bankroll))
        rolls_survived += 1
        stop = genome.get("stop_rules", {})
        if stop:
            profit = float(player.bankroll) - float(genome.get("bankroll", config.get("starting_bankroll", 1000.0)))
            if profit >= float(stop.get("profit_target", 1e18)): break
            if profit <= float(stop.get("loss_limit", -1e18)): break
            if rolls_survived >= int(stop.get("max_rolls", 1e18)): break

    profit = float(player.bankroll) - float(genome.get("bankroll", config.get("starting_bankroll", 1000.0)))
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
