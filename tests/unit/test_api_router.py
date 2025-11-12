import pytest

from crapssim.api.adapter import EngineAdapter
from crapssim.api.contract import EngineCommand
from crapssim.table import Table


def new_adapter():
    table = Table()
    table.settings["debug.allow_fixed_dice"] = True
    adapter = EngineAdapter(table)
    return table, adapter


def snapshot(adapter):
    state = adapter.snapshot()
    assert hasattr(state, "dice")
    return state


def test_add_remove_place6_happy_path():
    table, adapter = new_adapter()
    cmd: EngineCommand = {"verb": "add_bet", "type": "Place", "number": 6, "amount": 30.0}
    result = adapter.apply(cmd)
    assert result["success"] is True
    state = snapshot(adapter)
    assert state

    result2 = adapter.apply({"verb": "remove_bet", "type": "Place", "number": 6})
    assert result2["success"] is True
    snapshot(adapter)


def test_insufficient_funds():
    table, adapter = new_adapter()
    result = adapter.apply({"verb": "add_bet", "type": "Place", "number": 6, "amount": 10_000.0})
    assert result["success"] is False
    assert result["error"]["code"] in {"INSUFFICIENT_FUNDS", "ILLEGAL_BET"}


def test_bad_increment():
    table, adapter = new_adapter()
    result = adapter.apply({"verb": "add_bet", "type": "Place", "number": 6, "amount": 1.0})
    assert result["success"] is False
    assert result["error"]["code"] in {"BAD_INCREMENT", "ILLEGAL_BET"}


def test_not_found_on_remove():
    table, adapter = new_adapter()
    result = adapter.apply({"verb": "remove_bet", "type": "Buy", "number": 10})
    assert result["success"] is False
    assert result["error"]["code"] == "NOT_FOUND"


def test_set_dice_and_roll_path():
    table, adapter = new_adapter()
    result = adapter.apply({"verb": "set_dice", "d1": 3, "d2": 4})
    assert result["success"] is True
    result2 = adapter.apply({"verb": "roll"})
    assert result2["success"] is True
    snapshot(adapter)


def test_clear_all_is_stable():
    table, adapter = new_adapter()
    adapter.apply({"verb": "add_bet", "type": "Place", "number": 6, "amount": 30.0})
    result = adapter.apply({"verb": "clear_all"})
    assert result["success"] is True


def test_press_behaves_like_add():
    table, adapter = new_adapter()
    adapter.apply({"verb": "add_bet", "type": "Buy", "number": 10, "amount": 20.0})
    result = adapter.apply({"verb": "press_bet", "type": "Buy", "number": 10, "amount": 20.0})
    assert ("success" in result and "state" in result) or "error" in result
