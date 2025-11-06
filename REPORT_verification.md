# REPORT_verification

## A. Compliance Matrix
| Item | Status |
| --- | --- |
| Commission Logic | ✅ |
| Single `_compute_commission` only | ✅ |
| Fixed 5% (no settings) | ✅ |
| Floor is minimum | ✅ |
| Parity: on_bet == on_win | ✅ |
| Rounding (ceil/nearest/none) | ✅ |
| Buy/Lay use it correctly | ✅ |
| No “commission on gross win” paths remain | ✅ |
| Unit Tests | ✅ |
| File present and imports `_compute_commission` | ✅ |
| Param cases cover rounding/floor/modes | ✅ |
| Parity assertion included | ✅ |
| Tolerance 1e-9 | ✅ |
| Examples | ✅ |
| Horn amount set to 4.0 (single-line change) | ✅ |
| Gitignore | ✅ |
| All four entries present, no dupes | ✅ |
| Docs | ✅ |
| Changelog “Development version” added | ✅ |
| CONTRIBUTING.md removed | ✅ |
| Sanity | ✅ |
| `pytest -q` result | ✅ |
| `python -m examples.run_examples` result | ✅ |
| No stray REPORT_*/baseline artifacts tracked | ✅ |

## B. Notes & Next Steps
No follow-up needed.

Command results:
- `pytest -q` → `3878 passed, 1 skipped in 7.40s`
- `python -m examples.run_examples` → final line `Final bankroll: 98.00`
