import pytest

from crapssim.bet import DontPass
from crapssim.strategy import BetDontPass
from crapssim.table import Table, TableUpdate


@pytest.mark.parametrize("point, last_roll, strat_info, bets_before, dice_result, bets_after", [
    (
        None, None, None, 
        [],
        None, 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [DontPass(bet_amount=5.0)],
        (4, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [DontPass(bet_amount=5.0)],
        (3, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 10, None, 
        [DontPass(bet_amount=5.0)],
        (6, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 11, None, 
        [DontPass(bet_amount=5.0)],
        (5, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (2, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [DontPass(bet_amount=5.0)],
        (3, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [DontPass(bet_amount=5.0)],
        (6, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 4, None, 
        [DontPass(bet_amount=5.0)],
        (1, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [DontPass(bet_amount=5.0)],
        (1, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 5, None, 
        [DontPass(bet_amount=5.0)],
        (1, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 9, None, 
        [DontPass(bet_amount=5.0)],
        (4, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 9, None, 
        [DontPass(bet_amount=5.0)],
        (3, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 9, None, 
        [DontPass(bet_amount=5.0)],
        (3, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (2, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 3, None, 
        [DontPass(bet_amount=5.0)],
        (2, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [DontPass(bet_amount=5.0)],
        (2, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (6, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (3, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [DontPass(bet_amount=5.0)],
        (5, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (3, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [DontPass(bet_amount=5.0)],
        (6, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 6, None, 
        [DontPass(bet_amount=5.0)],
        (3, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [DontPass(bet_amount=5.0)],
        (2, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (5, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [DontPass(bet_amount=5.0)],
        (2, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 10, None, 
        [DontPass(bet_amount=5.0)],
        (6, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 2, None, 
        [DontPass(bet_amount=5.0)],
        (1, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [DontPass(bet_amount=5.0)],
        (4, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 5, None, 
        [],
        (1, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (6, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [DontPass(bet_amount=5.0)],
        (4, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 4, None, 
        [DontPass(bet_amount=5.0)],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [DontPass(bet_amount=5.0)],
        (1, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [DontPass(bet_amount=5.0)],
        (5, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [DontPass(bet_amount=5.0)],
        (3, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [DontPass(bet_amount=5.0)],
        (2, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [DontPass(bet_amount=5.0)],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (1, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [DontPass(bet_amount=5.0)],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 3, None, 
        [DontPass(bet_amount=5.0)],
        (1, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 11, None, 
        [DontPass(bet_amount=5.0)],
        (5, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 9, None, 
        [DontPass(bet_amount=5.0)],
        (5, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [DontPass(bet_amount=5.0)],
        (6, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 4, None, 
        [DontPass(bet_amount=5.0)],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [DontPass(bet_amount=5.0)],
        (5, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [],
        (3, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [DontPass(bet_amount=5.0)],
        (1, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 2, None, 
        [],
        (1, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [DontPass(bet_amount=5.0)],
        (2, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (2, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (6, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [DontPass(bet_amount=5.0)],
        (6, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 3, None, 
        [DontPass(bet_amount=5.0)],
        (2, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [DontPass(bet_amount=5.0)],
        (3, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 10, None, 
        [DontPass(bet_amount=5.0)],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 12, None, 
        [DontPass(bet_amount=5.0)],
        (6, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 4, None, 
        [DontPass(bet_amount=5.0)],
        (2, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 4, None, 
        [DontPass(bet_amount=5.0)],
        (2, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [DontPass(bet_amount=5.0)],
        (6, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [DontPass(bet_amount=5.0)],
        (2, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [DontPass(bet_amount=5.0)],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [],
        (5, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (2, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [DontPass(bet_amount=5.0)],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (2, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [DontPass(bet_amount=5.0)],
        (1, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [DontPass(bet_amount=5.0)],
        (5, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 5, None, 
        [DontPass(bet_amount=5.0)],
        (2, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [DontPass(bet_amount=5.0)],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 11, None, 
        [DontPass(bet_amount=5.0)],
        (5, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 2, None, 
        [],
        (1, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [DontPass(bet_amount=5.0)],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [DontPass(bet_amount=5.0)],
        (3, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 2, None, 
        [DontPass(bet_amount=5.0)],
        (1, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [DontPass(bet_amount=5.0)],
        (6, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 3, None, 
        [DontPass(bet_amount=5.0)],
        (2, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (2, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 11, None, 
        [DontPass(bet_amount=5.0)],
        (6, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [DontPass(bet_amount=5.0)],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [DontPass(bet_amount=5.0)],
        (6, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 3, None, 
        [DontPass(bet_amount=5.0)],
        (1, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 3, None, 
        [DontPass(bet_amount=5.0)],
        (2, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [DontPass(bet_amount=5.0)],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 10, None, 
        [],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [DontPass(bet_amount=5.0)],
        (2, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [DontPass(bet_amount=5.0)],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [DontPass(bet_amount=5.0)],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [DontPass(bet_amount=5.0)],
        (3, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [DontPass(bet_amount=5.0)],
        (2, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (5, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 9, None, 
        [DontPass(bet_amount=5.0)],
        (5, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [DontPass(bet_amount=5.0)],
        (3, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 11, None, 
        [DontPass(bet_amount=5.0)],
        (5, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [DontPass(bet_amount=5.0)],
        (1, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [DontPass(bet_amount=5.0)],
        (3, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [DontPass(bet_amount=5.0)],
        (4, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 9, None, 
        [DontPass(bet_amount=5.0)],
        (5, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [DontPass(bet_amount=5.0)],
        (5, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (6, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [DontPass(bet_amount=5.0)],
        (5, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [DontPass(bet_amount=5.0)],
        (1, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [DontPass(bet_amount=5.0)],
        (1, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [DontPass(bet_amount=5.0)],
        (4, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [DontPass(bet_amount=5.0)],
        (3, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [],
        (4, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [DontPass(bet_amount=5.0)],
        (4, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [],
        (4, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [DontPass(bet_amount=5.0)],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 3, None, 
        [],
        (1, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [DontPass(bet_amount=5.0)],
        (1, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 4, None, 
        [],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 6, None, 
        [DontPass(bet_amount=5.0)],
        (4, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 3, None, 
        [DontPass(bet_amount=5.0)],
        (1, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (3, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [DontPass(bet_amount=5.0)],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 10, None, 
        [],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [DontPass(bet_amount=5.0)],
        (2, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 5, None, 
        [DontPass(bet_amount=5.0)],
        (4, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 6, None, 
        [DontPass(bet_amount=5.0)],
        (5, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 8, None, 
        [DontPass(bet_amount=5.0)],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 11, None, 
        [DontPass(bet_amount=5.0)],
        (6, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 4, None, 
        [],
        (1, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [DontPass(bet_amount=5.0)],
        (2, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 9, None, 
        [DontPass(bet_amount=5.0)],
        (4, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 12, None, 
        [DontPass(bet_amount=5.0)],
        (6, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 2, None, 
        [DontPass(bet_amount=5.0)],
        (1, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 8, None, 
        [DontPass(bet_amount=5.0)],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 5, None, 
        [DontPass(bet_amount=5.0)],
        (4, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 4, None, 
        [],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (6, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [DontPass(bet_amount=5.0)],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [DontPass(bet_amount=5.0)],
        (3, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 4, None, 
        [DontPass(bet_amount=5.0)],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 3, None, 
        [DontPass(bet_amount=5.0)],
        (1, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [DontPass(bet_amount=5.0)],
        (5, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [DontPass(bet_amount=5.0)],
        (6, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [DontPass(bet_amount=5.0)],
        (2, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 11, None, 
        [DontPass(bet_amount=5.0)],
        (6, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [DontPass(bet_amount=5.0)],
        (3, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [DontPass(bet_amount=5.0)],
        (6, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [DontPass(bet_amount=5.0)],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [DontPass(bet_amount=5.0)],
        (2, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 5, None, 
        [DontPass(bet_amount=5.0)],
        (3, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 10, None, 
        [DontPass(bet_amount=5.0)],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 10, None, 
        [DontPass(bet_amount=5.0)],
        (5, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 4, None, 
        [DontPass(bet_amount=5.0)],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 4, None, 
        [DontPass(bet_amount=5.0)],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [DontPass(bet_amount=5.0)],
        (3, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 2, None, 
        [DontPass(bet_amount=5.0)],
        (1, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 10, None, 
        [DontPass(bet_amount=5.0)],
        (5, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [DontPass(bet_amount=5.0)],
        (6, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 12, None, 
        [DontPass(bet_amount=5.0)],
        (6, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [DontPass(bet_amount=5.0)],
        (6, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [DontPass(bet_amount=5.0)],
        (1, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 4, None, 
        [DontPass(bet_amount=5.0)],
        (2, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [DontPass(bet_amount=5.0)],
        (5, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [DontPass(bet_amount=5.0)],
        (1, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (6, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [DontPass(bet_amount=5.0)],
        (4, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [DontPass(bet_amount=5.0)],
        (6, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 10, None, 
        [DontPass(bet_amount=5.0)],
        (6, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [DontPass(bet_amount=5.0)],
        (3, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 9, None, 
        [DontPass(bet_amount=5.0)],
        (6, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [DontPass(bet_amount=5.0)],
        (4, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [DontPass(bet_amount=5.0)],
        (3, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 10, None, 
        [DontPass(bet_amount=5.0)],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [DontPass(bet_amount=5.0)],
        (3, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [DontPass(bet_amount=5.0)],
        (2, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [DontPass(bet_amount=5.0)],
        (3, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [DontPass(bet_amount=5.0)],
        (5, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 12, None, 
        [DontPass(bet_amount=5.0)],
        (6, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (5, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [DontPass(bet_amount=5.0)],
        (5, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 8, None, 
        [DontPass(bet_amount=5.0)],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 11, None, 
        [DontPass(bet_amount=5.0)],
        (5, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 5, None, 
        [DontPass(bet_amount=5.0)],
        (1, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 12, None, 
        [DontPass(bet_amount=5.0)],
        (6, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [DontPass(bet_amount=5.0)],
        (6, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 9, None, 
        [],
        (3, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 12, None, 
        [],
        (6, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [DontPass(bet_amount=5.0)],
        (4, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [DontPass(bet_amount=5.0)],
        (2, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 9, None, 
        [DontPass(bet_amount=5.0)],
        (5, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [DontPass(bet_amount=5.0)],
        (2, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 5, None, 
        [],
        (3, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [DontPass(bet_amount=5.0)],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [DontPass(bet_amount=5.0)],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 9, None, 
        [DontPass(bet_amount=5.0)],
        (4, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 9, None, 
        [DontPass(bet_amount=5.0)],
        (4, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 8, None, 
        [DontPass(bet_amount=5.0)],
        (6, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 5, None, 
        [DontPass(bet_amount=5.0)],
        (4, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 10, None, 
        [],
        (5, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [DontPass(bet_amount=5.0)],
        (4, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 8, None, 
        [DontPass(bet_amount=5.0)],
        (6, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [DontPass(bet_amount=5.0)],
        (3, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [DontPass(bet_amount=5.0)],
        (3, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 6, None, 
        [DontPass(bet_amount=5.0)],
        (3, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 4, None, 
        [DontPass(bet_amount=5.0)],
        (2, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (5, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, None, 
        [DontPass(bet_amount=5.0)],
        (6, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 3, None, 
        [DontPass(bet_amount=5.0)],
        (2, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        9, 6, None, 
        [DontPass(bet_amount=5.0)],
        (1, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [DontPass(bet_amount=5.0)],
        (1, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 2, None, 
        [],
        (1, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [DontPass(bet_amount=5.0)],
        (2, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 10, None, 
        [DontPass(bet_amount=5.0)],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, None, 
        [DontPass(bet_amount=5.0)],
        (6, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        10, 4, None, 
        [DontPass(bet_amount=5.0)],
        (2, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (1, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, None, 
        [],
        (5, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (2, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (5, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 2, None, 
        [DontPass(bet_amount=5.0)],
        (1, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 3, None, 
        [DontPass(bet_amount=5.0)],
        (2, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [DontPass(bet_amount=5.0)],
        (1, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [DontPass(bet_amount=5.0)],
        (1, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [DontPass(bet_amount=5.0)],
        (3, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 3, None, 
        [DontPass(bet_amount=5.0)],
        (2, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 9, None, 
        [DontPass(bet_amount=5.0)],
        (6, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (3, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (3, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [DontPass(bet_amount=5.0)],
        (1, 5), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 6, None, 
        [],
        (4, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, None, 
        [DontPass(bet_amount=5.0)],
        (1, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 6, None, 
        [DontPass(bet_amount=5.0)],
        (2, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 5, None, 
        [DontPass(bet_amount=5.0)],
        (3, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 10, None, 
        [DontPass(bet_amount=5.0)],
        (4, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 9, None, 
        [DontPass(bet_amount=5.0)],
        (5, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 9, None, 
        [DontPass(bet_amount=5.0)],
        (6, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 3, None, 
        [DontPass(bet_amount=5.0)],
        (1, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        4, 6, None, 
        [DontPass(bet_amount=5.0)],
        (5, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, None, 
        [],
        (4, 3), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, None, 
        [DontPass(bet_amount=5.0)],
        (4, 4), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 4, None, 
        [DontPass(bet_amount=5.0)],
        (2, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        8, 5, None, 
        [DontPass(bet_amount=5.0)],
        (4, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 8, None, 
        [],
        (2, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, None, 
        [DontPass(bet_amount=5.0)],
        (4, 1), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        None, 5, None, 
        [],
        (3, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, None, 
        [DontPass(bet_amount=5.0)],
        (4, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 8, None, 
        [DontPass(bet_amount=5.0)],
        (2, 6), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 3, None, 
        [DontPass(bet_amount=5.0)],
        (1, 2), 
        [DontPass(bet_amount=5.0)]
    ),
    (
        6, 4, None, 
        [DontPass(bet_amount=5.0)],
        (3, 1), 
        [DontPass(bet_amount=5.0)]
    )
])
def test_dontpass_integration(point, last_roll, strat_info, bets_before, dice_result, bets_after):
    table = Table()
    table.add_player(bankroll=float("inf"), strategy=BetDontPass(5))  # ADD STRATEGY HERE
    table.point.number = point
    table.last_roll = last_roll
    table.players[0].bets = bets_before
    table.dice.result = dice_result
    TableUpdate().run_strategies(table)
    assert table.players[0].bets == bets_after