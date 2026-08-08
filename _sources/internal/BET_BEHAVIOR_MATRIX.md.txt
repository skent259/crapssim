# Bet Behavior Matrix

This document defines the intended bet-resolution behavior in crapssim.

It is the implementation-focused reference for how bets resolve, whether they remain on the table, and how bankroll changes are applied.

## Scope

- This matrix captures current simulator behavior.
- Real-world casino rules vary by property.
- Where casinos vary, this project chooses explicit, testable defaults.

## Terms

- **WORKING** - Bet can resolve on this roll.
- **OFF** - Bet is temporarily inactive for this roll.
- **REMOVE** - Bet is taken off the table after resolution.
- **KEEP** - Bet remains active on the table after resolution.

## Come-Out Defaults (Point Off)

Policy setting: come_out_working_policy

- legacy: Place/Buy/Lay/Put are working by default.
- real_casino: Place/Buy/Lay/Put are off by default.

Per-bet always_working overrides the policy for Place/Buy/Lay/Put.

## Core Resolution Matrix

| Bet Type | Point Off + OFF Bet + Trigger Number Hits | Point Off + WORKING Bet Wins | Point Off + WORKING Bet Loses | Point On Win | Point On Loss |
| --- | --- | --- | --- | --- | --- |
| Place | No action, KEEP | Pay profit, KEEP | Lose stake, REMOVE | Pay profit, KEEP | Lose stake, REMOVE |
| Buy | No action, KEEP | Win payout (with vig policy), REMOVE | Lose stake (and vig when applicable), REMOVE | Win payout (with vig policy), REMOVE | Lose stake (and vig when applicable), REMOVE |
| Lay | No action, KEEP | Win payout (with vig policy), REMOVE | Lose stake (and vig when applicable), REMOVE | Win payout (with vig policy), REMOVE | Lose stake (and vig when applicable), REMOVE |
| Put | No action, KEEP | Win payout, REMOVE | Lose stake, REMOVE | Win payout, REMOVE | Lose stake, REMOVE |

## Contract Bets and Odds

| Bet Type | Come-Out Default | Notes |
| --- | --- | --- |
| Come (traveled) | WORKING | Contract behavior; remains active on come-out. |
| DontCome (traveled) | WORKING | Contract behavior; remains active on come-out. |
| Odds on Come | OFF by default | Can be set to working via always_working on odds bet. If OFF and a trigger number (base number or 7) rolls on come-out, odds push and are removed (stake returned). |
| Odds on DontCome | WORKING by default | Can be set off by always_working=False on odds bet. If OFF and a trigger number (base number or 7) rolls on come-out, odds push and are removed (stake returned). |

## Bankroll Accounting Rules

- Wins with REMOVE credit full returned amount (principal + winnings).
- Wins with KEEP credit profit only (principal stays on table).
- Losses never credit bankroll.
- OFF/no-action results do not change bankroll and do not remove the bet.
- Exception: OFF odds that hit a trigger on come-out push and are removed, returning principal.

## Example Outcomes

### Place 6, amount 12, real_casino mode, always_working unset

- Come-out roll of 6: no action, bet stays on table.
- Point-on roll of 6: pays 14 profit, bet stays up at 12.
- Roll of 7 while working: loses 12 and is removed.

### Buy 4, amount 10, real_casino mode, always_working unset

- Come-out roll of 4 or 7: no action, bet stays on table.
- WORKING roll of 4: win resolves and bet is removed.
- WORKING roll of 7: loss resolves and bet is removed.

### Put 6 with traveled Come 6 on come-out

- Put (off in real_casino): no action, stays on table.
- Traveled Come (contract): resolves as working.

## Related Files

- Settlement logic: crapssim/bet.py
- Bet update loop: crapssim/table.py
- Unit coverage: tests/unit/test_bet.py
- Integration coverage: tests/integration/test_bet.py, tests/integration/test_strategy.py, tests/integration/test_strategy_single_bet.py
