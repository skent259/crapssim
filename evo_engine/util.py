
from __future__ import annotations
from typing import Dict, Any

DARK_TYPES = {"dont_pass", "lay", "dont_come"}
LIGHT_TYPES = {"pass_line", "come", "place", "field", "hardway", "any7", "yo", "boxcars", "aces", "ace_deuce"}

def infer_play_mix(genome: Dict[str, Any]) -> dict:
    bets = genome.get("bets", []) or []
    total = max(1, len(bets))
    dark = sum(1 for b in bets if b.get("type") in DARK_TYPES)
    light = sum(1 for b in bets if b.get("type") in LIGHT_TYPES)
    return {"dark_frac": dark/total, "light_frac": light/total}

def category_fit_bonus(genome: Dict[str, Any]) -> float:
    # Small nudges: +0.02 if mix matches declared domain, -0.02 if strongly mismatched.
    domain = (genome.get("domain") or "").lower()
    mix = infer_play_mix(genome)
    bonus = 0.0
    if domain == "dark":
        if mix["dark_frac"] >= 0.5:
            bonus += 0.02
        elif mix["light_frac"] >= 0.7:
            bonus -= 0.02
    elif domain == "light":
        if mix["light_frac"] >= 0.5:
            bonus += 0.02
        elif mix["dark_frac"] >= 0.7:
            bonus -= 0.02
    elif domain == "hybrid":
        # reward balance
        if abs(mix["dark_frac"] - mix["light_frac"]) <= 0.25:
            bonus += 0.02
    return bonus
