import pytest

from crapssim import Table, Dice
from crapssim.bet import PassLine, Come, Odds
from crapssim.bet.hard_way import HardWay
from crapssim.bet.one_roll import Field, Any7, Two, Three, Yo, Boxcars, AnyCraps, CAndE
from crapssim.bet.pass_line import DontPass, DontCome
from crapssim.bet.place import Place
from crapssim.bet.side import Fire
from crapssim.point import Point
from crapssim.table import TableUpdate, TableSettings


@pytest.mark.parametrize('bet_one, bet_two', [
    (PassLine(5), PassLine(5)),
    (Come(5), Come(5)),
    (Odds(PassLine, 4, 5), Odds(PassLine, 4, 5)),
    (Odds(PassLine, 5, 5), Odds(PassLine, 5, 5)),
    (Odds(PassLine, 6, 5), Odds(PassLine, 6, 5)),
    (Odds(PassLine, 8, 5), Odds(PassLine, 8, 5)),
    (Odds(PassLine, 9, 5), Odds(PassLine, 9, 5)),
    (Odds(PassLine, 10, 5), Odds(PassLine, 10, 5)),
    (Place(4, 5), Place(4, 5)),
    (Place(5, 5), Place(5, 5)),
    (Place(6, 5), Place(6, 5)),
    (Place(8, 5), Place(8, 5)),
    (Place(9, 5), Place(9, 5)),
    (Place(10, 5), Place(10, 5)),
    (Field(5), Field(5)),
    (DontPass(5), DontPass(5)),
    (DontCome(5), DontCome(5)),
    (Any7(5), Any7(5)),
    (Two(5), Two(5)),
    (Three(5), Three(5)),
    (Yo(5), Yo(5)),
    (Boxcars(5), Boxcars(5)),
    (AnyCraps(5), AnyCraps(5)),
    (CAndE(5), CAndE(5)),
    (HardWay(4, 5), HardWay(4, 5)),
    (HardWay(6, 5), HardWay(6, 5)),
    (HardWay(8, 5), HardWay(8, 5)),
    (HardWay(10, 5), HardWay(10, 5)),
    (Fire(5), Fire(5))
])
def test_bet_equality(bet_one, bet_two):
    assert bet_one == bet_two


