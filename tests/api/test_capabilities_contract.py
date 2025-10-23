from crapssim_api.http import get_capabilities, start_session


def test_capabilities_basic():
    data = get_capabilities().body.decode()
    assert "capabilities" in data
    assert "bets" in data


def test_start_session_reflects_disabled_buylay():
    body = {"spec": {"enabled_buylay": False}, "seed": 1}
    res = start_session(body).body.decode()
    assert '"buy": []' in res
    assert "disabled_by_spec" in res
