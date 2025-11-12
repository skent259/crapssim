# REPORT_P3

- Verbs: add_bet ✅ remove_bet ✅ press_bet ✅ regress_bet ✅ (returns UNSUPPORTED) set_dice ✅ roll ✅ clear_all ✅
- Error codes: ILLEGAL_BET, BAD_INCREMENT, INSUFFICIENT_FUNDS, NOT_FOUND, FORBIDDEN, UNSUPPORTED, BAD_ARGUMENTS, INTERNAL
- Guarantee: No core math/behavior changed; router delegates to vanilla legality/funds checks; fixed dice gated by `debug.allow_fixed_dice`.

`pytest -q` → 11 errors in 2.66s
