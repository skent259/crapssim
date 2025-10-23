from __future__ import annotations

from typing import Dict, List, Literal, Optional, Union
from typing_extensions import TypedDict


class CommissionRule(TypedDict, total=False):
    mode: Literal["on_win", "up_front"]
    rate_bips: int
    rounding: Literal["nearest_dollar", "floor", "bankers"]


class Capabilities(TypedDict):
    schema_version: int
    bets: Dict[str, Union[List[str], Dict[str, Union[str, Dict[str, str]]]]]
    increments: Dict[str, Dict[str, int]]
    odds_limits: Dict[str, Union[str, int]]
    commission: Dict[str, CommissionRule]
    working_flags: Dict[str, bool]
    why_unsupported: Dict[str, str]


class TableSpec(TypedDict, total=False):
    table_profile: str
    field_pays: Dict[str, str]
    odds_policy: str
    odds_limit_max_x: int
    increments: Dict[str, Dict[str, int]]
    commission: Dict[str, CommissionRule]
    working_flags: Dict[str, bool]
    enabled_props: List[str]
    enabled_buylay: bool
    enabled_put: bool


class StartSessionRequest(TypedDict):
    spec: TableSpec
    seed: int


class StartSessionResponse(TypedDict):
    session_id: str
    snapshot: Dict[str, Union[Dict[str, Union[int, str, bool]], Capabilities]]
