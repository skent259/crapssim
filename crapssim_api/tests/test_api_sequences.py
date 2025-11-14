from __future__ import annotations

from typing import Dict

import pytest

from .sequence_harness_common import SequenceJournalEntry
from .sequence_scenarios import SEQUENCE_SCENARIOS


def _scenario_lookup() -> Dict[str, dict]:
    return {scenario["label"]: scenario for scenario in SEQUENCE_SCENARIOS}


@pytest.mark.usefixtures("api_sequence_journal")
def test_api_sequences_expectations(api_sequence_journal: list[SequenceJournalEntry]) -> None:
    lookup = _scenario_lookup()
    assert api_sequence_journal, "sequence journal should not be empty"

    for entry in api_sequence_journal:
        scenario = lookup[entry["scenario"]]
        expect = scenario.get("expect", {})

        final_state = entry["final_state"]
        expected_result = expect.get("expected_result")
        if expected_result is not None:
            assert (
                final_state["result"] == expected_result
            ), f"{entry['scenario']}: expected result {expected_result}, got {final_state['result']}"

        expected_error = expect.get("error_code")
        if expected_error is not None:
            assert (
                final_state.get("error_code") == expected_error
            ), f"{entry['scenario']}: expected error {expected_error}, got {final_state.get('error_code')}"

        expected_bankroll = expect.get("final_bankroll")
        if expected_bankroll is not None:
            assert pytest.approx(expected_bankroll, rel=1e-9, abs=1e-9) == final_state["bankroll"]

        expected_bets = expect.get("bets_after")
        if expected_bets is not None:
            assert (
                final_state["bets"] == expected_bets
            ), f"{entry['scenario']}: expected bets {expected_bets}, got {final_state['bets']}"

        assert len(entry["step_results"]) == len(scenario.get("steps", []))
