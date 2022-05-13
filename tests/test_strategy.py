from collections import namedtuple

import pytest

from crapssim import Player, Table
from crapssim.bet import Come, LayOdds, DontCome, Place6, Place8, PassLine, Place5, Place9, Field
from crapssim.strategy import BetPassLine, PassLineOdds, TwoCome, Pass2Come, BetPlace, PassLinePlace68, BetDontPass, \
    BetLayOdds, Place682Come, PlaceBetAndMove, PassLinePlace68Move59, IronCross, HammerLock, BetIfTrue, \
    Risk12, Knockout, DiceDoctor, Place68CPR, Place68DontCome2Odds


@pytest.mark.parametrize(['strategy', 'strategy_info', 'rolls', 'correct_bets'], [
    (BetPassLine(5), {}, [], {('PassLine', '', 5)}),
    (BetPassLine(5), {}, [(4, 4)], {('PassLine', '', 5)}),
    (BetPassLine(5) + PassLineOdds(1), {}, [], {('PassLine', '', 5)}),
    (BetPassLine(5) + PassLineOdds(1), {}, [(4, 4)], {('PassLine', '', 5),
                                                      ('Odds8', '', 5)}),
    (BetPassLine(5) + PassLineOdds(1), {}, [(4, 4), (3, 3)], {('PassLine', '', 5),
                                                              ('Odds8', '', 5)}),
    (BetPassLine(5) + PassLineOdds(), {'mult': '345'}, [], {('PassLine', '', 5)}),
    (BetPassLine(5) + PassLineOdds(), {'mult': '345'}, [(6, 4)], {('PassLine', '', 5),
                                                                  ('Odds10', '', 15)}),
    (BetPassLine(5) + PassLineOdds(2), {}, [(2, 2)], {('PassLine', '', 5),
                                                      ('Odds4', '', 10)}),
    (BetPassLine(5) + PassLineOdds({4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}),
     {}, [(3, 4), (3, 3)], {('PassLine', '', 5), ('Odds6', '', 25)}),
    (Pass2Come(5), {}, [], {('PassLine', '', 5)}),
    (Pass2Come(5), {}, [(4, 5)], {('PassLine', '', 5),
                                  ('Come', '', 5)}),
    (Pass2Come(5), {}, [(4, 5), (5, 5)], {('PassLine', '', 5),
                                          ('Come', '10', 5),
                                          ('Come', '', 5)}),
    (Pass2Come(5), {}, [(4, 5), (5, 5), (3, 3)], {('PassLine', '', 5),
                                                  ('Come', '10', 5),
                                                  ('Come', '6', 5)}),
    (BetPlace({4: 5}), {'numbers': {4}, 'skip_point': True}, [], set()),
    (BetPlace({5: 5}), {'numbers': {5}, 'skip_point': True}, [(3, 3)], {('Place5', '', 5)}),
    (BetPlace({5: 5}), {'numbers': {5}, 'skip_point': True}, [(3, 2)], set()),
    (BetPlace({5: 5}, False), {'numbers': {5}, 'skip_point': False}, [(3, 2)], {('Place5', '', 5)}),
    (PassLinePlace68(pass_line_amount=5,
                     six_amount=6,
                     eight_amount=6), {}, [(4, 5)], {('PassLine', '', 5), ('Place6', '', 6),
                                             ('Place8', '', 6)}),
    (PassLinePlace68(pass_line_amount=5,
                     six_amount=6,
                     eight_amount=6), {}, [(2, 4)], {('PassLine', '', 5), ('Place8', '', 6)}),
    (BetDontPass(5), {}, [], {('DontPass', '', 5)}),
    (BetDontPass(5) + BetLayOdds(1), {'win_mult': 1}, [], {('DontPass', '', 5)}),
    (BetDontPass(5) + BetLayOdds(6), {'win_mult': '345'}, [(3, 3)], {('DontPass', '', 5),
                                                                     ('LayOdds6', '', 30)}),
    (PassLinePlace68Move59(), {}, [], {('PassLine', '', 5)}),
    (PassLinePlace68Move59(), {}, [(3, 3)], {('PassLine', '', 5),
                                             ('Place8', '', 6),
                                             ('Place5', '', 5)}),
    (PassLinePlace68Move59(), {}, [(3, 3), (4, 4)], {('PassLine', '', 5),
                                                     ('Place8', '', 6),
                                                     ('Place5', '', 5),
                                                     ('Place9', '', 5)}),
    (Place682Come(), {}, [], set()),
    (Place682Come(), {}, [(3, 3)], {('Place6', '', 6),
                                    ('Place8', '', 6),
                                    ('Come', '', 5)}),
    (Place682Come(), {}, [(3, 3), (3, 6)], {('Place6', '', 6),
                                            ('Place8', '', 6),
                                            ('Come', '9', 5),
                                            ('Come', '', 5)}),
    (Place682Come(), {}, [(3, 3), (4, 4)], {('Place6', '', 6),
                                            ('Place5', '', 5),
                                            ('Come', '8', 5),
                                            ('Come', '', 5)}),
    (IronCross(5), {}, [], {('PassLine', '', 5)}),
    (IronCross(5), {'mult': '2'}, [(4, 4)], {('PassLine', '', 5),
                                             ('Odds8', '', 10),
                                             ('Place5', '', 10),
                                             ('Place6', '', 12),
                                             ('Field', '', 5)}),
    (HammerLock(5), {}, [], {('PassLine', '', 5), ('DontPass', '', 5)}),
    (HammerLock(5), {}, [(3, 3)], {('PassLine', '', 5),
                                   ('DontPass', '', 5),
                                   ('Place6', '', 12),
                                   ('Place8', '', 12),
                                   ('LayOdds6', '', 30)}),
    (HammerLock(5), {}, [(3, 3), (4, 4)], {('PassLine', '', 5),
                                           ('DontPass', '', 5),
                                           ('Place6', '', 6),
                                           ('Place8', '', 6),
                                           ('LayOdds6', '', 30),
                                           ('Place5', '', 5),
                                           ('Place9', '', 5)}),
    (BetIfTrue(PassLine(5), lambda p, t: t.point.status == 'Off'), {}, [], {('PassLine', '', 5)}),
    (Risk12(), {}, [], {('PassLine', '', 5), ('Field', '', 5)}),
    (Risk12(), {}, [(1, 3)], {('PassLine', '', 5),
                              ('Place6', '', 6),
                              ('Place8', '', 6)}),
    (Risk12(), {}, [(5, 6), (2, 3)], {('PassLine', '', 5),
                                      ('Place6', '', 6),
                                      ('Place8', '', 6)}),
    (Knockout(5), {}, [], {('PassLine', '', 5),
                           ('DontPass', '', 5)}),
    (Knockout(5), {}, [(4, 2)], {('PassLine', '', 5),
                                 ('DontPass', '', 5),
                                 ('Odds6', '', 25)}),
    (DiceDoctor(), {}, [], {('Field', '', 10)}),
    (DiceDoctor(), {}, [(1, 1), (5, 6), (5, 5)], {('Field', '', 30)}),
    (Place68DontCome2Odds(), {}, [], set()),
    (Place68DontCome2Odds(), {}, [(4, 4)], {('Place6', '', 6),
                                          ('Place8', '', 6),
                                          ('DontCome', '', 5)}),
    (Place68DontCome2Odds(), {}, [(4, 4), (2, 2)], {('Place6', '', 6),
                                                  ('Place8', '', 6),
                                                  ('DontCome', '4', 5),
                                                  ('LayOdds4', '', 10)}),
    (Place68CPR(), {}, [], set()),
    (Place68CPR(), {}, [(4, 4)], {('Place6', '', 6),
                                  ('Place8', '', 6)}),
    (Place68CPR(), {}, [(2, 2), (4, 4)], {('Place6', '', 6),
                                          ('Place8', '', 12)}),
    (Place68CPR(), {}, [(2, 2), (4, 4), (4, 4)], {('Place6', '', 6),
                                                  ('Place8', '', 6)}),
    (Place68CPR(), {}, [(2, 2), (4, 4), (4, 4), (4, 4)], {('Place6', '', 6),
                                                          ('Place8', '', 12)})
])
def test_strategies_compare_bets(strategy, strategy_info, rolls: list[tuple[int, int]],
                                 correct_bets: {(str, str, float)}):
    table = Table()
    table.add_player(strategy=strategy)
    table.fixed_run(rolls)
    table.add_player_bets(verbose=False)

    bets = table.players[0].bets_on_table

    check_list = []
    for bet in bets:
        if isinstance(bet, (Come, DontCome)) and bet.point is not None:
            subname = str(bet.point)
        else:
            subname = ''
        check_list.append((bet.name, subname, bet.bet_amount))
    assert set(check_list) == correct_bets
