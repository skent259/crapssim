from __future__ import annotations

from typing import Callable, Dict, List, Any


class EventBus:
    """
    Minimal synchronous event bus.
    - on(event, cb): register a callback
    - emit(event, **kwargs): call all callbacks for that event
    No threading, no async. Purely in-process.
    """
    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable[..., None]]] = {}

    def on(self, event: str, callback: Callable[..., None]) -> None:
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event: str, **kwargs: Any) -> None:
        for cb in self._listeners.get(event, []):
            cb(**kwargs)


__all__ = ["EventBus"]
