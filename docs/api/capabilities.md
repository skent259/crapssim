# CrapsSim-Vanilla API — Capabilities

### GET /capabilities
Returns engine capability truth table and supported bet families.

### POST /start_session
Accepts `{spec, seed}` and returns session snapshot including normalized capabilities.

See `examples/api_showcase_capabilities.py` for usage.
