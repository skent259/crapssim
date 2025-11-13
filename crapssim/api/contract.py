from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Literal, NotRequired, Optional, Protocol, Tuple, TypedDict, TYPE_CHECKING

Verb = Literal["add_bet", "remove_bet", "press_bet", "regress_bet", "set_dice", "roll", "clear_all"]


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


class EngineCommand(TypedDict, total=False):
    """Structured command sent to the engine router."""

    # Phase 3 verbs ---------------------------------------------------------
    verb: Verb
    type: NotRequired[str]
    number: NotRequired[int]
    amount: NotRequired[float]
    d1: NotRequired[int]
    d2: NotRequired[int]

    # Phase 1 legacy envelope ----------------------------------------------
    name: NotRequired[str]
    args: NotRequired[Dict[str, Any]]


class EngineError(TypedDict, total=False):
    code: str
    reason: str
    details: NotRequired[Dict[str, Any]]


if TYPE_CHECKING:
    class EngineResult(TypedDict, total=False):
        """Result payload returned by the command router."""

        success: bool
        error: NotRequired[EngineError]
        state: Dict[str, Any]
        reason: NotRequired[Optional[str]]  # legacy alias
        new_state: NotRequired[EngineState]  # legacy alias
else:

    @dataclass
    class EngineResult:
        """Runtime representation retained for Phase 1 compatibility."""

        success: bool
        state: Optional[Dict[str, Any] | EngineState] = None
        error: Optional[EngineError] = None
        reason: Optional[str] = None
        new_state: Optional[EngineState] = None

        def __post_init__(self) -> None:  # pragma: no cover - defensive
            if self.state is None and self.new_state is not None:
                self.state = self.new_state


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
    "EngineError",
    "EngineContract",
]
