import crapssim.bet
from crapssim.strategy.tools import NullStrategy
from crapssim.table import Table, TableUpdate


def test_put_only_allowed_when_point_on():
    t = Table()
    t.add_player(strategy=NullStrategy())
    p = t.players[0]
    starting_bankroll = p.bankroll

    # Come-out roll has point OFF; Put bet should not be accepted.
    p.add_bet(crapssim.bet.Put(6, 10))
    assert not any(isinstance(b, crapssim.bet.Put) for b in p.bets)
    assert p.bankroll == starting_bankroll

    # Establish the point and retry – bet should now be accepted.
    TableUpdate().run(t, dice_outcome=(3, 3))
    p.add_bet(crapssim.bet.Put(6, 10))
    assert any(isinstance(b, crapssim.bet.Put) for b in p.bets)
