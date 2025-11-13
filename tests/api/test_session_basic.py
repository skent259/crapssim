from crapssim_api.session import Session


def test_session_start_and_snapshot():
    s = Session()
    s.start()
    snap = s.snapshot()
    assert "bankroll" in snap
    assert "bets" in snap


def test_forced_dice_roll():
    s = Session()
    s.start()
    evt = s.step_roll(dice=[3,4])
    assert evt["dice"] == [3,4]


