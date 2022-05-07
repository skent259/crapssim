from collections import namedtuple

import pytest

from crapssim import Player, Table
from crapssim.strategy import passline, passline_odds, passline_odds2, passline_odds345, pass2come, place, place68, \
    dontpass, layodds, place68_2come, ironcross, hammerlock, risk12, knockout, dicedoctor, place68_dontcome2odds


@pytest.mark.parametrize(['strategy', 'strategy_info', 'rolls', 'correct_bets'], [
    (passline, {}, [], {('PassLine', '', 5)}),
    (passline, {}, [(4, 4)], {('PassLine', '', 5)}),
    (passline_odds, {}, [], {('PassLine', '', 5)}),
    (passline_odds, {}, [(4, 4)], {('PassLine', '', 5),
                                   ('Odds', '8', 5)}),
    (passline_odds, {}, [(4, 4), (3, 3)], {('PassLine', '', 5),
                                           ('Odds', '8', 5)}),
    (passline_odds, {'mult': '345'}, [], {('PassLine', '', 5)}),
    (passline_odds, {'mult': '345'}, [(6, 4)], {('PassLine', '', 5),
                                                ('Odds', '10', 15)}),
    (passline_odds2, {}, [(2, 2)], {('PassLine', '', 5),
                                    ('Odds', '4', 10)}),
    (passline_odds345, {}, [(3, 4), (3, 3)], {('PassLine', '', 5),
                                              ('Odds', '6', 25)}),
    (pass2come, {}, [], {('PassLine', '', 5)}),
    (pass2come, {}, [(4, 5)], {('PassLine', '', 5),
                               ('Come', '', 5)}),
    (pass2come, {}, [(4, 5), (5, 5)], {('PassLine', '', 5),
                                       ('Come', '10', 5),
                                       ('Come', '', 5)}),
    (pass2come, {}, [(4, 5), (5, 5), (3, 3)], {('PassLine', '', 5),
                                               ('Come', '10', 5),
                                               ('Come', '6', 5)}),
    (place, {'numbers': {4}, 'skip_point': True}, [], set()),
    (place, {'numbers': {5}, 'skip_point': True}, [(3, 3)], {('Place5', '', 5)}),
    (place, {'numbers': {5}, 'skip_point': True}, [(3, 2)], set()),
    (place, {'numbers': {5}, 'skip_point': False}, [(3, 2)], {('Place5', '', 5)}),
    (place68, {}, [(4, 5)], {('PassLine', '', 5), ('Place6', '', 6),
                             ('Place8', '', 6)}),
    (place68, {}, [(2, 4)], {('PassLine', '', 5),
                             ('Place8', '', 6)}),
    (dontpass, {}, [], {('DontPass', '', 5)}),
    (layodds, {'win_mult': 1}, [], {('DontPass', '', 5)}),
    (layodds, {'win_mult': '345'}, [(3, 3)], {('DontPass', '', 5),
                                              ('LayOdds', '6', 30)}),
    (place68_2come, {}, [], set()),
    (place68_2come, {}, [(3, 3)], {('Place6', '', 6),
                                   ('Place8', '', 6),
                                   ('Come', '', 5)}),
    (place68_2come, {}, [(3, 3), (3, 6)], {('Place6', '', 6),
                                           ('Place8', '', 6),
                                           ('Come', '9', 5),
                                           ('Come', '', 5)}),
    (place68_2come, {}, [(3, 3), (4, 4)], {('Place6', '', 6),
                                           ('Place5', '', 5),
                                           ('Come', '8', 5),
                                           ('Come', '', 5)}),
    (ironcross, {}, [], {('PassLine', '', 5)}),
    (ironcross, {'mult': '2'}, [(4, 4)], {('PassLine', '', 5),
                                          ('Odds', '8', 10),
                                          ('Place5', '', 5),
                                          ('Place6', '', 6),
                                          ('Field', '', 5)}),
    (hammerlock, {}, [], {('PassLine', '', 5), ('DontPass', '', 5)}),
    (hammerlock, {}, [(3, 3)], {('PassLine', '', 5),
                                ('DontPass', '', 5),
                                ('Place6', '', 6),
                                ('Place8', '', 6),
                                ('LayOdds', '6', 30)}),
    (hammerlock, {}, [(3, 3), (4, 4)], {('PassLine', '', 5),
                                        ('DontPass', '', 5),
                                        ('Place6', '', 6),
                                        ('Place8', '', 6),
                                        ('LayOdds', '6', 30),
                                        ('Place5', '', 5),
                                        ('Place9', '', 5)}),
    (risk12, {}, [], {('PassLine', '', 5), ('Field', '', 5)}),
    (risk12, {}, [(1, 3)], {('PassLine', '', 5),
                            ('Place6', '', 6),
                            ('Place8', '', 6)}),
    (risk12, {}, [(5, 6), (2, 3)], {('PassLine', '', 5),
                                    ('Place6', '', 6),
                                    ('Place8', '', 6)}),
    (knockout, {}, [], {('PassLine', '', 5),
                        ('DontPass', '', 5)}),
    (knockout, {}, [(4, 2)], {('PassLine', '', 5),
                              ('DontPass', '', 5),
                              ('Odds', '6', 25)}),
    (dicedoctor, {}, [], {('Field', '', 10)}),
    (dicedoctor, {}, [(1, 1), (5, 6), (5, 5)], {('Field', '', 30)}),
    (place68_dontcome2odds, {}, [], set()),
    (place68_dontcome2odds, {}, [(4, 4)], {('Place6', '', 6),
                                           ('Place8', '', 6),
                                           ('DontCome', '', 5)}),
    (place68_dontcome2odds, {}, [(4, 4), (2, 2)], {('Place6', '', 6),
                                                   ('Place8', '', 6),
                                                   ('DontCome', '4', 5),
                                                   ('LayOdds', '4', 20)})
])
def test_strategies_compare_bets(strategy, strategy_info, rolls: list[tuple[int, int]],
                                 correct_bets: {(str, str, float)}):
    def strat(player, table, **strat_info):
        if strat_info != {}:
            return strategy(player, table, **strat_info)
        return strategy(player, table, **strategy_info)

    table = Table()
    player = Player(100, bet_strategy=strat)
    table.add_player(player)

    table.fixed_run(rolls)
    table.add_player_bets(verbose=False)

    bets = table.players[0].bets_on_table

    assert {(b.name, b.subname, b.bet_amount) for b in bets} == correct_bets
