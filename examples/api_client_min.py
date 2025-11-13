from __future__ import annotations

import json
import sys
from http.client import HTTPConnection


def _get(path: str) -> dict:
    conn = HTTPConnection("127.0.0.1", 8000, timeout=5)
    try:
        conn.request("GET", path)
        resp = conn.getresponse()
        body = resp.read().decode("utf-8")
    finally:
        conn.close()
    if resp.status != 200:
        raise RuntimeError(f"GET {path} failed with {resp.status}: {body}")
    return json.loads(body)


def main() -> int:
    try:
        health = _get("/health")
        print("Health:", health)
    except Exception as exc:  # pragma: no cover - manual example
        print(f"Error calling /health: {exc}", file=sys.stderr)
        return 1

    try:
        caps = _get("/capabilities")
        print("Capabilities:")
        print(json.dumps(caps, indent=2, sort_keys=True))
    except Exception as exc:  # pragma: no cover - manual example
        print(f"Error calling /capabilities: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":  # pragma: no cover - manual example
    raise SystemExit(main())
