import crapssim.bet
from crapssim.table import Table, TableUpdate


def establish_point(table: Table, point_total: int):
    pair_map = {4: (2, 2), 5: (2, 3), 6: (3, 3), 8: (2, 6), 9: (3, 6), 10: (4, 6)}
    if table.point == "On":
        TableUpdate.roll(table, fixed_outcome=(4, 3))
    TableUpdate.roll(table, fixed_outcome=pair_map[point_total])


def test_put_wins_on_number_and_is_removed():
    t = Table()
    t.add_player()
    p = t.players[0]

    establish_point(t, 6)
    p.add_bet(crapssim.bet.Put(6, 5))

    TableUpdate.roll(t, fixed_outcome=(3, 3))
    assert not any(isinstance(b, crapssim.bet.Put) for b in p.bets)


def test_put_loses_on_seven_and_is_removed():
    t = Table()
    t.add_player()
    p = t.players[0]

    establish_point(t, 6)
    p.add_bet(crapssim.bet.Put(6, 5))

    TableUpdate.roll(t, fixed_outcome=(4, 3))
    assert not any(isinstance(b, crapssim.bet.Put) for b in p.bets)


def test_put_allows_odds_like_come():
    t = Table()
    t.add_player()
    p = t.players[0]

    establish_point(t, 5)
    p.add_bet(crapssim.bet.Put(5, 10))
    p.add_bet(crapssim.bet.Odds(crapssim.bet.Put, 5, 10, True))

    TableUpdate.roll(t, fixed_outcome=(2, 3))
    assert not any(isinstance(b, crapssim.bet.Put) for b in p.bets)
    assert not any(isinstance(b, crapssim.bet.Odds) for b in p.bets)
