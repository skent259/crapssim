# Engine API Status & Compatibility

## Python support window
- Declared support: Python 3.10–3.13.
- CI coverage mirrors the declared window across unit, stress, and gauntlet workflows.
- Older versions are not guaranteed; newer versions are adopted after CI validation.

## Packaging and optional extras
- Core installs remain lightweight: `pip install crapssim` pulls only the simulator.
- API usage is opt-in via extras: `pip install "crapssim[api]"` or editable installs with `.[api]`.
- Dev and gauntlet extras layer on additional tools without affecting the core package.

## CI alignment (Phase 6)
- `api-engine-ci` runs API unit and stress suites on Python 3.10–3.13 using editable installs.
- The gauntlet workflow covers deeper sequence and parity checks on the same window.
- Linting workflows target the API package without changing engine behavior.

## Compatibility plan snapshot
Phase 6 focused on documenting and enforcing the compatibility story:
- Declared Python classifiers and `requires-python` values in packaging metadata.
- Guarded optional imports (FastAPI, Pydantic) while keeping determinism hooks stable.
- Ensured tests skip gracefully when optional HTTP dependencies are absent.
