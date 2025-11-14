from __future__ import annotations

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from .sequence_harness_common import (
    PARITY_REPORT_PATH,
    compare_journals,
    write_parity_report,
)


def test_sequence_parity(
    api_sequence_json,  # noqa: ANN001 - provided by fixture
    vanilla_sequence_json,  # noqa: ANN001 - provided by fixture
) -> None:
    ok, mismatches = compare_journals(api_sequence_json, vanilla_sequence_json)
    write_parity_report(api_sequence_json, vanilla_sequence_json, mismatches)
    assert ok, "; ".join(mismatches)
    assert PARITY_REPORT_PATH.exists()
