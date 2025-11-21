# Installing the CrapsSim Engine API

This document explains how to install and use the CrapsSim Engine API as an **optional** extension on top of the core CrapsSim engine.

> **Status:** Phase 3·B wiring in place. Package names, extras, and install commands are now live.

---

## 1. Core Engine vs Engine + API

The CrapsSim project has two distinct layers:

- **Core engine (`crapssim`)**  
  - Responsible for all game logic, rules, and outcomes.  
  - This is the single source of truth for craps behavior.  
  - It does not require the HTTP API to function.

- **Engine API (`crapssim_api`)**  
  - An optional HTTP wrapper that exposes the engine over a FastAPI app.  
  - Intended for tools, controllers, and external systems that want to talk to CrapsSim via HTTP rather than direct Python imports.  
  - Should remain clearly separated so engine users are not forced to install extra dependencies.

The goal of this document is to spell out how to install each layer cleanly.

---

## 2. Python Version Support (Declared)

The Engine API advertises support for:

- **Python 3.10, 3.11, 3.12, 3.13**
- Older versions are not guaranteed to work.
- Newer versions may work but are not declared until CI verifies them.

---

## 3. Dependency Groups (Conceptual)

To avoid bloating core engine users, we treat dependencies in three conceptual groups:

- **Core engine dependencies**  
  - Whatever `crapssim` itself needs today.  
  - These will not be changed or expanded just because the Engine API exists.

- **Engine API runtime dependencies**  
  - Frameworks required to actually run the HTTP API, such as:
    - FastAPI
    - Pydantic
    - Uvicorn
    - typing-extensions
  - These will be grouped together so they can be installed only when the API is needed.

- **Dev / test extras (future refinement)**  
  - Tools used only for testing and development of the API layer, such as:
    - pytest
    - HTTP client libraries (e.g. httpx)
  - These will be treated as an optional extra so they do not affect normal users.

Phase 3·B will wire these concepts into the actual packaging configuration (e.g. extras in `pyproject.toml` / `setup.cfg`).

---

## 4. Installation Patterns (Live Commands)

- **Engine-only install (no API):**
  - `pip install crapssim`
- **Engine + API in one environment:**
  - `pip install crapssim[api]`
- **Editable install for contributors:**
  - From a local clone, run `pip install -e .[api]`
- **CI / manual gauntlet setup:**
  - From a local clone, run `pip install -e .[gauntlet]`

---

## 5. Next Steps

Phase 3 is split into three steps:

- **P3·A (this document):**  
  - Design and write down the support window, dependency groups, and installation approach.

- **P3·B (metadata + wiring):**  
  - Update packaging configuration so the declared Python versions and extras match this intent.  
  - Finalize the exact `pip install` commands and examples.

- **P3·C (CI + verification):**  
  - Ensure CI runs API tests across the advertised Python versions.  
  - Confirm that local installs and CI installs follow the same documented path.

Until P3·B and P3·C are complete, treat this document as the design contract for how the Engine API should behave from a packaging and installation perspective.
