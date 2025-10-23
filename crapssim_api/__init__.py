"""CrapsSim-Vanilla HTTP API adapter (skeleton).

This package exposes a thin, deterministic API surface on top of the engine.
Phase 1 focuses on scaffolding and test visibility only.
"""

from .version import get_identity  # re-export helper

__all__ = ["__version__", "get_identity"]
__version__ = "0.3.0-api-p3"
