from numpy import random as r


class Dice:
    """
    Simulate the rolling of a dice

    Attributes
    ----------
    n_rolls : int
        Number of rolls for the dice
    result : array, shape = [2]
        Most recent outcome of the roll of two dice
    total : int
        Sum of dice outcome

    """

    def __init__(self):
        self.total = None
        self.result = None
        self.n_rolls = 0

    def roll(self):
        self.n_rolls += 1
        self.result = r.randint(1, 7, size=2)
        self.total = sum(self.result)

    def fixed_roll(self, outcome):
        self.n_rolls += 1
        self.result = outcome
        self.total = sum(self.result)


if __name__ == "__main__":

    d1 = Dice()

    d1.roll()
    d1.roll()
    d1.roll()

    print("Number of rolls: {}".format(d1.n_rolls))
    print("Last Roll: {}".format(d1.result))
    print("Last Roll Total: {}".format(d1.total))
