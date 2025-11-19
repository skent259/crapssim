# CrapsSim Engine API — Phase 1 Compatibility Scan

## 1. Context

- Target core version: `0.4.0`
- API branch: `api`
- Scan date: `2025-11-19`
- Summary: Scanned the current CrapsSim core surfaces against the HTTP API layer to catalog which engine objects the API touches, how bet verbs map onto engine bet classes, and where settings or behaviors diverge. Test baselines were captured to anchor future API evolution.

## 2. Engine Surface Map (What the API Touches)

### 2.1 Core Engine Modules

- `crapssim.bet`: Defines all bet classes, `BetResult`, vig helpers (`_compute_vig`, `_vig_policy`), and the `TableSettings` TypedDict consumed by API vig handling.
- `crapssim.table`: Provides `Table`, `Player`, and `TableSettings` defaults that the API reads/writes for vig configuration. Player bankroll changes and bet placement are driven here without raising engine-side errors.
- `crapssim.player` or equivalent: `Player` lives in `crapssim.table` and governs bankroll, add/remove bet behavior, and bet resolution, which the API relies on for state updates and legality checks.
- Other direct imports: the API pulls bet helpers directly in `http.py` and individual bet classes in `actions.py` and `capabilities.py`; no other core modules are imported directly.

### 2.2 Bet Types Covered by API Verbs

- PassLine — **Has API verb?** yes — **Verb name:** `pass_line` — amount only.
- Come — **Has API verb?** yes — **Verb name:** `come` — amount only.
- DontPass — **Has API verb?** yes — **Verb name:** `dont_pass` — amount only.
- DontCome — **Has API verb?** yes — **Verb name:** `dont_come` — amount only.
- Odds — **Has API verb?** yes — **Verb name:** `odds` — requires base bet (`pass_line`, `dont_pass`, `come`, `dont_come`, or `put`); pass/don’t versions infer the point, others require `number`; optional `working` flag.
- Put — **Has API verb?** yes — **Verb name:** `put` — requires `number`.
- Place — **Has API verb?** yes — **Verb name:** `place` — requires `number`.
- Field — **Has API verb?** yes — **Verb name:** `field` — amount only.
- CAndE — **Has API verb?** yes — **Verb name:** `c&e` — amount only.
- Any7 — **Has API verb?** yes — **Verb name:** `any7` — amount only.
- Two — **Has API verb?** yes — **Verb name:** `two` — amount only.
- Three — **Has API verb?** yes — **Verb name:** `three` — amount only.
- Yo — **Has API verb?** yes — **Verb name:** `yo` — amount only.
- Boxcars — **Has API verb?** yes — **Verb name:** `boxcars` — amount only.
- AnyCraps — **Has API verb?** yes — **Verb name:** `any_craps` — amount only.
- Horn — **Has API verb?** yes — **Verb name:** `horn` — amount only.
- World — **Has API verb?** yes — **Verb name:** `world` — amount only.
- Big6 — **Has API verb?** yes — **Verb name:** `big6` — amount only.
- Big8 — **Has API verb?** yes — **Verb name:** `big8` — amount only.
- HardWay — **Has API verb?** yes — **Verb name:** `hardway` — requires `number` (hardway point).
- Hop — **Has API verb?** yes — **Verb name:** `hop` — requires `result` as `[die1, die2]`.
- Fire — **Has API verb?** yes — **Verb name:** `fire` — amount only.
- All — **Has API verb?** yes — **Verb name:** `all` — amount only.
- Tall — **Has API verb?** yes — **Verb name:** `tall` — amount only.
- Small — **Has API verb?** yes — **Verb name:** `small` — amount only.
- Buy — **Has API verb?** yes — **Verb name:** `buy` — requires `number`.
- Lay — **Has API verb?** yes — **Verb name:** `lay` — requires `number`.

### 2.3 Table / Settings Assumptions

- Core `TableSettings` keys in use: `ATS_payouts`, `field_payouts`, `fire_payouts`, `hop_payouts`, `max_odds`, `max_dont_odds`, `vig_rounding`, `vig_floor`, `vig_paid_on_win`.
- API-assumed/specifiable keys: `field_pays`, `odds_policy`, `odds_limit_max_x`, `increments`, `vig.rounding`, `vig.floor`, `vig.paid_on_win`, `working_flags`, `enabled_props`, `enabled_buylay`, `enabled_put`, plus bet enablement implied by capabilities.
- Mismatches: Only vig-related fields are currently applied from the API spec into `Table.settings`; other spec knobs (field payouts, odds policy, increments, working flags, enablement toggles) are not wired into the core `TableSettings` or bet logic.

## 3. Detected Drift vs Core

- **Capabilities omit some supported bets (Big6/Big8) despite verbs existing.** Impact: medium impact — clients relying on capabilities may not attempt these bets even though the engine and verbs support them.
- **Table customization knobs in API spec (field pays, odds policy, increments, working flags, enablement toggles) are not propagated to `Table.settings`.** Impact: medium impact — API advertises or accepts settings the engine does not consume, so sessions silently run with engine defaults.
- **Engine bet placement rejects silently via no-op when bankroll or rules block, while API infers success via state deltas.** Impact: low impact — API compensates by pre-checking bankroll and verifying bet signature changes, but behavior relies on indirect detection rather than explicit engine errors.
- **Legacy reference to `crapssim_api/verbs.py` in expectations; verbs are implemented in `actions.py`.** Impact: low impact — documentation or external callers assuming a `verbs` module would need to target `actions.py` mappings instead.

## 4. Test Baseline (Phase 1-A)

- Command(s) executed:
  - `PYTHONPATH=. pytest -q`
    - Result: 3953 passed, 21 skipped in 9.91s. Skip reasons not displayed in `-q` output.
  - `PYTHONPATH=. pytest -q crapssim_api/tests`
    - Result: 50 passed, 20 skipped in 0.22s. Skip reasons not displayed in `-q` output.
  - `PYTHONPATH=. pytest -q crapssim_api/tests/stress/test_api_sequences.py`
    - Result: 1 skipped in 0.03s. Skip reason not displayed in `-q` output.

> Note: No code or configuration changes were made; all commands used the existing repository state.

## 5. Compatibility Verdict & Next-Step Hooks

- Verdict: The API is compatible with minor fixes; most bet classes are exposed, but capability metadata and table customization wiring lag behind the core defaults.
- Next steps:
  - Add capability entries (and any wiring) for Big6/Big8 or clarify their absence in advertised features.
  - Wire API `TableSpec` controls (field payouts, odds policy/limits, increments, working flags, enablement toggles) into `Table.settings` so sessions honor requested policies.
  - Consider explicit engine-side feedback for rejected bets to reduce reliance on post-hoc signature comparisons.
  - Align public docs/examples to `actions.py` as the verb map to avoid confusion with the non-existent `verbs.py` module.
