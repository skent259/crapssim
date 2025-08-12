
def table_cq(rolls):
    return 50  # placeholder score

def variance_score(rolls):
    return 0.5  # placeholder

def ef_score(cq, variance, profit_loss):
    return (100-cq)/100 * (1-variance) * (1 if profit_loss > 0 else 0.5)

def danger_zone(cq, variance):
    return cq > 80 or variance > 0.9
