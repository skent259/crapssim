import pytest

from crapssim.strategy import BetPassLine, PassLineOdds
from crapssim.table import Table
from crapssim.bet import PassLine, Odds4, Odds5, Odds6, Odds8, Odds9, Odds10


@pytest.mark.parametrize("point, last_roll, strat_info, bets_before, dice_result, bets_after", [
    (
        None, None, None, 
        [],
        None, 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 3, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 2, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 10, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 11, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 11, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 3, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 8, None, 
        [],
        (5, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 11, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        None, 5, None, 
        [],
        (3, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (5, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 3, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 2, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 12, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 6, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 5, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 9, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 12, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 10, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        None, 6, None, 
        [],
        (5, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 8, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 5, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        None, 6, None, 
        [],
        (4, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 10, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 6, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        None, 4, None, 
        [],
        (2, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 4, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 10, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (5, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 11, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 8, None, 
        [],
        (3, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        None, 6, None, 
        [],
        (2, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 10, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 8, None, 
        [],
        (4, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 4, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 4, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 2, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 4, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 2, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 12, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 3, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 2, None, 
        [],
        (1, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 11, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (2, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 12, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        None, 10, None, 
        [],
        (5, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        None, 5, None, 
        [],
        (2, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 3, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 4, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        None, 6, None, 
        [],
        (5, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 10, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 8, None, 
        [],
        (2, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 8, None, 
        [],
        (3, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (2, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 3, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        None, 5, None, 
        [],
        (2, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 8, None, 
        [],
        (6, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        None, 6, None, 
        [],
        (1, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 11, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 4, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        None, 6, None, 
        [],
        (3, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 11, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        10, 4, None, 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        None, 10, None, 
        [],
        (4, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 6, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 6, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 9, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        None, 4, None, 
        [],
        (1, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 12, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 3, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 12, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 8, None, 
        [],
        (6, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 6, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        None, 4, None, 
        [],
        (3, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 11, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 2, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 9, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 5, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 5, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 6, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        None, 4, None, 
        [],
        (1, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds10(bet_amount=10.0)]
    ),
    (
        None, 10, None, 
        [],
        (5, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 10, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 10, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        4, 8, None, 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds4(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 10, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 2, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        None, 6, None, 
        [],
        (2, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 3, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 10, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 8, None, 
        [],
        (2, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 12, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 11, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds5(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds9(bet_amount=10.0)]
    ),
    (
        None, 9, None, 
        [],
        (6, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 2, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Odds8(bet_amount=10.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 4, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 8, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Odds6(bet_amount=10.0)]
    )
])
def test_passline_odds2_integration(point, last_roll, strat_info, bets_before, dice_result, bets_after):
    table = Table()
    table.add_player(bankroll=float("inf"), strategy=BetPassLine(5) + PassLineOdds(2)) # ADD STRATEGY HERE
    table.point.number = point
    table.last_roll = last_roll
    table.players[0].bets_on_table = bets_before
    table.dice.result = dice_result
    table.add_player_bets()
    assert table.players[0].bets_on_table == bets_after