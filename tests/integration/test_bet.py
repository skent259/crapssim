from itertools import combinations

import pytest

from crapssim import Dice, Table
from crapssim.bet import (
    All,
    Any7,
    AnyCraps,
    Boxcars,
    CAndE,
    Come,
    DontCome,
    DontPass,
    Field,
    Fire,
    HardWay,
    Odds,
    PassLine,
    Place,
    Small,
    Tall,
    Three,
    Two,
    Yo,
)
from crapssim.point import Point
from crapssim.strategy.odds import ComeOddsMultiplier
from crapssim.strategy.single_bet import BetCome, BetPassLine
from crapssim.strategy.tools import NullStrategy
from crapssim.table import TableUpdate

ALL_BETS = [
    PassLine(5),
    Come(5),
    Odds(PassLine, 4, 5),
    Odds(PassLine, 5, 5),
    Odds(PassLine, 6, 5),
    Odds(PassLine, 8, 5),
    Odds(PassLine, 9, 5),
    Odds(PassLine, 10, 5),
    Odds(Come, 4, 5),
    Odds(Come, 5, 5),
    Odds(Come, 6, 5),
    Odds(Come, 8, 5),
    Odds(Come, 9, 5),
    Odds(Come, 10, 5),
    Place(4, 5),
    Place(5, 5),
    Place(6, 5),
    Place(8, 5),
    Place(9, 5),
    Place(10, 5),
    Field(5),
    DontPass(5),
    DontCome(5),
    Odds(DontPass, 4, 5),
    Odds(DontPass, 5, 5),
    Odds(DontPass, 6, 5),
    Odds(DontPass, 8, 5),
    Odds(DontPass, 9, 5),
    Odds(DontPass, 10, 5),
    Odds(DontCome, 4, 5),
    Odds(DontCome, 5, 5),
    Odds(DontCome, 6, 5),
    Odds(DontCome, 8, 5),
    Odds(DontCome, 9, 5),
    Odds(DontCome, 10, 5),
    Any7(5),
    Two(5),
    Three(5),
    Yo(5),
    Boxcars(5),
    AnyCraps(5),
    CAndE(5),
    HardWay(4, 5),
    HardWay(6, 5),
    HardWay(8, 5),
    HardWay(10, 5),
    Fire(5),
    All(5),
    Small(5),
    Tall(5),
]


@pytest.mark.parametrize("bet_one, bet_two", [(x, x) for x in ALL_BETS])
def test_bet_equality2(bet_one, bet_two):
    assert bet_one == bet_two


@pytest.mark.parametrize("bet_one, bet_two", [x for x in combinations(ALL_BETS, r=2)])
def test_bet_type_inequality(bet_one, bet_two):
    assert bet_one != bet_two


@pytest.mark.parametrize(
    "bet_one, bet_two",
    [
        (PassLine(10), PassLine(15)),
        (Come(25), Come(10)),
        (Odds(PassLine, 4, 5), Odds(PassLine, 4, 20)),
        (Odds(PassLine, 5, 10), Odds(PassLine, 5, 25)),
        (Odds(PassLine, 6, 25), Odds(PassLine, 6, 10)),
        (Odds(PassLine, 8, 20), Odds(PassLine, 8, 30)),
        (Odds(PassLine, 9, 15), Odds(PassLine, 9, 5)),
        (Odds(PassLine, 10, 20), Odds(PassLine, 10, 5)),
        (Place(4, 10), Place(4, 30)),
        (Place(5, 30), Place(5, 10)),
        (Place(6, 25), Place(6, 20)),
        (Place(8, 30), Place(8, 15)),
        (Place(9, 15), Place(9, 25)),
        (Place(10, 5), Place(10, 10)),
        (Field(30), Field(5)),
        (DontPass(20), DontPass(5)),
        (DontCome(15), DontCome(25)),
        (Odds(DontPass, 4, 10), Odds(DontPass, 4, 25)),
        (Odds(DontPass, 5, 10), Odds(DontPass, 5, 15)),
        (Odds(DontPass, 6, 30), Odds(DontPass, 6, 5)),
        (Odds(DontPass, 8, 30), Odds(DontPass, 8, 10)),
        (Odds(DontPass, 9, 5), Odds(DontPass, 9, 10)),
        (Odds(DontPass, 10, 10), Odds(DontPass, 10, 30)),
        (Any7(30), Any7(25)),
        (Two(20), Two(25)),
        (Three(10), Three(25)),
        (Yo(30), Yo(10)),
        (Boxcars(30), Boxcars(10)),
        (AnyCraps(25), AnyCraps(15)),
        (CAndE(5), CAndE(25)),
        (HardWay(4, 25), HardWay(4, 10)),
        (HardWay(6, 15), HardWay(6, 25)),
        (HardWay(8, 15), HardWay(8, 5)),
        (HardWay(10, 20), HardWay(10, 5)),
        (Fire(20), Fire(30)),
        (All(2), All(7)),
        (Small(5), Small(10)),
        (Tall(5), Tall(30)),
    ],
)
def test_bet_amount_inequality(bet_one, bet_two):
    assert bet_one != bet_two


