from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pytest

from .sequence_harness_api import run_api_sequence_harness
from .sequence_harness_common import (
    API_JSON_PATH,
    SequenceJournalEntry,
    VANILLA_JSON_PATH,
)
from .sequence_harness_vanilla import run_vanilla_sequence_harness


@pytest.fixture(scope="session")
def api_sequence_journal() -> List[SequenceJournalEntry]:
    return run_api_sequence_harness()


@pytest.fixture(scope="session")
def vanilla_sequence_journal() -> List[SequenceJournalEntry]:
    return run_vanilla_sequence_harness()


@pytest.fixture(scope="session")
def api_sequence_json(api_sequence_journal: List[SequenceJournalEntry]) -> List[SequenceJournalEntry]:
    data = json.loads(Path(API_JSON_PATH).read_text(encoding="utf-8"))
    assert data == api_sequence_journal
    return data


@pytest.fixture(scope="session")
def vanilla_sequence_json(vanilla_sequence_journal: List[SequenceJournalEntry]) -> List[SequenceJournalEntry]:
    data = json.loads(Path(VANILLA_JSON_PATH).read_text(encoding="utf-8"))
    assert data == vanilla_sequence_journal
    return data
