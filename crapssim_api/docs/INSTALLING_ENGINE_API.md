# Installing the CrapsSim Engine API

This document explains how to install and use the CrapsSim Engine API as an **optional** extension on top of the core CrapsSim engine.

> **Status:** Draft for Phase 3. The intent and structure are defined here; exact package names, extras, and examples will be finalized in Phase 3·B and 3·C once metadata and CI are wired up.

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

## 2. Python Version Support (Design Intent)

The Engine API is being designed with the following Python versions in mind:

- Target support window: **3.10, 3.11, 3.12, 3.13**
- Older versions are not guaranteed to work.
- Newer future versions may work but will not be claimed until CI verifies them.

Exact metadata (`python_requires`, classifiers) will be updated in Phase 3·B so that the packaging configuration matches this intent.

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

## 4. Installation Patterns (To Be Finalized)

This section will be filled in concretely in Phase 3·B and 3·C. The expected patterns are:

- **Engine-only install (no API):**
  - Something equivalent to:
    - `pip install crapssim`
- **Engine + API in one environment:**
  - Something equivalent to:
    - `pip install crapssim[api]`
- **Editable install for contributors:**
  - From a local clone, something equivalent to:
    - `pip install -e .[api]`
  - Then run the test suite and manual gauntlet workflows.

Once the packaging metadata and CI are updated, this section will be revised with exact commands and any caveats discovered during testing.

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
