# CrapsSim-Vanilla HTTP API — Roadmap (V2)

This roadmap tracks the lightweight, optional HTTP API for CrapsSim-Vanilla.
The API lives in `crapssim_api` and must **not** change core engine behavior.

Design tenets:

- No core rewrites. The engine stays the engine.
- Dumb I/O. Emit raw facts; clients compute stats and policies.
- Opt-in runtime. HTTP server only runs when explicitly started.
- Optional deps. `fastapi` / `uvicorn` are optional and only needed for HTTP.
- Clear responsibility split: Vanilla vs API vs external tools (e.g. CSC).

---

## Phase Status

| Phase | Title                                    | Status     | Notes                                                      |
| ----- | ---------------------------------------- | ---------- | ---------------------------------------------------------- |
| P1    | Core Types & Error Model                 | ✅ Done    | Data classes, enums, and error types defined in API layer.|
| P2    | Session & Point-Cycle Scaffolding        | ✅ Done    | Session, step-roll, and point-cycle utilities in place.   |
| P3    | HTTP Surface (FastAPI, Optional Import)  | ✅ Done    | Basic HTTP app created; FastAPI remains optional.         |
| P4    | DX & Capabilities Polish                 | ✅ Done    | `/health`, `/capabilities`, docs, and example client.     |
| P5    | Extended Orchestration & Tape Hooks      | Planned    | Optional helpers for orchestration and replay.            |
| P6    | Docs, Examples, and Long-Term Support    | Planned    | Final polish, docs hardening, and maintenance guidance.   |

---

## Notes

- The API package is optional. Users can run CrapsSim-Vanilla without ever importing or installing the HTTP pieces.
- All future changes to the API must respect the core design tenets above.
