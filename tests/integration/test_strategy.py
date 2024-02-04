import pytest

from crapssim import Table
from crapssim.bet import PassLine, Come, Place, DontPass, Field, DontCome, Odds
from crapssim.strategy import BetPassLine, PassLineOddsMultiplier, BetPlace, BetDontPass, \
    DontPassOddsMultiplier, \
    BetIfTrue
from crapssim.strategy.examples import Pass2Come, PassLinePlace68, PassLinePlace68Move59, \
    Place682Come, IronCross, HammerLock, Risk12, Knockout, DiceDoctor, Place68DontCome2Odds, \
    Place68CPR
from crapssim.table import TableUpdate


@pytest.mark.parametrize(['strategy', 'rolls', 'correct_bets'],
[(BetPassLine(bet_amount=5), [], [PassLine(bet_amount=5.0)]),
 (BetPassLine(bet_amount=5), [(4, 4)], [PassLine(bet_amount=5.0)]),
 (BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier=1),
  [],
  [PassLine(bet_amount=5.0)]),
 (BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier=1),
  [(4, 4)],
  [Odds(PassLine, 8, bet_amount=5.0), PassLine(bet_amount=5.0)]),
 (BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier=1),
  [(4, 4), (3, 3)],
  [Odds(PassLine, 8, bet_amount=5.0), PassLine(bet_amount=5.0)]),
 (BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier={4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}),
  [],
  [PassLine(bet_amount=5.0)]),
 (BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier={4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}),
  [(6, 4)],
  [PassLine(bet_amount=5.0), Odds(PassLine, 10, bet_amount=15.0)]),
 (BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier=2),
  [(2, 2)],
  [PassLine(bet_amount=5.0), Odds(PassLine, 4, bet_amount=10.0)]),
 (BetPassLine(bet_amount=5) + PassLineOddsMultiplier(odds_multiplier={4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3}),
  [(3, 4), (3, 3)],
  [PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=25.0)]),
 (Pass2Come(bet_amount=5), [], [PassLine(bet_amount=5.0)]),
 (Pass2Come(bet_amount=5),
  [(4, 5)],
  [Come(bet_amount=5.0), PassLine(bet_amount=5.0)]),
 (Pass2Come(bet_amount=5),
  [(4, 5), (5, 5)],
  [PassLine(bet_amount=5.0),
   Come(bet_amount=5.0, point=10),
   Come(bet_amount=5.0)]),
 (Pass2Come(bet_amount=5),
  [(4, 5), (5, 5), (3, 3)],
  [PassLine(bet_amount=5.0),
   Come(bet_amount=5.0, point=10),
   Come(bet_amount=5.0, point=6)]),
 (BetPlace(place_bet_amounts={4: 5}, skip_point=True), [], []),
 (BetPlace(place_bet_amounts={5: 5}, skip_point=True),
  [(3, 3)],
  [Place(number=5, bet_amount=5.0)]),
 (BetPlace(place_bet_amounts={5: 5}, skip_point=True), [(3, 2)], []),
 (BetPlace(place_bet_amounts={5: 5}, skip_point=False),
  [(3, 2)],
  [Place(number=5, bet_amount=5.0)]),
 (PassLinePlace68(pass_line_amount=5, six_amount=6, eight_amount=6, skip_point=True),
  [(4, 5)],
  [Place(number=8, bet_amount=6.0),
   PassLine(bet_amount=5.0),
   Place(number=6, bet_amount=6.0)]),
 (PassLinePlace68(pass_line_amount=5, six_amount=6, eight_amount=6, skip_point=True),
  [(2, 4)],
  [Place(number=8, bet_amount=6.0), PassLine(bet_amount=5.0)]),
 (BetDontPass(bet_amount=5), [], [DontPass(bet_amount=5.0)]),
 (BetDontPass(bet_amount=5) + DontPassOddsMultiplier(odds_multiplier=1),
  [],
  [DontPass(bet_amount=5.0)]),
 (BetDontPass(bet_amount=5) + DontPassOddsMultiplier(odds_multiplier=6),
  [(3, 3)],
  [Odds(DontPass, 6, bet_amount=30.0), DontPass(bet_amount=5.0)]),
 (PassLinePlace68Move59(pass_line_amount=5, six_eight_amount=6, five_nine_amount=5),
  [],
  [PassLine(bet_amount=5.0)]),
 (PassLinePlace68Move59(pass_line_amount=5, six_eight_amount=6, five_nine_amount=5),
  [(3, 3)],
  [Place(number=8, bet_amount=6.0),
   Place(number=5, bet_amount=5.0),
   PassLine(bet_amount=5.0)]),
 (PassLinePlace68Move59(pass_line_amount=5, six_eight_amount=6, five_nine_amount=5),
  [(3, 3), (4, 4)],
  [Place(number=8, bet_amount=6.0),
   Place(number=5, bet_amount=5.0),
   PassLine(bet_amount=5.0)]),
 (Place682Come(pass_come_amount=5, six_eight_amount=6, five_nine_amount=5),
  [],
  [PassLine(bet_amount=5.0)]),
 (Place682Come(pass_come_amount=5, six_eight_amount=6, five_nine_amount=5),
  [(3, 3)],
  [PassLine(5), Place(number=8, bet_amount=6.0),
   Place(number=5, bet_amount=5),
   Come(bet_amount=5.0)]),
 (Place682Come(pass_come_amount=5, six_eight_amount=6, five_nine_amount=5),
  [(3, 3), (3, 6)],
  [Place(number=8, bet_amount=6.0),
   Come(bet_amount=5.0, point=9),
   PassLine(bet_amount=5.0),
   Place(number=5, bet_amount=5)]),
 (Place682Come(pass_come_amount=5, six_eight_amount=6, five_nine_amount=5),
  [(3, 3), (4, 4)],
  [Place(number=9, bet_amount=5.0),
   Place(number=5, bet_amount=5.0),
   PassLine(bet_amount=5.0),
   Come(bet_amount=5.0, point=8)]),
 (IronCross(base_amount=5), [], [PassLine(bet_amount=5.0)]),
 (IronCross(base_amount=5),
  [(4, 4)],
  [PassLine(bet_amount=5.0),
   Place(number=5, bet_amount=10.0),
   Place(number=6, bet_amount=12.0),
   Field(bet_amount=5.0),
   Odds(PassLine, 8, bet_amount=10.0)]),
 (HammerLock(base_amount=5),
  [],
  [DontPass(bet_amount=5.0), PassLine(bet_amount=5.0)]),
 (HammerLock(base_amount=5),
  [(3, 3)],
  [Odds(DontPass, 6, bet_amount=30.0),
   PassLine(bet_amount=5.0),
   Place(number=8, bet_amount=12.0),
   DontPass(bet_amount=5.0),
   Place(number=6, bet_amount=12.0)]),
 (HammerLock(base_amount=5),
  [(3, 3), (4, 4)],
  [Place(number=8, bet_amount=6.0),
   Place(number=9, bet_amount=5.0),
   Odds(DontPass, 6, bet_amount=30.0),
   PassLine(bet_amount=5.0),
   Place(number=6, bet_amount=6.0),
   DontPass(bet_amount=5.0),
   Place(number=5, bet_amount=5.0)]),
 (BetIfTrue(bet=PassLine(bet_amount=5.0), key=lambda p: p.table.point.status == 'Off'),
  [],
  [PassLine(bet_amount=5.0)]),
 (Risk12(), [], [PassLine(bet_amount=5.0), Field(bet_amount=5.0)]),
 (Risk12(),
  [(1, 3)],
  [Place(number=8, bet_amount=6.0),
   PassLine(bet_amount=5.0),
   Place(number=6, bet_amount=6.0)]),
 (Risk12(),
  [(5, 6), (2, 3)],
  [Place(number=8, bet_amount=6.0),
   PassLine(bet_amount=5.0),
   Place(number=6, bet_amount=6.0)]),
 (Knockout(bet_amount=5),
  [],
  [DontPass(bet_amount=5.0), PassLine(bet_amount=5.0)]),
 (Knockout(bet_amount=5),
  [(4, 2)],
  [DontPass(bet_amount=5.0), PassLine(bet_amount=5.0), Odds(PassLine, 6, bet_amount=25.0)]),
 (DiceDoctor(), [], [Field(bet_amount=10.0)]),
 (DiceDoctor(), [(1, 1), (5, 6), (5, 5)], [Field(bet_amount=30.0)]),
 (Place68DontCome2Odds(six_eight_amount=6, dont_come_amount=5), [], []),
 (Place68DontCome2Odds(six_eight_amount=6, dont_come_amount=5),
  [(4, 4)],
  [Place(number=8, bet_amount=6.0),
   Place(number=6, bet_amount=6.0),
   DontCome(bet_amount=5.0)]),
 (Place68DontCome2Odds(six_eight_amount=6, dont_come_amount=5),
  [(4, 4), (2, 2)],
  [Place(number=8, bet_amount=6.0),
   Odds(DontCome, 4, bet_amount=10.0),
   Place(number=6, bet_amount=6.0),
   DontCome(bet_amount=5.0, point=4)]),
 (Place68CPR(bet_amount=6), [], []),
 (Place68CPR(bet_amount=6),
  [(4, 4)],
  [Place(number=8, bet_amount=6.0), Place(number=6, bet_amount=6.0)]),
 (Place68CPR(bet_amount=6),
  [(2, 2), (4, 4)],
  [Place(number=8, bet_amount=12.0), Place(number=6, bet_amount=6.0)]),
 (Place68CPR(bet_amount=6),
  [(2, 2), (4, 4), (4, 4)],
  [Place(number=8, bet_amount=6.0), Place(number=6, bet_amount=6.0)]),
 (Place68CPR(bet_amount=6),
  [(2, 2), (4, 4), (4, 4), (4, 4)],
  [Place(number=8, bet_amount=12.0), Place(number=6, bet_amount=6.0)])])
def test_strategies_compare_bets(strategy, rolls: list[tuple[int, int]],
                                 correct_bets: {(str, str, float)}):
    table = Table()
    table.add_player(strategy=strategy)
    table.fixed_run(rolls, verbose=False)
    TableUpdate().run_strategies(table)

    bets = table.players[0].bets

    assert set(bets) == set(correct_bets)
