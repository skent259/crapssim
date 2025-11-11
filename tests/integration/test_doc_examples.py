import pytest

import crapssim


def test_supported_bets_example_1():
    from crapssim.bet import Boxcars as Midnight

    my_bet = Midnight(1)  # $1 bet on 12 in the next roll
    # Note, bet will still print out as `Boxcars(amount=1.0)`

    assert isinstance(my_bet, crapssim.bet.Boxcars)


def test_supported_bets_example_2():
    from crapssim.bet import Boxcars

    class Midnight(Boxcars):
        pass

    my_bet = Midnight(1)  # $1 bet on 12 in the next roll
    # Prints out as `Mignight(amount=1.0)`

    assert isinstance(my_bet, crapssim.bet.Boxcars)


def test_supported_bets_example_3():
    from crapssim.bet import Yo
    from crapssim.strategy.single_bet import BetSingle

    class MyYo(Yo):
        payout_ratio: int = 14  # vs 15 in Yo

    my_bet = MyYo(1)

    class BetMyYo(BetSingle):
        """Place a Yo bet if none currently placed."""

        bet_type = MyYo

    my_strategy = BetMyYo(bet_amount=1)

    assert my_bet.payout_ratio == 14
    assert my_strategy.bet_type == MyYo
