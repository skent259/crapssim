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


@pytest.mark.parametrize("roll, total", [
    ([3, 4], 7),
    ([1, 1], 2),
    ([4, 3], 7),
    ([5, 6], 11),
])
def test_fixed_roll(d1, roll, total):
    d1.fixed_roll(roll)
    assert d1.result == roll
    assert d1.total == total
