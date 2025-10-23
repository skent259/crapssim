from __future__ import annotations

__version__ = "0.4.0-api-p4"
ENGINE_API_VERSION = __version__
CAPABILITIES_SCHEMA_VERSION = 1


def get_identity() -> dict[str, str | int]:
    return {
        "engine_api_version": ENGINE_API_VERSION,
        "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
    }
