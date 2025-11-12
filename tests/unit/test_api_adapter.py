from __future__ import annotations

from crapssim.api.adapter import EngineAdapter
from crapssim.api.events import EventBus
from crapssim.api import hooks
from crapssim.table import Table, TableUpdate


def test_snapshot_basic_fields():
    table = Table()
    table.add_player()
    adapter = EngineAdapter(table)
    snapshot = adapter.snapshot()

    assert snapshot.dice == (0, 0)
    assert snapshot.point is None
    assert isinstance(snapshot.active_bets, dict)


def test_event_bus_emission():
    table = Table()
    table.add_player()
    adapter = EngineAdapter(table)
    bus = EventBus()
    hooks.attach(bus, table, adapter)

    seen: dict[str, float] = {}

    def on_roll_resolved(*, state):
        seen["roll_id"] = state.roll_id
        seen["bankroll"] = state.bankroll
        seen["dice"] = state.dice

    bus.on("roll_resolved", on_roll_resolved)
    TableUpdate().run(table, dice_outcome=(3, 4))

    assert seen["roll_id"] == 1
    assert isinstance(seen["bankroll"], (int, float))
    assert seen["dice"] == (3, 4)


def test_label_stability():
    class DummyBet:
        def __init__(self, number):
            self.number = number
            self.amount = 25

    bet6 = DummyBet(6)
    bet8 = DummyBet(8)
    label6 = EngineAdapter._label(bet6)
    label8 = EngineAdapter._label(bet8)

    assert label6 != label8
    assert "6" in label6
    assert "8" in label8