@pytest.mark.parametrize('bet_one, bet_two', [
    (PassLine(5), Come(5)),
    (PassLine(5), Odds(PassLine, 4, 5)),
    (PassLine(5), Odds(PassLine, 5, 5)),
    (PassLine(5), Odds(PassLine, 6, 5)),
    (PassLine(5), Odds(PassLine, 8, 5)),
    (PassLine(5), Odds(PassLine, 9, 5)),
    (PassLine(5), Odds(PassLine, 10, 5)),
    (PassLine(5), Place(4, 5)),
    (PassLine(5), Place(5, 5)),
    (PassLine(5), Place(6, 5)),
    (PassLine(5), Place(8, 5)),
    (PassLine(5), Place(9, 5)),
    (PassLine(5), Place(10, 5)),
    (PassLine(5), Field(5)),
    (PassLine(5), DontPass(5)),
    (PassLine(5), DontCome(5)),
    (PassLine(5), Any7(5)),
    (PassLine(5), Two(5)),
    (PassLine(5), Three(5)),
    (PassLine(5), Yo(5)),
    (PassLine(5), Boxcars(5)),
    (PassLine(5), AnyCraps(5)),
    (PassLine(5), CAndE(5)),
    (PassLine(5), HardWay(4, 5)),
    (PassLine(5), HardWay(6, 5)),
    (PassLine(5), HardWay(8, 5)),
    (PassLine(5), HardWay(10, 5)),
    (PassLine(5), Fire(5)),
    (Come(5), Odds(PassLine, 4, 5)),
    (Come(5), Odds(PassLine, 5, 5)),
    (Come(5), Odds(PassLine, 6, 5)),
    (Come(5), Odds(PassLine, 8, 5)),
    (Come(5), Odds(PassLine, 9, 5)),
    (Come(5), Odds(PassLine, 10, 5)),
    (Come(5), Place(4, 5)),
    (Come(5), Place(5, 5)),
    (Come(5), Place(6, 5)),
    (Come(5), Place(8, 5)),
    (Come(5), Place(9, 5)),
    (Come(5), Place(10, 5)),
    (Come(5), Field(5)),
    (Come(5), DontPass(5)),
    (Come(5), DontCome(5)),
    (Come(5), Any7(5)),
    (Come(5), Two(5)),
    (Come(5), Three(5)),
    (Come(5), Yo(5)),
    (Come(5), Boxcars(5)),
    (Come(5), AnyCraps(5)),
    (Come(5), CAndE(5)),
    (Come(5), HardWay(4, 5)),
    (Come(5), HardWay(6, 5)),
    (Come(5), HardWay(8, 5)),
    (Come(5), HardWay(10, 5)),
    (Come(5), Fire(5)),
    (Odds(PassLine, 4, 5), Odds(PassLine, 5, 5)),
    (Odds(PassLine, 4, 5), Odds(PassLine, 6, 5)),
    (Odds(PassLine, 4, 5), Odds(PassLine, 8, 5)),
    (Odds(PassLine, 4, 5), Odds(PassLine, 9, 5)),
    (Odds(PassLine, 4, 5), Odds(PassLine, 10, 5)),
    (Odds(PassLine, 4, 5), Place(4, 5)),
    (Odds(PassLine, 4, 5), Place(5, 5)),
    (Odds(PassLine, 4, 5), Place(6, 5)),
    (Odds(PassLine, 4, 5), Place(8, 5)),
    (Odds(PassLine, 4, 5), Place(9, 5)),
    (Odds(PassLine, 4, 5), Place(10, 5)),
    (Odds(PassLine, 4, 5), Field(5)),
    (Odds(PassLine, 4, 5), DontPass(5)),
    (Odds(PassLine, 4, 5), DontCome(5)),
    (Odds(PassLine, 4, 5), Any7(5)),
    (Odds(PassLine, 4, 5), Two(5)),
    (Odds(PassLine, 4, 5), Three(5)),
    (Odds(PassLine, 4, 5), Yo(5)),
    (Odds(PassLine, 4, 5), Boxcars(5)),
    (Odds(PassLine, 4, 5), AnyCraps(5)),
    (Odds(PassLine, 4, 5), CAndE(5)),
    (Odds(PassLine, 4, 5), HardWay(4, 5)),
    (Odds(PassLine, 4, 5), HardWay(6, 5)),
    (Odds(PassLine, 4, 5), HardWay(8, 5)),
    (Odds(PassLine, 4, 5), HardWay(10, 5)),
    (Odds(PassLine, 4, 5), Fire(5)),
    (Odds(PassLine, 5, 5), Odds(PassLine, 6, 5)),
    (Odds(PassLine, 5, 5), Odds(PassLine, 8, 5)),
    (Odds(PassLine, 5, 5), Odds(PassLine, 9, 5)),
    (Odds(PassLine, 5, 5), Odds(PassLine, 10, 5)),
    (Odds(PassLine, 5, 5), Place(4, 5)),
    (Odds(PassLine, 5, 5), Place(5, 5)),
    (Odds(PassLine, 5, 5), Place(6, 5)),
    (Odds(PassLine, 5, 5), Place(8, 5)),
    (Odds(PassLine, 5, 5), Place(9, 5)),
    (Odds(PassLine, 5, 5), Place(10, 5)),
    (Odds(PassLine, 5, 5), Field(5)),
    (Odds(PassLine, 5, 5), DontPass(5)),
    (Odds(PassLine, 5, 5), DontCome(5)),
    (Odds(PassLine, 5, 5), Any7(5)),
    (Odds(PassLine, 5, 5), Two(5)),
    (Odds(PassLine, 5, 5), Three(5)),
    (Odds(PassLine, 5, 5), Yo(5)),
    (Odds(PassLine, 5, 5), Boxcars(5)),
    (Odds(PassLine, 5, 5), AnyCraps(5)),
    (Odds(PassLine, 5, 5), CAndE(5)),
    (Odds(PassLine, 5, 5), HardWay(4, 5)),
    (Odds(PassLine, 5, 5), HardWay(6, 5)),
    (Odds(PassLine, 5, 5), HardWay(8, 5)),
    (Odds(PassLine, 5, 5), HardWay(10, 5)),
    (Odds(PassLine, 5, 5), Fire(5)),
    (Odds(PassLine, 6, 5), Odds(PassLine, 8, 5)),
    (Odds(PassLine, 6, 5), Odds(PassLine, 9, 5)),
    (Odds(PassLine, 6, 5), Odds(PassLine, 10, 5)),
    (Odds(PassLine, 6, 5), Place(4, 5)),
    (Odds(PassLine, 6, 5), Place(5, 5)),
    (Odds(PassLine, 6, 5), Place(6, 5)),
    (Odds(PassLine, 6, 5), Place(8, 5)),
    (Odds(PassLine, 6, 5), Place(9, 5)),
    (Odds(PassLine, 6, 5), Place(10, 5)),
    (Odds(PassLine, 6, 5), Field(5)),
    (Odds(PassLine, 6, 5), DontPass(5)),
    (Odds(PassLine, 6, 5), DontCome(5)),
    (Odds(PassLine, 6, 5), Any7(5)),
    (Odds(PassLine, 6, 5), Two(5)),
    (Odds(PassLine, 6, 5), Three(5)),
    (Odds(PassLine, 6, 5), Yo(5)),
    (Odds(PassLine, 6, 5), Boxcars(5)),
    (Odds(PassLine, 6, 5), AnyCraps(5)),
    (Odds(PassLine, 6, 5), CAndE(5)),
    (Odds(PassLine, 6, 5), HardWay(4, 5)),
    (Odds(PassLine, 6, 5), HardWay(6, 5)),
    (Odds(PassLine, 6, 5), HardWay(8, 5)),
    (Odds(PassLine, 6, 5), HardWay(10, 5)),
    (Odds(PassLine, 6, 5), Fire(5)),
    (Odds(PassLine, 8, 5), Odds(PassLine, 9, 5)),
    (Odds(PassLine, 8, 5), Odds(PassLine, 10, 5)),
    (Odds(PassLine, 8, 5), Place(4, 5)),
    (Odds(PassLine, 8, 5), Place(5, 5)),
    (Odds(PassLine, 8, 5), Place(6, 5)),
    (Odds(PassLine, 8, 5), Place(8, 5)),
    (Odds(PassLine, 8, 5), Place(9, 5)),
    (Odds(PassLine, 8, 5), Place(10, 5)),
    (Odds(PassLine, 8, 5), Field(5)),
    (Odds(PassLine, 8, 5), DontPass(5)),
    (Odds(PassLine, 8, 5), DontCome(5)),
    (Odds(PassLine, 8, 5), Any7(5)),
    (Odds(PassLine, 8, 5), Two(5)),
    (Odds(PassLine, 8, 5), Three(5)),
    (Odds(PassLine, 8, 5), Yo(5)),
    (Odds(PassLine, 8, 5), Boxcars(5)),
    (Odds(PassLine, 8, 5), AnyCraps(5)),
    (Odds(PassLine, 8, 5), CAndE(5)),
    (Odds(PassLine, 8, 5), HardWay(4, 5)),
    (Odds(PassLine, 8, 5), HardWay(6, 5)),
    (Odds(PassLine, 8, 5), HardWay(8, 5)),
    (Odds(PassLine, 8, 5), HardWay(10, 5)),
    (Odds(PassLine, 8, 5), Fire(5)),
    (Odds(PassLine, 9, 5), Odds(PassLine, 10, 5)),
    (Odds(PassLine, 9, 5), Place(4, 5)),
    (Odds(PassLine, 9, 5), Place(5, 5)),
    (Odds(PassLine, 9, 5), Place(6, 5)),
    (Odds(PassLine, 9, 5), Place(8, 5)),
    (Odds(PassLine, 9, 5), Place(9, 5)),
    (Odds(PassLine, 9, 5), Place(10, 5)),
    (Odds(PassLine, 9, 5), Field(5)),
    (Odds(PassLine, 9, 5), DontPass(5)),
    (Odds(PassLine, 9, 5), DontCome(5)),
    (Odds(PassLine, 9, 5), Any7(5)),
    (Odds(PassLine, 9, 5), Two(5)),
    (Odds(PassLine, 9, 5), Three(5)),
    (Odds(PassLine, 9, 5), Yo(5)),
    (Odds(PassLine, 9, 5), Boxcars(5)),
    (Odds(PassLine, 9, 5), AnyCraps(5)),
    (Odds(PassLine, 9, 5), CAndE(5)),
    (Odds(PassLine, 9, 5), HardWay(4, 5)),
    (Odds(PassLine, 9, 5), HardWay(6, 5)),
    (Odds(PassLine, 9, 5), HardWay(8, 5)),
    (Odds(PassLine, 9, 5), HardWay(10, 5)),
    (Odds(PassLine, 9, 5), Fire(5)),
    (Odds(PassLine, 10, 5), Place(4, 5)),
    (Odds(PassLine, 10, 5), Place(5, 5)),
    (Odds(PassLine, 10, 5), Place(6, 5)),
    (Odds(PassLine, 10, 5), Place(8, 5)),
    (Odds(PassLine, 10, 5), Place(9, 5)),
    (Odds(PassLine, 10, 5), Place(10, 5)),
    (Odds(PassLine, 10, 5), Field(5)),
    (Odds(PassLine, 10, 5), DontPass(5)),
    (Odds(PassLine, 10, 5), DontCome(5)),
    (Odds(PassLine, 10, 5), Any7(5)),
    (Odds(PassLine, 10, 5), Two(5)),
    (Odds(PassLine, 10, 5), Three(5)),
    (Odds(PassLine, 10, 5), Yo(5)),
    (Odds(PassLine, 10, 5), Boxcars(5)),
    (Odds(PassLine, 10, 5), AnyCraps(5)),
    (Odds(PassLine, 10, 5), CAndE(5)),
    (Odds(PassLine, 10, 5), HardWay(4, 5)),
    (Odds(PassLine, 10, 5), HardWay(6, 5)),
    (Odds(PassLine, 10, 5), HardWay(8, 5)),
    (Odds(PassLine, 10, 5), HardWay(10, 5)),
    (Odds(PassLine, 10, 5), Fire(5)),
    (Place(4, 5), Place(5, 5)),
    (Place(4, 5), Place(6, 5)),
    (Place(4, 5), Place(8, 5)),
    (Place(4, 5), Place(9, 5)),
    (Place(4, 5), Place(10, 5)),
    (Place(4, 5), Field(5)),
    (Place(4, 5), DontPass(5)),
    (Place(4, 5), DontCome(5)),
    (Place(4, 5), Any7(5)),
    (Place(4, 5), Two(5)),
    (Place(4, 5), Three(5)),
    (Place(4, 5), Yo(5)),
    (Place(4, 5), Boxcars(5)),
    (Place(4, 5), AnyCraps(5)),
    (Place(4, 5), CAndE(5)),
    (Place(4, 5), HardWay(4, 5)),
    (Place(4, 5), HardWay(6, 5)),
    (Place(4, 5), HardWay(8, 5)),
    (Place(4, 5), HardWay(10, 5)),
    (Place(4, 5), Fire(5)),
    (Place(5, 5), Place(6, 5)),
    (Place(5, 5), Place(8, 5)),
    (Place(5, 5), Place(9, 5)),
    (Place(5, 5), Place(10, 5)),
    (Place(5, 5), Field(5)),
    (Place(5, 5), DontPass(5)),
    (Place(5, 5), DontCome(5)),
    (Place(5, 5), Any7(5)),
    (Place(5, 5), Two(5)),
    (Place(5, 5), Three(5)),
    (Place(5, 5), Yo(5)),
    (Place(5, 5), Boxcars(5)),
    (Place(5, 5), AnyCraps(5)),
    (Place(5, 5), CAndE(5)),
    (Place(5, 5), HardWay(4, 5)),
    (Place(5, 5), HardWay(6, 5)),
    (Place(5, 5), HardWay(8, 5)),
    (Place(5, 5), HardWay(10, 5)),
    (Place(5, 5), Fire(5)),
    (Place(6, 5), Place(8, 5)),
    (Place(6, 5), Place(9, 5)),
    (Place(6, 5), Place(10, 5)),
    (Place(6, 5), Field(5)),
    (Place(6, 5), DontPass(5)),
    (Place(6, 5), DontCome(5)),
    (Place(6, 5), Any7(5)),
    (Place(6, 5), Two(5)),
    (Place(6, 5), Three(5)),
    (Place(6, 5), Yo(5)),
    (Place(6, 5), Boxcars(5)),
    (Place(6, 5), AnyCraps(5)),
    (Place(6, 5), CAndE(5)),
    (Place(6, 5), HardWay(4, 5)),
    (Place(6, 5), HardWay(6, 5)),
    (Place(6, 5), HardWay(8, 5)),
    (Place(6, 5), HardWay(10, 5)),
    (Place(6, 5), Fire(5)),
    (Place(8, 5), Place(9, 5)),
    (Place(8, 5), Place(10, 5)),
    (Place(8, 5), Field(5)),
    (Place(8, 5), DontPass(5)),
    (Place(8, 5), DontCome(5)),
    (Place(8, 5), Any7(5)),
    (Place(8, 5), Two(5)),
    (Place(8, 5), Three(5)),
    (Place(8, 5), Yo(5)),
    (Place(8, 5), Boxcars(5)),
    (Place(8, 5), AnyCraps(5)),
    (Place(8, 5), CAndE(5)),
    (Place(8, 5), HardWay(4, 5)),
    (Place(8, 5), HardWay(6, 5)),
    (Place(8, 5), HardWay(8, 5)),
    (Place(8, 5), HardWay(10, 5)),
    (Place(8, 5), Fire(5)),
    (Place(9, 5), Place(10, 5)),
    (Place(9, 5), Field(5)),
    (Place(9, 5), DontPass(5)),
    (Place(9, 5), DontCome(5)),
    (Place(9, 5), Any7(5)),
    (Place(9, 5), Two(5)),
    (Place(9, 5), Three(5)),
    (Place(9, 5), Yo(5)),
    (Place(9, 5), Boxcars(5)),
    (Place(9, 5), AnyCraps(5)),
    (Place(9, 5), CAndE(5)),
    (Place(9, 5), HardWay(4, 5)),
    (Place(9, 5), HardWay(6, 5)),
    (Place(9, 5), HardWay(8, 5)),
    (Place(9, 5), HardWay(10, 5)),
    (Place(9, 5), Fire(5)),
    (Place(10, 5), Field(5)),
    (Place(10, 5), DontPass(5)),
    (Place(10, 5), DontCome(5)),
    (Place(10, 5), Any7(5)),
    (Place(10, 5), Two(5)),
    (Place(10, 5), Three(5)),
    (Place(10, 5), Yo(5)),
    (Place(10, 5), Boxcars(5)),
    (Place(10, 5), AnyCraps(5)),
    (Place(10, 5), CAndE(5)),
    (Place(10, 5), HardWay(4, 5)),
    (Place(10, 5), HardWay(6, 5)),
    (Place(10, 5), HardWay(8, 5)),
    (Place(10, 5), HardWay(10, 5)),
    (Place(10, 5), Fire(5)),
    (Field(5), DontPass(5)),
    (Field(5), DontCome(5)),
    (Field(5), Any7(5)),
    (Field(5), Two(5)),
    (Field(5), Three(5)),
    (Field(5), Yo(5)),
    (Field(5), Boxcars(5)),
    (Field(5), AnyCraps(5)),
    (Field(5), CAndE(5)),
    (Field(5), HardWay(4, 5)),
    (Field(5), HardWay(6, 5)),
    (Field(5), HardWay(8, 5)),
    (Field(5), HardWay(10, 5)),
    (Field(5), Fire(5)),
    (DontPass(5), DontCome(5)),
    (DontPass(5), Any7(5)),
    (DontPass(5), Two(5)),
    (DontPass(5), Three(5)),
    (DontPass(5), Yo(5)),
    (DontPass(5), Boxcars(5)),
    (DontPass(5), AnyCraps(5)),
    (DontPass(5), CAndE(5)),
    (DontPass(5), HardWay(4, 5)),
    (DontPass(5), HardWay(6, 5)),
    (DontPass(5), HardWay(8, 5)),
    (DontPass(5), HardWay(10, 5)),
    (DontPass(5), Fire(5)),
    (DontCome(5), Any7(5)),
    (DontCome(5), Two(5)),
    (DontCome(5), Three(5)),
    (DontCome(5), Yo(5)),
    (DontCome(5), Boxcars(5)),
    (DontCome(5), AnyCraps(5)),
    (DontCome(5), CAndE(5)),
    (DontCome(5), HardWay(4, 5)),
    (DontCome(5), HardWay(6, 5)),
    (DontCome(5), HardWay(8, 5)),
    (DontCome(5), HardWay(10, 5)),
    (DontCome(5), Fire(5)),
    (Odds(DontPass, 4, 5), Odds(DontPass, 5, 5)),
    (Odds(DontPass, 4, 5), Odds(DontPass, 6, 5)),
    (Odds(DontPass, 4, 5), Odds(DontPass, 8, 5)),
    (Odds(DontPass, 4, 5), Odds(DontPass, 9, 5)),
    (Odds(DontPass, 4, 5), Odds(DontPass, 10, 5)),
    (Odds(DontPass, 4, 5), Any7(5)),
    (Odds(DontPass, 4, 5), Two(5)),
    (Odds(DontPass, 4, 5), Three(5)),
    (Odds(DontPass, 4, 5), Yo(5)),
    (Odds(DontPass, 4, 5), Boxcars(5)),
    (Odds(DontPass, 4, 5), AnyCraps(5)),
    (Odds(DontPass, 4, 5), CAndE(5)),
    (Odds(DontPass, 4, 5), HardWay(4, 5)),
    (Odds(DontPass, 4, 5), HardWay(6, 5)),
    (Odds(DontPass, 4, 5), HardWay(8, 5)),
    (Odds(DontPass, 4, 5), HardWay(10, 5)),
    (Odds(DontPass, 4, 5), Fire(5)),
    (Odds(DontPass, 5, 5), Odds(DontPass, 6, 5)),
    (Odds(DontPass, 5, 5), Odds(DontPass, 8, 5)),
    (Odds(DontPass, 5, 5), Odds(DontPass, 9, 5)),
    (Odds(DontPass, 5, 5), Odds(DontPass, 10, 5)),
    (Odds(DontPass, 5, 5), Any7(5)),
    (Odds(DontPass, 5, 5), Two(5)),
    (Odds(DontPass, 5, 5), Three(5)),
    (Odds(DontPass, 5, 5), Yo(5)),
    (Odds(DontPass, 5, 5), Boxcars(5)),
    (Odds(DontPass, 5, 5), AnyCraps(5)),
    (Odds(DontPass, 5, 5), CAndE(5)),
    (Odds(DontPass, 5, 5), HardWay(4, 5)),
    (Odds(DontPass, 5, 5), HardWay(6, 5)),
    (Odds(DontPass, 5, 5), HardWay(8, 5)),
    (Odds(DontPass, 5, 5), HardWay(10, 5)),
    (Odds(DontPass, 5, 5), Fire(5)),
    (Odds(DontPass, 6, 5), Odds(DontPass, 8, 5)),
    (Odds(DontPass, 6, 5), Odds(DontPass, 9, 5)),
    (Odds(DontPass, 6, 5), Odds(DontPass, 10, 5)),
    (Odds(DontPass, 6, 5), Any7(5)),
    (Odds(DontPass, 6, 5), Two(5)),
    (Odds(DontPass, 6, 5), Three(5)),
    (Odds(DontPass, 6, 5), Yo(5)),
    (Odds(DontPass, 6, 5), Boxcars(5)),
    (Odds(DontPass, 6, 5), AnyCraps(5)),
    (Odds(DontPass, 6, 5), CAndE(5)),
    (Odds(DontPass, 6, 5), HardWay(4, 5)),
    (Odds(DontPass, 6, 5), HardWay(6, 5)),
    (Odds(DontPass, 6, 5), HardWay(8, 5)),
    (Odds(DontPass, 6, 5), HardWay(10, 5)),
    (Odds(DontPass, 6, 5), Fire(5)),
    (Odds(DontPass, 8, 5), Odds(DontPass, 9, 5)),
    (Odds(DontPass, 8, 5), Odds(DontPass, 10, 5)),
    (Odds(DontPass, 8, 5), Any7(5)),
    (Odds(DontPass, 8, 5), Two(5)),
    (Odds(DontPass, 8, 5), Three(5)),
    (Odds(DontPass, 8, 5), Yo(5)),
    (Odds(DontPass, 8, 5), Boxcars(5)),
    (Odds(DontPass, 8, 5), AnyCraps(5)),
    (Odds(DontPass, 8, 5), CAndE(5)),
    (Odds(DontPass, 8, 5), HardWay(4, 5)),
    (Odds(DontPass, 8, 5), HardWay(6, 5)),
    (Odds(DontPass, 8, 5), HardWay(8, 5)),
    (Odds(DontPass, 8, 5), HardWay(10, 5)),
    (Odds(DontPass, 8, 5), Fire(5)),
    (Odds(DontPass, 9, 5), Odds(DontPass, 10, 5)),
    (Odds(DontPass, 9, 5), Any7(5)),
    (Odds(DontPass, 9, 5), Two(5)),
    (Odds(DontPass, 9, 5), Three(5)),
    (Odds(DontPass, 9, 5), Yo(5)),
    (Odds(DontPass, 9, 5), Boxcars(5)),
    (Odds(DontPass, 9, 5), AnyCraps(5)),
    (Odds(DontPass, 9, 5), CAndE(5)),
    (Odds(DontPass, 9, 5), HardWay(4, 5)),
    (Odds(DontPass, 9, 5), HardWay(6, 5)),
    (Odds(DontPass, 9, 5), HardWay(8, 5)),
    (Odds(DontPass, 9, 5), HardWay(10, 5)),
    (Odds(DontPass, 9, 5), Fire(5)),
    (Odds(DontPass, 10, 5), Any7(5)),
    (Odds(DontPass, 10, 5), Two(5)),
    (Odds(DontPass, 10, 5), Three(5)),
    (Odds(DontPass, 10, 5), Yo(5)),
    (Odds(DontPass, 10, 5), Boxcars(5)),
    (Odds(DontPass, 10, 5), AnyCraps(5)),
    (Odds(DontPass, 10, 5), CAndE(5)),
    (Odds(DontPass, 10, 5), HardWay(4, 5)),
    (Odds(DontPass, 10, 5), HardWay(6, 5)),
    (Odds(DontPass, 10, 5), HardWay(8, 5)),
    (Odds(DontPass, 10, 5), HardWay(10, 5)),
    (Odds(DontPass, 10, 5), Fire(5)),
    (Any7(5), Two(5)),
    (Any7(5), Three(5)),
    (Any7(5), Yo(5)),
    (Any7(5), Boxcars(5)),
    (Any7(5), AnyCraps(5)),
    (Any7(5), CAndE(5)),
    (Any7(5), HardWay(4, 5)),
    (Any7(5), HardWay(6, 5)),
    (Any7(5), HardWay(8, 5)),
    (Any7(5), HardWay(10, 5)),
    (Any7(5), Fire(5)),
    (Two(5), Three(5)),
    (Two(5), Yo(5)),
    (Two(5), Boxcars(5)),
    (Two(5), AnyCraps(5)),
    (Two(5), CAndE(5)),
    (Two(5), HardWay(4, 5)),
    (Two(5), HardWay(6, 5)),
    (Two(5), HardWay(8, 5)),
    (Two(5), HardWay(10, 5)),
    (Two(5), Fire(5)),
    (Three(5), Yo(5)),
    (Three(5), Boxcars(5)),
    (Three(5), AnyCraps(5)),
    (Three(5), CAndE(5)),
    (Three(5), HardWay(4, 5)),
    (Three(5), HardWay(6, 5)),
    (Three(5), HardWay(8, 5)),
    (Three(5), HardWay(10, 5)),
    (Three(5), Fire(5)),
    (Yo(5), Boxcars(5)),
    (Yo(5), AnyCraps(5)),
    (Yo(5), CAndE(5)),
    (Yo(5), HardWay(4, 5)),
    (Yo(5), HardWay(6, 5)),
    (Yo(5), HardWay(8, 5)),
    (Yo(5), HardWay(10, 5)),
    (Yo(5), Fire(5)),
    (Boxcars(5), AnyCraps(5)),
    (Boxcars(5), CAndE(5)),
    (Boxcars(5), HardWay(4, 5)),
    (Boxcars(5), HardWay(6, 5)),
    (Boxcars(5), HardWay(8, 5)),
    (Boxcars(5), HardWay(10, 5)),
    (Boxcars(5), Fire(5)),
    (AnyCraps(5), CAndE(5)),
    (AnyCraps(5), HardWay(4, 5)),
    (AnyCraps(5), HardWay(6, 5)),
    (AnyCraps(5), HardWay(8, 5)),
    (AnyCraps(5), HardWay(10, 5)),
    (AnyCraps(5), Fire(5)),
    (CAndE(5), HardWay(4, 5)),
    (CAndE(5), HardWay(6, 5)),
    (CAndE(5), HardWay(8, 5)),
    (CAndE(5), HardWay(10, 5)),
    (CAndE(5), Fire(5)),
    (HardWay(4, 5), HardWay(6, 5)),
    (HardWay(4, 5), HardWay(8, 5)),
    (HardWay(4, 5), HardWay(10, 5)),
    (HardWay(4, 5), Fire(5)),
    (HardWay(6, 5), HardWay(8, 5)),
    (HardWay(6, 5), HardWay(10, 5)),
    (HardWay(6, 5), Fire(5)),
    (HardWay(8, 5), HardWay(10, 5)),
    (HardWay(8, 5), Fire(5)),
    (HardWay(10, 5), Fire(5))
])
def test_bet_type_inequality(bet_one, bet_two):
    assert bet_one != bet_two


