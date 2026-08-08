# Come-Out Bet Behavior in Craps

This document summarizes the standard behavior of common craps bets during the **come-out roll** (when the puck is OFF).

It was prepared while researching [GitHub Issue #80](https://github.com/skent259/crapssim/issues/80) for the `crapssim` project.

For the simulator's implementation-level behavior matrix, see `docs/internal/BET_BEHAVIOR_MATRIX.md`.

> **Important:** Craps table rules are not completely standardized across all casinos. Some behaviors are universal, while others are house rules. Where casino practices differ, this document notes the uncertainty.

---

# Summary Table

| Bet | Default During Come-Out | Player Can Override? | Notes |
|------|-------------------------|----------------------|-------|
| Come Bet | ✅ Working | No | The contract bet always remains active. |
| Come Odds | ❌ Off | Yes ("Working") | Standard casino default. |
| Don't Come Bet | ✅ Working | No | Contract bet always remains active. |
| Don't Come Odds | ✅ Working | Yes ("Off") | Industry standard; this is the behavior described in GitHub Issue #80. |
| Place Bet | ❌ Off | Yes ("Working") | Typically follows the puck unless instructed otherwise. |
| Buy Bet | ❌ Off | Yes ("Working") | Generally treated the same as Place bets. |
| Lay Bet | ⚠ Usually Off (house rule) | Yes | Casino rules vary more than other bet types. |
| Put Bet | ⚠ House Rule | Yes | No widely documented industry standard. |

## Bet Removability vs. Working State

| Bet Type | Can Be Turned Off? | Can Be Removed? | Notes |
|----------|:------------------:|:---------------:|-------|
| Come Bet | ❌ No | ❌ No | Contract bet once established. Always working until resolved. |
| Come Odds | ✅ Yes | ✅ Yes | Default OFF during the come-out. May also be reduced. |
| Don't Come Bet | ❌ No | ✅ Yes | Not a contract bet. May be removed or reduced, but cannot simply be turned OFF while remaining on the layout. |
| Don't Come Odds | ✅ Yes | ✅ Yes | Default ON during the come-out. May be turned OFF, removed, or reduced. |
| Place Bet | ✅ Yes | ✅ Yes | Typically OFF during the come-out unless called "working." |
| Buy Bet | ✅ Yes | ✅ Yes | Typically treated the same as Place bets. May be turned OFF or removed. |
| Lay Bet | ✅ Yes* | ✅ Yes | Most casinos allow both, but the default come-out behavior is house-dependent. |
| Put Bet | ✅ Yes* | ✅ Yes | House rules vary. Generally treated similarly to Place or Buy bets. |

---

# 1. Come Bet

## How it works

A Come bet is essentially a Pass Line bet made after a point has already been established.

Example:

- Table point is 8.
- You make a $10 Come bet.
- Next roll is 5.
- Your Come bet moves onto the 5.

From that point forward, it behaves exactly like a Pass Line bet on the 5.

You win if:

- 5 rolls before 7.

You lose if:

- 7 rolls before 5.

---

## During the Come-Out

Suppose:

- Your Come bet is sitting on the 5.
- The shooter makes the table point.
- The puck turns OFF.

The Come bet itself **remains working**.

If the come-out roll is another 5:

- The Come bet wins immediately.

This is because the contract portion of the Come bet is always active.

### Odds are different

Only the **odds behind the Come bet** are OFF by default.

---

# 2. Come Odds

Come odds are an optional wager placed behind an established Come bet.

Example:

- Come bet travels to 6.
- You add $60 odds.

When the puck turns OFF:

Default behavior:

**OFF**

If the come-out roll is 6:

- The Come bet wins.
- The odds are simply returned without winning or losing.

If you want the odds active, tell the dealer:

> "Working."

The dealer will usually place an ON lammer behind the odds.

---

# 3. Don't Come Bet

A Don't Come bet is the opposite of a Come bet.

Example:

- Table point is 9.
- You make a Don't Come bet.
- Next roll is 4.

The bet moves behind the 4.

You now win if:

- 7 rolls before 4.

You lose if:

- 4 rolls before 7.

---

## During the Come-Out

Suppose:

- Your Don't Come bet is behind the 4.
- The shooter sevens out.
- A new shooter begins.

The Don't Come contract remains active.

If the come-out roll is:

- 4 → Lose
- 7 → Win

The contract bet itself does not automatically turn OFF.

---

# 4. Don't Come Odds

This is the subject of [GitHub Issue #80](https://github.com/skent259/crapssim/issues/80).

Suppose:

- Your Don't Come bet is behind the 4.
- You have laid odds behind it.
- A new shooter begins.

Industry-standard behavior:

**The odds remain WORKING during the come-out roll.**

Unlike Come odds, Don't Come odds are active unless the player specifically requests they be OFF.

This is intentionally the opposite of Come odds.

---

# 5. Place Bets

A Place bet is a wager that a particular box number will roll before a 7.

Example:

Place the 6.

You win if:

- 6 rolls before 7.

You lose if:

- 7 rolls first.

Unlike Pass or Come bets, Place bets are not contract bets and may be removed at any time.

---

## During the Come-Out

At most casinos:

**Place bets are OFF by default.**

Players often describe this as:

> "The Place bets follow the puck."

If you want them active during the come-out, you tell the dealer:

> "Place bets working."

---

# 6. Buy Bets

Buy bets work almost exactly like Place bets except they pay true odds and charge a commission (vig).

Example:

Buy the 4.

You win if:

- 4 rolls before 7.

You lose if:

- 7 rolls first.

---

## During the Come-Out

Standard behavior:

**OFF**

Players may request that Buy bets remain working.

Most casinos handle Buy bets the same way they handle Place bets.

---

# 7. Lay Bets

Lay bets are the opposite of Buy bets.

Example:

Lay the 10.

You win if:

- 7 rolls before 10.

You lose if:

- 10 rolls before 7.

---

## During the Come-Out

This is less standardized.

Many casinos default Lay bets to OFF unless instructed otherwise.

Other casinos treat them differently because they are effectively bets on the 7.

Published casino rules are less consistent on Lay bets than on Place or Buy bets.

For simulation software, Lay bets will be OFF on the come-out roll.

---

# 8. Put Bets

A Put bet allows a player to place a Pass Line-style contract directly onto a point number without first making a Come bet.

Example:

The table point is 8.

Instead of making a Come bet and waiting for it to travel, you simply Put $10 directly onto the 5.

You may immediately take odds.

You win if:

- 5 rolls before 7.

You lose if:

- 7 rolls before 5.

---

## During the Come-Out

There is no widely documented industry standard.

Many casinos appear to treat Put bets similarly to Place or Buy bets, allowing them to be either ON or OFF.

However, unlike Come odds or Don't Come odds, there is no authoritative published default that is consistently documented.

For simulation software, Put bets will be OFF on the come-out roll.

---

# Why GitHub Issue #80 Suggests an `always_working` Property

The discussion on Issue #80 suggests adding an `always_working` parameter to several bet classes:

- Place
- Buy
- Lay
- Put

The motivation is to make come-out behavior consistent throughout the codebase while allowing each bet type to specify its default behavior.

Example defaults might look like:

| Bet | Suggested Default |
|------|-------------------|
| Don't Come Odds | `always_working = True` |
| Place | `always_working = False` |
| Buy | `always_working = False` |
| Lay | `always_working = False` |
| Put | `always_working = False` |

This approach would centralize the "working" logic, reduce duplicated code, and make future casino rule variations easier to support.

---

# References

- Wikipedia: *Craps* – discussion of Come odds, Don't Come odds, Place bets, and working bets.
  https://en.wikipedia.org/wiki/Craps

- Easy.Vegas – Come Bet rules and working odds.
  https://easy.vegas/games/craps-come

- Hard Rock Atlantic City – Craps rules discussing Place and Buy bets.
  https://casino.hardrock.com/atlantic-city/casino/table-games/craps-at-hard-rock-atlantic-city

- GitHub Issue #80 (`crapssim`)
  "DC odds should be working during the come-out by default."
  https://github.com/skent259/crapssim/issues/80