@pytest.mark.parametrize(
    "bet",
    [
        PassLine(5),
        Odds(PassLine, 4, 5),
        Odds(PassLine, 5, 5),
        Odds(PassLine, 6, 5),
        Odds(PassLine, 8, 5),
        Odds(PassLine, 9, 5),
        Odds(PassLine, 10, 5),
        Place(4, 5),
        Place(5, 5),
        Place(6, 6),
        Place(8, 8),
        Place(9, 9),
        Place(10, 10),
        Odds(DontPass, 4, 5),
        Odds(DontPass, 5, 5),
        Odds(DontPass, 6, 5),
        Odds(DontPass, 8, 5),
        Odds(DontPass, 9, 5),
        Odds(DontPass, 10, 5),
        Field(5),
        DontPass(5),
        DontCome(5),
        Any7(5),
        Two(5),
        Three(5),
        Yo(5),
        Boxcars(5),
        AnyCraps(5),
        HardWay(4, 5),
        HardWay(6, 5),
        HardWay(8, 5),
        HardWay(10, 5),
    ],
)
def test_is_removable_table_point_off(bet):
    table = Table()
    assert bet.is_removable(table) is True


@pytest.mark.parametrize(
    "bet",
    [
        Odds(PassLine, 4, 5),
        Odds(PassLine, 5, 5),
        Odds(PassLine, 6, 5),
        Odds(PassLine, 8, 5),
        Odds(PassLine, 9, 5),
        Odds(PassLine, 10, 5),
        Place(4, 5),
        Place(5, 5),
        Place(6, 6),
        Place(8, 8),
        Place(9, 9),
        Place(10, 10),
        Odds(DontPass, 4, 5),
        Odds(DontPass, 5, 5),
        Odds(DontPass, 6, 5),
        Odds(DontPass, 8, 5),
        Odds(DontPass, 9, 5),
        Odds(DontPass, 10, 5),
        Field(5),
        DontPass(5),
        DontCome(5),
        Any7(5),
        Two(5),
        Three(5),
        Yo(5),
        Boxcars(5),
        AnyCraps(5),
        HardWay(4, 5),
        HardWay(6, 5),
        HardWay(8, 5),
        HardWay(10, 5),
    ],
)
def test_is_removable_table_point_on(bet):
    table = Table()
    table.point.number = 6
    assert bet.is_removable(table) is True


@pytest.mark.parametrize(
    "bet, new_shooter, is_removable",
    [
        (Fire(5), True, True),
        (Fire(5), False, False),
        (All(5), True, True),
        (All(5), False, False),
        (Tall(5), True, True),
        (Tall(5), False, False),
        (Small(5), True, True),
        (Small(5), False, False),
    ],
)
def test_bet_is_removable_new_shooter(bet, new_shooter, is_removable):
    table = Table()
    table.new_shooter = new_shooter

    assert bet.is_removable(table) == is_removable