@pytest.mark.parametrize('bet_one, bet_two', [
    (PassLine(10), PassLine(15)),
    (Come(25), Come(10)),
    (Odds(PassLine, 4, 5), Odds(PassLine, 4, 20)),
    (Odds(PassLine, 5, 10), Odds(PassLine, 5, 25)),
    (Odds(PassLine, 6, 25), Odds(PassLine, 6, 10)),
    (Odds(PassLine, 8, 20), Odds(PassLine, 8, 30)),
    (Odds(PassLine, 9, 15), Odds(PassLine, 9, 5)),
    (Odds(PassLine, 10, 20), Odds(PassLine, 10, 5)),
    (Place(4, 10), Place(4, 30)),
    (Place(5, 30), Place(5, 10)),
    (Place(6, 25), Place(6, 20)),
    (Place(8, 30), Place(8, 15)),
    (Place(9, 15), Place(9, 25)),
    (Place(10, 5), Place(10, 10)),
    (Field(30), Field(5)),
    (DontPass(20), DontPass(5)),
    (DontCome(15), DontCome(25)),
    (Odds(DontPass, 4, 10), Odds(DontPass, 4, 25)),
    (Odds(DontPass, 5, 10), Odds(DontPass, 5, 15)),
    (Odds(DontPass, 6, 30), Odds(DontPass, 6, 5)),
    (Odds(DontPass, 8, 30), Odds(DontPass, 8, 10)),
    (Odds(DontPass, 9, 5), Odds(DontPass, 9, 10)),
    (Odds(DontPass, 10, 10), Odds(DontPass, 10, 30)),
    (Any7(30), Any7(25)),
    (Two(20), Two(25)),
    (Three(10), Three(25)),
    (Yo(30), Yo(10)),
    (Boxcars(30), Boxcars(10)),
    (AnyCraps(25), AnyCraps(15)),
    (CAndE(5), CAndE(25)),
    (HardWay(4, 25), HardWay(4, 10)),
    (HardWay(6, 15), HardWay(6, 25)),
    (HardWay(8, 15), HardWay(8, 5)),
    (HardWay(10, 20), HardWay(10, 5)),
    (Fire(20), Fire(30))
])
def test_bet_amount_inequality(bet_one, bet_two):
    assert bet_one != bet_two


