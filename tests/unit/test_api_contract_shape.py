from crapssim.api.adapter import EngineAdapter
from crapssim.api.contract import EngineCommand
from crapssim.table import Table


def test_contract_smoke_all_verbs():
    table = Table()
    table.settings["debug.allow_fixed_dice"] = True
    adapter = EngineAdapter(table)

    cmds: list[EngineCommand] = [
        {"verb": "add_bet", "type": "Place", "number": 6, "amount": 30.0},
        {"verb": "press_bet", "type": "Place", "number": 6, "amount": 30.0},
        {"verb": "remove_bet", "type": "Place", "number": 6},
        {"verb": "set_dice", "d1": 3, "d2": 4},
        {"verb": "roll"},
        {"verb": "clear_all"},
        {"verb": "regress_bet", "type": "Place", "number": 6, "amount": 6.0},
    ]

    for command in cmds:
        result = adapter.apply(command)
        assert isinstance(result, dict)
        assert "success" in result
        if result["success"]:
            assert "state" in result
        else:
            assert "error" in result and "code" in result["error"]
