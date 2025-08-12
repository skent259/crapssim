
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class StrategyStats:
    id: str
    generation: int
    rolls_survived: int
    profit: float
    bankroll_curve: List[float]
    variance_score: float
    ef: float
    table_cq: int
    danger_zone: bool
    hall_flags: Dict[str, bool]
