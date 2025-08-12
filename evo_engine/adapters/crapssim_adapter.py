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
                ops.append(PassLineOddsMultiplier(
                    int(str(odds).rstrip("x")) if isinstance(odds, str) and odds.endswith("x") else int(odds)
                ))

        elif btype == "come":
            amt = float(bet.get("amount", base_unit))
            maxc = int(bet.get("max_concurrent", 1))
            # CountStrategy wants a Bet instance, not a Strategy.
            come_strat = CountStrategy(craps.bet.Come, maxc, craps.bet.Come(amt))
            ops.append(come_strat)
            odds = bet.get("odds", 0)
            if odds:
                # Use ComeOddsMultiplier for come bets
                ops.append(craps.strategy.ComeOddsMultiplier(
                    int(str(odds).rstrip("x")) if isinstance(odds, str) and odds.endswith("x") else int(odds)
                ))

        elif btype == "dont_pass":
            amt = float(bet.get("amount", base_unit))
            ops.append(BetDontPass(amt))
            odds = bet.get("odds", 0)
            if odds:
                ops.append(DontPassOddsMultiplier(
                    int(str(odds).rstrip("x")) if isinstance(odds, str) and odds.endswith("x") else int(odds)
                ))

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
