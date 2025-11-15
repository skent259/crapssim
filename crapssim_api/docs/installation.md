# Installation

The HTTP API ships as an optional extra so that core `crapssim` users do not need to install web dependencies unless they want them.

## Install with the API extra

```bash
pip install "crapssim[api]"
```

For local development you can install the editable checkout:

```bash
python -m pip install -e ".[api]"
```

## Run the server

Use uvicorn to expose the packaged FastAPI application:

```bash
uvicorn crapssim_api.http:app --reload
```

The default port is 8000. The `app` object is created at import time so the command above works without extra glue code. The `api` extra also installs `requests` so the bundled example client can run without additional packages.

## Quick health check

With the server running, verify the `/health` endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status": "ok"}
```

You are now ready to start sessions and drive rolls via the documented verbs.
