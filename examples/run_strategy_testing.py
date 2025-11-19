from crapssim import strategy
from crapssim.table import Table

# SELECT ONE STRATEGY TO TEST
STRATEGY_TO_TEST = strategy.examples.ThreePointDolly(10)

# Create fixed roll scenarios that can be pulled as needed
# fmt: off
SCENARIOS = {
    "basic_point_on": [(3, 3), (4, 4), (4, 3), (1, 1), (2, 2), (6, 4)],
    "seven_out_after_point": [(5, 1), (3, 3), (2, 5), (4, 2)],
    "multiple_points": [(2, 2), (2, 2), (3, 3), (3, 3), (4, 4), (1, 6)],
    "multipler_comeout_winners": [(5, 6), (3, 4), (6, 5), (1, 6), (2, 2), (3, 4)],
    "multipler_comeout_losers": [(1, 1), (6, 6), (1, 2), (2, 1), (3, 3), (3, 4)],
    "hit_68_when_on_4": [(2, 2), (3, 3), (4, 4), (5, 1), (5, 3), (2, 4), (6, 2), (3, 4)],
    "8,8,3,5": [(4, 4), (4, 4), (1, 2), (2, 3), (3, 4)],
    "hit_all_except_point": [(2, 2), (2, 3), (3, 3), (4, 4), (4, 5), (5, 5), (3, 4)],
}
# fmt: on


def run_scenario(rolls):
    table = Table()
    player = table.add_player(bankroll=1000, strategy=STRATEGY_TO_TEST)

    table.fixed_run(dice_outcomes=rolls, verbose=True)

    print(f"Final bankroll: {player.bankroll:.2f}")
    # Show remaining open bets (should be few or none in these demos)
    # Note this does not run strategy to add/clear bets for next roll
    if player.bets:
        print("Open bets:", [str(bet) for bet in player.bets])


def main():
    for scenario, rolls in SCENARIOS.items():
        print(f"\n=== Scenario: {scenario} ===")
        print(f"Rolls: {rolls}")
        run_scenario(rolls)


if __name__ == "__main__":
    main()
