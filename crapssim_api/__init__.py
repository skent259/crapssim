"""CrapsSim-Vanilla HTTP API adapter (skeleton).

This package exposes a thin, deterministic API surface on top of the engine.
Phase 1 focuses on scaffolding and test visibility only.
"""

from .version import ENGINE_API_VERSION, __version__, get_identity  # re-export helper

__all__ = ["__version__", "ENGINE_API_VERSION", "get_identity"]

