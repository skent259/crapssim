import typing

from crapssim.bet import Bet, Odds, LayOdds, PassLine, Come, DontPass, DontCome
from crapssim.strategy import STRATEGY_TYPE, passline

if typing.TYPE_CHECKING:
    from crapssim.table import Table


class Player:
    """
    Player standing at the craps table

    Parameters
    ----------
    bankroll : typing.SupportsFloat
        Starting amount of cash for the player
    bet_strategy : function(table, player, unit=5)
        A function that implements a particular betting strategy.  See betting_strategies.py
    name : string, default = "Player"
        Name of the player
    unit : typing.SupportsFloat, default=5
        Standard amount of bet to be used by bet_strategy

    Attributes
    ----------
    bankroll : typing.SupportsFloat
        Current amount of cash for the player
    name : str
        Name of the player
    bet_strategy :
        A function that implements a particular betting strategy. See betting_strategies.py.
    strat_info : dict[str, typing.Any]
        Variables to be used by the players bet_strategy
    unit : typing.SupportsFloat
        Standard amount of bet to be used by bet_strategy
    bets_on_table : list
        List of betting objects for the player
    total_bet_amount : int
        Sum of bet value for the player
    """

    def __init__(self, bankroll: typing.SupportsFloat,
                 bet_strategy: STRATEGY_TYPE = passline,
                 name: str = "Player",
                 unit: typing.SupportsFloat = 5):
        self.bankroll: float = bankroll
        self.bet_strategy: STRATEGY_TYPE = bet_strategy
        self.strat_info: dict[str, typing.Any] = {}
        self.name: str = name
        self.unit: typing.SupportsFloat = unit
        self.bets_on_table: list[Bet] = []

    @property
    def total_bet_amount(self) -> float:
        return sum(x.bet_amount for x in self.bets_on_table)

    def sit_at_table(self, table: "Table"):
        table.add_player(self)

    def place_bet(self, bet: Bet, table: "Table") -> None:
        if bet.already_placed(self):
            existing_bet: Bet = self.get_bet(type(bet))
            existing_bet.bet_amount += bet.bet_amount
            self.bankroll -= bet.bet_amount
            if not existing_bet.allowed(table=table, player=self):
                existing_bet -= bet.bet_amount
                self.bankroll += bet.bet_amount
        else:
            if bet.allowed(table=table, player=self):
                self.bets_on_table.append(bet)
                self.bankroll -= bet.bet_amount

    def remove_bet(self, bet: Bet) -> None:
        if bet in self.bets_on_table and bet.removable:
            self.bankroll += bet.bet_amount
            self.bets_on_table.remove(bet)

    def get_bets(self, *bet_types: typing.Type[Bet], **bet_attributes) -> list[Bet]:
        if len(bet_types) == 0:
            bet_types = (Bet,)
        else:
            bet_types = tuple(bet_types)
        return [x for x in self.bets_on_table if isinstance(x, bet_types)
                and x.__dict__.items() >= bet_attributes.items()]

    def has_bets(self, *bet_types: typing.Type[Bet], **bet_attributes) -> bool:
        """ returns True if bets_to_check and self.bets_on_table
        has at least one thing in common """
        return len(self.get_bets(*bet_types, **bet_attributes)) > 0

    def get_bet(self, bet_type: typing.Type[Bet], **bet_attributes) -> Bet:
        """returns first betting object matching bet and bet_subname.
        If bet_subname="Any", returns first betting object matching bet"""
        return self.get_bets(bet_type, **bet_attributes)[0]

    def count_bets(self, *bet_types: typing.Type[Bet], **bet_attributes) -> int:
        """ returns the total number of bets in self.bets_on_table that match bets_to_check """
        return len(self.get_bets(*bet_types, **bet_attributes))

    def remove_if_present(self, bet_type: typing.Type[Bet]) -> None:
        if self.has_bets(bet_type):
            self.remove_bet(self.get_bet(bet_type))

    def add_strategy_bets(self, table: "Table") -> None:
        """ Implement the given betting strategy

        Parameters
        ----------
        table
        """
        if self.bet_strategy:
            self.bet_strategy(self, table, **self.strat_info)

    def update_bet(self, table, verbose: bool = False) -> None:
        info = {}
        for bet in self.bets_on_table[:]:
            bet.update(table)

            self.bankroll += bet.get_return_amount(table)

            if verbose:
                self.print_bet_update(bet, table)

            if bet.should_remove(table):
                self.bets_on_table.remove(bet)

            info[bet.name] = {"status": bet.get_status(table),
                              "win_amount": bet.get_win_amount(table)}

    def print_bet_update(self, bet, table):
        status = bet.get_status(table)
        win_amount = bet.get_win_amount(table)
        if status == "win":
            print(f"{self.name} won ${win_amount} on {bet.name} bet!")
        elif status == "lose":
            print(f"{self.name} lost ${bet.bet_amount} on {bet.name} bet.")

    def place_odds(self, table: "Table",
                   bet_amount: float = None,
                   number: int = None):
        if number is None:
            pass_come_bets = self.get_bets(PassLine, Come)
            if len(pass_come_bets) == 0:
                raise ValueError('No PassLine or Come bets found to lay odds on.')
            if len(pass_come_bets) > 1:
                raise ValueError('If there is more than one PassLine and '
                                 'Come bet for this Player you must specify a number.')
        else:
            pass_come_bets = self.get_bets(PassLine, Come, point=number)
            if len(pass_come_bets) == 0:
                raise ValueError(f'No PassLine or Come bets found with point={number}.')

        pass_come_bet: PassLine | Come = pass_come_bets[0]
        number = pass_come_bet.point

        if bet_amount is None:
            bet_amount = table.settings['max_odds'][number] * pass_come_bet.bet_amount

        odds_bet = Odds.by_number(number, bet_amount)
        self.place_bet(odds_bet, table)

    def lay_odds(self, table: "Table",
                 bet_amount: float = None,
                 number: int = None):
        if number is None:
            dont_pass_come_bets = self.get_bets(DontPass, DontCome)
            if len(dont_pass_come_bets) == 0:
                raise ValueError('No DontPass or DontCome bets found to lay odds on.')
            if len(dont_pass_come_bets) > 1:
                raise ValueError('If there is more than one DontPass and '
                                 'DontCome bet for this Player you must specify a number.')
        else:
            dont_pass_come_bets = self.get_bets(DontPass, DontCome, point=number)
            if len(dont_pass_come_bets) == 0:
                raise ValueError(f'No DontPass or DontCome bets found with point={number}.')

        dont_pass_come_bet: PassLine | Come = dont_pass_come_bets[0]
        number = dont_pass_come_bet.point

        if bet_amount is None:
            bet_amount = table.settings['max_odds'][number] * dont_pass_come_bet.bet_amount

        lay_odds_bet = LayOdds.by_number(number, bet_amount)
        self.place_bet(lay_odds_bet, table)
