# API Sync Report

## A. Checklist
- ✅ Vig model updated: API now reports vig via `_compute_vig`/`_vig_policy` helpers and no commission calls remain.
- ✅ Settings keys use `vig_*` / `vig_paid_on_win` across API, tests, and docs.
- ✅ Legacy identifiers (`compute_commission`, `_commission_policy`, `placement_cost`, `buy_vig_on_win`, `commission_mode`, raw `wager`) absent outside engine defaults; cleanup scan output below shows only sanctioned `vig_paid_on_win` references.
- ✅ API payloads, docs, and capability schema refer to vig terminology.
- ✅ No API logic depends on automatic Put takedowns.
- ✅ Horn/World handling defers to engine computations; no hard-coded ratios in API.
- ✅ Bankroll debits now use vig-aware `cash_required` derived from bet amount + `_compute_vig` when needed.
- ✅ Tests pass locally: `pytest -q`.
- ✅ Examples run: `python -m examples.run_examples`.

## B. Cleanup scans
```
crapssim/bet.py:69:    vig_paid_on_win: bool
crapssim/bet.py:766:    Vig may be taken on the win or upfront based on ``vig_paid_on_win``.
crapssim/bet.py:786:        if table.settings.get("vig_paid_on_win", True):
crapssim/bet.py:793:            if table.settings.get("vig_paid_on_win", True):
crapssim/bet.py:819:    Vig may be taken on the win or upfront based on ``vig_paid_on_win``.
crapssim/bet.py:839:        if table.settings.get("vig_paid_on_win", True):
crapssim/bet.py:846:            if table.settings.get("vig_paid_on_win", True):
crapssim/table.py:167:      vig_paid_on_win: bool
crapssim/table.py:179:    vig_paid_on_win: bool
crapssim/table.py:199:            "vig_paid_on_win": False,
crapssim_api/http.py:44:    "vig_paid_on_win": False,
crapssim_api/http.py:105:            settings["vig_paid_on_win"] = paid
crapssim_api/http.py:118:            updated["paid_on_win"] = vig_settings["vig_paid_on_win"]
crapssim_api/http.py:262:                "paid_on_win": bool(table_settings.get("vig_paid_on_win", False)),
crapssim_api/http.py:264:            if not table_settings.get("vig_paid_on_win", False):
docs/internal/VXP_METHODOLOGY.md:18:- `vig_paid_on_win`: (bool, default `False`)
docs/supported-bets.md:57:- `vig_paid_on_win` (bool, default `False`)
docs/supported-bets.md:66:The `vig_paid_on_win` setting will determine whether to charge the vig after the bet wins (if `True`)
or up-front when the bet is placed (if `False`). For example, if there is a $20 buy bet on the 4, up-front cost is $21 ($1 vig)
and a win will give the player $60 = $40 win + $20 bet cost. If the vig is paid on win, the up-front cost is $20 and a win will
give the player $59 = $40 win + $20 bet cost - $1 vig.
tools/vxp_gauntlet.py:140:            "settings": {"vig_rounding": "none", "vig_paid_on_win": True},
tools/vxp_gauntlet.py:147:                "vig_paid_on_win": False,
```

## C. Commands summary
- ✅ `PYTHONPATH=. pytest -q`
- ✅ `PYTHONPATH=. python -m examples.run_examples`

### Files touched
- `crapssim_api/http.py` — migrate commission fields to vig, persist session vig settings, and debit bankrolls via vig-aware cash requirements.
- `crapssim_api/types.py` — rename commission typed dicts to vig equivalents for capabilities/specs.
- `tests/api/test_apply_action_bankroll.py` — cover vig-aware debits and new response fields.
- `tests/api/test_baseline_smoke.py`, `tests/integration/test_vxp_baseline.py`, `tests/stress/test_vxp_torture.py` — update expectations/comments to new terminology.
- Documentation (`docs/**`, `tools/vxp_stress_report.py`) — reflect vig naming and policy knobs.
- `crapssim/bet.py` — tidy docstrings to avoid forbidden legacy terms.

## D. Follow-ups
- None.
