
from __future__ import annotations
from typing import Dict, Any, List, Callable

import crapssim as craps
from crapssim.strategy import (
    BetPassLine,
    BetDontPass,
    BetPlace,
    PassLineOddsMultiplier,
    DontPassOddsMultiplier,
    ComeOddsMultiplier,
    DontComeOddsMultiplier,
    AggregateStrategy,
    CountStrategy,
)
from crapssim.strategy.single_bet import (
    BetHardWay,
    BetAny7,
    BetTwo,
    BetThree,
    BetYo,
    BetBoxcars,
    BetField,
)
from evo_engine.stats import StrategyStats


def _odds_from_any(odds: str | int | float) -> int:
    if isinstance(odds, (int, float)):
        return int(odds)
    if isinstance(odds, str) and odds.endswith("x"):
        core = odds[:-1]
        try:
            return int(core) if core else 0
        except ValueError:
            return 0
    return 0


# ---- Bet Handlers ----------------------------------------------------------

Handler = Callable[[dict, float], List[object]]

def _h_pass_line(bet: dict, base_unit: float) -> List[object]:
    amt = float(bet.get("amount", base_unit))
    ops: List[object] = [BetPassLine(amt)]
    odds = bet.get("odds", 0)
    if odds:
        ops.append(PassLineOddsMultiplier(_odds_from_any(odds)))
    return ops

def _h_come(bet: dict, base_unit: float) -> List[object]:
    amt = float(bet.get("amount", base_unit))
    maxc = int(bet.get("max_concurrent", 1))
    ops: List[object] = [CountStrategy(craps.bet.Come, maxc, craps.bet.Come(amt))]
    odds = bet.get("odds", 0)
    if odds:
        ops.append(ComeOddsMultiplier(_odds_from_any(odds)))
    return ops

def _h_dont_pass(bet: dict, base_unit: float) -> List[object]:
    amt = float(bet.get("amount", base_unit))
    ops: List[object] = [BetDontPass(amt)]
    odds = bet.get("odds", 0)
    if odds:
        ops.append(DontPassOddsMultiplier(_odds_from_any(odds)))
    return ops

def _h_place(bet: dict, base_unit: float) -> List[object]:
    targets = bet.get("targets", [])
    amount = float(bet.get("amount", base_unit))
    return [BetPlace({int(t): amount for t in targets})]

def _h_hardway(bet: dict, base_unit: float) -> List[object]:
    targets = [int(t) for t in bet.get("targets", []) if int(t) in (4, 6, 8, 10)]
    amount = float(bet.get("amount", base_unit))
    return [BetHardWay(t, amount) for t in targets]

def _h_field(bet: dict, base_unit: float) -> List[object]:
    amount = float(bet.get("amount", base_unit))
    return [BetField(amount)]

def _h_any7(bet: dict, base_unit: float) -> List[object]:
    amount = float(bet.get("amount", base_unit))
    return [BetAny7(amount)]

def _h_yo(bet: dict, base_unit: float) -> List[object]:
    amount = float(bet.get("amount", base_unit))
    return [BetYo(amount)]

def _h_boxcars(bet: dict, base_unit: float) -> List[object]:
    amount = float(bet.get("amount", base_unit))
    return [BetBoxcars(amount)]

def _h_aces(bet: dict, base_unit: float) -> List[object]:
    amount = float(bet.get("amount", base_unit))
    return [BetTwo(amount)]

def _h_ace_deuce(bet: dict, base_unit: float) -> List[object]:
    amount = float(bet.get("amount", base_unit))
    return [BetThree(amount)]

def _h_lay(bet: dict, base_unit: float) -> List[object]:
    # Emulate Lay via Don't Come entries + odds multiplier (no commission modeled).
    targets = [int(t) for t in bet.get("targets", []) if int(t) in (4, 5, 6, 8, 9, 10)]
    amount = float(bet.get("amount", base_unit))
    odds = _odds_from_any(bet.get("odds", 2))  # default to 2x if omitted
    count = max(1, len(targets)) if targets else 1
    ops: List[object] = [CountStrategy(craps.bet.DontCome, count, craps.bet.DontCome(amount))]
    if odds:
        ops.append(DontComeOddsMultiplier(odds))
    return ops


BET_HANDLERS: Dict[str, Handler] = {
    "pass_line": _h_pass_line,
    "come": _h_come,
    "dont_pass": _h_dont_pass,
    "place": _h_place,
    "hardway": _h_hardway,
    "field": _h_field,
    "any7": _h_any7,
    "yo": _h_yo, "eleven": _h_yo, "11": _h_yo,
    "boxcars": _h_boxcars, "12": _h_boxcars,
    "aces": _h_aces, "2": _h_aces,
    "ace_deuce": _h_ace_deuce, "three": _h_ace_deuce, "3": _h_ace_deuce,
    "lay": _h_lay,
}


def _build_strategy_from_genome(genome: Dict[str, Any]):
    ops: List[object] = []
    base_unit = float(genome.get("base_unit", 10))

    for bet in genome.get("bets", []) or []:
        btype = str(bet.get("type", "")).lower()
        handler = BET_HANDLERS.get(btype)
        if handler is None:
            # Unknown type: ignore for now
            continue
        ops.extend(handler(bet, base_unit))

    if not ops:
        # default to a simple pass line
        return BetPassLine(base_unit)
    if len(ops) == 1:
        return ops[0]
    return AggregateStrategy(*ops)


def run_strategy_with_crapssim(genome: dict, roll_set: dict, config: dict) -> StrategyStats:
    table = craps.Table()
    strategy = _build_strategy_from_genome(genome)
    table.add_player(
        bankroll=float(genome.get("bankroll", config.get("starting_bankroll", 1000.0))),
        strategy=strategy,
        name=genome.get("name", "Genome"),
    )
    player = table.players[0]

    bankroll_curve = [float(player.bankroll)]
    rolls_survived = 0

    for roll in roll_set.get("rolls", []):
        craps.table.TableUpdate().run(table, dice_outcome=roll, verbose=False)
        bankroll_curve.append(float(player.bankroll))
        rolls_survived += 1

        stop = genome.get("stop_rules", {})
        if stop:
            profit = float(player.bankroll) - float(
                genome.get("bankroll", config.get("starting_bankroll", 1000.0))
            )
            if profit >= float(stop.get("profit_target", 1e18)):
                break
            if profit <= float(stop.get("loss_limit", -1e18)):
                break
            if rolls_survived >= int(stop.get("max_rolls", 1e18)):
                break

    profit = float(player.bankroll) - float(
        genome.get("bankroll", config.get("starting_bankroll", 1000.0))
    )

    return StrategyStats(
        id=str(genome.get("id", genome.get("name", "genome"))),
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