@pytest.mark.parametrize(
    "dice1, dice2, correct_ratio",
    [(1, 1, 2), (1, 2, 1), (2, 2, 1), (5, 4, 1), (5, 5, 1), (6, 5, 1), (6, 6, 2)],
)
def test_get_field_default_table_payout_ratio(dice1, dice2, correct_ratio):
    table = Table()
    table.dice.fixed_roll((dice1, dice2))
    assert Field(5).get_payout_ratio(table) == correct_ratio


@pytest.mark.parametrize(
    "dice1, dice2, correct_ratio",
    [(1, 1, 2), (1, 2, 14), (2, 2, 14000), (5, 4, 1), (5, 5, 1), (6, 5, 1), (6, 6, 3)],
)
def test_get_field_non_default_table_payout_ratio(dice1, dice2, correct_ratio):
    table = Table()
    table.settings["field_payouts"].update({3: 14, 12: 3, 4: 14000})
    table.dice.fixed_roll((dice1, dice2))
    assert Field(5).get_payout_ratio(table) == correct_ratio


@pytest.mark.parametrize(
    "points_made, correct_ratio",
    [
        ({4, 5, 6, 9}, 24),
        ({4, 5, 6, 9, 10}, 249),
        ({4, 5, 6, 8, 9, 10}, 999),
    ],
)
def test_get_fire_default_table_payout_ratio(points_made, correct_ratio):
    table = Table()
    bet = Fire(1)
    table.point.number = 8
    table.dice.result = [3, 4]  # 7-out
    bet.points_made = points_made

    ratio = (bet.get_result(table).amount - bet.amount) / bet.amount
    assert ratio == correct_ratio


@pytest.mark.parametrize(
    "points_made, correct_ratio",
    [
        ({4, 5, 6}, 6),
        ({4, 5, 6, 9}, 9),
        ({4, 5, 6, 9, 10}, 69),
        ({4, 5, 6, 8, 9, 10}, 420),
    ],
)
def test_get_fire_non_default_table_payout_ratio(points_made, correct_ratio):
    table = Table()
    table.settings["fire_payouts"] = {3: 6, 4: 9, 5: 69, 6: 420}
    bet = Fire(1)
    table.point.number = 8
    table.dice.result = [3, 4]  # 7-out
    bet.points_made = points_made

    ratio = (bet.get_result(table).amount - bet.amount) / bet.amount
    assert ratio == correct_ratio


# fmt: off
@pytest.mark.parametrize(
    'rolls, correct_bankroll_change, correct_value_change, correct_exists', 
    [
        (
            [(6, 1)], 
            -1, 0, True
        ),
        (
            [(2, 2), (3, 1), (4, 3), (6, 6)], 
            -1, 0, True
        ),
        (
            [(2, 2), (4, 3)], 
            -1, -1, False
        ),
        (
            [(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), 
             (5, 5)],
            -1, 0, True,
        ),
        (
            [(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), 
             (5, 5), (5, 5), (5, 5)],
            -1, 0, True,
        ),
        (
            [(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), 
             (5, 5), (5, 5), (3, 4)],
            24, 24, False
        ),
        (
            [(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), 
             (5, 5), (2, 3), (2, 3)],
            -1, 0, True,
        ),
        (
            [(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), 
             (5, 5), (2, 3), (2, 3), (5, 4)],
            -1, 0, True
        ),
        (
            [(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), 
             (5, 5), (2, 3), (2, 3), (4, 4), (3, 4)],
            249, 249, False
        ),
        (
            [(2, 2), (2, 2), (2, 3), (3, 2), (3, 3), (3, 3), (4, 4), (4, 4), 
             (4, 5), (5, 4), (5, 5), (5, 5)],
            999, 999, False
        ),
    ]
)
# fmt: on
def test_fire_on_table(
    rolls: list[tuple[int]],
    correct_bankroll_change: float,
    correct_value_change: float,
    correct_exists: bool,
):

    table = Table()
    start_bankroll = 100
    table.add_player(bankroll=start_bankroll, strategy=NullStrategy())
    player = table.players[0]
    player.add_bet(Fire(1))

    table.fixed_run(rolls, verbose=True)

    bankroll_change = player.bankroll - start_bankroll
    value_change = player.bankroll + player.total_bet_amount - start_bankroll
    exists = player.has_bets(Fire)

    assert (bankroll_change, value_change, exists) == (
        correct_bankroll_change,
        correct_value_change,
        correct_exists,
    )


