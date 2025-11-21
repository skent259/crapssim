import pytest


@pytest.mark.skip(
    reason="Replay tape contract tests will be implemented in Phase 4-B/4-C."
)
def test_replay_tape_round_trips_consistently():
    """
    Placeholder for replay-tape round-trip tests.

    Expected future behavior:
    - Run a short session via the Engine API using the engine's RNG (seeded).
    - Export a replay tape that contains engine/API version, seed, table config, and rolls.
    - Start a new session that replays the exported tape without additional randomness.
    - Assert that bankroll and layout match the original run exactly.

    These tests will be wired up when the replay tape endpoints are added.
    """
    assert True
