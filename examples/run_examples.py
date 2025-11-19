from crapssim.strategy.examples import BuySampler, LaySampler, PutWithOdds, QuickProps
from crapssim.strategy.single_bet import BetHorn, BetWorld
from crapssim.table import Table

# Fixed roll sequence to exercise typical paths:
# - Set point ON at 6, hit 6/8, toss a 7, then a horn number, then 4/10.
ROLLS = [(3, 3), (4, 4), (4, 3), (1, 1), (2, 2), (6, 4)]


def run_example(name, strategy_factory):
    print(f"\n=== {name} ===")
    table = Table()
    player = table.add_player()
    player.strategy = strategy_factory()

    table.fixed_run(dice_outcomes=ROLLS, verbose=False)

    print(f"Final bankroll: {player.bankroll:.2f}")
    # Show remaining open bets (should be few or none in these demos)
    if player.bets:
        print("Open bets:", [str(bet) for bet in player.bets])


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
        ("HornExample", lambda: BetHorn(amount=4.0)),
        ("WorldExample", lambda: BetWorld(amount=5.0)),
    ]
    for name, factory in runs:
        run_example(name, factory)


if __name__ == "__main__":
    main()
    main()