@pytest.mark.parametrize(
    "bet, point_number, is_allowed",
    [
        (PassLine(5), None, True),
        (PassLine(5), 6, False),
        (Come(5), None, False),
        (Come(5), 6, True),
        (DontPass(5), None, True),
        (DontPass(5), 4, False),
        (DontCome(5), None, False),
        (DontCome(5), 8, True),
        (Field(5), None, True),
        (Field(5), 4, True),
    ],
)
def test_bet_is_allowed_point(bet, point_number, is_allowed):
    table = Table()
    table.add_player()
    dice = Dice()
    if point_number is None:
        dice.result = None
    else:
        dice.result = [point_number // 2, point_number - point_number // 2]
    # dice.total = point_number

    point = Point()
    point.update(dice)

    table.point = point

    assert bet.is_allowed(player=table.players[0]) == is_allowed


@pytest.mark.parametrize(
    "bet, new_shooter, is_allowed",
    [
        (Field(5), True, True),
        (Field(5), False, True),
        (Fire(5), True, True),
        (Fire(5), False, False),
        (All(5), True, True),
        (All(5), False, False),
        (Tall(5), True, True),
        (Tall(5), False, False),
        (Small(5), True, True),
        (Small(5), False, False),
    ],
)
def test_bet_is_allowed_new_shooter(bet, new_shooter, is_allowed):
    table = Table()
    table.add_player()

    table.new_shooter = new_shooter

    assert bet.is_allowed(player=table.players[0]) == is_allowed


@pytest.mark.parametrize(
    "bet",
    [
        PassLine(5),
        Place(4, 5),
        Place(5, 5),
        Place(6, 5),
        Place(8, 5),
        Place(9, 5),
        Place(10, 5),
        DontPass(5),
        Field(5),
        Any7(5),
        Two(5),
        Three(5),
        Yo(5),
        Boxcars(5),
        AnyCraps(5),
        HardWay(4, 5),
        HardWay(6, 5),
        HardWay(8, 5),
        HardWay(10, 5),
    ],
)
def test_bets_always_is_allowed_point_off(bet):
    table = Table()
    table.add_player()
    assert bet.is_allowed(table.players[0])


@pytest.mark.parametrize(
    "bet",
    [
        Come(5),
        Place(4, 5),
        Place(5, 5),
        Place(6, 5),
        Place(8, 5),
        Place(9, 5),
        Place(10, 5),
        DontCome(5),
        Field(5),
        Any7(5),
        Two(5),
        Three(5),
        Yo(5),
        Boxcars(5),
        AnyCraps(5),
        HardWay(4, 5),
        HardWay(6, 5),
        HardWay(8, 5),
        HardWay(10, 5),
    ],
)
def test_bets_always_is_allowed_point_on(bet):
    table = Table()
    table.point.number = 10
    table.add_player()
    assert bet.is_allowed(table.players[0])


# fmt: off
@pytest.mark.parametrize('rolls, correct_bankroll_change, correct_value_change, correct_exists', [
    (
        [(2, 2)], 
        -1, 0, True
    ),
    (
        [(10, 1), (10, 2), (7, 2), (5, 5), (2, 6), (1, 1), 
         (1, 2), (2, 2), (2, 3), (3, 3)], 
        150, 150, False
    ),
    (
        [(10, 1), (10, 2), (7, 2), (5, 5), (2, 6), (1, 1), 
         (1, 2), (2, 2), (2, 3)], 
        -1, 0, True
    ),
    (
        [(1, 1), (1, 2), (2, 2), (2, 3), (3, 4)], 
        -1, -1, False
    )
])
# fmt: on
def test_all_on_table(
    rolls: list[tuple[int]],
    correct_bankroll_change: float,
    correct_value_change: float,
    correct_exists: bool,
):

    table = Table()
    start_bankroll = 100
    table.add_player(bankroll=start_bankroll, strategy=NullStrategy())
    player = table.players[0]
    player.add_bet(All(1))

    table.fixed_run(rolls, verbose=True)

    bankroll_change = player.bankroll - start_bankroll
    value_change = player.bankroll + player.total_bet_amount - start_bankroll
    exists = player.has_bets(All)

    assert (bankroll_change, value_change, exists) == (
        correct_bankroll_change,
        correct_value_change,
        correct_exists,
    )


# fmt: off
@pytest.mark.parametrize('rolls, correct_bankroll_change, correct_value_change, correct_exists', [
    (
        [(5, 6)], 
        10, 10, False
    ),
    (
        [(3, 3)], 
        -10, 0, True
    ),
])
# fmt: on
def test_passline_on_table(
    rolls: list[tuple[int]],
    correct_bankroll_change: float,
    correct_value_change: float,
    correct_exists: bool,
):

    table = Table()
    start_bankroll = 100
    table.add_player(bankroll=start_bankroll, strategy=NullStrategy())
    player = table.players[0]
    player.add_bet(PassLine(10))

    table.fixed_run(rolls, verbose=True)

    bankroll_change = player.bankroll - start_bankroll
    value_change = player.bankroll + player.total_bet_amount - start_bankroll
    exists = player.has_bets(PassLine)

    assert (bankroll_change, value_change, exists) == (
        correct_bankroll_change,
        correct_value_change,
        correct_exists,
    )


@pytest.mark.parametrize(
    "rolls, correct_bankroll_change, correct_value_change, correct_exists",
    [
        ([(6, 6)], 0, 0, False),
        ([(1, 1)], 10, 10, False),
        ([(3, 3)], -10, 0, True),
        ([(3, 4)], -10, -10, False),
    ],
)
# fmt: on
def test_dontpass_on_table(
    rolls: list[tuple[int]],
    correct_bankroll_change: float,
    correct_value_change: float,
    correct_exists: bool,
):

    table = Table()
    start_bankroll = 100
    table.add_player(bankroll=start_bankroll, strategy=NullStrategy())
    player = table.players[0]
    player.add_bet(DontPass(10))

    table.fixed_run(rolls, verbose=True)

    bankroll_change = player.bankroll - start_bankroll
    value_change = player.bankroll + player.total_bet_amount - start_bankroll
    exists = player.has_bets(DontPass)

    assert (bankroll_change, value_change, exists) == (
        correct_bankroll_change,
        correct_value_change,
        correct_exists,
    )


# fmt: off
@pytest.mark.parametrize('rolls, correct_bankroll_change, correct_value_change, correct_exists', [
    (
        [(2, 2)], 
        -1, 0, True
    ),
    (
        [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3)], 
        -1, 0, True
    ),
    (
        [(10, 1), (10, 2), (7, 2), (5, 5), (2, 6)], 
        30, 30, False
    ),
    (
        [(10, 1), (10, 2), (7, 2), (5, 5), (3, 4)], 
        -1, -1, False
    ),
    (
        [(10, 1), (10, 2), (7, 2), (5, 5)], 
        -1, 0, True
    ),
])
# fmt: on
def test_tall_on_table(
    rolls: list[tuple[int]],
    correct_bankroll_change: float,
    correct_value_change: float,
    correct_exists: bool,
):

    table = Table()
    start_bankroll = 100
    table.add_player(bankroll=start_bankroll, strategy=NullStrategy())
    player = table.players[0]
    player.add_bet(Tall(1))

    table.fixed_run(rolls, verbose=True)

    bankroll_change = player.bankroll - start_bankroll
    value_change = player.bankroll + player.total_bet_amount - start_bankroll
    exists = player.has_bets(Tall)

    assert (bankroll_change, value_change, exists) == (
        correct_bankroll_change,
        correct_value_change,
        correct_exists,
    )


