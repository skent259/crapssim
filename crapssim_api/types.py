from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from typing_extensions import TypedDict


class VigRule(TypedDict, total=False):
    rate_bips: int
    rounding: Literal["none", "ceil_dollar", "nearest_dollar"]
    floor: float
    paid_on_win: bool


class Capabilities(TypedDict):
    schema_version: int
    bets: Dict[str, Union[List[str], Dict[str, Union[str, Dict[str, str]]]]]
    increments: Dict[str, Dict[str, int]]
    odds_limits: Dict[str, Union[str, int]]
    vig: Dict[str, VigRule]
    working_flags: Dict[str, bool]
    why_unsupported: Dict[str, str]
    verbs: Dict[str, Dict[str, Any]]
    bet_management: List[str]


class TableSpec(TypedDict, total=False):
    table_profile: str
    field_pays: Dict[str, str]
    odds_policy: str
    odds_limit_max_x: int
    increments: Dict[str, Dict[str, int]]
    vig: Dict[str, VigRule]
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


class ApplyActionRequest(TypedDict, total=False):
    verb: str
    args: Dict[str, Any]
    session_id: Optional[str]


class EffectSummary(TypedDict, total=False):
    verb: str
    args: Dict[str, Any]
    applied: bool
    bankroll_delta: float
    note: str


class ApplyActionResponse(TypedDict, total=False):
    effect_summary: EffectSummary
    snapshot: Dict[str, Any]


class RollSnapshot(TypedDict, total=False):
    session_id: str
    hand_id: int
    roll_seq: int
    dice: List[int]
    puck: str
    point: Optional[int]
    bankroll_after: str
    events: List[Dict[str, Any]]
    identity: Dict[str, Any]
    bets: List[Dict[str, Any]]
    is_push: bool


class SessionTapeStep(TypedDict):
    """
    One deterministic step in a recorded session.

    - step_index: monotonically increasing, 0-based.
    - dice: the rolled dice for this step (d1, d2).
    - actions: list of action payloads sent between the previous roll and this roll.
      These should be exactly the JSON payloads the API received.
    """

    step_index: int
    dice: Tuple[int, int]
    actions: List[dict]


class SessionTapeMetadata(TypedDict, total=False):
    """
    Minimal metadata needed to reconstitute a session deterministically.

    - engine_version: version string of CrapsSim engine that produced this tape.
    - api_version: version string of the Engine API that produced this tape.
    - seed: RNG seed used to start the session (if any).
    - table_spec: Table spec that was passed to the engine.
    - initial_bankroll: bankroll at session start.
    """

    engine_version: str
    api_version: str
    seed: Optional[int]
    table_spec: dict
    initial_bankroll: float


class SessionTape(TypedDict):
    """
    Deterministic replay tape for a single session.

    - session_id: ID of the original session, for reference only.
    - metadata: session configuration and versions.
    - steps: ordered list of dice + action bundles.
    - final_state: optional summary of the final engine state as seen by the API.
    """

    session_id: str
    metadata: SessionTapeMetadata
    steps: List[SessionTapeStep]
    final_state: dict


class ReplayResult(TypedDict):
    """
    Result of replaying a SessionTape.

    - deterministic: True if the replayed session produced the same final_state.
    - mismatch_step: first step index where a mismatch was detected, or None.
    - original_final_state: final_state as recorded on the tape.
    - replay_final_state: final_state returned by the replay run.
    """

    deterministic: bool
    mismatch_step: Optional[int]
    original_final_state: dict
    replay_final_state: dict


class BetState(TypedDict, total=False):
    type: str
    number: int | None
    amount: float
    working: bool | None
    odds_amount: float | None


class LastRollState(TypedDict, total=False):
    total: int | None
    dice: list[int] | None
    resolved: bool | None


class SessionStateResponse(TypedDict, total=False):
    state_schema: str
    session_id: str
    seed: int | None
    determinism_contract: str | None
    tape_loaded: bool

    bankroll: float
    point: int | None
    roll_index: int | None
    hand_index: int | None

    last_roll: LastRollState | None
    bets: list[BetState]

    ats: dict[str, Any] | None
    fire: dict[str, Any] | None
    table: dict[str, Any] | None


class BankrollMetrics(TypedDict, total=False):
    start: float
    current: float
    net: float
    roi: float | None


class RollMetrics(TypedDict, total=False):
    total: int | None
    comeout: int | None
    point_resolutions: int | None


class HandMetrics(TypedDict, total=False):
    total: int | None
    completed: int | None


class OutcomeMetrics(TypedDict, total=False):
    wins: int | None
    losses: int | None
    pushes: int | None


class PointMetrics(TypedDict, total=False):
    made: int | None
    seven_outs: int | None
    pso_count: int | None


class BetTypeMetrics(TypedDict, total=False):
    type: str
    wins: int | None
    losses: int | None
    pushes: int | None
    net: float | None


class SessionMetricsResponse(TypedDict, total=False):
    metrics_schema: str
    session_id: str

    bankroll: BankrollMetrics
    rolls: RollMetrics
    hands: HandMetrics
    outcomes: OutcomeMetrics
    points: PointMetrics
    by_bet_type: list[BetTypeMetrics]

    determinism_contract: str | None
