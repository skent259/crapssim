import pytest

from crapssim.strategy.defaults import Pass2Come
from crapssim.table import Table
from crapssim.bet import PassLine, Come


@pytest.mark.parametrize("point, last_roll, strat_info, bets_before, dice_result, bets_after", [
    (
        None, None, None, 
        [],
        None, 
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
        (2, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [Come(bet_amount=5.0, point=8)],
        (3, 5), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [Come(bet_amount=5.0, point=8)],
        (5, 6), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
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
        (4, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 11, None, 
        [PassLine(bet_amount=5.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        6, 10, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0)]
    ),
    (
        6, 3, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6)],
        (4, 2), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (4, 1), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        None, 5, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6)],
        (4, 1), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (5, 4), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (1, 4), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)],
        (4, 2), 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (3, 2), 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)]
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
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 11, None, 
        [PassLine(bet_amount=5.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 2, None, 
        [PassLine(bet_amount=5.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        6, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=4)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=4)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
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
        (6, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 10, None, 
        [Come(bet_amount=5.0, point=10)],
        (5, 5), 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)],
        (2, 4), 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6)],
        (2, 4), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
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
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        5, 12, None, 
        [PassLine(bet_amount=5.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        (4, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=8)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=8)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        9, 11, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=8)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=8)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=8)],
        (3, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=8)]
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
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        5, 3, None, 
        [PassLine(bet_amount=5.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0)]
    ),
    (
        5, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4)]
    ),
    (
        5, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0)]
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
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [Come(bet_amount=5.0, point=8)],
        (4, 4), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0)]
    ),
    (
        8, 10, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=10)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=10)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=10)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=10)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        6, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=6)],
        (5, 1), 
        [Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (6, 4), 
        [Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        10, 6, None, 
        [Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0)],
        (3, 3), 
        [Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
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
        (6, 1), 
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
        (2, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 11, None, 
        [PassLine(bet_amount=5.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        (3, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4)]
    ),
    (
        None, 8, None, 
        [Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4)],
        (4, 4), 
        [Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0)],
        (4, 1), 
        [Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0)]
    ),
    (
        5, 11, None, 
        [Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0)],
        (6, 5), 
        [Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0)]
    ),
    (
        5, 4, None, 
        [Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0)],
        (2, 2), 
        [Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 3, None, 
        [PassLine(bet_amount=5.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
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
        (1, 6), 
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
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=5)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=5)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        5, 11, None, 
        [PassLine(bet_amount=5.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 2, None, 
        [],
        (1, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        10, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0)]
    ),
    (
        10, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=5)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=5)]
    ),
    (
        None, 10, None, 
        [Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=5)],
        (6, 4), 
        [Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=5), PassLine(bet_amount=5.0)]
    ),
    (
        None, 2, None, 
        [Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=5)],
        (1, 1), 
        [Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=5), PassLine(bet_amount=5.0)]
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
        (2, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [Come(bet_amount=5.0, point=8)],
        (4, 4), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [Come(bet_amount=5.0, point=8)],
        (6, 6), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [PassLine(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=9)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=9)]
    ),
    (
        8, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0)]
    ),
    (
        8, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=6)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=6)]
    ),
    (
        8, 3, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=6)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=6)]
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
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8)],
        (3, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8)]
    ),
    (
        None, 9, None, 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8)],
        (3, 6), 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        None, 2, None, 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8)],
        (1, 1), 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
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
        (3, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        6, 3, None, 
        [PassLine(bet_amount=5.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        6, 12, None, 
        [PassLine(bet_amount=5.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        6, 11, None, 
        [PassLine(bet_amount=5.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        6, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=4)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=4)]
    ),
    (
        6, 10, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=4)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=4)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=4)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=4)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=6)],
        (1, 5), 
        [Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (1, 3), 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        4, 11, None, 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (6, 5), 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        (4, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [Come(bet_amount=5.0, point=9)],
        (3, 6), 
        [Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0)],
        (1, 4), 
        [Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        None, 3, None, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 4, None, 
        [Come(bet_amount=5.0, point=4)],
        (3, 1), 
        [Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0)],
        (5, 3), 
        [Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (1, 4), 
        [Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)]
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
        (5, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6)]
    ),
    (
        9, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6)]
    ),
    (
        None, 9, None, 
        [Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6)],
        (3, 6), 
        [Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (6, 2), 
        [Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        8, 10, None, 
        [Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (6, 4), 
        [Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
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
        None, 7, None, 
        [],
        (1, 6), 
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
        (6, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0)]
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
        (2, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8)],
        (4, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0)]
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
        (5, 2), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [PassLine(bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=8)],
        (2, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=8)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=8)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=8)]
    ),
    (
        9, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0)]
    ),
    (
        9, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=4)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=4)]
    ),
    (
        9, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8)],
        (6, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=6)],
        (2, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=6)]
    ),
    (
        None, 9, None, 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=6)],
        (6, 3), 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=6)],
        (2, 1), 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (2, 6), 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6), Come(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8)],
        (3, 5), 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)],
        (4, 6), 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        10, 9, None, 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)],
        (3, 6), 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        10, 9, None, 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)],
        (4, 5), 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        10, 9, None, 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)],
        (6, 3), 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        10, 5, None, 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)],
        (3, 2), 
        [Come(bet_amount=5.0, point=6), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (3, 5), 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        10, 12, None, 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (6, 6), 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        10, 5, None, 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (4, 1), 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)]
    ),
    (
        10, 4, None, 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (3, 1), 
        [Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        10, 2, None, 
        [PassLine(bet_amount=5.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        (4, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 11, None, 
        [PassLine(bet_amount=5.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        (6, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [Come(bet_amount=5.0, point=8)],
        (5, 3), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)],
        (6, 3), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=9)],
        (4, 5), 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)],
        (3, 6), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)],
        (5, 1), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)]
    ),
    (
        9, 5, None, 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)],
        (4, 1), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)]
    ),
    (
        9, 4, None, 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)],
        (2, 2), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=6)]
    ),
    (
        9, 6, None, 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)],
        (2, 4), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 10, None, 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (6, 4), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)]
    ),
    (
        None, 9, None, 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=10)],
        (6, 3), 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)],
        (4, 5), 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)]
    ),
    (
        9, 11, None, 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)],
        (5, 6), 
        [Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)]
    ),
    (
        9, 10, None, 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)],
        (4, 6), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 3, None, 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)],
        (2, 1), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (2, 3), 
        [Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)]
    ),
    (
        9, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        9, 10, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=10)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0, point=10)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 5, None, 
        [Come(bet_amount=5.0, point=5)],
        (1, 4), 
        [Come(bet_amount=5.0, point=5), PassLine(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [Come(bet_amount=5.0, point=5)],
        (2, 1), 
        [Come(bet_amount=5.0, point=5), PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [Come(bet_amount=5.0, point=5), PassLine(bet_amount=5.0)],
        (6, 2), 
        [Come(bet_amount=5.0, point=5), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 12, None, 
        [Come(bet_amount=5.0, point=5), PassLine(bet_amount=5.0)],
        (6, 6), 
        [Come(bet_amount=5.0, point=5), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (2, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
    ),
    (
        8, 3, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5)],
        (2, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=5), Come(bet_amount=5.0)]
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
        (2, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [PassLine(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0)]
    ),
    (
        6, 10, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=10)],
        (4, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=10)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (6, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0)]
    ),
    (
        6, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=4)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=4)]
    ),
    (
        6, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=4)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=4)]
    ),
    (
        6, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=4)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=4)]
    ),
    (
        6, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (2, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0)]
    ),
    (
        6, 11, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (5, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0)]
    ),
    (
        6, 12, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (6, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6)],
        (3, 3), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)],
        (1, 3), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6), PassLine(bet_amount=5.0)]
    ),
    (
        4, 6, None, 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)],
        (4, 2), 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
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
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        8, 10, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=5)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=5)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (3, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0)]
    ),
    (
        8, 3, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (2, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6)],
        (5, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6)]
    ),
    (
        8, 5, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6)],
        (1, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=6)]
    ),
    (
        8, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10)],
        (4, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=10), Come(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        None, 2, None, 
        [],
        (1, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 10, None, 
        [Come(bet_amount=5.0, point=10)],
        (4, 6), 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)],
        (4, 5), 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=9)],
        (6, 3), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0)],
        (3, 5), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0)],
        (5, 1), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=9)],
        (5, 3), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=9), PassLine(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0)],
        (3, 6), 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8)],
        (5, 3), 
        [Come(bet_amount=5.0, point=10), PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8)]
    ),
    (
        None, 9, None, 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=8)],
        (6, 3), 
        [Come(bet_amount=5.0, point=10), Come(bet_amount=5.0, point=8), PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [PassLine(bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        4, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9)],
        (3, 6), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=9), Come(bet_amount=5.0)]
    ),
    (
        None, 4, None, 
        [Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4)],
        (2, 2), 
        [Come(bet_amount=5.0, point=9), Come(bet_amount=5.0, point=4), PassLine(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [PassLine(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8)],
        (5, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0)]
    ),
    (
        10, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=4)],
        (3, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=4)]
    ),
    (
        10, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=4)],
        (4, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=8), Come(bet_amount=5.0, point=4)]
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
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [PassLine(bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0)]
    ),
    (
        5, 4, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4)],
        (1, 3), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0)]
    ),
    (
        5, 3, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4)],
        (1, 2), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0)]
    ),
    (
        5, 11, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4)],
        (6, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=9)],
        (5, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=9)]
    ),
    (
        5, 10, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=9)],
        (6, 4), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=9)]
    ),
    (
        5, 6, None, 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=9)],
        (1, 5), 
        [PassLine(bet_amount=5.0), Come(bet_amount=5.0, point=4), Come(bet_amount=5.0, point=9)]
    )
])
def test_pass2come_integration(point, last_roll, strat_info, bets_before, dice_result, bets_after):
    table = Table()
    table.add_player(bankroll=float("inf"), strategy=Pass2Come(5)) # ADD STRATEGY HERE
    table.point.number = point
    table.last_roll = last_roll
    table.players[0].bets_on_table = bets_before
    table.dice.result = dice_result
    table.add_player_bets()
    assert table.players[0].bets_on_table == bets_after