# fmt: off
@pytest.mark.parametrize('rolls, correct_bankroll_change, correct_value_change, correct_exists', [
    (
        [(2, 2)], 
        -1, 0, True
    ),
    (
        [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3)], 
        30, 30, False
    ),
    (
        [(10, 1), (10, 2), (7, 2), (5, 5), (2, 6)], 
        -1, 0, True
    ),
    (
        [(1, 1), (1, 2), (2, 2), (2, 3), (3, 4)], 
        -1, -1, False
    ),
    (
        [(1, 1), (1, 2), (2, 2), (2, 3)], 
        -1, 0, True
    ),
])
# fmt: on
def test_small_on_table(
    rolls: list[tuple[int]],
    correct_bankroll_change: float,
    correct_value_change: float,
    correct_exists: bool,
):

    table = Table()
    start_bankroll = 100
    table.add_player(bankroll=start_bankroll, strategy=NullStrategy())
    player = table.players[0]
    player.add_bet(Small(1))

    table.fixed_run(rolls, verbose=True)

    bankroll_change = player.bankroll - start_bankroll
    value_change = player.bankroll + player.total_bet_amount - start_bankroll
    exists = player.has_bets(Small)

    assert (bankroll_change, value_change, exists) == (
        correct_bankroll_change,
        correct_value_change,
        correct_exists,
    )


