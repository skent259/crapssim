# Phase 6 — Python Compatibility & Packaging Plan

## 1. Current Support and CI Matrix

### 1.1 Declared Python Versions

- Core package (`setup.cfg`): `python_requires >=3.10`; classifiers only declare generic "Python :: 3" with no per-version specificity.【F:setup.cfg†L12-L22】
- Engine API (`crapssim_api/pyproject.toml`): classifiers list Python 3.10, 3.11, 3.12, and 3.13 with `requires-python >=3.10`; mirrored in `crapssim_api/setup.cfg` extras metadata.【F:crapssim_api/pyproject.toml†L1-L36】【F:crapssim_api/setup.cfg†L1-L27】
- Top-level docs (e.g., `crapssim_api/docs/INSTALLING_ENGINE_API.md`) already state API support for Python 3.10–3.13.【F:crapssim_api/docs/INSTALLING_ENGINE_API.md†L22-L32】

### 1.2 CI Python Matrix

- Core workflow (`python-package.yml`): runs lint + pytest on Python 3.10–3.13 but does not target the Engine API specifically.【F:.github/workflows/python-package.yml†L14-L40】
- API-focused workflow (`api-engine-ci.yml`): executes API unit and stress suites on Python 3.10–3.13 with editable installs of both the core engine and `crapssim_api` extras `[api,dev,gauntlet]`.【F:.github/workflows/api-engine-ci.yml†L14-L39】
- API gauntlet workflow (`crapsim_api_gauntlet.yml`): runs stress/gauntlet suites on Python 3.11–3.13 via `[tests,gauntlet]` extras.【F:.github/workflows/crapsim_api_gauntlet.yml†L13-L52】
- API linting workflow (`ci.yml`): uses only Python 3.12 for ruff/black checks against `crapssim_api`.【F:.github/workflows/ci.yml†L15-L34】
- Current gaps: core CI covers engine on 3.10–3.13 but is not API-aware; gauntlet skips 3.10; linting fixed at 3.12.

## 2. Engine API Dependencies

### 2.1 Runtime Imports

- Non-stdlib imports inside `crapssim_api` include `fastapi`, `pydantic`, `uvicorn`, and `typing_extensions` (explicit in packaging metadata).【F:crapssim_api/pyproject.toml†L24-L36】
- `crapssim_api/http.py` lazily imports FastAPI symbols and provides stub fallbacks when the modules are missing; `_ensure_fastapi` raises a runtime error if the server is invoked without FastAPI installed.【F:crapssim_api/http.py†L7-L41】【F:crapssim_api/http.py†L23-L33】
- `pydantic` is attempted first (v2), then v1-style `validator`, and finally a no-op stub if completely unavailable, meaning the module remains importable without Pydantic but validation weakens.【F:crapssim_api/http.py†L35-L69】
- `crapssim_api/types.py` imports `TypedDict` from `typing_extensions`; all other imports are from `typing`. No guards are present there, so the module requires `typing_extensions` at import time.【F:crapssim_api/types.py†L3-L7】

### 2.2 typing_extensions vs typing

- `types.py` depends on `typing_extensions.TypedDict` regardless of Python version, even though `typing.TypedDict` is available in the stdlib for 3.8+. This forces `typing-extensions` as a hard dependency today.【F:crapssim_api/types.py†L3-L7】
- Packaging for the Engine API lists `typing-extensions>=4.5` both in core dependencies and the `[api]` extra, so all installs currently pull it in unconditionally.【F:crapssim_api/pyproject.toml†L24-L36】【F:crapssim_api/setup.cfg†L20-L27】

### 2.3 HTTP Layer Optionality

- FastAPI imports in `http.py` are guarded by try/except with stub replacements; server creation via `_ensure_fastapi` enforces presence when routes/apps are instantiated.【F:crapssim_api/http.py†L7-L41】【F:crapssim_api/http.py†L23-L33】
- Pydantic imports degrade gracefully (v2 → v1 → stub), allowing module import even when Pydantic is absent, at the cost of validation fidelity.【F:crapssim_api/http.py†L35-L69】
- Test suite uses `pytest.importorskip` for `fastapi`/`pydantic` across integration, stress, and some unit suites, skipping cleanly when deps are missing; some tests also gate on TestClient availability.【F:crapssim_api/tests/integration/test_session_state.py†L1-L17】【F:crapssim_api/tests/stress/test_api_sequences.py†L1-L11】

## 3. Packaging & Extras Strategy

### 3.1 Proposed Installation Story

- Core users: `pip install crapssim` should remain lightweight and **not** pull HTTP dependencies by default.
- Engine API users: propose `pip install crapssim[api]` as the canonical extra to enable the HTTP Engine API and associated tooling (matching existing docs and workflows). This should install FastAPI, Pydantic, Uvicorn, and any compatibility helpers.
- Contributors/CI: editable installs can continue to use `pip install -e .[api]` (or `.[api,dev]`) to run API suites; gauntlet/stress extras remain additive.

### 3.2 Optional Dependencies (Draft)

- API extra should include: `fastapi`, `pydantic`, `uvicorn`, and `typing-extensions` (conditionally for <3.11 if we switch `TypedDict` to stdlib on newer versions).
- Dev/gauntlet extras can continue to layer pytest/httpx as today, keeping them separate from runtime API needs.

## 4. Phase 6 Implementation Plan

### 4.1 Changes for 6·B

- Add/confirm an `[api]` extra on the root package so `pip install crapssim[api]` pulls HTTP deps without affecting core installs.
- Refine imports so importing `crapssim_api` modules (e.g., `types.py`) does not hard-require FastAPI when unused; keep `_ensure_fastapi` for server startup.
- Adjust `TypedDict` usage to prefer `typing.TypedDict` on Python ≥3.11, falling back to `typing_extensions` only when needed.
- Ensure tests that rely on optional deps continue to skip gracefully when deps are absent; avoid regressions in existing guards.

### 4.2 Changes for 6·C

- Update CI matrices so Engine API tests (at least smoke/sequence slices) run on every supported Python version, including 3.10.
- Add CI steps that install the API extra (and dev/gauntlet extras as appropriate) before running HTTP-related tests.
- Validate documented install commands (`pip install crapssim[api]`, editable variants) across the full supported version set.

## 5. Open Questions and Assumptions

- Should `typing-extensions` remain an unconditional dependency for API users, or be conditional based on Python version to reduce overhead?
- Do we need to align core package classifiers with the Engine API’s explicit 3.10–3.13 listing, or keep core broader until CI coverage is updated?
- How should the stubbed Pydantic behavior be handled when Pydantic is absent—should imports fail fast to avoid silent validation gaps?
- Are there additional docs that should advertise the API extra once wired at the root level, or is the existing `INSTALLING_ENGINE_API` sufficient after alignment?
