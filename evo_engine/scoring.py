
import numpy as np
def variance_score(bankroll_curve:list[float], start_bankroll:float)->float:
    if not bankroll_curve or len(bankroll_curve)<2: return 0.0
    deltas=np.diff(np.array(bankroll_curve,dtype=float))
    if deltas.size==0: return 0.0
    stdev=float(np.std(deltas)); norm=stdev/max(1.0,float(start_bankroll))
    return float(min(1.5,max(0.0,norm)))
def ef_main(rolls_survived:int, profit:float, variance_norm:float, category_fit_bonus:float=0.0, start_bankroll:float=1000.0, max_rolls_cap:int=2000)->float:
    ps=max(0.0,min(1.0,rolls_survived/float(max_rolls_cap))); pr=max(-1.0,min(1.0,profit/float(start_bankroll))); vn=1.0-max(0.0,min(1.0,variance_norm))
    return round(0.5*ps+0.4*pr+0.1*vn+category_fit_bonus,6)
def ef_danger(rolls_survived:int, profit:float, variance_norm:float, category_fit_bonus:float=0.0, start_bankroll:float=1000.0, max_rolls_cap:int=2000)->float:
    ps=max(0.0,min(1.0,rolls_survived/float(max_rolls_cap))); pr=max(-1.0,min(1.0,profit/float(start_bankroll))); vn=1.0-max(0.0,min(1.0,variance_norm))
    return round(0.3*ps+0.3*pr+0.4*vn+category_fit_bonus,6)
def in_danger(variance_norm:float, threshold:float)->bool: return variance_norm>=threshold