@pytest.mark.parametrize('bet', [
    PassLine(5),
    Odds(PassLine, 4, 5),
    Odds(PassLine, 5, 5),
    Odds(PassLine, 6, 5),
    Odds(PassLine, 8, 5),
    Odds(PassLine, 9, 5),
    Odds(PassLine, 10, 5),
    Place(4, 5),
    Place(5, 5),
    Place(6, 6),
    Place(8, 8),
    Place(9, 9),
    Place(10, 10),
    Odds(DontPass, 4, 5),
    Odds(DontPass, 5, 5),
    Odds(DontPass, 6, 5),
    Odds(DontPass, 8, 5),
    Odds(DontPass, 9, 5),
    Odds(DontPass, 10, 5),
    Field(5),
    DontPass(5),
    DontCome(5),
    Any7(5),
    Two(5),
    Three(5),
    Yo(5),
    Boxcars(5),
    AnyCraps(5),
    HardWay(4, 5),
    HardWay(6, 5),
    HardWay(8, 5),
    HardWay(10, 5)
])
def test_is_removable_table_point_off(bet):
    table = Table()
    table.add_player()
    assert bet.is_removable(table.players[0]) is True


@pytest.mark.parametrize('bet', [
    Odds(PassLine, 4, 5),
    Odds(PassLine, 5, 5),
    Odds(PassLine, 6, 5),
    Odds(PassLine, 8, 5),
    Odds(PassLine, 9, 5),
    Odds(PassLine, 10, 5),
    Place(4, 5),
    Place(5, 5),
    Place(6, 6),
    Place(8, 8),
    Place(9, 9),
    Place(10, 10),
    Odds(DontPass, 4, 5),
    Odds(DontPass, 5, 5),
    Odds(DontPass, 6, 5),
    Odds(DontPass, 8, 5),
    Odds(DontPass, 9, 5),
    Odds(DontPass, 10, 5),
    Field(5),
    DontPass(5),
    DontCome(5),
    Any7(5),
    Two(5),
    Three(5),
    Yo(5),
    Boxcars(5),
    AnyCraps(5),
    HardWay(4, 5),
    HardWay(6, 5),
    HardWay(8, 5),
    HardWay(10, 5)
])
def test_is_removable_table_point_on(bet):
    table = Table()
    table.add_player()
    table.point.number = 6
    assert bet.is_removable(table.players[0]) is True


