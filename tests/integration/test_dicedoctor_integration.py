import pytest

from crapssim.strategy.defaults import DiceDoctor
from crapssim.table import Table
from crapssim.bet.one_roll import Field


@pytest.mark.parametrize("point, last_roll, strat_info, bets_before, dice_result, bets_after", [
    (
        None, None, {'progression': 0}, 
        [],
        None, 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 11, {'progression': 1}, 
        [],
        (5, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 2, {'progression': 2}, 
        [],
        (1, 1), 
        [Field(bet_amount=15.0)]
    ),
    (
        4, 4, {'progression': 3}, 
        [],
        (1, 3), 
        [Field(bet_amount=30.0)]
    ),
    (
        4, 10, {'progression': 4}, 
        [],
        (4, 6), 
        [Field(bet_amount=25.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (2, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 5, {'progression': 0}, 
        [],
        (2, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (4, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 5, {'progression': 0}, 
        [],
        (4, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (4, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        4, 4, {'progression': 1}, 
        [],
        (1, 3), 
        [Field(bet_amount=20.0)]
    ),
    (
        4, 5, {'progression': 0}, 
        [],
        (4, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        4, 5, {'progression': 0}, 
        [],
        (1, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        4, 11, {'progression': 1}, 
        [],
        (5, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        4, 12, {'progression': 2}, 
        [],
        (6, 6), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 4, {'progression': 3}, 
        [],
        (3, 1), 
        [Field(bet_amount=30.0)]
    ),
    (
        None, 11, {'progression': 4}, 
        [],
        (5, 6), 
        [Field(bet_amount=25.0)]
    ),
    (
        5, 5, {'progression': 0}, 
        [],
        (1, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 4, {'progression': 1}, 
        [],
        (3, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (6, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 10, {'progression': 1}, 
        [],
        (5, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 8, {'progression': 0}, 
        [],
        (4, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (6, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 9, {'progression': 1}, 
        [],
        (4, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 5, {'progression': 0}, 
        [],
        (2, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 3, {'progression': 1}, 
        [],
        (1, 2), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 4, {'progression': 2}, 
        [],
        (2, 2), 
        [Field(bet_amount=15.0)]
    ),
    (
        8, 3, {'progression': 3}, 
        [],
        (1, 2), 
        [Field(bet_amount=30.0)]
    ),
    (
        None, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (3, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        10, 10, {'progression': 1}, 
        [],
        (5, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        10, 6, {'progression': 0}, 
        [],
        (1, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (5, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 4, {'progression': 1}, 
        [],
        (2, 2), 
        [Field(bet_amount=20.0)]
    ),
    (
        6, 3, {'progression': 2}, 
        [],
        (2, 1), 
        [Field(bet_amount=15.0)]
    ),
    (
        6, 9, {'progression': 3}, 
        [],
        (3, 6), 
        [Field(bet_amount=30.0)]
    ),
    (
        6, 4, {'progression': 4}, 
        [],
        (2, 2), 
        [Field(bet_amount=25.0)]
    ),
    (
        6, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 9, {'progression': 1}, 
        [],
        (6, 3), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 3, {'progression': 2}, 
        [],
        (2, 1), 
        [Field(bet_amount=15.0)]
    ),
    (
        8, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (6, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 9, {'progression': 1}, 
        [],
        (4, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 11, {'progression': 2}, 
        [],
        (6, 5), 
        [Field(bet_amount=15.0)]
    ),
    (
        9, 3, {'progression': 3}, 
        [],
        (2, 1), 
        [Field(bet_amount=30.0)]
    ),
    (
        9, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 3, {'progression': 1}, 
        [],
        (2, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 9, {'progression': 2}, 
        [],
        (4, 5), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (2, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 11, {'progression': 1}, 
        [],
        (6, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (1, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 9, {'progression': 1}, 
        [],
        (3, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        6, 2, {'progression': 2}, 
        [],
        (1, 1), 
        [Field(bet_amount=15.0)]
    ),
    (
        6, 5, {'progression': 0}, 
        [],
        (4, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 10, {'progression': 1}, 
        [],
        (5, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 6, {'progression': 0}, 
        [],
        (2, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 12, {'progression': 1}, 
        [],
        (6, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        5, 5, {'progression': 0}, 
        [],
        (3, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 5, {'progression': 0}, 
        [],
        (2, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (6, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (3, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 10, {'progression': 1}, 
        [],
        (5, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 4, {'progression': 1}, 
        [],
        (1, 3), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 4, {'progression': 2}, 
        [],
        (3, 1), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (3, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (1, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (1, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 4, {'progression': 1}, 
        [],
        (2, 2), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (1, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 3, {'progression': 1}, 
        [],
        (2, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 11, {'progression': 2}, 
        [],
        (5, 6), 
        [Field(bet_amount=15.0)]
    ),
    (
        8, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 9, {'progression': 1}, 
        [],
        (4, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 4, {'progression': 2}, 
        [],
        (1, 3), 
        [Field(bet_amount=15.0)]
    ),
    (
        8, 3, {'progression': 3}, 
        [],
        (2, 1), 
        [Field(bet_amount=30.0)]
    ),
    (
        8, 10, {'progression': 4}, 
        [],
        (6, 4), 
        [Field(bet_amount=25.0)]
    ),
    (
        8, 4, {'progression': 5}, 
        [],
        (1, 3), 
        [Field(bet_amount=50.0)]
    ),
    (
        8, 4, {'progression': 6}, 
        [],
        (2, 2), 
        [Field(bet_amount=35.0)]
    ),
    (
        8, 10, {'progression': 7}, 
        [],
        (4, 6), 
        [Field(bet_amount=70.0)]
    ),
    (
        8, 3, {'progression': 8}, 
        [],
        (1, 2), 
        [Field(bet_amount=50.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (1, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        4, 4, {'progression': 1}, 
        [],
        (3, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        4, 5, {'progression': 0}, 
        [],
        (2, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        4, 11, {'progression': 1}, 
        [],
        (5, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 4, {'progression': 2}, 
        [],
        (2, 2), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 2, {'progression': 3}, 
        [],
        (1, 1), 
        [Field(bet_amount=30.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (6, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 6, {'progression': 0}, 
        [],
        (5, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 5, {'progression': 0}, 
        [],
        (1, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 3, {'progression': 1}, 
        [],
        (2, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 6, {'progression': 0}, 
        [],
        (5, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (1, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 5, {'progression': 0}, 
        [],
        (2, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 6, {'progression': 0}, 
        [],
        (2, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 4, {'progression': 1}, 
        [],
        (3, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 11, {'progression': 1}, 
        [],
        (5, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        10, 10, {'progression': 2}, 
        [],
        (5, 5), 
        [Field(bet_amount=15.0)]
    ),
    (
        10, 5, {'progression': 0}, 
        [],
        (4, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        10, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 5, {'progression': 0}, 
        [],
        (1, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 8, {'progression': 0}, 
        [],
        (4, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 10, {'progression': 1}, 
        [],
        (4, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        5, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 3, {'progression': 1}, 
        [],
        (2, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        5, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 9, {'progression': 1}, 
        [],
        (5, 4), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 8, {'progression': 0}, 
        [],
        (6, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 5, {'progression': 0}, 
        [],
        (4, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 9, {'progression': 1}, 
        [],
        (3, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 9, {'progression': 2}, 
        [],
        (4, 5), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 9, {'progression': 3}, 
        [],
        (4, 5), 
        [Field(bet_amount=30.0)]
    ),
    (
        10, 10, {'progression': 4}, 
        [],
        (6, 4), 
        [Field(bet_amount=25.0)]
    ),
    (
        10, 5, {'progression': 0}, 
        [],
        (4, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        10, 6, {'progression': 0}, 
        [],
        (5, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        10, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        10, 5, {'progression': 0}, 
        [],
        (1, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        10, 2, {'progression': 1}, 
        [],
        (1, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (5, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (1, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 11, {'progression': 1}, 
        [],
        (6, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 11, {'progression': 2}, 
        [],
        (5, 6), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 2, {'progression': 3}, 
        [],
        (1, 1), 
        [Field(bet_amount=30.0)]
    ),
    (
        None, 3, {'progression': 4}, 
        [],
        (2, 1), 
        [Field(bet_amount=25.0)]
    ),
    (
        None, 12, {'progression': 5}, 
        [],
        (6, 6), 
        [Field(bet_amount=50.0)]
    ),
    (
        9, 9, {'progression': 6}, 
        [],
        (5, 4), 
        [Field(bet_amount=35.0)]
    ),
    (
        None, 9, {'progression': 7}, 
        [],
        (3, 6), 
        [Field(bet_amount=70.0)]
    ),
    (
        9, 9, {'progression': 8}, 
        [],
        (5, 4), 
        [Field(bet_amount=50.0)]
    ),
    (
        9, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 10, {'progression': 1}, 
        [],
        (6, 4), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 11, {'progression': 2}, 
        [],
        (6, 5), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 4, {'progression': 1}, 
        [],
        (1, 3), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 8, {'progression': 0}, 
        [],
        (3, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 10, {'progression': 1}, 
        [],
        (5, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 6, {'progression': 0}, 
        [],
        (1, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 9, {'progression': 1}, 
        [],
        (4, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 5, {'progression': 0}, 
        [],
        (4, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 6, {'progression': 0}, 
        [],
        (1, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 4, {'progression': 1}, 
        [],
        (3, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 4, {'progression': 2}, 
        [],
        (3, 1), 
        [Field(bet_amount=15.0)]
    ),
    (
        9, 4, {'progression': 3}, 
        [],
        (2, 2), 
        [Field(bet_amount=30.0)]
    ),
    (
        None, 9, {'progression': 4}, 
        [],
        (3, 6), 
        [Field(bet_amount=25.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 9, {'progression': 1}, 
        [],
        (3, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 10, {'progression': 2}, 
        [],
        (6, 4), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 5, {'progression': 0}, 
        [],
        (4, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 4, {'progression': 1}, 
        [],
        (2, 2), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 5, {'progression': 0}, 
        [],
        (2, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 3, {'progression': 1}, 
        [],
        (1, 2), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 10, {'progression': 2}, 
        [],
        (5, 5), 
        [Field(bet_amount=15.0)]
    ),
    (
        8, 9, {'progression': 3}, 
        [],
        (3, 6), 
        [Field(bet_amount=30.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 11, {'progression': 1}, 
        [],
        (5, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (4, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (6, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 3, {'progression': 1}, 
        [],
        (2, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (6, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 11, {'progression': 1}, 
        [],
        (6, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 11, {'progression': 2}, 
        [],
        (6, 5), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (4, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 9, {'progression': 1}, 
        [],
        (3, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 6, {'progression': 0}, 
        [],
        (5, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 10, {'progression': 1}, 
        [],
        (6, 4), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 8, {'progression': 0}, 
        [],
        (4, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (6, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (4, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (6, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 8, {'progression': 0}, 
        [],
        (3, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (2, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        10, 10, {'progression': 1}, 
        [],
        (5, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 10, {'progression': 2}, 
        [],
        (6, 4), 
        [Field(bet_amount=15.0)]
    ),
    (
        9, 9, {'progression': 3}, 
        [],
        (4, 5), 
        [Field(bet_amount=30.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (2, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (2, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 5, {'progression': 0}, 
        [],
        (1, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 4, {'progression': 1}, 
        [],
        (1, 3), 
        [Field(bet_amount=20.0)]
    ),
    (
        5, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 11, {'progression': 1}, 
        [],
        (5, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        5, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 10, {'progression': 1}, 
        [],
        (6, 4), 
        [Field(bet_amount=20.0)]
    ),
    (
        5, 6, {'progression': 0}, 
        [],
        (1, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 9, {'progression': 1}, 
        [],
        (5, 4), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 10, {'progression': 2}, 
        [],
        (5, 5), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (1, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 11, {'progression': 1}, 
        [],
        (5, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        5, 5, {'progression': 0}, 
        [],
        (1, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 11, {'progression': 1}, 
        [],
        (6, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        5, 10, {'progression': 2}, 
        [],
        (4, 6), 
        [Field(bet_amount=15.0)]
    ),
    (
        5, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 3, {'progression': 1}, 
        [],
        (2, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        5, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (1, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (4, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 8, {'progression': 0}, 
        [],
        (4, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (2, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 11, {'progression': 1}, 
        [],
        (6, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        6, 5, {'progression': 0}, 
        [],
        (1, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 5, {'progression': 0}, 
        [],
        (4, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 4, {'progression': 1}, 
        [],
        (1, 3), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (3, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        5, 5, {'progression': 0}, 
        [],
        (2, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (6, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 8, {'progression': 0}, 
        [],
        (6, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 11, {'progression': 1}, 
        [],
        (5, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        6, 10, {'progression': 2}, 
        [],
        (6, 4), 
        [Field(bet_amount=15.0)]
    ),
    (
        6, 12, {'progression': 3}, 
        [],
        (6, 6), 
        [Field(bet_amount=30.0)]
    ),
    (
        6, 9, {'progression': 4}, 
        [],
        (3, 6), 
        [Field(bet_amount=25.0)]
    ),
    (
        6, 4, {'progression': 5}, 
        [],
        (1, 3), 
        [Field(bet_amount=50.0)]
    ),
    (
        6, 9, {'progression': 6}, 
        [],
        (5, 4), 
        [Field(bet_amount=35.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (1, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (1, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (4, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        10, 10, {'progression': 1}, 
        [],
        (4, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (2, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 10, {'progression': 1}, 
        [],
        (5, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        8, 4, {'progression': 2}, 
        [],
        (1, 3), 
        [Field(bet_amount=15.0)]
    ),
    (
        8, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (1, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 9, {'progression': 1}, 
        [],
        (4, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 5, {'progression': 0}, 
        [],
        (4, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (6, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (1, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        4, 4, {'progression': 1}, 
        [],
        (1, 3), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 4, {'progression': 2}, 
        [],
        (3, 1), 
        [Field(bet_amount=15.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (5, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 9, {'progression': 1}, 
        [],
        (3, 6), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 9, {'progression': 1}, 
        [],
        (4, 5), 
        [Field(bet_amount=20.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (4, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (3, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 9, {'progression': 1}, 
        [],
        (5, 4), 
        [Field(bet_amount=20.0)]
    ),
    (
        9, 2, {'progression': 2}, 
        [],
        (1, 1), 
        [Field(bet_amount=15.0)]
    ),
    (
        9, 5, {'progression': 0}, 
        [],
        (2, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 8, {'progression': 0}, 
        [],
        (2, 6), 
        [Field(bet_amount=10.0)]
    ),
    (
        9, 8, {'progression': 0}, 
        [],
        (3, 5), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (6, 1), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 8, {'progression': 0}, 
        [],
        (4, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        8, 6, {'progression': 0}, 
        [],
        (4, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 8, {'progression': 0}, 
        [],
        (5, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 3, {'progression': 1}, 
        [],
        (1, 2), 
        [Field(bet_amount=20.0)]
    ),
    (
        10, 10, {'progression': 2}, 
        [],
        (5, 5), 
        [Field(bet_amount=15.0)]
    ),
    (
        10, 8, {'progression': 0}, 
        [],
        (4, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        10, 4, {'progression': 1}, 
        [],
        (3, 1), 
        [Field(bet_amount=20.0)]
    ),
    (
        10, 9, {'progression': 2}, 
        [],
        (5, 4), 
        [Field(bet_amount=15.0)]
    ),
    (
        10, 5, {'progression': 0}, 
        [],
        (2, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        10, 5, {'progression': 0}, 
        [],
        (1, 4), 
        [Field(bet_amount=10.0)]
    ),
    (
        None, 7, {'progression': 0}, 
        [],
        (5, 2), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 6, {'progression': 0}, 
        [],
        (3, 3), 
        [Field(bet_amount=10.0)]
    ),
    (
        6, 9, {'progression': 1}, 
        [],
        (6, 3), 
        [Field(bet_amount=20.0)]
    ),
    (
        6, 5, {'progression': 0}, 
        [],
        (3, 2), 
        [Field(bet_amount=10.0)]
    )
])
def test_dicedoctor_integration(point, last_roll, strat_info, bets_before, dice_result, bets_after):
    table = Table()
    strategy = DiceDoctor()
    strategy.current_progression = strat_info['progression']
    table.add_player(bankroll=float("inf"), strategy=strategy) # ADD STRATEGY HERE
    table.point.number = point
    table.last_roll = last_roll
    table.players[0].bets_on_table = bets_before
    table.dice.result = dice_result
    table.add_player_bets()
    assert table.players[0].bets_on_table == bets_after