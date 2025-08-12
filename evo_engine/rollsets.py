
import random
def _roll_until_seven_out(rng: random.Random):
    rolls = []; point=None
    while True:
        d1=rng.randint(1,6); d2=rng.randint(1,6); total=d1+d2; rolls.append((d1,d2))
        if point is None:
            if total in (4,5,6,8,9,10): point=total
        else:
            if total==7: return rolls
            elif total==point: point=None
def generate_roll_set(num_shooters:int, seed:int|None=None)->dict:
    rng=random.Random(seed); all_rolls=[]
    for _ in range(max(1,int(num_shooters))): all_rolls.extend(_roll_until_seven_out(rng))
    return {"rolls": all_rolls, "meta":{"num_shooters":num_shooters,"seed":seed}}
def compute_table_cq(roll_set:dict)->int:
    totals=[sum(r) for r in roll_set.get("rolls",[])]; 
    if not totals: return 60
    sevens=totals.count(7)
    points_made=sum(1 for i in range(1,len(totals)) if totals[i-1] in (4,5,6,8,9,10) and totals[i]==totals[i-1])
    length=max(1,len(totals)); seven_rate=sevens/length; made_rate=points_made/length
    cq=70+int(20*made_rate)-int(50*seven_rate)
    return max(0,min(100,cq))
def validate_table_cq(cq:int, ok_range=(40,90))->bool: return ok_range[0]<=cq<=ok_range[1]
