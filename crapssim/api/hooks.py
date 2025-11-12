from __future__ import annotations

from typing import Tuple
from weakref import WeakKeyDictionary

from crapssim.api.adapter import EngineAdapter
from crapssim.api.events import EventBus
from crapssim.table import TableUpdate

HookPayload = Tuple[EventBus, EngineAdapter]

_HOOKS: WeakKeyDictionary[object, HookPayload] = WeakKeyDictionary()
_PATCHED = False
_ORIG_UPDATE_BETS = TableUpdate.update_bets


def attach(bus: EventBus, table, adapter: EngineAdapter) -> None:
    """Attach lightweight hooks that emit events after each roll."""
    global _PATCHED

    if getattr(table, "_api_hooks_installed", False):
        return

    _HOOKS[table] = (bus, adapter)
    table._api_hooks_installed = True

    if not _PATCHED:
        _patch_update_bets()


def _patch_update_bets() -> None:
    global _PATCHED

    def wrapped_update_bets(table_obj, verbose: bool = False) -> None:
        _ORIG_UPDATE_BETS(table_obj, verbose)
        hook = _HOOKS.get(table_obj)
        if not hook:
            return

        bus, adapter = hook
        adapter.increment_roll()
        try:
            state = adapter.snapshot()
            bus.emit("roll_resolved", state=state)
        except Exception:
            pass

    TableUpdate.update_bets = staticmethod(wrapped_update_bets)
    _PATCHED = True
