# CrapsSim Engine API Docs

The `crapssim_api` package wraps the CrapsSim engine with an optional FastAPI surface. It keeps all craps rules and payouts inside the engine while exposing deterministic HTTP verbs that automation tools, CSC/Evo pipelines, or research notebooks can drive.

## Table of Contents
- [Overview](overview.md)
- [Quickstart](quickstart.md)
- [Installation](installation.md)
- [API verbs](verbs.md) with supporting [error semantics](errors.md)
- [Determinism & replay](determinism.md)
- [Session state](session_state.md), [metrics](metrics.md), and [push semantics](push_semantics.md)
- [Gauntlet overview](gauntlet_user.md)
- [Developer docs](dev/README.md)

## Getting Started
Start with the [Quickstart](quickstart.md) for a minimal session→bet→roll walkthrough, then review the [verb reference](verbs.md) to see the full bet surface. Installation details for the optional HTTP extras live in [installation.md](installation.md).

## For Developers & Maintainers
- Stress suites and gauntlet workflow: [dev/testing.md](dev/testing.md)
- Roadmap, philosophy, compatibility notes, and reports: [dev/](dev/README.md)

## Determinism & Replay
Seeded runs and replay tapes enable reproducible sequences for parity checks and research. See [determinism.md](determinism.md) for how seeds, dice injection, and tapes interact with the engine’s authoritative outcomes.
