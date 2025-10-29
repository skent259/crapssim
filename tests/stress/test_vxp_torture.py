import math
import random
from typing import Optional, Set

import pytest

import crapssim.bet as B
from crapssim.table import Table, TableUpdate
from crapssim.strategy.tools import NullStrategy

# --- Utilities ---------------------------------------------------------------

DICE_PAIRS = [(d1, d2) for d1 in range(1, 7) for d2 in range(1, 7)]
BOX = [4, 5, 6, 8, 9, 10]


@pytest.fixture
def require_stress(pytestconfig):
    """Skip the heavy stress test unless explicitly requested via -m stress."""
    markexpr = getattr(pytestconfig.option, "markexpr", "") or ""
    if "stress" not in markexpr:
        pytest.skip("stress test: run with -m stress")


def roll_fixed(table: Table, total: int):
    """Roll a specific total using a consistent (d1,d2) producing that total."""
    # deterministic mapping picking the first matching pair
    for d1, d2 in DICE_PAIRS:
        if d1 + d2 == total:
            TableUpdate().run(table, dice_outcome=(d1, d2))
            return
    raise ValueError(f"Bad total {total}")


def try_add(player, bet):
    """Attempt to add a bet via Player.add_bet(). Silently ignore if not allowed."""
    try:
        player.add_bet(bet)  # relies on is_allowed & bankroll check
    except Exception:
        # We never want a randomized harness to explode on add attempts
        pass


def random_bet_mix(rng: random.Random, bankroll_scale=1.0):
    """Return a function that, given (table, player), attempts random bet adds."""

    def attempt(table: Table, player):
        amt = bankroll_scale * rng.choice([5, 10, 15, 25, 30])
        num = rng.choice(BOX)

        # Put is only allowed when point is ON; others may be attempted any time.
        choices = [
            lambda: try_add(player, B.Horn(amt)),
            lambda: try_add(player, B.World(amt)),
            lambda: try_add(player, B.Big6(amt)),
            lambda: try_add(player, B.Big8(amt)),
            lambda: try_add(player, B.Buy(num, amt)),
            lambda: try_add(player, B.Lay(num, amt)),
            lambda: try_add(player, B.Put(num, amt)),  # will be blocked if point OFF
        ]
        # Try a few random actions each roll
        for _ in range(rng.randint(1, 3)):
            rng.choice(choices)()
            # Infrequently take odds behind Put if present and point ON
            if table.point == "On":
                for bet in list(player.bets):
                    if isinstance(bet, B.Put):
                        # modest odds amount to avoid bankroll starvation
                        odds_amt = min(amt, max(5.0, player.bankroll * 0.05))
                        try_add(player, B.Odds(B.Put, bet.number, odds_amt, True))
                        break

    return attempt


def invariants_after_roll(
    table: Table,
    pre_bankroll: float,
    point_was_on: bool,
    prior_one_roll_ids: Optional[Set[int]] = None,
):
    """General invariants that should always hold after a roll."""
    p = table.players[0]

    # Bankroll should be finite
    assert isinstance(p.bankroll, (int, float))
    assert math.isfinite(p.bankroll)

    # No duplicate exact objects; type-level uniqueness is enforced by the engine already.
    # Basic repr sanity for all bets
    for b in p.bets:
        r = repr(b)
        assert isinstance(r, str) and len(r) > 0

    # Put legality: while the point is OFF, Put bets should not exist on the layout
    # because they cannot be added and seven-outs resolve any active puts.
    if table.point != "On":
        assert all(not isinstance(b, B.Put) for b in p.bets)

    # One-roll bets (Horn, World) must not persist beyond one resolution.
    if prior_one_roll_ids:
        current_one_roll = {id(b) for b in p.bets if isinstance(b, (B.Horn, B.World))}
        assert prior_one_roll_ids.isdisjoint(current_one_roll)

    # Bankroll continuity: bankroll should only change by resolved results on the roll.
    # We can't recompute exact payoff here without duplicating engine math; ensure no absurd jumps:
    #   - No negative infinity / NaN (covered)
    #   - Avoid massive spikes relative to table limits: if it happens, it's a bug or overflow.
    assert abs(p.bankroll - pre_bankroll) < 1e9  # very loose, just a sanity cap


# --- Quick, deterministic smoke test (always runs) ---------------------------


def test_vxp_randomized_smoke():
    rng = random.Random(1337)

    t = Table()
    t.add_player()
    p = t.players[0]
    p.strategy = NullStrategy()

    attempt = random_bet_mix(rng, bankroll_scale=1.0)

    # Establish point ON early to exercise Put/odds paths
    roll_fixed(t, 6)  # come-out 6 → point ON

    # 200 rolls of randomized betting/rolling
    for _ in range(200):
        pre = p.bankroll
        prior_one_roll = {id(b) for b in p.bets if isinstance(b, (B.Horn, B.World))}

        # Occasionally seven-out to clear board and flip to come-out
        point_was_on = t.point == "On"

        if rng.random() < 0.12:
            roll_fixed(t, 7)
        else:
            # random non-zero roll
            roll_fixed(t, rng.choice([2, 3, 4, 5, 6, 8, 9, 10, 11, 12]))

        invariants_after_roll(t, pre, point_was_on, prior_one_roll)

        # Randomly attempt to add/press bets after roll (like a player acting between rolls)
        attempt(t, p)

    # End smoke: bankroll finite, table consistent
    assert math.isfinite(p.bankroll)


# --- Heavy stress (opt-in via -m stress) -------------------------------------


@pytest.mark.stress
def test_vxp_heavy_stress(require_stress):
    rng = random.Random(424242)

    # Multiple sessions with varied commission policies & seeds
    for sess in range(60):  # sessions
        t = Table()
        t.add_player()
        p = t.players[0]
        p.strategy = NullStrategy()
        # Vary commission policy knobs (mode/rounding/floor) across runs
        t.settings["commission_mode"] = rng.choice(["on_win", "on_bet"])
        t.settings["commission_rounding"] = rng.choice(
            ["none", "ceil_dollar", "nearest_dollar"]
        )
        t.settings["commission_floor"] = rng.choice([0.0, 10.0, 25.0])
        attempt = random_bet_mix(rng, bankroll_scale=rng.choice([0.5, 1.0, 2.0]))

        # Randomly choose to start with point ON or OFF
        if rng.random() < 0.5:
            roll_fixed(t, rng.choice([4, 5, 6, 8, 9, 10]))  # set point ON

        # Occasionally start with very low bankroll to stress rejection paths
        if rng.random() < 0.25:
            p.bankroll = rng.choice([30.0, 40.0, 50.0])

        # Rolls per session
        for _ in range(300):
            pre = p.bankroll
            prior_one_roll = {id(b) for b in p.bets if isinstance(b, (B.Horn, B.World))}

            # Random next roll, 7-outs sprinkled to churn table state
            point_was_on = t.point == "On"

            if rng.random() < 0.18:
                roll_fixed(t, 7)
            else:
                roll_fixed(t, rng.choice([2, 3, 4, 5, 6, 8, 9, 10, 11, 12]))

            invariants_after_roll(t, pre, point_was_on, prior_one_roll)

            # Post-roll random bet attempts
            attempt(t, p)

        # Session ends; bankroll stays finite
        assert math.isfinite(p.bankroll)
