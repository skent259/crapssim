# Installation

The CrapsSim Engine API is an optional HTTP wrapper around the core `crapssim` engine. You can keep the engine lightweight or add the API extras when you want the FastAPI surface.

## Supported Python versions
- Python 3.10–3.13 are explicitly supported and exercised in CI.
- Older versions may work but are not validated; newer versions are adopted after CI coverage lands.

## Install options

### Engine only
Keep dependencies minimal when you only need the simulator:

```bash
pip install crapssim
```

### Engine + API
Install the FastAPI-powered layer via the published extra:

```bash
pip install "crapssim[api]"
```

### Editable checkout for contributors
From a local clone, install both the engine and API extras in editable mode:

```bash
python -m pip install -e ".[api]"
```

This matches the packaging metadata and keeps the API optional for core engine users.

## Run the server
Expose the packaged FastAPI application with uvicorn:

```bash
uvicorn crapssim_api.http:app --reload
```

The default port is 8000. The `app` object is created at import time, so the command above works without extra glue code.

## Quick health check
With the server running, verify the `/health` endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Expected response shape:

```json
{"status": "ok"}
```

You are now ready to start sessions and drive rolls via the documented verbs.
