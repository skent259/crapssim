# CrapsSim Engine API

The CrapsSim Engine API wraps the core CrapsSim engine with a stable HTTP surface powered by FastAPI. It keeps all craps rules and payout truth inside CrapsSim, exposing structured endpoints that are easy to integrate with CSC, Evo, or other automation tooling. The API ships as an optional package under `crapssim_api/` so core engine users are never forced to install HTTP dependencies.

## Quick Links
- Docs index and table of contents: [docs/README.md](docs/README.md)
- Minimal HTTP walk-through: [docs/quickstart.md](docs/quickstart.md)
- Determinism and replay overview: [docs/determinism.md](docs/determinism.md)
- Stress and gauntlet tests for parity checks: [docs/dev/testing.md](docs/dev/testing.md)
- Minimal client example (Python): [examples/api_client_min.py](examples/api_client_min.py)

## Who is this for?
- Developers integrating CrapsSim with external systems (CSC, Node-RED, Evo) who want a deterministic HTTP endpoint without reimplementing craps rules.
- Researchers who need a reproducible engine surface they can drive from Python, R, or any HTTP-capable environment.

The API does not implement game logic. Every decision, error code, and payout comes from the CrapsSim engine; the API only transports requests and responses.
