"""Compare API and vanilla engine journals for parity."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List

from .api_surface_scenarios import SCENARIOS

API_JSON = Path("build/api_surface_api.json")
VANILLA_JSON = Path("build/api_surface_vanilla.json")
PARITY_MARKDOWN = Path("crapssim_api/docs/dev/API_SURFACE_STRESS_PARITY.md")


@dataclass
class Mismatch:
    scenario: str
    field: str
    api_value: Any
    vanilla_value: Any


class ParityResult:
    def __init__(self, matches: List[str], mismatches: List[Mismatch], missing_api: List[str], missing_vanilla: List[str]):
        self.matches = matches
        self.mismatches = mismatches
        self.missing_api = missing_api
        self.missing_vanilla = missing_vanilla

    @property
    def has_mismatch(self) -> bool:
        return bool(self.mismatches or self.missing_api or self.missing_vanilla)


def _ensure_output_dirs(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"journal not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _compare_entries(api_entry: dict, vanilla_entry: dict) -> list[Mismatch]:
    mismatches: list[Mismatch] = []
    if api_entry.get("result") != vanilla_entry.get("result"):
        mismatches.append(Mismatch(api_entry["scenario"], "result", api_entry.get("result"), vanilla_entry.get("result")))

    if (api_entry.get("error_code") or "") != (vanilla_entry.get("error_code") or ""):
        mismatches.append(
            Mismatch(
                api_entry["scenario"],
                "error_code",
                api_entry.get("error_code"),
                vanilla_entry.get("error_code"),
            )
        )

    api_after = float(api_entry.get("after_bankroll", 0.0))
    vanilla_after = float(vanilla_entry.get("after_bankroll", 0.0))
    if abs(api_after - vanilla_after) > 1e-6:
        mismatches.append(
            Mismatch(
                api_entry["scenario"],
                "after_bankroll",
                api_after,
                vanilla_after,
            )
        )

    if api_entry.get("bets_after") != vanilla_entry.get("bets_after"):
        mismatches.append(
            Mismatch(
                api_entry["scenario"],
                "bets_after",
                api_entry.get("bets_after"),
                vanilla_entry.get("bets_after"),
            )
        )
    return mismatches


def _index_journal(journal: Iterable[dict]) -> dict[str, dict]:
    return {entry["scenario"]: entry for entry in journal}


def _render_markdown(
    path: Path,
    api_journal: list[dict],
    vanilla_journal: list[dict],
    parity: ParityResult,
) -> None:
    _ensure_output_dirs(path)
    scenario_count = len(SCENARIOS)
    lines = ["# API vs Engine Parity Report", ""]
    lines.append("## Summary")
    lines.append("")
    lines.append(f"* Scenarios defined: **{scenario_count}**")
    lines.append(f"* Matches: **{len(parity.matches)}**")
    lines.append(f"* Mismatches: **{len(parity.mismatches)}**")
    lines.append(f"* Missing in API journal: **{len(parity.missing_api)}**")
    lines.append(f"* Missing in engine journal: **{len(parity.missing_vanilla)}**")
    lines.append("")

    lines.append("## Mismatch Overview")
    lines.append("")
    if parity.mismatches:
        lines.append("| Scenario | Field | API | Engine |")
        lines.append("| --- | --- | --- | --- |")
        for mismatch in parity.mismatches:
            lines.append(
                "| {scenario} | {field} | {api} | {engine} |".format(
                    scenario=mismatch.scenario,
                    field=mismatch.field,
                    api=json.dumps(mismatch.api_value, sort_keys=True) if isinstance(mismatch.api_value, (dict, list)) else mismatch.api_value,
                    engine=json.dumps(mismatch.vanilla_value, sort_keys=True) if isinstance(mismatch.vanilla_value, (dict, list)) else mismatch.vanilla_value,
                )
            )
    else:
        lines.append("All compared fields match.")
    lines.append("")

    if parity.missing_api:
        lines.append("## Scenarios Missing From API Journal")
        lines.append("")
        for label in parity.missing_api:
            lines.append(f"- {label}")
        lines.append("")

    if parity.missing_vanilla:
        lines.append("## Scenarios Missing From Engine Journal")
        lines.append("")
        for label in parity.missing_vanilla:
            lines.append(f"- {label}")
        lines.append("")

    if parity.mismatches:
        lines.append("## Detailed Diffs")
        lines.append("")
        api_index = _index_journal(api_journal)
        vanilla_index = _index_journal(vanilla_journal)
        seen = set()
        for mismatch in parity.mismatches:
            if mismatch.scenario in seen:
                continue
            seen.add(mismatch.scenario)
            lines.append(f"### {mismatch.scenario}")
            lines.append("")
            lines.append("#### API Entry")
            lines.append("```json")
            lines.append(json.dumps(api_index.get(mismatch.scenario, {}), indent=2, sort_keys=True))
            lines.append("```")
            lines.append("")
            lines.append("#### Engine Entry")
            lines.append("```json")
            lines.append(json.dumps(vanilla_index.get(mismatch.scenario, {}), indent=2, sort_keys=True))
            lines.append("```")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def compare(
    api_path: Path = API_JSON,
    vanilla_path: Path = VANILLA_JSON,
    markdown_path: Path = PARITY_MARKDOWN,
) -> ParityResult:
    api_journal = _load_json(api_path)
    vanilla_journal = _load_json(vanilla_path)

    api_index = _index_journal(api_journal)
    vanilla_index = _index_journal(vanilla_journal)

    matches: list[str] = []
    mismatches: list[Mismatch] = []
    missing_api: list[str] = []
    missing_vanilla: list[str] = []

    for scenario in SCENARIOS:
        label = scenario["label"]
        api_entry = api_index.get(label)
        vanilla_entry = vanilla_index.get(label)
        if api_entry is None:
            missing_api.append(label)
            continue
        if vanilla_entry is None:
            missing_vanilla.append(label)
            continue
        diffs = _compare_entries(api_entry, vanilla_entry)
        if diffs:
            mismatches.extend(diffs)
        else:
            matches.append(label)

    parity = ParityResult(matches, mismatches, missing_api, missing_vanilla)
    _render_markdown(markdown_path, api_journal, vanilla_journal, parity)
    return parity


def main() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Compare API and vanilla engine journals for parity")
    parser.add_argument("--api", type=Path, default=API_JSON, help="Path to the API JSON journal")
    parser.add_argument("--vanilla", type=Path, default=VANILLA_JSON, help="Path to the vanilla JSON journal")
    parser.add_argument(
        "--markdown", type=Path, default=PARITY_MARKDOWN, help="Path to write the markdown parity report"
    )
    args = parser.parse_args()

    parity = compare(api_path=args.api, vanilla_path=args.vanilla, markdown_path=args.markdown)
    if parity.has_mismatch:
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
