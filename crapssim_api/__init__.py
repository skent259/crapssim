"""CrapsSim HTTP API adapter.

This package exposes a thin, deterministic API surface on top of the engine.
Phase 2 introduces compatibility metadata, dependency extras, and push-aware
reporting while keeping game logic in the core engine.
"""

from .version import ENGINE_API_VERSION, get_identity  # re-export helper

__version__ = "0.2.0"
__determinism_contract__ = "v1.0"

__all__ = [
    "__version__",
    "ENGINE_API_VERSION",
    "get_identity",
    "__determinism_contract__",
]
