import pytest

from crapssim.dice import Dice


@pytest.fixture
def d1():
    return Dice()


def test_no_rolls(d1):
    assert d1.n_rolls == 0


def test_one_roll(d1):
    d1.roll()
    assert d1.n_rolls == 1


def test_many_roll(d1):
    d1.roll()
    d1.roll()
    d1.roll()
    d1.roll()
    assert d1.n_rolls == 4


@pytest.mark.parametrize(
    "roll, total",
    [
        ([3, 4], 7),
        ([1, 1], 2),
        ([4, 3], 7),
        ([5, 6], 11),
    ],
)
def test_fixed_roll(d1, roll, total):
    d1.fixed_roll(roll)
    assert d1.result == tuple(roll)
    assert d1.total == total


@pytest.mark.parametrize("seed", [8, 15, 21234, 0])
def test_roll_seed_idential(seed):
    d1 = Dice(seed)
    d2 = Dice(seed)

    d1.roll()
    d2.roll()
    assert d1.result == d2.result
    assert d1.total == d2.total
