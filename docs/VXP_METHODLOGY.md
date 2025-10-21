# Vanilla Expansion Project (VXP) — Methods & Evidence

This document summarizes what changed, why it changed, and how we validated it.
It is meant to be a maintainer-facing record rather than a user guide.

## Scope

### New bet types
- **Horn** (net-modeled equal split across 2/3/11/12)  
- **World (Whirl)** (Horn + Any 7 break-even; net-modeled)  
- **Big6 / Big8** (even-money; persistent)  
- **Buy / Lay** (true-odds with commission policy knobs)  
- **Put** (legal only with point ON; odds optional)

### Policy toggles (Table.settings)
- `commission` (float rate, default `0.05`)
- `commission_mode`: `"on_win"` (default) | `"on_bet"`
- `commission_rounding`: `"none"` (default) | `"ceil_dollar"` | `"nearest_dollar"` (banker’s rounding)
- `commission_floor` (float dollars, default `0.0`)
- `commission_multiplier_legacy` (bool, default `True`)  
  If `True` **and** `commission_mode` **unset**, Buy/Lay use calibrated multipliers
  to preserve legacy simulation parity.
- `allow_put_odds` (bool, default `True`)

### Guards
- **Put** bets automatically stripped pre-roll when point is OFF.
- **One-roll props** (Horn/World) cannot persist post-resolution.

---

## Design choices (brief rationale)

- **Net-modeled Horn/World:**  
  We model equal-split books as a single net wager to keep payouts transparent and avoid sub-bet bookkeeping. This is documented and tested with EV pins.

- **Commission policy as first-class settings:**  
  Houses vary on “on-win vs on-bet,” rounding, and floors. We exposed the variants as settings and kept **defaults backward compatible**.

- **Legacy multiplier gate:**  
  Some existing baselines expected a number-based fee base when `commission_mode` wasn’t explicitly set. We retained it behind `commission_multiplier_legacy=True` and documented the behavior.

- **Odds behind Put:**  
  Default allowed (common), with a table toggle for strict houses.

---

## Validation methodology

1. **Unit tests**
   - EV and `repr` tests for new bets.
   - Input validation: Buy/Lay only on {4,5,6,8,9,10}.
   - Commission variants: `on_win`, `on_bet`, rounding, floor.
   - Put-odds toggle: odds refused when disabled.
   - Legacy gate: differential outcome proves the toggle is effective.

2. **Stress tests**
   - Randomized harness (`@pytest.mark.stress`) varying:
     - commission rate/mode/rounding/floor, `allow_put_odds`
     - bankroll size (including small)
     - injected illegal Put (guard check)
   - Invariants: no NaN/inf, no lingering one-roll props, Put absent when point OFF.

3. **Gauntlet runs**
   - Deterministic end-to-end scenarios:
     - Horn/World with PL present,
     - **PropsIsolated** (PL suppressed) to show **pure net**,
     - Big6/Big8 resolves,
     - Buy/Lay matrix with policy permutations,
     - Put with/without odds and illegal Put guard.
   - Artifacts per run: `gauntlet.json`, `gauntlet_rolls.csv` (with Δ), `summary.md`.
   - Batch evidence: 25 repeated runs, collated summaries retained.

4. **Semantic diff auditing**
   - AST-based normalization verifies C6–C10 are **non-behavioral** (annotations/docstrings/comments only).
   - Numeric literal sets in `bet.py`/`table.py` unchanged across doc passes.

---

## How to reproduce the evidence (developer quickstart)

```bash
# Install
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip wheel
pip install -e .
pip install pytest

# Default tests
pytest -q

# Stress (opt-in)
pytest -q -m stress

# Gauntlet (single run)
python tools/vxp_gauntlet.py

# Batch (20–30 runs)
bash -lc 'for i in $(seq 1 25); do python tools/vxp_gauntlet.py; sleep 0.2; done'

Artifacts live under reports/vxp_stress/ and reports/vxp_gauntlet/.
The gauntlet summary.md explicitly notes that Δ includes stake returns and whether the $5 Pass Line is present.
```

---

## Non-goals
	•	No core behavior changes outside the documented toggles.
	•	No opinionated house defaults beyond configurable settings.
	•	No extension API yet (planned as a separate proposal).

---