@pytest.mark.parametrize('dice1, dice2, correct_ratio', [
    (1, 1, 2),
    (1, 2, 1),
    (2, 2, 1),
    (5, 4, 1),
    (5, 5, 1),
    (6, 5, 1),
    (6, 6, 2)
])
def test_get_field_default_table_payout_ratio(dice1, dice2, correct_ratio):
    table = Table()
    table.dice.fixed_roll((dice1, dice2))
    assert Field(5).get_payout_ratio(table) == correct_ratio


@pytest.mark.parametrize('dice1, dice2, correct_ratio', [
    (1, 1, 2),
    (1, 2, 14),
    (2, 2, 14000),
    (5, 4, 1),
    (5, 5, 1),
    (6, 5, 1),
    (6, 6, 3)
])
def test_get_field_non_default_table_payout_ratio(dice1, dice2, correct_ratio):
    table = Table()
    new_field_payouts = table.settings.field_payouts
    new_field_payouts.update({3: 14, 12: 3, 4: 14000})
    table.settings = TableSettings(field_payouts=new_field_payouts)
    table.dice.fixed_roll((dice1, dice2))
    assert Field(5).get_payout_ratio(table) == correct_ratio


@pytest.mark.parametrize('points_made, correct_ratio', [
    ([4, 5, 6, 9], 24),
    ([4, 5, 6, 9, 10], 249),
    ([4, 5, 6, 8, 9, 10], 999)
])
def test_get_fire_default_table_payout_ratio(points_made, correct_ratio):
    table = Table()
    bet = Fire(1)
    bet.points_made = points_made
    bet.ended = True
    ratio = (bet.get_result(table).amount - bet.amount) / bet.amount
    assert ratio == correct_ratio


