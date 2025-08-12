#!/usr/bin/env python3
import os
import sys

# Ensure repo root is on sys.path so "evo_engine" is importable
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from evo_engine import scoring

def main():
    # Fake roll history just for a sanity check
    rolls = [7, 6, 8, 7, 5, 9, 7]

    cq = scoring.table_cq(rolls)
    variance = scoring.variance_score(rolls)
    ef = scoring.ef_score(cq, variance, profit_loss=100)
    dz = scoring.danger_zone(cq, variance)

    print("TableCQ:", cq)
    print("VarianceScore:", variance)
    print("EF Score:", ef)
    print("Danger Zone:", dz)

if __name__ == "__main__":
    main()

