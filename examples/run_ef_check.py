
from evo_engine import scoring

# Fake roll history for test
rolls = [7, 6, 8, 7, 5, 9, 7]

cq = scoring.table_cq(rolls)
variance = scoring.variance_score(rolls)
ef = scoring.ef_score(cq, variance, profit_loss=100)
dz = scoring.danger_zone(cq, variance)

print("TableCQ:", cq)
print("VarianceScore:", variance)
print("EF Score:", ef)
print("Danger Zone:", dz)
