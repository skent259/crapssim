import pytest

from crapssim.bet import Buy, Lay, _compute_vig
from crapssim.table import Table, TableUpdate


@pytest.mark.parametrize(
    ("rounding", "floor", "bet", "expected"),
    [
        ("none", 0.0, 20.0, 1.0),
        ("none", 0.0, 25.0, 1.25),
        ("none", 0.0, 50.0, 2.50),
        ("none", 0.0, 85.0, 4.25),
        ("none", 2.0, 20.0, 2.0),
        ("ceil_dollar", 0.0, 20.0, 1.0),
        ("ceil_dollar", 0.0, 25.0, 2.0),
        ("ceil_dollar", 0.0, 50.0, 3.0),
        ("ceil_dollar", 0.0, 85.0, 5.0),
        ("ceil_dollar", 2.0, 20.0, 2.0),
        ("nearest_dollar", 0.0, 20.0, 1.0),
        ("nearest_dollar", 0.0, 25.0, 1.0),
        ("nearest_dollar", 0.0, 50.0, 3.0),
        ("nearest_dollar", 0.0, 85.0, 4.0),
        ("nearest_dollar", 1.0, 5.0, 1.0),
    ],
)
def test_compute_vig_expected_values(rounding, floor, bet, expected):
    result = _compute_vig(
        bet,
        rounding=rounding,
        floor=floor,
    )

    assert abs(result - expected) < 1e-9


def test_buy_upfront_vig_debits_bankroll():
    table = Table()
    table.settings["vig_paid_on_win"] = False
    player = table.add_player(bankroll=100)

    for _ in range(5):
        player.add_bet(Buy(4, 20))

    assert len(player.bets) == 1
    placed_bet = player.bets[0]
    assert placed_bet.amount == 80
    assert player.bankroll == pytest.approx(100 - 4 * (20 + 1))


def test_buy_upfront_vig_loss_is_principal_plus_vig():
    table = Table()
    table.settings["vig_paid_on_win"] = False
    player = table.add_player(bankroll=100)

    starting_bankroll = player.bankroll
    player.add_bet(Buy(4, 20))
    assert player.bankroll == pytest.approx(starting_bankroll - 21)

    TableUpdate.roll(table, fixed_outcome=(3, 4))
    TableUpdate.update_bets(table)

    assert not player.bets
    assert player.bankroll == pytest.approx(starting_bankroll - 21)


def test_vig_paid_on_win_does_not_charge_at_placement():
    table = Table()
    table.settings["vig_paid_on_win"] = True
    player = table.add_player(bankroll=100)

    player.add_bet(Buy(4, 20))
    assert player.bankroll == pytest.approx(80)
    active_bet = player.bets[0]

    gross_win = active_bet.payout_ratio * active_bet.amount
    vig = _compute_vig(active_bet.amount)

    TableUpdate.roll(table, fixed_outcome=(2, 2))
    TableUpdate.update_bets(table)

    assert player.bankroll == pytest.approx(100 + gross_win - vig)


def test_vig_for_lay_is_on_win_amount():
    table = Table()
    table.settings["vig_paid_on_win"] = True
    table.settings["vig_rounding"] = "none"
    player = table.add_player(bankroll=100)

    player.add_bet(Lay(4, 40))
    assert player.bankroll == pytest.approx(60)
    active_bet = player.bets[0]

    gross_win = active_bet.payout_ratio * active_bet.amount
    vig = _compute_vig(gross_win)  # based on win amount

    TableUpdate.roll(table, fixed_outcome=(3, 4))
    TableUpdate.update_bets(table)

    assert player.bankroll == pytest.approx(100 + gross_win - vig)