@pytest.mark.parametrize(
    "ATS_payouts, bet, rolled_numbers, correct_ratio",
    [
        (
            {"all": 150, "tall": 30, "small": 30},
            All(1),
            [2, 3, 4, 5, 6, 8, 9, 10, 11, 12],
            150,
        ),
        (
            {"all": 150, "tall": 30, "small": 30},
            All(5),
            [2, 3, 4, 5, 6, 8, 9, 10, 11, 12],
            150,
        ),
        (
            {"all": 150, "tall": 30, "small": 30},
            Tall(1),
            [8, 9, 10, 11, 12],
            30,
        ),
        (
            {"all": 150, "tall": 30, "small": 30},
            Small(5),
            [2, 3, 4, 5, 6],
            30,
        ),
        (
            {"all": 174, "tall": 34, "small": 34},
            All(1),
            [2, 3, 4, 5, 6, 8, 9, 10, 11, 12],
            174,
        ),
        (
            {"all": 174, "tall": 34, "small": 34},
            Tall(5),
            [8, 9, 10, 11, 12],
            34,
        ),
        (
            {"all": 174, "tall": 34, "small": 34},
            Small(1),
            [2, 3, 4, 5, 6],
            34,
        ),
    ],
)
def test_all_tall_small_table_payout_ratio(
    ATS_payouts, bet, rolled_numbers, correct_ratio
):
    table = Table()
    table.settings["ATS_payouts"] = ATS_payouts
    bet.rolled_numbers = set(rolled_numbers)

    ratio = (bet.get_result(table).amount - bet.amount) / bet.amount
    assert ratio == correct_ratio


def test_all_tall_small_allowed_after_comeout_seven():
    table = Table()
    table.add_player(strategy=NullStrategy())
    player = table.players[0]
    player.add_bet(All(1))

    rolls = [(1, 2), (3, 4)]
    table.fixed_run(rolls, verbose=True)

    for bet in [All(1), Small(1), Tall(1)]:
        assert bet.is_allowed(player)
        assert bet.is_removable(table)

    player.add_bet(All(1))
    rolls = [(2, 2)]
    table.fixed_run(rolls, verbose=True)

    assert player.has_bets(All)
    for bet in [All(1), Small(1), Tall(1)]:
        assert not bet.is_allowed(player)
        assert not bet.is_removable(table)


def test_odds_inactive_when_point_off_unless_always_working():

    table = Table()
    strat1 = BetPassLine(10) + BetCome(10) + ComeOddsMultiplier()
    strat2 = BetPassLine(10) + BetCome(10) + ComeOddsMultiplier(always_working=True)

    table.add_player(bankroll=200, strategy=strat1)
    table.add_player(bankroll=200, strategy=strat2)
    table.fixed_run(
        dice_outcomes=[(5, 5), (5, 1), (5, 5), (5, 2), (3, 3)], verbose=True
    )

    assert table.players[0].bankroll == 190
    assert table.players[1].bankroll == 110
