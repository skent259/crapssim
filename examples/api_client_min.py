"""Minimal client for the optional CrapsSim HTTP API.

The script assumes a server is already running. It exercises the `/health`,
`/session/*`, and `/capabilities` routes to demonstrate control and state access.
"""
from __future__ import annotations

import json
import os
import sys
from urllib import request, error

REQUIRED_MODULES = ("fastapi", "pydantic")


def _ensure_api_deps() -> bool:
    missing = []
    for module_name in REQUIRED_MODULES:
        try:
            __import__(module_name)
        except ModuleNotFoundError:
            missing.append(module_name)
    if missing:
        print("This example requires the optional API extras.")
        print('Install with: pip install "crapssim[testing]" uvicorn')
        return False
    return True


def request_json(method: str, path: str, payload: dict | None = None) -> dict | None:
    base_url = os.environ.get("CRAPSSIM_API_BASE", "http://127.0.0.1:8000")
    url = base_url.rstrip("/") + path
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["content-type"] = "application/json"
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            payload = json.loads(body) if body else None
            print(f"{method} {path} -> {resp.status}")
            print(json.dumps(payload, indent=2))
            return payload
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        print(f"{method} {path} -> HTTP {exc.code}")
        if body:
            print(body)
    except error.URLError as exc:
        print(f"Failed to reach {url}: {exc.reason}")
    return None


def main() -> None:
    if not _ensure_api_deps():
        return

    request_json("GET", "/health")

    session_start = request_json("POST", "/session/start")
    if not session_start or not session_start.get("ok"):
        print("Session helper did not start; aborting further calls.")
        return

    request_json("GET", "/session/state")

    request_json("GET", "/capabilities")

    request_json("POST", "/session/roll", payload={"dice": [3, 4]})

    request_json("POST", "/session/stop")


if __name__ == "__main__":
    sys.exit(main())
