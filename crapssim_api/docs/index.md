# CrapsSim Engine API Docs

The `crapssim_api` package wraps the CrapsSim engine with an optional FastAPI surface. It keeps all craps rules and payouts inside the engine while exposing deterministic HTTP verbs that automation tools, CSC/Evo pipelines, or research notebooks can drive.

## Table of Contents
- [Quickstart](quickstart.md)
- [Installation](INSTALLING_ENGINE_API.md)
- [API verbs and contracts](API_VERB_INDEX.md) with supporting [error semantics](API_ERRORS_AND_CONTRACT.md)
- [Determinism & replay](DETERMINISM.md)
- [Session state and metrics surfaces](session_state.md) and [metrics overview](metrics_surface.md)
- [Developer stress and gauntlet tests](dev/testing.md)
- [Roadmap / design notes](ROADMAP.md)

## Getting Started

Start with the [Quickstart](quickstart.md) for a minimal session→bet→roll walkthrough, then review the [API verb index](API_VERB_INDEX.md) to see the full bet surface. Installation details for the optional HTTP extras live in [INSTALLING_ENGINE_API.md](INSTALLING_ENGINE_API.md).

## For Developers & Maintainers

- Stress suites and gauntlet workflow: [dev/testing.md](dev/testing.md)
- Deep design references and reports: [dev/](dev/README.md)

## Determinism & Replay

Seeded runs and replay tapes enable reproducible sequences for parity checks and research. See [DETERMINISM.md](DETERMINISM.md) for how seeds, dice injection, and tapes interact with the engine’s authoritative outcomes.
