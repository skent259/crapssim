# Bet Management Verbs

The CrapsSim API now includes dedicated verbs for manipulating bets that are
already on the layout. These helpers operate entirely within the API layer and
respect the engine's `is_removable` checks, so non-removable bets remain in
place.

- `remove_bet` — remove bets of a given type (and optional number) when the bet
  reports itself as removable. Chips are returned to the player's bankroll.
- `reduce_bet` — lower the total amount on a given bet type/number to
  `new_amount`. Attempts to increase the action are rejected.
- `clear_all_bets` — remove every removable bet for the player.
- `clear_center_bets` — remove Field, prop, hop, Fire, ATS, and other
  center-action bets.
- `clear_place_buy_lay` — clear Place, Buy, and Lay bets.
- `clear_ats_bets` — remove All/Tall/Small bets.
- `clear_fire_bets` — remove Fire bets.

These verbs only adjust existing bet state; they do not implement any betting
strategy or payoffs.

## Working Status

- Engine-level working support detected: **YES** — the `Odds` bet exposes an
  `always_working` flag.
- `set_odds_working` toggles the `always_working` flag for matching odds bets
  (identified by base bet and number).

Generic working-status control for other bet types is not currently exposed by
the engine.
