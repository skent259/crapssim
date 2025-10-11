import pytest

from crapssim import Table
from crapssim.bet import Come, DontCome, DontPass, Field, Fire, Odds, PassLine, Place
from crapssim.strategy import (
    AddIfTrue,
    BetDontPass,
    BetPassLine,
    BetPlace,
    DontPassOddsMultiplier,
    PassLineOddsMultiplier,
)
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
    PlaceInside,
    Risk12,
)
from crapssim.strategy.single_bet import BetAll, BetFire
from crapssim.strategy.tools import AddIfNewShooter, AddIfTrue, WinProgression
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
            AddIfTrue(
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
        (
            Risk12(base_amount=5),
            [(2, 6), (6, 2), (1, 2), (1, 4)],
            [
                PassLine(amount=5.0),
            ],
        ),
        (
            Risk12(base_amount=5),
            [(2, 5), (2, 3)],
            [
                PassLine(amount=5.0),
            ],
        ),
        (
            Risk12(base_amount=5),
            [(2, 5), (2, 3), (3, 2)],
            [PassLine(amount=5.0), Field(amount=5.0)],
        ),
        (Knockout(base_amount=5), [], [DontPass(amount=5.0), PassLine(amount=5.0)]),
        (
            Knockout(base_amount=5),
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
        (Place68PR(base_amount=6), [], []),
        (
            Place68PR(base_amount=6),
            [(4, 4)],
            [Place(number=8, amount=6.0), Place(number=6, amount=6.0)],
        ),
        (
            Place68PR(base_amount=6),
            [(2, 2), (4, 4)],
            [Place(number=8, amount=12.0), Place(number=6, amount=6.0)],
        ),
        (
            Place68PR(base_amount=6),
            [(2, 2), (4, 4), (4, 4)],
            [Place(number=8, amount=6.0), Place(number=6, amount=6.0)],
        ),
        (
            Place68PR(base_amount=6),
            [(2, 2), (4, 4), (4, 4), (4, 4)],
            [Place(number=8, amount=12.0), Place(number=6, amount=6.0)],
        ),
        (
            Place68PR(base_amount=6),
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


def test_strategies_in_simulation_persistent_features():

    bankroll = 100
    strategies = {"Fire 1": AddIfNewShooter(Fire(1)), "Fire 2": BetFire(1)}

    # Simulation 1, five fire points hit
    outcomes = [
        (2, 2),
        (2, 2),
        (2, 3),
        (2, 3),
        (3, 3),
        (3, 3),
        (4, 4),
        (4, 4),
        (4, 5),
        (4, 5),
        (4, 4),  # set the last point
        (1, 6),  # seven-out
    ]
    table = Table()
    for s in strategies:
        table.add_player(bankroll, strategy=strategies[s], name=s)
    table.fixed_run(outcomes, verbose=False)
    for p in table.players:
        print(f"{p.name}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")

    assert p.bankroll == bankroll + table.settings["fire_payouts"][5]

    # Simulation 2, no fire points hit
    outcomes = [
        (2, 2),  # set a point
        (1, 6),  # seven-out
    ]
    table = Table()
    for s in strategies:
        table.add_player(bankroll, strategy=strategies[s], name=s)
    table.fixed_run(outcomes, verbose=False)
    for p in table.players:
        print(f"{p.name}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")

    assert p.bankroll == bankroll - 1


def test_placeinside_with_betpointon():

    bankroll = 100
    strategy = PlaceInside(10)

    # Simulation 1, point hit, then come-out seven, nothing should happen
    outcomes = [
        (2, 2),
        (2, 2),
        (1, 6),  # come-out seven, should not lose
    ]
    table = Table()
    table.add_player(bankroll, strategy)

    table.fixed_run(outcomes, verbose=False)
    for p in table.players:
        print(f"{p.name}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")

    assert p.total_player_cash == bankroll
    assert p.bets == []

    # Simulation 2, point hit, then come-out seven, reset point and win one
    outcomes = [
        (2, 2),
        (2, 2),
        (1, 6),  # come-out seven, should not lose
        (3, 3),
        (4, 4),  # 8 wins
        (1, 2),
    ]
    table = Table()
    table.add_player(bankroll, strategy)

    table.fixed_run(outcomes, verbose=True)
    for p in table.players:
        print(f"{p.name}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")

    assert p.total_player_cash == bankroll + 14
    assert len(p.bets) == 4


def test_ATS_in_simulation():

    bankroll = 100
    strategy = BetAll(1)

    # results = []
    for i in range(100):

        table = Table(seed=8)
        table.add_player(bankroll, strategy)

        table.run(max_rolls=200, max_shooter=float("inf"), verbose=False, runout=True)

        p = table.players[0]
        res = [i, p.name, p.bankroll, table.dice.n_rolls]
        print(res)
        assert p.bankroll < 500  # very unlikely to win >2 ATS in one session


def test_ATS_in_simulation_persistent_features():

    bankroll = 100
    strategies = {
        "All": BetAll(1),
    }

    # Simulation 1, All hits

    # Simulation 1, five fire points hit
    outcomes = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (6, 2),
        (6, 3),
        (6, 4),
        (6, 5),
        (6, 6),  # last one
        (1, 6),  # seven-out
    ]
    table = Table()
    for s in strategies:
        table.add_player(bankroll, strategy=strategies[s], name=s)
    table.fixed_run(outcomes, verbose=False)
    for p in table.players:
        print(f"{p.name}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")

    assert p.bankroll == bankroll + table.settings["ATS_payouts"]["all"]

    # Simulation 2, no fire points hit
    outcomes = [
        (2, 2),  # set a point
        (1, 6),  # seven-out
    ]
    table = Table()
    for s in strategies:
        table.add_player(bankroll, strategy=strategies[s], name=s)
    table.fixed_run(outcomes, verbose=False)
    for p in table.players:
        print(f"{p.name}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")

    assert p.bankroll == bankroll - 1
