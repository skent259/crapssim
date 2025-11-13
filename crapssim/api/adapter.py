from __future__ import annotations

import time
from typing import Any, Dict

from crapssim.api.contract import EngineCommand, EngineResult, EngineState
from crapssim.api.router import route


class EngineAdapter:
    """Expose snapshots of a live ``Table`` as :class:`EngineState`."""

    def __init__(self, table) -> None:
        self.table = table
        self._roll_id = 0
        self._hand_id = 0
        self._last_resolved: Dict[str, float] = {}
        setattr(self.table, "adapter", self)

    # ------------------------------------------------------------------
    def snapshot(self) -> EngineState:
        """Build a deterministic snapshot of the current table state."""
        dice_values = (0, 0)
        dice_obj = getattr(self.table, "dice", None)
        if dice_obj is not None:
            result = getattr(dice_obj, "result", None)
            if result:
                dice_values = (int(result[0]), int(result[1]))

        point_obj = getattr(self.table, "point", None)
        point_number = getattr(point_obj, "number", None)

        player = self.table.players[0] if getattr(self.table, "players", []) else None
        bankroll = float(getattr(player, "bankroll", 0.0)) if player else 0.0
        active: Dict[str, float] = {}
        bets = getattr(player, "bets", []) if player else []
        for bet in bets:
            active[self._label(bet)] = float(getattr(bet, "amount", 0.0))

        resolved = dict(self._last_resolved)
        timestamp = time.time()
        return EngineState(
            roll_id=self._roll_id,
            hand_id=self._hand_id,
            dice=dice_values,
            point=point_number,
            bankroll=bankroll,
            active_bets=active,
            resolved=resolved,
            timestamp=timestamp,
        )

    # ------------------------------------------------------------------
    def apply(self, command: EngineCommand) -> EngineResult:
        """Validate and apply a command via the in-process router."""
        return route(self, self.table, command)

    # ------------------------------------------------------------------
    def register_resolution(self, bet_label: str, delta: float) -> None:
        """Record the last resolved delta for ``bet_label``."""
        self._last_resolved[bet_label] = float(delta)

    def increment_roll(self) -> None:
        self._roll_id += 1

    def increment_hand(self) -> None:
        self._hand_id += 1

    @staticmethod
    def _label(bet: Any) -> str:
        """Produce a stable label for a bet instance."""
        name = bet.__class__.__name__
        number = getattr(bet, "number", "")
        return f"{name}{number}"
