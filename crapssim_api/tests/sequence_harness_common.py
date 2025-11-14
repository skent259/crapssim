"""Common utilities for sequence harness tests."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, TypedDict

from .sequence_scenarios import NormalizedBet, SEQUENCE_SCENARIOS


RESULTS_DIR = Path(__file__).parent / "results"
API_JSON_PATH = RESULTS_DIR / "api_sequences_journal.json"
API_REPORT_PATH = RESULTS_DIR / "API_SEQUENCE_STRESS_API.md"
VANILLA_JSON_PATH = RESULTS_DIR / "vanilla_sequences_journal.json"
VANILLA_REPORT_PATH = RESULTS_DIR / "API_SEQUENCE_STRESS_VANILLA.md"
PARITY_REPORT_PATH = RESULTS_DIR / "API_SEQUENCE_STRESS_PARITY.md"


class ActionResult(TypedDict):
    verb: str
    args: Dict[str, Any]
    result: str
    error_code: str | None


class StepResult(TypedDict):
    step_label: str
    dice: List[int] | None
    before_bankroll: float
    after_bankroll: float
    bets_before: List[NormalizedBet]
    bets_after: List[NormalizedBet]
    actions: List[ActionResult]
    errors: List[str]


class FinalState(TypedDict):
    bankroll: float
    bets: List[NormalizedBet]
    result: str
    error_code: str | None


class SequenceJournalEntry(TypedDict):
    scenario: str
    seed: int
    step_results: List[StepResult]
    final_state: FinalState


@dataclass(frozen=True)
class SequenceRunConfig:
    seed_base: int = 42000


def ensure_results_dir() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def normalize_bets(bets: Iterable[dict[str, Any]]) -> List[NormalizedBet]:
    normalized: List[NormalizedBet] = []
    for bet in bets:
        normalized.append(
            {
                "type": str(bet.get("type")),
                "number": bet.get("number"),
                "amount": float(bet.get("amount", 0.0)),
            }
        )
    normalized.sort(
        key=lambda item: (
            item["type"],
            item["number"] if item["number"] is not None else -1,
            item["amount"],
        )
    )
    return normalized


def write_json(path: Path, data: Any) -> None:
    ensure_results_dir()
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _summary_counts(journal: Sequence[SequenceJournalEntry]) -> tuple[int, int, int]:
    total = len(journal)
    ok_count = sum(1 for entry in journal if entry["final_state"]["result"] == "ok")
    error_count = total - ok_count
    return total, ok_count, error_count


def _render_step_table(entry: SequenceJournalEntry) -> List[str]:
    lines = ["| Step | Dice | Before | After | Result | Errors |", "| --- | --- | --- | --- | --- | --- |"]
    for step in entry["step_results"]:
        dice = step["dice"]
        dice_display = "-" if dice is None else f"{dice[0]}+{dice[1]}"
        action_desc = "; ".join(
            f"{action['verb']}:{action['result']}" for action in step["actions"]
        )
        error_desc = ", ".join(step["errors"]) if step["errors"] else ""
        lines.append(
            "| {label} | {dice} | {before:.2f} | {after:.2f} | {actions} | {errors} |".format(
                label=step["step_label"],
                dice=dice_display,
                before=step["before_bankroll"],
                after=step["after_bankroll"],
                actions=action_desc or "",
                errors=error_desc,
            )
        )
    lines.append("")
    return lines


def write_sequence_report(path: Path, journal: Sequence[SequenceJournalEntry], *, title: str) -> None:
    ensure_results_dir()
    total, ok_count, error_count = _summary_counts(journal)
    scenario_lookup = {scenario["label"]: scenario for scenario in SEQUENCE_SCENARIOS}

    lines: List[str] = [f"# {title}", ""]
    lines.append("## Summary")
    lines.append("")
    lines.append(f"* Total sequences: **{total}**")
    lines.append(f"* Final OK states: **{ok_count}**")
    lines.append(f"* Final errors: **{error_count}**")
    lines.append("")

    lines.append("## Sequence Results")
    lines.append("")
    lines.append("| Scenario | Final Result | Final Error | Expected |")
    lines.append("| --- | --- | --- | --- |")
    for entry in journal:
        expect = scenario_lookup.get(entry["scenario"], {}).get("expect", {})
        expected_desc = expect.get("expected_result")
        expected_code = expect.get("error_code")
        if expected_code:
            expected_desc = f"{expected_desc} ({expected_code})"
        lines.append(
            "| {scenario} | {result} | {error} | {expected} |".format(
                scenario=entry["scenario"],
                result=entry["final_state"]["result"],
                error=entry["final_state"].get("error_code") or "",
                expected=expected_desc or "",
            )
        )
    lines.append("")

    lines.append("## Sequence Journals")
    lines.append("")
    for entry in journal:
        lines.append(f"### {entry['scenario']}")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(entry, indent=2, sort_keys=True))
        lines.append("```")
        lines.append("")
        lines.extend(_render_step_table(entry))

    path.write_text("\n".join(lines), encoding="utf-8")


def compare_journals(
    api_journal: Sequence[SequenceJournalEntry],
    vanilla_journal: Sequence[SequenceJournalEntry],
    *,
    epsilon: float = 1e-6,
) -> tuple[bool, List[str]]:
    mismatches: List[str] = []
    vanilla_lookup = {entry["scenario"]: entry for entry in vanilla_journal}

    for api_entry in api_journal:
        label = api_entry["scenario"]
        vanilla_entry = vanilla_lookup.get(label)
        if vanilla_entry is None:
            mismatches.append(f"Scenario {label} missing in vanilla journal")
            continue

        api_final = api_entry["final_state"]
        vanilla_final = vanilla_entry["final_state"]

        if api_final["result"] != vanilla_final["result"]:
            mismatches.append(f"{label}: final result mismatch ({api_final['result']} vs {vanilla_final['result']})")

        if api_final.get("error_code") != vanilla_final.get("error_code"):
            mismatches.append(
                f"{label}: final error code mismatch ({api_final.get('error_code')} vs {vanilla_final.get('error_code')})"
            )

        if abs(api_final["bankroll"] - vanilla_final["bankroll"]) > epsilon:
            mismatches.append(
                f"{label}: bankroll mismatch ({api_final['bankroll']:.2f} vs {vanilla_final['bankroll']:.2f})"
            )

        if api_final["bets"] != vanilla_final["bets"]:
            mismatches.append(f"{label}: final bets mismatch")

        # Optional per-step comparisons for debugging
        vanilla_steps = vanilla_entry["step_results"]
        api_steps = api_entry["step_results"]
        if len(api_steps) != len(vanilla_steps):
            mismatches.append(f"{label}: step count mismatch")
            continue
        for idx, (api_step, vanilla_step) in enumerate(zip(api_steps, vanilla_steps)):
            step_label = api_step["step_label"]
            if api_step["step_label"] != vanilla_step["step_label"]:
                mismatches.append(
                    f"{label} step {idx}: label mismatch ({api_step['step_label']} vs {vanilla_step['step_label']})"
                )
            if abs(api_step["before_bankroll"] - vanilla_step["before_bankroll"]) > epsilon:
                mismatches.append(
                    f"{label} step {step_label}: before bankroll mismatch ({api_step['before_bankroll']:.2f} vs {vanilla_step['before_bankroll']:.2f})"
                )
            if abs(api_step["after_bankroll"] - vanilla_step["after_bankroll"]) > epsilon:
                mismatches.append(
                    f"{label} step {step_label}: after bankroll mismatch ({api_step['after_bankroll']:.2f} vs {vanilla_step['after_bankroll']:.2f})"
                )
            if api_step["bets_after"] != vanilla_step["bets_after"]:
                mismatches.append(f"{label} step {step_label}: bets after mismatch")
            if len(api_step["actions"]) != len(vanilla_step["actions"]):
                mismatches.append(f"{label} step {step_label}: action count mismatch")
            else:
                for action_idx, (api_action, vanilla_action) in enumerate(
                    zip(api_step["actions"], vanilla_step["actions"])
                ):
                    if api_action["verb"] != vanilla_action["verb"]:
                        mismatches.append(
                            f"{label} step {step_label} action {action_idx}: verb mismatch"
                        )
                    if api_action["result"] != vanilla_action["result"]:
                        mismatches.append(
                            f"{label} step {step_label} action {action_idx}: result mismatch ({api_action['result']} vs {vanilla_action['result']})"
                        )
                    if api_action.get("error_code") != vanilla_action.get("error_code"):
                        mismatches.append(
                            f"{label} step {step_label} action {action_idx}: error code mismatch ({api_action.get('error_code')} vs {vanilla_action.get('error_code')})"
                        )

    ok = not mismatches
    return ok, mismatches


def write_parity_report(
    api_journal: Sequence[SequenceJournalEntry],
    vanilla_journal: Sequence[SequenceJournalEntry],
    mismatches: Sequence[str],
) -> None:
    ensure_results_dir()
    total = len(api_journal)
    vanilla_total = len(vanilla_journal)

    lines: List[str] = ["# CrapsSim API vs Vanilla Sequence Parity", ""]
    lines.append(f"* API sequences: **{total}**")
    lines.append(f"* Vanilla sequences: **{vanilla_total}**")
    lines.append(f"* Mismatches: **{len(mismatches)}**")
    lines.append("")

    if mismatches:
        lines.append("## Mismatches")
        lines.append("")
        for item in mismatches:
            lines.append(f"- {item}")
        lines.append("")
    else:
        lines.append("All scenarios matched between API and vanilla runs.")
        lines.append("")

    lines.append("## Final State Comparison")
    lines.append("")
    vanilla_lookup = {entry["scenario"]: entry for entry in vanilla_journal}
    for api_entry in api_journal:
        label = api_entry["scenario"]
        vanilla_entry = vanilla_lookup.get(label)
        lines.append(f"### {label}")
        lines.append("")
        if vanilla_entry is None:
            lines.append("Vanilla result missing.")
            lines.append("")
            continue
        lines.append("| Field | API | Vanilla |")
        lines.append("| --- | --- | --- |")
        api_final = api_entry["final_state"]
        vanilla_final = vanilla_entry["final_state"]
        lines.append(
            "| Result | {api_result} | {vanilla_result} |".format(
                api_result=api_final["result"], vanilla_result=vanilla_final["result"]
            )
        )
        lines.append(
            "| Error Code | {api_error} | {vanilla_error} |".format(
                api_error=api_final.get("error_code") or "",
                vanilla_error=vanilla_final.get("error_code") or "",
            )
        )
        lines.append(
            "| Bankroll | {api_bankroll:.2f} | {vanilla_bankroll:.2f} |".format(
                api_bankroll=api_final["bankroll"],
                vanilla_bankroll=vanilla_final["bankroll"],
            )
        )
        lines.append(
            "| Bets | `{api_bets}` | `{vanilla_bets}` |".format(
                api_bets=api_final["bets"],
                vanilla_bets=vanilla_final["bets"],
            )
        )
        lines.append("")

    PARITY_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
