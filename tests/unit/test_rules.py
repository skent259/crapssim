import pytest

from crapssim.rules import AbstractRules, ClassicRules, CraplessRules


@pytest.fixture
def base_rules():
    return AbstractRules()


@pytest.fixture
def classic_rules():
    return ClassicRules()


@pytest.fixture
def crapless_rules():
    return CraplessRules()


def test_base_point_numbers(base_rules):
    assert base_rules.point_numbers() == []


def test_base_point_winners_none_returns_empty(base_rules):
    assert base_rules.point_winners(None) == []


@pytest.mark.parametrize("point", [2, 4, 10, 12])
def test_base_point_winners_number_returns_number(base_rules, point):
    assert base_rules.point_winners(point) == [point]


@pytest.mark.parametrize("point", [None, 4, 6, 10])
def test_base_point_losers_always_seven(base_rules, point):
    assert base_rules.point_losers(point) == [7]


def test_base_allow_dont_pass(base_rules):
    assert base_rules.allow_dont_pass() is True


def test_base_allow_dont_come(base_rules):
    assert base_rules.allow_dont_come() is True


def test_classic_point_numbers(classic_rules):
    assert classic_rules.point_numbers() == [4, 5, 6, 8, 9, 10]


def test_classic_come_out_winners(classic_rules):
    assert classic_rules.come_out_winners() == [7, 11]


def test_classic_come_out_losers(classic_rules):
    assert classic_rules.come_out_losers() == [2, 3, 12]


def test_classic_inherits_dont_side_allowed(classic_rules):
    assert classic_rules.allow_dont_pass() is True
    assert classic_rules.allow_dont_come() is True


def test_crapless_point_numbers(crapless_rules):
    assert crapless_rules.point_numbers() == [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]


def test_crapless_come_out_winners(crapless_rules):
    assert crapless_rules.come_out_winners() == [7]


def test_crapless_come_out_losers(crapless_rules):
    assert crapless_rules.come_out_losers() == []


def test_crapless_disallows_dont_side(crapless_rules):
    assert crapless_rules.allow_dont_pass() is False
    assert crapless_rules.allow_dont_come() is False


def test_cross_variant_differences(classic_rules, crapless_rules):
    assert 11 in classic_rules.come_out_winners()
    assert 11 not in crapless_rules.come_out_winners()
    assert {2, 3, 11, 12}.issubset(set(crapless_rules.point_numbers()))
    assert {2, 3, 11, 12}.isdisjoint(set(classic_rules.point_numbers()))
