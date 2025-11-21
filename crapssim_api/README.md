# CrapsSim Engine API

Optional HTTP API wrapper for the CrapsSim engine. This package exposes the engine via FastAPI while keeping the core engine untouched.

## Installation

To install the Engine API:

```bash
pip install crapssim[api]
```

For contributors:

```bash
pip install -e .[api]
```

## Session State & Metrics (Phase 5)

The Engine API will expose read-only session snapshots and metrics surfaces designed for CSC/Evo tools and research consumers. These views serialize the engine’s truth without adding business logic. See:

- [Session state snapshot design](docs/session_state.md)
- [Metrics surface design](docs/metrics_surface.md)
- [Determinism & replay contract](docs/DETERMINISM.md)
