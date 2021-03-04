from crapssim.dice import Dice


class Bet(object):
    """
    A generic bet for the craps table

    Parameters
    ----------
    bet_amount : float
        Wagered amount for the bet

    Attributes
    ----------
    name : string
        Name for the bet
    subname : string
        Subname, usually denotes number for a come/don't come bet
    winning_numbers : list
        Numbers to roll for this bet to win
    losing_numbers : list
        Numbers to roll that cause this bet to lose
    payoutratio : float
        Ratio that bet pays out on a win

    """

    name = None
    subname = ""
    winning_numbers = []
    losing_numbers = []
    payoutratio = float(1)
    # TODO: add whether bet can be removed

    def __init__(self, bet_amount):
        self.bet_amount = float(bet_amount)

    # def __eq__(self, other):
    #     return self.name == other.name

    def _update_bet(self, table_object, dice_object: Dice):
        status = None
        win_amount = 0

        if dice_object.total in self.winning_numbers:
            status = "win"
            win_amount = self.payoutratio * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            status = "lose"

        return status, win_amount


"""
Passline and Come bets
"""


class PassLine(Bet):
    # TODO: make this require that table_object.point = "Off",
    # probably better in the player module
    def __init__(self, bet_amount):
        self.name = "PassLine"
        self.winning_numbers = [7, 11]
        self.losing_numbers = [2, 3, 12]
        self.payoutratio = 1.0
        self.prepoint = True
        super().__init__(bet_amount)

    def _update_bet(self, table_object, dice_object):
        status = None
        win_amount = 0

        if dice_object.total in self.winning_numbers:
            status = "win"
            win_amount = self.payoutratio * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            status = "lose"
        elif self.prepoint:
            self.winning_numbers = [dice_object.total]
            self.losing_numbers = [7]
            self.prepoint = False

        return status, win_amount


class Come(PassLine):
    def __init__(self, bet_amount):
        super().__init__(bet_amount)
        self.name = "Come"

    def _update_bet(self, table_object, dice_object):
        status, win_amount = super()._update_bet(table_object, dice_object)
        if not self.prepoint and self.subname == "":
            self.subname = "".join(str(e) for e in self.winning_numbers)
        return status, win_amount


"""
Passline/Come bet odds
"""


class Odds(Bet):
    def __init__(self, bet_amount, bet_object):
        super().__init__(bet_amount)
        self.name = "Odds"
        self.subname = "".join(str(e) for e in bet_object.winning_numbers)
        self.winning_numbers = bet_object.winning_numbers
        self.losing_numbers = bet_object.losing_numbers

        if self.winning_numbers == [4] or self.winning_numbers == [10]:
            self.payoutratio = 2 / 1
        elif self.winning_numbers == [5] or self.winning_numbers == [9]:
            self.payoutratio = 3 / 2
        elif self.winning_numbers == [6] or self.winning_numbers == [8]:
            self.payoutratio = 6 / 5


"""
Place Bets on 4,5,6,8,9,10
"""


class Place(Bet):
    def _update_bet(self, table_object, dice_object):
        # place bets are inactive when point is "Off"
        if table_object.point == "On":
            return super()._update_bet(table_object, dice_object)
        else:
            return None, 0


class Place4(Place):
    def __init__(self, bet_amount):
        self.name = "Place4"
        self.winning_numbers = [4]
        self.losing_numbers = [7]
        self.payoutratio = 9 / 5
        super().__init__(bet_amount)


class Place5(Place):
    def __init__(self, bet_amount):
        self.name = "Place5"
        self.winning_numbers = [5]
        self.losing_numbers = [7]
        self.payoutratio = 7 / 5
        super().__init__(bet_amount)


class Place6(Place):
    def __init__(self, bet_amount):
        self.name = "Place6"
        self.winning_numbers = [6]
        self.losing_numbers = [7]
        self.payoutratio = 7 / 6
        super().__init__(bet_amount)


class Place8(Place):
    def __init__(self, bet_amount):
        self.name = "Place8"
        self.winning_numbers = [8]
        self.losing_numbers = [7]
        self.payoutratio = 7 / 6
        super().__init__(bet_amount)


class Place9(Place):
    def __init__(self, bet_amount):
        self.name = "Place9"
        self.winning_numbers = [9]
        self.losing_numbers = [7]
        self.payoutratio = 7 / 5
        super().__init__(bet_amount)


class Place10(Place):
    def __init__(self, bet_amount):
        self.name = "Place10"
        self.winning_numbers = [10]
        self.losing_numbers = [7]
        self.payoutratio = 9 / 5
        super().__init__(bet_amount)


"""
Field bet
"""


class Field(Bet):
    """
    Parameters
    ----------
    double : list
        Set of numbers that pay double on the field bet (default = [2,12])
    triple : list
        Set of numbers that pay triple on the field bet (default = [])
    """

    def __init__(self, bet_amount, double=[2, 12], triple=[]):
        self.name = "Field"
        self.double_winning_numbers = double
        self.triple_winning_numbers = triple
        self.winning_numbers = [2, 3, 4, 9, 10, 11, 12]
        self.losing_numbers = [5, 6, 7, 8]
        super().__init__(bet_amount)

    def _update_bet(self, table_object, dice_object):
        status = None
        win_amount = 0

        if dice_object.total in self.triple_winning_numbers:
            status = "win"
            win_amount = 3 * self.bet_amount
        elif dice_object.total in self.double_winning_numbers:
            status = "win"
            win_amount = 2 * self.bet_amount
        elif dice_object.total in self.winning_numbers:
            status = "win"
            win_amount = 1 * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            status = "lose"

        return status, win_amount


"""
Don't pass and Don't come bets
"""


class DontPass(Bet):
    # TODO: make this require that table_object.point = "Off",
    #  probably better in the player module
    def __init__(self, bet_amount):
        self.name = "DontPass"
        self.winning_numbers = [2, 3]
        self.losing_numbers = [7, 11]
        self.push_numbers = [12]
        self.payoutratio = 1.0
        self.prepoint = True
        super().__init__(bet_amount)

    def _update_bet(self, table_object, dice_object):
        status = None
        win_amount = 0

        if dice_object.total in self.winning_numbers:
            status = "win"
            win_amount = self.payoutratio * self.bet_amount
        elif dice_object.total in self.losing_numbers:
            status = "lose"
        elif dice_object.total in self.push_numbers:
            status = "push"
        elif self.prepoint:
            self.winning_numbers = [7]
            self.losing_numbers = [dice_object.total]
            self.push_numbers = []
            self.prepoint = False

        return status, win_amount


"""
Don't pass/Don't come lay odds
"""


class LayOdds(Bet):
    def __init__(self, bet_amount, bet_object):
        super().__init__(bet_amount)
        self.name = "LayOdds"
        self.subname = "".join(str(e) for e in bet_object.losing_numbers)
        self.winning_numbers = bet_object.winning_numbers
        self.losing_numbers = bet_object.losing_numbers

        if self.losing_numbers == [4] or self.losing_numbers == [10]:
            self.payoutratio = 1 / 2
        elif self.losing_numbers == [5] or self.losing_numbers == [9]:
            self.payoutratio = 2 / 3
        elif self.losing_numbers == [6] or self.losing_numbers == [8]:
            self.payoutratio = 5 / 6
