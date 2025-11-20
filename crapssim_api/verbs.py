"""Verb adapters for the CrapsSim HTTP API.

This module exists to mirror the upstream engine's naming and string
resolution system while keeping the HTTP surface anchored to the
implementation in ``actions.py``. It re-exports the supported verb
helpers so callers expecting a ``verbs`` module (as documented in
Phase 1-A) resolve correctly.
"""

from __future__ import annotations

from .actions import (
    SUPPORTED_VERBS,
    apply_bet_management,
    build_bet,
    compute_required_cash,
    describe_vig,
    is_bet_management_verb,
    is_bet_placement_verb,
)

__all__ = [
    "SUPPORTED_VERBS",
    "apply_bet_management",
    "build_bet",
    "compute_required_cash",
    "describe_vig",
    "is_bet_management_verb",
    "is_bet_placement_verb",
]
