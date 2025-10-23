from __future__ import annotations

ENGINE_API_VERSION = "0.3.0-api-p3"
CAPABILITIES_SCHEMA_VERSION = 1


def get_identity() -> dict[str, str | int]:
    return {
        "engine_api_version": ENGINE_API_VERSION,
        "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
    }
