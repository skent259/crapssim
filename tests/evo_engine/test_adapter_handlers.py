
import types
import pytest

# Ensure repo root is on path
import os, sys
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from evo_engine.adapters.crapssim_adapter import _build_strategy_from_genome, BET_HANDLERS
import crapssim as craps
from crapssim.strategy import AggregateStrategy, CountStrategy
from crapssim.strategy.single_bet import BetHardWay
from crapssim.strategy import DontComeOddsMultiplier, ComeOddsMultiplier, PassLineOddsMultiplier

def test_bet_handlers_registered_minimum():
    for key in ["pass_line","come","dont_pass","place","hardway","field","any7","yo","boxcars","aces","ace_deuce","lay"]:
        assert key in BET_HANDLERS, f"Handler missing for {key}"

def _ops_for(genome):
    strat = _build_strategy_from_genome(genome)
    # Normalize to list for inspection
    if isinstance(strat, AggregateStrategy):
        return list(strat.strategies)
    return [strat]

def test_pass_line_with_odds_maps():
    g = {"base_unit": 10, "bets":[{"type":"pass_line","amount":10,"odds":"2x"}]}
    ops = _ops_for(g)
    assert any(isinstance(x, PassLineOddsMultiplier) for x in ops)

def test_come_bet_uses_countstrategy_and_come_odds():
    g = {"base_unit": 10, "bets":[{"type":"come","amount":10,"odds":"2x","max_concurrent":2}]}
    ops = _ops_for(g)
    assert any(isinstance(x, CountStrategy) for x in ops), "Come should use CountStrategy"
    assert any(isinstance(x, ComeOddsMultiplier) for x in ops), "Come should apply ComeOddsMultiplier"

def test_hardway_uses_proper_signature():
    g = {"base_unit": 10, "bets":[{"type":"hardway","targets":[6,8],"amount":5}]}
    ops = _ops_for(g)
    assert sum(isinstance(x, BetHardWay) for x in ops) == 2

def test_lay_emulation_uses_dc_and_odds():
    g = {"base_unit": 10, "bets":[{"type":"lay","targets":[4,10],"amount":20,"odds":"2x"}]}
    ops = _ops_for(g)
    # Should include a CountStrategy on DontCome, and a DontComeOddsMultiplier
    assert any(isinstance(x, CountStrategy) for x in ops)
    assert any(isinstance(x, DontComeOddsMultiplier) for x in ops)

def test_unknown_bet_types_are_ignored():
    g = {"base_unit": 10, "bets":[{"type":"unknown_bet_type","amount":5}]}
    ops = _ops_for(g)
    # Should default to pass line if nothing valid was added
    assert len(ops) == 1
    assert isinstance(ops[0], craps.strategy.BetPassLine)
