from __future__ import annotations

from typing import Any, Callable, Dict


def stub_handler(args: Dict[str, Any]) -> Dict[str, Any]:
    # No side effects: deterministic, verb-agnostic no-op
    return {
        "applied": True,
        "bankroll_delta": 0.0,
        "note": "stub: action accepted, no-op",
    }


VerbRegistry: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "pass_line": stub_handler,
    "dont_pass": stub_handler,
    "come": stub_handler,
    "dont_come": stub_handler,
    "place": stub_handler,
    "buy": stub_handler,
    "lay": stub_handler,
    "put": stub_handler,
    "hardway": stub_handler,
    "field": stub_handler,
    "horn": stub_handler,
    "world": stub_handler,
}
