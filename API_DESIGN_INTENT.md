# CrapsSim API — Design Intent

This document captures targeted clarifications about the policy boundaries between CrapsSim-Vanilla components.

### Policy Responsibilities

- Vanilla engine: resolve bets and table state; no policy checks (increments, bankroll strategy, semantics).
- API layer: transport-only; passes commands to engine without extra constraints.
- CSC / tools: enforce increment rules, strategy validation, and advanced legality checks.
