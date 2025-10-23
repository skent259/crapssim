from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

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
