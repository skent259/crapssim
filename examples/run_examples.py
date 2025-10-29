from crapssim.table import Table, TableUpdate
from crapssim.strategy.examples import (
    QuickProps,
    BuySampler,
    LaySampler,
    PutWithOdds,
    HornShowcase,
)

# Fixed roll sequence to exercise typical paths:
# - Set point ON at 6, hit 6/8, toss a 7, then a horn number, then 4/10.
ROLLS = [(3, 3), (4, 4), (4, 3), (1, 1), (2, 2), (6, 4)]


def run_example(name, strategy_factory):
    print(f"\n=== {name} ===")
    table = Table()
    player = table.add_player()
    player.strategy = strategy_factory()

    for die_one, die_two in ROLLS:
        TableUpdate.roll(table, fixed_outcome=(die_one, die_two), verbose=False)

    print(f"Final bankroll: {player.bankroll:.2f}")
    # Show remaining open bets (should be few or none in these demos)
    if player.bets:
        print("Open bets:", [repr(bet) for bet in player.bets])


def main():
    runs = [
        ("QuickProps", lambda: QuickProps(world_amount=5.0, big_amount=10.0)),
        ("BuySampler", lambda: BuySampler(amount=25.0)),
        ("LaySampler", lambda: LaySampler(amount=30.0)),
        (
            "PutWithOdds",
            lambda: PutWithOdds(
                flat_amount=10.0,
                odds_multiple=2.0,
                always_working=True,
            ),
        ),
        ("HornShowcase", lambda: HornShowcase(horn_amount=5.0, world_amount=5.0)),
    ]
    for name, factory in runs:
        run_example(name, factory)


if __name__ == "__main__":
    main()
