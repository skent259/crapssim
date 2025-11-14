from __future__ import annotations

from pathlib import Path

import pytest

from crapssim_api.tools import api_surface_parity, api_surface_stress, vanilla_surface_stress
from crapssim_api.tools.api_surface_scenarios import SCENARIOS

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")


def test_surface_harnesses_smoke(tmp_path: Path) -> None:
    assert len(SCENARIOS) >= 3

    api_json = tmp_path / "api.json"
    api_md = tmp_path / "api.md"
    vanilla_json = tmp_path / "vanilla.json"
    vanilla_md = tmp_path / "vanilla.md"
    parity_md = tmp_path / "parity.md"

    api_journal = api_surface_stress.run(limit=3, json_path=api_json, markdown_path=api_md)
    assert len(api_journal) == 3
    assert api_json.exists()
    assert api_md.exists()

    vanilla_journal = vanilla_surface_stress.run(limit=3, json_path=vanilla_json, markdown_path=vanilla_md)
    assert len(vanilla_journal) == 3
    assert vanilla_json.exists()
    assert vanilla_md.exists()

    parity_result = api_surface_parity.compare(
        api_path=api_json, vanilla_path=vanilla_json, markdown_path=parity_md
    )
    assert parity_md.exists()
    assert not parity_result.mismatches
    assert len(parity_result.matches) == 3
    assert len(parity_result.missing_api) == len(SCENARIOS) - 3
