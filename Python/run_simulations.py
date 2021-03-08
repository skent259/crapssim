from crapssim import Table
from crapssim import Player
from crapssim import strategy
import sys 
import os 


def run_printout(n_roll, n_shooter, bankroll, strategy, strategy_name, runout):
    runout_str = "-runout" if runout else ""
    # Run one simulation with verbose=True to check strategy
    outfile_name = f"./output/printout/{strategy_name}_roll-{n_roll}_shooter-{n_shooter}_br-{bankroll}{runout_str}.txt"
    # outfile_name = "./output/printout/{}_roll-{}_br-{}{}.txt".format(strategy_name, n_roll, bankroll, runout_str)
    print("Running printout for " + os.path.basename(outfile_name))
    # print("Running printout for {}_sim-{}_roll-{}_br-{}{}.txt".format(strategy_name, n_sim, n_roll, bankroll, runout_str))
    with open(outfile_name, 'w') as f_out:
        sys.stdout = f_out
        table = Table()
        table.add_player(Player(bankroll, strategy))
        table.run(n_roll, n_shooter, verbose=True)
    sys.stdout = sys.__stdout__ # reset stdout

def run_simulation(n_sim, n_roll, bankroll, strategy, strategy_name, runout):
    runout_str = "_runout" if runout else ""
    # Run simulation of n_roll rolls (estimated rolls/hour with 5 players) 1000 times
    outfile_name = "./output/simulations/{}_sim-{}_roll-{}_br-{}{}.txt".format(strategy_name, n_sim, n_roll, bankroll, runout_str)
    print("Running simulations for {}_sim-{}_roll-{}_br-{}{}.txt".format(strategy_name, n_sim, n_roll, bankroll, runout_str))
    with open(outfile_name, 'w') as f_out:
        # Headers to match out
        f_out.write("total_cash,bankroll,n_rolls") 
        f_out.write(str('\n'))
        for _ in range(n_sim):
            table = Table()
            table.add_player(Player(bankroll, strategy))
            table.run(n_roll, verbose=False, runout=runout)
            # write data to file
            out = "{},{},{}".format(table.total_player_cash, bankroll, table.dice.n_rolls_)
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
        for _ in range(n_sim):
            table = Table()
            table.add_player(Player(bankroll, strategy))

            table.run(burn_in, verbose=False, runout=False)
            burn_in_bankroll = table.total_player_cash
            table.run(n_roll, verbose=False, runout=runout)
            # write data to file
            out = "{},{},{}".format(table.total_player_cash, burn_in_bankroll, table.dice.n_rolls_)
            f_out.write(str(out))
            f_out.write(str('\n'))

def run_multi_simulation(n_sim, n_roll, n_shooter, bankroll, strategy, name, runout=True):
    runout_str = "_runout" if runout else ""
    # Run simulation of n_roll rolls (estimated rolls/hour with 5 players) 1000 times
    outfile_name = "./output/simulations/{}_sim-{}_roll-{}_br-{}_burnin{}.txt".format(name, n_sim, n_roll, bankroll, runout_str)
    print("Running simulations for {}_sim-{}_roll-{}_br-{}_burnin{}.txt".format(name, n_sim, n_roll, bankroll, runout_str))
    with open(outfile_name, 'w') as f_out:
        # Headers to match out
        f_out.write("simid,strategy,total_cash,bankroll,n_rolls") 
        f_out.write(str('\n'))
        for i in range(n_sim):
            if i % 1000 == 0:
                print(f"i: {i}")
            table = Table() 
            table.set_payouts("fielddouble", [2])
            table.set_payouts("fieldtriple", [12])
            for bank, s in zip(bankroll, strategy):
                table.add_player(Player(bank, strategy[s], s))

            # table.run(burn_in, verbose=False, runout=False)
            # burn_in_bankroll = table.total_player_cash
            table.run(n_roll, n_shooter, verbose=False, runout=runout)
            # write data to file
            # TODO: get actual player cash 
            for bank, s in zip(bankroll, strategy):
                out = f"{i},{s},{table._get_player(s).bankroll},{bank},{table.dice.n_rolls}"
                # out = "{},{},{},{}".format(s, table.total_player_cash, bank, table.dice.n_rolls_)
                f_out.write(str(out))
                f_out.write(str('\n'))



if __name__ == "__main__":
    
    sim = True 
    printout = True

    n_sim = 10
    n_roll = float('inf')
    n_shooter = 1
    bankrolls= [10000]
    strategies = {"passline": strategy.passline}
    name = "testing"
    # strategy = strat._strat_place68
    # strategy_name = "place68" # don't include any "_" in this
    runout = True
    # runout_str = "-runout" if runout else ""

    """ Run one strategy  """
    if printout: 
        for bank, s in zip(bankrolls, strategies):
            run_printout(n_roll, n_shooter, bank, strategies[s], s, runout)    
        # run_printout(n_roll, bankroll, strategy, strategy_name, runout)

    if sim:
        run_multi_simulation(n_sim, n_roll, n_shooter, bankrolls, strategies, name, runout)
        # run_simulation_burnin(n_sim, n_roll, bankroll, strategy, strategy_name, burn_in=20, runout=runout)

    

    """ Run multiple strategies """
    # strategies = [strat._strat_place68, strat._strat_place68_2come, strat._strat_pass2come, strat._strat_passline_odds2]
    # strategy_names = ["place68", "place68-2come", "pass-2come", "passline-w-2odds"]

    # for strategy, strategy_name in zip(strategies,strategy_names):
    #     # run_simulation_burnin(n_sim, n_roll, bankroll, strategy, strategy_name, burn_in=20, runout=runout)
    #     run_simulation(n_sim, n_roll, bankroll, strategy, strategy_name, runout=runout)
