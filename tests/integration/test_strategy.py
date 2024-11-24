import pytest

from crapssim import Table
from crapssim.bet import Come, DontCome, DontPass, Field, Odds, PassLine, Place
from crapssim.strategy import (
    BetDontPass,
    BetIfTrue,
    BetPassLine,
    BetPlace,
    DontPassOddsMultiplier,
    PassLineOddsMultiplier,
)
from crapssim.strategy.core import WinProgression
from crapssim.strategy.examples import (
    DiceDoctor,
    HammerLock,
    IronCross,
    Knockout,
    Pass2Come,
    PassLinePlace68,
    PassLinePlace68Move59,
    Place68DontCome2Odds,
    Place68PR,
    Place682Come,
    Risk12,
)
from crapssim.table import TableUpdate


@pytest.mark.parametrize(
    ["strategy", "rolls", "correct_bets"],
    [
        (BetPassLine(bet_amount=5), [], [PassLine(amount=5.0)]),
        (BetPassLine(bet_amount=5), [(4, 4)], [PassLine(amount=5.0)]),
        (
            BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier=1),
            [],
            [PassLine(amount=5.0)],
        ),
        (
            BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier=1),
            [(4, 4)],
            [Odds(PassLine, 8, amount=5.0), PassLine(amount=5.0)],
        ),
        (
            BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier=1),
            [(4, 4), (3, 3)],
            [Odds(PassLine, 8, amount=5.0), PassLine(amount=5.0)],
        ),
        (
            BetPassLine(bet_amount=5)
            + PassLineOddsMultiplier(
                odds_multiplier={4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
            ),
            [],
            [PassLine(amount=5.0)],
        ),
        (
            BetPassLine(bet_amount=5)
            + PassLineOddsMultiplier(
                odds_multiplier={4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
            ),
            [(6, 4)],
            [PassLine(amount=5.0), Odds(PassLine, 10, amount=15.0)],
        ),
        (
            BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier=2),
            [(2, 2)],
            [PassLine(amount=5.0), Odds(PassLine, 4, amount=10.0)],
        ),
        (
            BetPassLine(bet_amount=5)
            + PassLineOddsMultiplier(
                odds_multiplier={4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}
            ),
            [(3, 4), (3, 3)],
            [PassLine(amount=5.0), Odds(PassLine, 6, amount=25.0)],
        ),
        (Pass2Come(bet_amount=5), [], [PassLine(amount=5.0)]),
        (Pass2Come(bet_amount=5), [(4, 5)], [Come(amount=5.0), PassLine(amount=5.0)]),
        (
            Pass2Come(bet_amount=5),
            [(4, 5), (5, 5)],
            [PassLine(amount=5.0), Come(amount=5.0, number=10), Come(amount=5.0)],
        ),
        (
            Pass2Come(bet_amount=5),
            [(4, 5), (5, 5), (3, 3)],
            [
                PassLine(amount=5.0),
                Come(amount=5.0, number=10),
                Come(amount=5.0, number=6),
            ],
        ),
        (BetPlace(place_bet_amounts={4: 5}, skip_point=True), [], []),
        (
            BetPlace(place_bet_amounts={5: 5}, skip_point=True),
            [(3, 3)],
            [Place(number=5, amount=5.0)],
        ),
        (BetPlace(place_bet_amounts={5: 5}, skip_point=True), [(3, 2)], []),
        (
            BetPlace(place_bet_amounts={5: 5}, skip_point=False),
            [(3, 2)],
            [Place(number=5, amount=5.0)],
        ),
        (
            PassLinePlace68(
                pass_line_amount=5, six_amount=6, eight_amount=6, skip_point=True
            ),
            [(4, 5)],
            [
                Place(number=8, amount=6.0),
                PassLine(amount=5.0),
                Place(number=6, amount=6.0),
            ],
        ),
        (
            PassLinePlace68(
                pass_line_amount=5, six_amount=6, eight_amount=6, skip_point=True
            ),
            [(2, 4)],
            [Place(number=8, amount=6.0), PassLine(amount=5.0)],
        ),
        (BetDontPass(bet_amount=5), [], [DontPass(amount=5.0)]),
        (
            BetDontPass(bet_amount=5) + DontPassOddsMultiplier(odds_multiplier=1),
            [],
            [DontPass(amount=5.0)],
        ),
        (
            BetDontPass(bet_amount=5) + DontPassOddsMultiplier(odds_multiplier=6),
            [(3, 3)],
            [Odds(DontPass, 6, amount=30.0), DontPass(amount=5.0)],
        ),
        (
            PassLinePlace68Move59(
                pass_line_amount=5, six_eight_amount=6, five_nine_amount=5
            ),
            [],
            [PassLine(amount=5.0)],
        ),
        (
            PassLinePlace68Move59(
                pass_line_amount=5, six_eight_amount=6, five_nine_amount=5
            ),
            [(3, 3)],
            [
                Place(number=8, amount=6.0),
                Place(number=5, amount=5.0),
                PassLine(amount=5.0),
            ],
        ),
        (
            PassLinePlace68Move59(
                pass_line_amount=5, six_eight_amount=6, five_nine_amount=5
            ),
            [(3, 3), (4, 4)],
            [
                Place(number=8, amount=6.0),
                Place(number=5, amount=5.0),
                PassLine(amount=5.0),
            ],
        ),
        (
            Place682Come(pass_come_amount=5, six_eight_amount=6, five_nine_amount=5),
            [],
            [PassLine(amount=5.0)],
        ),
        (
            Place682Come(pass_come_amount=5, six_eight_amount=6, five_nine_amount=5),
            [(3, 3)],
            [
                PassLine(5),
                Place(number=8, amount=6.0),
                Place(number=5, amount=5),
                Come(amount=5.0),
            ],
        ),
        (
            Place682Come(pass_come_amount=5, six_eight_amount=6, five_nine_amount=5),
            [(3, 3), (3, 6)],
            [
                Place(number=8, amount=6.0),
                Come(amount=5.0, number=9),
                PassLine(amount=5.0),
                Place(number=5, amount=5),
            ],
        ),
        (
            Place682Come(pass_come_amount=5, six_eight_amount=6, five_nine_amount=5),
            [(3, 3), (4, 4)],
            [
                Place(number=9, amount=5.0),
                Place(number=5, amount=5.0),
                PassLine(amount=5.0),
                Come(amount=5.0, number=8),
            ],
        ),
        (IronCross(base_amount=5), [], [PassLine(amount=5.0)]),
        (
            IronCross(base_amount=5),
            [(4, 4)],
            [
                PassLine(amount=5.0),
                Place(number=5, amount=10.0),
                Place(number=6, amount=12.0),
                Field(amount=5.0),
                Odds(PassLine, 8, amount=10.0),
            ],
        ),
        (HammerLock(base_amount=5), [], [DontPass(amount=5.0), PassLine(amount=5.0)]),
        (
            HammerLock(base_amount=5),
            [(3, 3)],
            [
                Odds(DontPass, 6, amount=30.0),
                PassLine(amount=5.0),
                Place(number=8, amount=12.0),
                DontPass(amount=5.0),
                Place(number=6, amount=12.0),
            ],
        ),
        (
            HammerLock(base_amount=5),
            [(3, 3), (4, 4)],
            [
                Place(number=8, amount=6.0),
                Place(number=9, amount=5.0),
                Odds(DontPass, 6, amount=30.0),
                PassLine(amount=5.0),
                Place(number=6, amount=6.0),
                DontPass(amount=5.0),
                Place(number=5, amount=5.0),
            ],
        ),
        (
            BetIfTrue(
                bet=PassLine(amount=5.0), key=lambda p: p.table.point.status == "Off"
            ),
            [],
            [PassLine(amount=5.0)],
        ),
        (Risk12(), [], [PassLine(amount=5.0), Field(amount=5.0)]),
        (
            Risk12(),
            [(1, 3)],
            [
                Place(number=8, amount=6.0),
                PassLine(amount=5.0),
                Place(number=6, amount=6.0),
            ],
        ),
        (
            Risk12(),
            [(5, 6), (2, 3)],
            [
                Place(number=8, amount=6.0),
                PassLine(amount=5.0),
                Place(number=6, amount=6.0),
            ],
        ),
        (Knockout(bet_amount=5), [], [DontPass(amount=5.0), PassLine(amount=5.0)]),
        (
            Knockout(bet_amount=5),
            [(4, 2)],
            [
                DontPass(amount=5.0),
                PassLine(amount=5.0),
                Odds(PassLine, 6, amount=25.0),
            ],
        ),
        (DiceDoctor(), [], [Field(amount=10.0)]),
        (DiceDoctor(), [(1, 1)], [Field(amount=20.0)]),
        (DiceDoctor(), [(1, 1), (5, 6)], [Field(amount=15.0)]),
        (DiceDoctor(), [(1, 1), (5, 6), (5, 5)], [Field(amount=30.0)]),
        (WinProgression(Place(6, 12), [1, 2, 3]), [], [Place(6, amount=12.0)]),
        (WinProgression(Place(6, 12), [1, 2, 3]), [(3, 3)], [Place(6, amount=24.0)]),
        (
            WinProgression(Place(6, 12), [1, 2, 3]),
            [(3, 3), (2, 4)],
            [Place(6, amount=36.0)],
        ),
        (
            WinProgression(Place(6, 12), [1, 2, 3]),
            [(3, 3), (2, 4), (3, 3)],
            [Place(6, amount=36.0)],
        ),
        (Place68DontCome2Odds(six_eight_amount=6, dont_come_amount=5), [], []),
        (
            Place68DontCome2Odds(six_eight_amount=6, dont_come_amount=5),
            [(4, 4)],
            [
                Place(number=8, amount=6.0),
                Place(number=6, amount=6.0),
                DontCome(amount=5.0),
            ],
        ),
        (
            Place68DontCome2Odds(six_eight_amount=6, dont_come_amount=5),
            [(4, 4), (2, 2)],
            [
                Place(number=8, amount=6.0),
                Odds(DontCome, 4, amount=10.0),
                Place(number=6, amount=6.0),
                DontCome(amount=5.0, number=4),
            ],
        ),
        (Place68PR(bet_amount=6), [], []),
        (
            Place68PR(bet_amount=6),
            [(4, 4)],
            [Place(number=8, amount=6.0), Place(number=6, amount=6.0)],
        ),
        (
            Place68PR(bet_amount=6),
            [(2, 2), (4, 4)],
            [Place(number=8, amount=12.0), Place(number=6, amount=6.0)],
        ),
        (
            Place68PR(bet_amount=6),
            [(2, 2), (4, 4), (4, 4)],
            [Place(number=8, amount=6.0), Place(number=6, amount=6.0)],
        ),
        (
            Place68PR(bet_amount=6),
            [(2, 2), (4, 4), (4, 4), (4, 4)],
            [Place(number=8, amount=12.0), Place(number=6, amount=6.0)],
        ),
        (
            Place68PR(bet_amount=6),
            [(2, 2), (3, 3), (3, 3), (3, 3)],
            [Place(number=8, amount=6.0), Place(number=6, amount=12.0)],
        ),
    ],
)
def test_strategies_compare_bets(
    strategy, rolls: list[tuple[int, int]], correct_bets: {(str, str, float)}
):
    table = Table()
    table.add_player(strategy=strategy)
    table.fixed_run(rolls, verbose=False)
    TableUpdate().run_strategies(table)

    bets = table.players[0].bets

    assert set(bets) == set(correct_bets)
