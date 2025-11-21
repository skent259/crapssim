# Engine API Roadmap

### Phase 3·C — CI & Packaging Validation

- Added a dedicated `api-engine-ci` GitHub Actions workflow.
- Runs API tests against Python 3.10–3.13 without touching core engine behavior.
- Installs the Engine API via editable extras (`crapssim_api[api,dev,gauntlet]`).
- Runs both the fast unit suite and the sequence/gauntlet stress suite.
- Keeps the Engine API optional: core users are unaffected unless they enable the workflow or install extras.
