from player import Player
from CrapsTable import CrapsTable
import betting_strategies as strat
import sys 


def run_printout(n_roll, bankroll, strategy, strategy_name, runout):
    runout_str = "-runout" if runout else ""
    # Run one simulation with verbose=True to check strategy
    outfile_name = "./output/printout/{}_roll-{}_br-{}{}.txt".format(strategy_name, n_roll, bankroll, runout_str)
    print("Running simulations for {}_sim-{}_roll-{}_br-{}{}.txt".format(strategy_name, n_sim, n_roll, bankroll, runout_str))
    with open(outfile_name, 'w') as f_out:
        sys.stdout = f_out
        table = CrapsTable()
        table._add_player(Player(bankroll, strategy))
        table.run(n_roll, verbose=True)
    sys.stdout = sys.__stdout__ # reset stdout

def run_simulation(n_sim, n_roll, bankroll, strategy, strategy_name, runout):
    runout_str = "_runout" if runout else ""
    # Run simulation of n_roll rolls (estimated rolls/hour with 5 players) 1000 times
    outfile_name = "./output/simulations/{}_sim-{}_roll-{}_br-{}{}.txt".format(strategy_name, n_sim, n_roll, bankroll, runout_str)
    print("Running simulations for {}_sim-{}_roll-{}_br-{}{}.txt".format(strategy_name, n_sim, n_roll, bankroll, runout_str))
    with open(outfile_name, 'w') as f_out:
        # Headers to match out
        f_out.write("total_cash,n_rolls") 
        f_out.write(str('\n'))
        for i in range(n_sim):
            table = CrapsTable()
            table._add_player(Player(bankroll, strategy))
            table.run(n_roll, verbose=False, runout=runout)
            # write data to file
            out = "{},{}".format(table.total_player_cash, table.dice.n_rolls_)
            f_out.write(str(out))
            f_out.write(str('\n'))

def run_simulation_burnin(n_sim, n_roll, bankroll, strategy, strategy_name, burn_in=20, runout=True):
    runout_str = "_runout" if runout else ""
    # Run simulation of n_roll rolls (estimated rolls/hour with 5 players) 1000 times
    outfile_name = "./output/simulations/{}_sim-{}_roll-{}_br-{}_burnin{}.txt".format(strategy_name, n_sim, n_roll, bankroll, runout_str)
    print("Running simulations for {}_sim-{}_roll-{}_br-{}_burnin{}.txt".format(strategy_name, n_sim, n_roll, bankroll, runout_str))
    with open(outfile_name, 'w') as f_out:
        # Headers to match out
        f_out.write("total_cash,bankroll,n_rolls") 
        f_out.write(str('\n'))
        for i in range(n_sim):
            table = CrapsTable()
            table._add_player(Player(bankroll, strategy))

            table.run(burn_in, verbose=False, runout=False)
            burn_in_bankroll = table.total_player_cash
            table.run(n_roll, verbose=False, runout=runout)
            # write data to file
            out = "{},{},{}".format(table.total_player_cash, burn_in_bankroll, table.dice.n_rolls_)
            f_out.write(str(out))
            f_out.write(str('\n'))



if __name__ == "__main__":
    
    sim = True
    printout = True

    n_sim = 500000
    n_roll = 144
    bankroll = 2000
    strategy = strat._strat_passline_odds
    strategy_name = "passline-w-1odds" # don't include any "_" in this
    runout = False
    runout_str = "-runout" if runout else ""
        
    # if sim:
    #     run_simulation_burnin(n_sim, n_roll, bankroll, strategy, strategy_name, runout)

    # if printout:
    #     run_printout(n_roll, bankroll, strategy, strategy_name, runout)


    # Run multiple strategies
    strategies = [strat._strat_passline_odds, strat._strat_passline_odds2, strat._strat_passline_odds345]
    strategy_names = ["passline-w-1odds", "passline-w-2odds", "passline-w-345odds"]

    for strategy, strategy_name in zip(strategies,strategy_names):
        run_simulation_burnin(n_sim, n_roll, bankroll, strategy, strategy_name, burn_in=20, runout=runout)