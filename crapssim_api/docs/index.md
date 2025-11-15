# CrapsSim HTTP API

The `crapssim_api` package exposes the vanilla CrapsSim engine over HTTP. It ships as a light-weight sidecar that keeps all game logic inside the core `crapssim` package while providing JSON endpoints for automation and tooling.

## Who this is for

- Developers who need a deterministic craps engine reachable over HTTP on a local network.
- Test harnesses that want to drive the full bet surface without embedding the Python engine.
- Integrators building dashboards or bots that rely on CrapsSim for rules and outcomes.

## Getting started

1. [Install the optional API extra](installation.md) to bring in FastAPI and uvicorn.
2. Start the app with `uvicorn crapssim_api.http:app --reload`.
3. Review the [verb reference](API_VERBS.md) for supported bets and management actions.
4. Run the minimal [API client example](../examples/api_client_min.py) to see an end-to-end flow.

## Capabilities & Non-Goals

**Capabilities**

- Full craps bet surface matching the vanilla engine (Pass/Don’t, Come/Don’t, Odds, Place/Buy/Lay/Big6/Big8, Field, Hardways, Horn/World, Any7/AnyCraps/2/3/11/12, Hop, Fire, All/Tall/Small).
- Bet-management verbs covering removal, reduction, layout clears, and toggling odds working.

**Non-Goals**

- Built-in authentication, rate limiting, or multi-tenant isolation.
- Persistence layers or bankroll analytics beyond the engine’s core snapshot.
- Exposure as an internet-facing service; it is intended to run as a local sidecar.

## Related documentation

Additional design notes and diagnostic reports live under [`dev/`](dev/README.md) for engine/API maintainers.
