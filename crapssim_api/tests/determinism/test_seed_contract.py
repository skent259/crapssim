import pytest


@pytest.mark.skip(
    reason="Determinism contract tests will be implemented in Phase 4-B/4-C."
)
def test_seed_based_determinism_contract_documented():
    """
    Placeholder for seed-based determinism tests.

    This test module will eventually:
    - Start a session with a fixed seed via the Engine API.
    - Run a small, fixed number of rolls.
    - Capture the resulting bankroll and layout.
    - Assert stability of those results across repeated runs and Python versions.

    The actual behavior and expectations are documented in `crapssim_api/docs/DETERMINISM.md`.
    """
    assert True
