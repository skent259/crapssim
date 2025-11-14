#!/usr/bin/env python
"""Emit the CrapsSim API fingerprint for compatibility checks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crapssim_api.version import CAPABILITIES_SCHEMA_VERSION, ENGINE_API_VERSION


def main() -> None:
    fingerprint = {
        "engine_api_version": ENGINE_API_VERSION,
        "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
    }
    print(json.dumps(fingerprint))


if __name__ == "__main__":
    main()
