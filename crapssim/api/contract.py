from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, TypedDict, Dict, Tuple, Optional


@dataclass(frozen=True)
class EngineState:
    """
    Deterministic snapshot of the engine suitable for external consumers.
    All fields are primitive or simple containers for easy serialization.
    """
    roll_id: int                  # monotonically increasing per roll
    hand_id: int                  # increments when a new hand starts
    dice: Tuple[int, int]         # (d1, d2)
    point: Optional[int]          # None if no point
    bankroll: float               # active player's bankroll (if single-player table)
    active_bets: Dict[str, float] # bet label -> amount currently working
    resolved: Dict[str, float]    # bet label -> last resolution delta (+/-)
    timestamp: float              # seconds since epoch (float)


class EngineCommand(TypedDict):
    """
    Generic command envelope. Future phases may define stricter shapes,
    but Phase 1 keeps this simple and typed.
    """
    name: str                   # "roll", "bet", "remove", "clear", etc.
    args: Dict[str, Any]        # e.g., {"type":"Place","number":6,"amount":30}


@dataclass(frozen=True)
class EngineResult:
    """
    Result from applying a command. Phase 1 does not enforce legality
    here—this is just the contract type. Later phases may add codes.
    """
    success: bool
    reason: Optional[str]
    new_state: EngineState


class EngineContract(Protocol):
    """
    Minimal protocol for an engine adapter. Implementations must be
    deterministic given the same command sequence and dice outcomes.
    """
    def apply(self, command: EngineCommand) -> EngineResult: ...
    def snapshot(self) -> EngineState: ...


__all__ = [
    "EngineState",
    "EngineCommand",
    "EngineResult",
    "EngineContract",
]