@pytest.mark.parametrize('points_made, correct_ratio', [
    ([4, 5, 6], 6),
    ([4, 5, 6, 9], 9),
    ([4, 5, 6, 9, 10], 69),
    ([4, 5, 6, 8, 9, 10], 420)
])
def test_get_fire_non_default_table_payout_ratio(points_made, correct_ratio):
    table = Table()
    table.settings = TableSettings(fire_points={3: 6, 4: 9, 5: 69, 6: 420})
    bet = Fire(1)
    bet.points_made = points_made
    bet.ended = True
    ratio = (bet.get_result(table).amount - bet.amount) / bet.amount
    assert ratio == correct_ratio


@pytest.mark.parametrize('rolls, correct_status, correct_win_amt, correct_remove', [
    ([(6, 1)], None, 0.0, False),
    ([(2, 2), (3, 1), (4, 3), (6, 6)], None, 0.0, False),
    ([(2, 2), (4, 3)], 'lose', 0.0, True),
    ([(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), (5, 5)], None, 0.0, False),
    ([(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), (5, 5), (5, 5), (5, 5)],
     None, 0.0, False),
    ([(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), (5, 5), (5, 5), (3, 4)],
     'win', 24, True),
    ([(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), (5, 5), (2, 3), (2, 3)],
     None, 0.0, False),
    ([(2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (4, 4), (5, 5), (5, 5), (2, 3), (2, 3),
      (4, 5), (4, 5)],
     None, 0.0, False)
])
def test_fire(rolls, correct_status, correct_win_amt, correct_remove):
    table = Table()
    table.add_player()
    table.players[0].add_bet(Fire(1))
    bet = table.players[0].bets[0]

    # table.fixed_run(rolls)
    for roll in rolls:
        TableUpdate().run(table, roll)

    result = bet.get_result(table)
    print(result.amount)
    if result.won:
        status = 'win'
    elif result.lost:
        status = 'lose'
    else:
        status = None

    if result.won:
        win_amount = result.amount - bet.amount
    else:
        win_amount = 0

    remove = result.remove

    assert (status, win_amount, remove) == (correct_status, correct_win_amt, correct_remove)


@pytest.mark.parametrize('bet, point_number, allowed', [
    (PassLine(5), None, True),
    (PassLine(5), 6, False),
    (Come(5), None, False),
    (Come(5), 6, True),
    (DontPass(5), None, True),
    (DontPass(5), 4, False),
    (DontCome(5), None, False),
    (DontCome(5), 8, True),
    (Field(5), None, True),
    (Field(5), 4, True)
])
def test_bet_allowed_point(bet, point_number, allowed):
    table = Table()
    table.add_player()
    dice = Dice()
    dice.total = point_number

    point = Point()
    point.update(dice)

    table.point = point

    assert bet.allowed(player=table.players[0]) == allowed


@pytest.mark.parametrize('bet, new_shooter, allowed', [
    (Field(5), True, True),
    (Field(5), False, True),
    (Fire(5), True, True),
    (Fire(5), False, False)
])
def test_bet_allowed_new_shooter(bet, new_shooter, allowed):
    table = Table()
    table.add_player()

    table.new_shooter = new_shooter

    assert bet.allowed(player=table.players[0]) == allowed


@pytest.mark.parametrize('bet', [
    PassLine(5),
    Place(4, 5),
    Place(5, 5),
    Place(6, 5),
    Place(8, 5),
    Place(9, 5),
    Place(10, 5),
    DontPass(5),
    Field(5),
    Any7(5),
    Two(5),
    Three(5),
    Yo(5),
    Boxcars(5),
    AnyCraps(5),
    HardWay(4, 5),
    HardWay(6, 5),
    HardWay(8, 5),
    HardWay(10, 5)
])
def test_bets_always_allowed_point_off(bet):
    table = Table()
    table.add_player()
    assert bet.allowed(table.players[0])


@pytest.mark.parametrize('bet', [
    Come(5),
    Place(4, 5),
    Place(5, 5),
    Place(6, 5),
    Place(8, 5),
    Place(9, 5),
    Place(10, 5),
    DontCome(5),
    Field(5),
    Any7(5),
    Two(5),
    Three(5),
    Yo(5),
    Boxcars(5),
    AnyCraps(5),
    HardWay(4, 5),
    HardWay(6, 5),
    HardWay(8, 5),
    HardWay(10, 5)
])
def test_bets_always_allowed_point_on(bet):
    table = Table()
    table.point.number = 10
    table.add_player()
    assert bet.allowed(table.players[0])