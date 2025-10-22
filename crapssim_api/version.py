"""Version and schema identity for the CrapsSim-Vanilla HTTP API adapter."""

ENGINE_API_VERSION: str = "0.1.0-api.dev"
CAPABILITIES_SCHEMA_VERSION: int = 1

def get_identity() -> dict:
    """Return adapter identity for embedding in snapshots and responses."""
    return {
        "engine_api_version": ENGINE_API_VERSION,
        "capabilities_schema_version": CAPABILITIES_SCHEMA_VERSION,
    }
