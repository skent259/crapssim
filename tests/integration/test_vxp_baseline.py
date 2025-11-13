import pytest

import crapssim.bet
from crapssim.strategy.tools import NullStrategy
from crapssim.table import Table, TableUpdate


def test_vxp_full_integration():
    """
    Integration baseline verifying all new CrapsSim-Vanilla Expansion bets:
    Horn, World, Big6, Big8, Buy, Lay, Put.
    """
    table = Table()
    table.add_player(strategy=NullStrategy())

    table_update = TableUpdate()
    player = table.players[0]
    starting_bankroll = player.bankroll

    def do_roll(outcome: tuple[int, int]):
        table_update.run(table, dice_outcome=outcome, verbose=False)

    # --- Horn & World (one-roll) ---
    player.add_bet(crapssim.bet.Horn(4))
    player.add_bet(crapssim.bet.World(5))
    do_roll((1, 1))  # total = 2 → Horn + World hit

    # --- Big6 / Big8 (persistence then resolve) ---
    player.add_bet(crapssim.bet.Big6(10))
    player.add_bet(crapssim.bet.Big8(10))
    do_roll((3, 3))  # total = 6 → Big6 wins
    do_roll((4, 4))  # total = 8 → Big8 wins

    # --- Buy / Lay (commission check) ---
    player.add_bet(crapssim.bet.Buy(4, 20))
    player.add_bet(crapssim.bet.Lay(10, 20))
    do_roll((2, 2))  # 4 → Buy hit (commission applied)
    do_roll((4, 3))  # 7 → Lay hit (commission applied)

    # --- Put (point ON only) ---
    # Establish point ON at 6 then Put and resolve.
    do_roll((3, 3))  # come-out 6 → point ON
    player.add_bet(crapssim.bet.Put(6, 10))
    do_roll((3, 3))  # 6 → Put wins

    # Sanity — no remaining bets after resolutions.
    assert not player.bets, "All bets should be resolved"

    # Bankroll continuity — ensure deterministic ending bankroll.
    expected_final_bankroll = pytest.approx(231.0, rel=1e-9, abs=1e-9)
    assert player.bankroll == expected_final_bankroll

    # Net profit should equal bankroll delta.
    assert player.bankroll - starting_bankroll == pytest.approx(
        131.0, rel=1e-9, abs=1e-9
    )
