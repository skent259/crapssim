from itertools import combinations

import pytest

from crapssim import Dice, Table
from crapssim.bet import (
    All,
    Any7,
    AnyCraps,
    Buy,
    Boxcars,
    CAndE,
    Come,
    DontCome,
    DontPass,
    Field,
    Fire,
    HardWay,
    Lay,
    Odds,
    PassLine,
    Place,
    Put,
    Small,
    Tall,
    Three,
    Two,
    Yo,
)
from crapssim.point import Point
from crapssim.rules import ClassicRules, CraplessRules
from crapssim.strategy.odds import ComeOddsMultiplier
from crapssim.strategy.single_bet import BetCome, BetPassLine
from crapssim.strategy.tools import NullStrategy

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
    [
        (1, 1, 2),
        (1, 2, 1),
        (2, 2, 1),
        (5, 4, 1),
        (5, 5, 1),
        (6, 5, 1),
        (6, 6, 2),
        (3, 3, 0),
    ],
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


def test_come_out_policy_changes_place_buy_lay_resolution():
    legacy = Table()
    legacy.settings["vig_paid_on_win"] = True
    legacy.settings["come_out_working_policy"] = "legacy"
    real_casino = Table()
    real_casino.settings["come_out_working_policy"] = "real_casino"
    real_casino.settings["vig_paid_on_win"] = True

    for table in (legacy, real_casino):
        player = table.add_player(bankroll=200, strategy=NullStrategy())
        player.add_bet(Place(6, 12))
        player.add_bet(Buy(4, 10))
        player.add_bet(Lay(5, 12))
        table.fixed_run(dice_outcomes=[(4, 3)], verbose=True)

    assert legacy.players[0].bankroll == 186.0
    assert legacy.players[0].has_bets(Place) is False
    assert legacy.players[0].has_bets(Buy) is False
    assert legacy.players[0].has_bets(Lay) is False
    assert legacy.players[0].total_bet_amount == 0.0
    assert real_casino.players[0].bankroll == 166.0
    assert real_casino.players[0].has_bets(Place) is True
    assert real_casino.players[0].has_bets(Buy) is True
    assert real_casino.players[0].has_bets(Lay) is True
    assert real_casino.players[0].total_bet_amount == 34.0


@pytest.mark.parametrize(
    "policy, expected_bankroll",
    [
        ("legacy", 206.66666666666666),
        ("real_casino", 206.66666666666666),
    ],
)
def test_policy_changes_traveled_come_dontcome_and_odds_on_come_out(
    policy, expected_bankroll
):
    table = Table()
    table.settings["come_out_working_policy"] = policy
    table.add_player(bankroll=200, strategy=NullStrategy())
    player = table.players[0]

    table.point.number = 4
    player.add_bet(Come(10, 6))
    player.add_bet(DontCome(10, 5))
    player.add_bet(Odds(Come, 6, 10))
    player.add_bet(Odds(DontCome, 5, 10))

    # Roll point then a come-out 7 for policy-sensitive bet resolution.
    table.fixed_run(dice_outcomes=[(2, 2), (3, 4)], verbose=True)

    assert player.bankroll == pytest.approx(expected_bankroll)
    assert len(player.bets) == 0


@pytest.mark.parametrize(
    "rules, number, roll, bet_type",
    [
        (ClassicRules(), 4, (2, 2), Place),
        (ClassicRules(), 4, (2, 2), Buy),
        (CraplessRules(), 2, (1, 1), Place),
        (CraplessRules(), 2, (1, 1), Buy),
    ],
)
def test_real_casino_policy_keeps_place_and_buy_inactive_on_come_out(
    rules, number, roll, bet_type
):
    table = Table(rules=rules)
    table.settings["come_out_working_policy"] = "real_casino"
    table.settings["vig_paid_on_win"] = True
    table.add_player(bankroll=100, strategy=NullStrategy())
    player = table.players[0]

    player.add_bet(bet_type(number, 10))
    table.fixed_run([roll], verbose=True)

    assert player.bankroll == pytest.approx(90)
    assert len(player.bets) == 1


@pytest.mark.parametrize("rules", [ClassicRules(), CraplessRules()])
def test_real_casino_policy_keeps_lay_inactive_on_come_out(rules):
    table = Table(rules=rules)
    table.settings["come_out_working_policy"] = "real_casino"
    table.settings["vig_paid_on_win"] = True
    table.add_player(bankroll=100, strategy=NullStrategy())
    player = table.players[0]

    player.add_bet(Lay(4, 10))
    table.fixed_run([(4, 3)], verbose=True)

    assert player.bankroll == pytest.approx(90)
    assert len(player.bets) == 1


@pytest.mark.parametrize(
    "rules, put_number, come_number, second_roll",
    [
        (ClassicRules(), 6, 6, (3, 3)),
        (CraplessRules(), 2, 2, (1, 1)),
    ],
)
def test_real_casino_policy_keeps_put_inactive_but_keeps_traveled_come_working(
    rules, put_number, come_number, second_roll
):
    table = Table(rules=rules)
    table.settings["come_out_working_policy"] = "real_casino"
    table.add_player(bankroll=200, strategy=NullStrategy())
    player = table.players[0]

    table.point.number = 4
    player.add_bet(Put(put_number, 10))
    player.add_bet(Come(10, come_number))

    # Resolve the current point, then roll a matching come-out total.
    table.fixed_run([(2, 2), second_roll], verbose=True)

    assert player.bankroll == pytest.approx(200)
    assert len(player.bets) == 1


def test_real_casino_policy_keeps_traveled_dontcome_working_on_come_out_classic():
    table = Table(rules=ClassicRules())
    table.settings["come_out_working_policy"] = "real_casino"
    table.add_player(bankroll=100, strategy=NullStrategy())
    player = table.players[0]

    table.point.number = 4
    player.add_bet(DontCome(10, 5))

    table.fixed_run([(2, 2), (3, 4)], verbose=True)

    assert player.bankroll == pytest.approx(110)
    assert len(player.bets) == 0


@pytest.mark.parametrize(
    "comeout_roll, expected_bankroll",
    [
        ((3, 3), 90),
        ((3, 4), 110),
    ],
)
def test_dontcome_odds_always_working_false_pushes_on_comeout_triggers(
    comeout_roll, expected_bankroll
):
    table = Table(rules=ClassicRules())
    table.settings["come_out_working_policy"] = "real_casino"
    table.add_player(bankroll=100, strategy=NullStrategy())
    player = table.players[0]

    table.point.number = 4
    player.add_bet(DontCome(10, 6))
    player.add_bet(Odds(DontCome, 6, 10, always_working=False))

    table.fixed_run([(2, 2), comeout_roll], verbose=True)

    assert player.bankroll == pytest.approx(expected_bankroll)
    assert len(player.bets) == 0


def test_dontcome_not_allowed_in_crapless_integration_even_with_policy_enabled():
    table = Table(rules=CraplessRules())
    table.settings["come_out_working_policy"] = "real_casino"
    table.add_player(bankroll=100, strategy=NullStrategy())
    player = table.players[0]

    table.point.number = 4
    player.add_bet(DontCome(10))

    assert player.bankroll == pytest.approx(100)
    assert len(player.bets) == 0
