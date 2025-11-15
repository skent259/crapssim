from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Tuple

Puck = Literal["ON", "OFF"]


@dataclass
class HandState:
    hand_id: int = 1
    puck: Puck = "OFF"
    point: Optional[int] = None

    def to_snapshot_fields(self):
        return {
            "hand_id": self.hand_id,
            "puck": self.puck,
            "point": self.point,
        }

    def reset_for_new_hand(self) -> None:
        self.hand_id += 1
        self.puck = "OFF"
        self.point = None

    def on_roll(self, dice: Tuple[int, int]) -> List[Dict[str, Any]]:
        """
        Pure state transitions for craps hand rhythm. Returns a list of event dicts:
        {"type": <event_type>, "data": <payload or {}>}
        Does NOT touch bankroll or resolve bets.
        """

        d1, d2 = dice
        total = d1 + d2
        evs: List[Dict[str, Any]] = []

        if self.puck == "OFF":
            # Point numbers start a hand; naturals/craps do not.
            if total in (4, 5, 6, 8, 9, 10):
                self.puck = "ON"
                self.point = total
                evs.append({"type": "point_set", "data": {"point": total}})
            # 7 or 11: nothing to do; hand remains in come-out
            # 2, 3, 12: nothing to do; hand remains in come-out
            return evs

        # Puck is ON
        if total == 7:
            evs.append({"type": "seven_out", "data": {}})
            evs.append({"type": "hand_ended", "data": {"end_reason": "seven_out"}})
            self.reset_for_new_hand()
            return evs

        if self.point is not None and total == self.point:
            evs.append({"type": "point_made", "data": {"point": total}})
            evs.append({"type": "hand_ended", "data": {"end_reason": "point_made"}})
            self.reset_for_new_hand()
            return evs

        # Otherwise: nothing changes this roll; hand stays ON same point.
        return evs
