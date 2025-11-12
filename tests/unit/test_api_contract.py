from __future__ import annotations

import time
from crapssim.api.contract import EngineState, EngineCommand, EngineResult, EngineContract
from crapssim.api.events import EventBus


def test_engine_state_dataclass_constructs():
    now = time.time()
    state = EngineState(
        roll_id=1,
        hand_id=1,
        dice=(3, 4),
        point=4,
        bankroll=1000.0,
        active_bets={"Place6": 30.0},
        resolved={"Place6": 7.0},
        timestamp=now,
    )
    assert state.dice == (3, 4)
    assert state.point == 4
    assert isinstance(state.active_bets, dict)


def test_engine_command_typed_dict_shape():
    cmd: EngineCommand = {"name": "bet", "args": {"type": "Place", "number": 6, "amount": 30}}
    assert cmd["name"] == "bet"
    assert "args" in cmd and isinstance(cmd["args"], dict)


def test_engine_result_dataclass_constructs():
    state = EngineState(
        roll_id=0, hand_id=0, dice=(1, 1), point=None,
        bankroll=0.0, active_bets={}, resolved={}, timestamp=0.0
    )
    res = EngineResult(success=True, reason=None, new_state=state)
    assert res.success is True
    assert res.new_state is state


def test_event_bus_on_emit():
    bus = EventBus()
    seen = {}

    def handler(**kw):
        seen.update(kw)

    bus.on("roll", handler)
    bus.emit("roll", dice=(2, 3), point=None)
    assert seen["dice"] == (2, 3)
    assert "point" in seen


def test_engine_contract_protocol_example():
    """
    Smoke-check that a minimal fake implementation satisfies the protocol.
    This does not import or bind to the real engine in Phase 1.
    """
    class FakeEngine:
        def __init__(self):
            self._s = EngineState(
                roll_id=0, hand_id=0, dice=(1, 1), point=None,
                bankroll=0.0, active_bets={}, resolved={}, timestamp=0.0
            )
        def apply(self, command: EngineCommand) -> EngineResult:
            return EngineResult(True, None, self._s)
        def snapshot(self) -> EngineState:
            return self._s

    def consume(e: EngineContract) -> None:
        snap = e.snapshot()
        assert isinstance(snap, EngineState)

    consume(FakeEngine())
