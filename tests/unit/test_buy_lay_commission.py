import math

import pytest

from crapssim.bet import Buy, _compute_commission
from crapssim.table import Table, TableUpdate


def test_buy_upfront_vig_debits_bankroll():
    table = Table()
    table.settings["buy_vig_on_win"] = False
    player = table.add_player(bankroll=100)

    for _ in range(5):
        player.add_bet(Buy(4, 20))

    assert len(player.bets) == 1
    placed_bet = player.bets[0]
    assert placed_bet.amount == 80
    assert player.bankroll == pytest.approx(100 - 4 * (20 + 1))


def test_buy_upfront_vig_loss_is_principal_plus_vig():
    table = Table()
    table.settings["buy_vig_on_win"] = False
    player = table.add_player(bankroll=100)

    starting_bankroll = player.bankroll
    player.add_bet(Buy(4, 20))
    assert player.bankroll == pytest.approx(starting_bankroll - 21)

    TableUpdate.roll(table, fixed_outcome=(3, 4))
    TableUpdate.update_bets(table)

    assert not player.bets
    assert player.bankroll == pytest.approx(starting_bankroll - 21)


def test_buy_vig_on_win_does_not_charge_at_placement():
    table = Table()
    table.settings["buy_vig_on_win"] = True
    player = table.add_player(bankroll=100)

    player.add_bet(Buy(4, 20))
    assert player.bankroll == pytest.approx(80)
    active_bet = player.bets[0]
    assert math.isclose(active_bet.vig_paid, 0.0)

    gross_win = active_bet.payout_ratio * active_bet.wager
    commission = _compute_commission(
        table, gross_win=gross_win, bet_amount=active_bet.wager
    )

    TableUpdate.roll(table, fixed_outcome=(2, 2))
    TableUpdate.update_bets(table)

    assert player.bankroll == pytest.approx(100 + gross_win - commission)
