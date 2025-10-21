import crapssim.bet
from crapssim.strategy.tools import NullStrategy
from crapssim.table import Table, TableUpdate


def test_illegal_put_removed_when_point_off():
    t = Table()
    t.add_player(strategy=NullStrategy())
    p = t.players[0]
    starting_bankroll = p.bankroll

    # Point should be OFF by default at table start; force-append an illegal Put.
    p.bets.append(crapssim.bet.Put(6, 10))

    # Run a table update; guard should strip the illegal Put before any roll.
    TableUpdate().run(t, dice_outcome=(1, 1))

    # Bet is removed and bankroll unchanged (because manual append never debited bankroll)
    assert not any(isinstance(b, crapssim.bet.Put) for b in p.bets)
    assert p.bankroll == starting_bankroll
