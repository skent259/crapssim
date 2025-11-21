from __future__ import annotations

__version__ = "0.2.1-api-p6"
ENGINE_API_VERSION = __version__
CAPABILITIES_SCHEMA_VERSION = 1


def get_identity() -> dict[str, str | int]:
    return {
        "engine_api_version": ENGINE_API_VERSION,
        "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
    }
