from collections import namedtuple

import pytest

from crapssim import Player, Table
from crapssim.bet import PassLine, Odds, Bet, Come, Place, Place6, Place8, Place4
from crapssim.strategy import passline, passline_odds, passline_odds2, passline_odds345, pass2come, place

Roll = namedtuple('Roll', ['bets', 'd1', 'd2'])


@pytest.fixture
def set_table():
    def _set_table(strategy, rolls):
        table = Table()
        player = Player(100, bet_strategy=strategy)
        table.add_player(player)

        for r in rolls:
            for bet in r.bets:
                player.bet(bet, table)

            if r.d1 is not None and r.d2 is not None:
                table.dice.fixed_roll((r.d1, r.d2))
                table._update_player_bets(table.dice)
                table._update_table(table.dice)

        table._add_player_bets()
        return table

    return _set_table


@pytest.fixture
def get_added_bets(set_table):
    def _get_added_bets(strategy, rolls):
        table = set_table(strategy, rolls)
        return table.players[0].bets_on_table

    return _get_added_bets


@pytest.mark.parametrize(['rolls', "correct_bets"], [
    ([], [PassLine(5)]),
    ([Roll([], 4, 4)], []),
    ([Roll([PassLine(5)], None, None)], [PassLine(5)])
])
def test_pass_line(rolls, correct_bets, get_added_bets):
    bets = get_added_bets(passline, rolls)
    assert [(b.name, b.bet_amount) for b in bets] == \
           [(b.name, b.bet_amount) if isinstance(b, Bet) else b for b in correct_bets]


@pytest.mark.parametrize(['mult', 'point', 'correct_amount'], [
    (2, 4, 10),
    (3, 6, 15),
    ('345', 9, 20),
    ('345', 6, 25),
    ('345', 4, 15),
    (10, 4, 50)
]
)
def test_odds(mult, point, correct_amount, get_added_bets):
    def strat(player, table, **strat_info):
        passline_odds(player, table, mult=mult)

    d1, d2 = point_to_dice(point)
    bets = get_added_bets(strat, [Roll([PassLine(5)], d1, d2)])
    assert ('Odds', str(point), correct_amount) in [(x.name, x.subname, x.bet_amount) for x in bets]


def point_to_dice(point):
    d1 = int(point / 2)
    d2 = int(point / 2)
    if point % 2 == 1:
        d1 += 1
    return d1, d2


@pytest.mark.parametrize(['rolls', 'correct_bets'], [
    ([], [PassLine(5)]),
    ([Roll([PassLine(5)], 3, 6)], [PassLine(5), ('Come', '', 5)]),
    ([Roll([PassLine(5)], 4, 4),
      Roll([Come(5)], 3, 3)],
     [PassLine(5), ('Come', '6', 5), ('Come', '', 5)])
])
def test_pass2come(rolls, correct_bets, get_added_bets):
    bets = get_added_bets(pass2come, rolls)
    compare_bets(bets, correct_bets)


def compare_bets(bets, correct_bets):
    assert [(b.name, b.subname, b.bet_amount) for b in bets] == \
           [(b.name, b.subname, b.bet_amount) if isinstance(b, Bet) else b for b in correct_bets]


@pytest.mark.parametrize(['numbers', 'skip_point', 'point', 'correct_bets'], [
    ({6, 8}, False, 4, [Place6(6), Place8(6)]),
    ({4}, True, 4, []),
    ({4}, False, 4, [Place4(5)])
])
def test_place(numbers, skip_point, point, correct_bets, get_added_bets):
    def strat(player, table, **strat_info):
        place(player, table, skip_point=skip_point, numbers=numbers)

    d1, d2 = point_to_dice(point)
    bets = get_added_bets(strat, [Roll([], d1, d2)])
    compare_bets(bets, correct_bets)
