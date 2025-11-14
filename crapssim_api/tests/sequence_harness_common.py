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
    lines = [
        "| Step | Dice | Before | After | Result | Errors |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
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


def _render_step_overview(entry: SequenceJournalEntry) -> List[str]:
    lines: List[str] = ["#### Step Overview", ""]
    if not entry["step_results"]:
        lines.append("(no steps recorded)")
        lines.append("")
        return lines

    for step in entry["step_results"]:
        fragments: List[str] = []
        dice = step["dice"]
        if dice is not None:
            fragments.append(f"dice {dice[0]}+{dice[1]}")
        if step["actions"]:
            action_bits = []
            for action in step["actions"]:
                verb = action["verb"]
                result = action["result"]
                error_code = action.get("error_code")
                if error_code:
                    action_bits.append(f"{verb} ({result}, {error_code})")
                else:
                    action_bits.append(f"{verb} ({result})")
            fragments.append("actions: " + ", ".join(action_bits))
        if step["errors"]:
            fragments.append("errors: " + ", ".join(step["errors"]))
        if not fragments:
            fragments.append("no actions")
        lines.append(f"- **{step['step_label']}**: " + "; ".join(fragments))
    lines.append("")
    return lines


def write_sequence_report(path: Path, journal: Sequence[SequenceJournalEntry], *, title: str) -> None:
    ensure_results_dir()
    total, ok_count, error_count = _summary_counts(journal)
    scenario_lookup = {scenario["label"]: scenario for scenario in SEQUENCE_SCENARIOS}

    lines: List[str] = [f"# {title}", ""]
    lines.extend(["## Summary", ""])
    lines.append(f"* Total sequences: **{total}**")
    lines.append(f"* Final OK states: **{ok_count}**")
    lines.append(f"* Final errors: **{error_count}**")
    lines.append("")

    lines.extend(["## Sequence Results", ""])
    lines.append("| Scenario | Final Result | Error Code | Expected Result | Expected Error |")
    lines.append("| --- | --- | --- | --- | --- |")
    for entry in journal:
        expect = scenario_lookup.get(entry["scenario"], {}).get("expect", {})
        expected_desc = expect.get("expected_result")
        expected_code = expect.get("error_code")
        lines.append(
            "| {scenario} | {result} | {error} | {expected_result} | {expected_error} |".format(
                scenario=entry["scenario"],
                result=entry["final_state"]["result"],
                error=entry["final_state"].get("error_code") or "",
                expected_result=expected_desc or "",
                expected_error=expected_code or "",
            )
        )
    lines.append("")

    lines.extend(["## Sequence Journals", ""])
    for entry in journal:
        lines.append(f"### {entry['scenario']}")
        lines.append("")
        lines.extend(_render_step_overview(entry))
        lines.append("```json")
        lines.append(json.dumps(entry, indent=2, sort_keys=True))
        lines.append("```")
        lines.append("")
        lines.extend(_render_step_table(entry))

    path.write_text("\n".join(lines), encoding="utf-8")


def build_parity_rows(
    api_journal: Sequence[SequenceJournalEntry],
    vanilla_journal: Sequence[SequenceJournalEntry],
    *,
    epsilon: float = 1e-6,
) -> Dict[str, List[Dict[str, Any]]]:
    vanilla_lookup = {entry["scenario"]: entry for entry in vanilla_journal}
    rows: Dict[str, List[Dict[str, Any]]] = {}

    for api_entry in api_journal:
        label = api_entry["scenario"]
        scenario_rows: List[Dict[str, Any]] = []
        vanilla_entry = vanilla_lookup.get(label)
        if vanilla_entry is None:
            scenario_rows.append(
                {
                    "field": "scenario",
                    "api": "present",
                    "vanilla": "missing",
                    "status": "❌",
                }
            )
            rows[label] = scenario_rows
            continue

        api_final = api_entry["final_state"]
        vanilla_final = vanilla_entry["final_state"]

        scenario_rows.append(
            {
                "field": "final_result",
                "api": api_final["result"],
                "vanilla": vanilla_final["result"],
                "status": "✅" if api_final["result"] == vanilla_final["result"] else "❌",
            }
        )
        scenario_rows.append(
            {
                "field": "error_code",
                "api": api_final.get("error_code") or "",
                "vanilla": vanilla_final.get("error_code") or "",
                "status": "✅"
                if (api_final.get("error_code") or "") == (vanilla_final.get("error_code") or "")
                else "❌",
            }
        )

        bankroll_match = abs(api_final["bankroll"] - vanilla_final["bankroll"]) <= epsilon
        scenario_rows.append(
            {
                "field": "final_bankroll",
                "api": f"{api_final['bankroll']:.2f}",
                "vanilla": f"{vanilla_final['bankroll']:.2f}",
                "status": "✅" if bankroll_match else "❌",
            }
        )

        api_bets = json.dumps(api_final["bets"], sort_keys=True)
        vanilla_bets = json.dumps(vanilla_final["bets"], sort_keys=True)
        scenario_rows.append(
            {
                "field": "final_bets",
                "api": api_bets,
                "vanilla": vanilla_bets,
                "status": "✅" if api_bets == vanilla_bets else "❌",
            }
        )

        rows[label] = scenario_rows

    for vanilla_entry in vanilla_journal:
        label = vanilla_entry["scenario"]
        if label not in rows:
            rows[label] = [
                {
                    "field": "scenario",
                    "api": "missing",
                    "vanilla": "present",
                    "status": "❌",
                }
            ]

    return rows


def _extract_mismatch_label(message: str) -> str:
    if message.startswith("Scenario "):
        return message.split(" ", 2)[1]
    prefix = message.split(":", 1)[0]
    if " step" in prefix:
        return prefix.split(" step", 1)[0]
    return prefix


def compare_journals(
    api_journal: Sequence[SequenceJournalEntry],
    vanilla_journal: Sequence[SequenceJournalEntry],
    *,
    epsilon: float = 1e-6,
) -> tuple[bool, List[str]]:
    mismatches: List[str] = []
    vanilla_lookup = {entry["scenario"]: entry for entry in vanilla_journal}

    parity_rows = build_parity_rows(api_journal, vanilla_journal, epsilon=epsilon)
    for label, scenario_rows in parity_rows.items():
        for row in scenario_rows:
            if row["status"] == "❌":
                mismatches.append(
                    f"{label}: {row['field']} mismatch ({row['api']} vs {row['vanilla']})"
                )

    for api_entry in api_journal:
        label = api_entry["scenario"]
        vanilla_entry = vanilla_lookup.get(label)
        if vanilla_entry is None:
            continue

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

    lines: List[str] = ["# CrapsSim API Sequence Parity", ""]
    lines.extend(["## Summary", ""])
    lines.append(f"* API sequences: **{total}**")
    lines.append(f"* Vanilla sequences: **{vanilla_total}**")
    lines.append(f"* Mismatches: **{len(mismatches)}**")
    lines.append("")

    parity_rows = build_parity_rows(api_journal, vanilla_journal)

    lines.extend(["## Field Comparisons", ""])
    lines.append("| Scenario | Field | API | Vanilla | Status |")
    lines.append("| --- | --- | --- | --- | --- |")
    for label in sorted(parity_rows):
        for row in parity_rows[label]:
            lines.append(
                "| {scenario} | {field} | {api} | {vanilla} | {status} |".format(
                    scenario=label,
                    field=row["field"],
                    api=row["api"],
                    vanilla=row["vanilla"],
                    status=row["status"],
                )
            )
    lines.append("")

    mismatch_labels = {label for label, rows in parity_rows.items() if any(row["status"] == "❌" for row in rows)}
    mismatch_labels.update(_extract_mismatch_label(msg) for msg in mismatches)
    mismatch_labels = {label for label in mismatch_labels if label}

    if mismatch_labels:
        lines.extend(["## Mismatch Details", ""])
        api_lookup = {entry["scenario"]: entry for entry in api_journal}
        vanilla_lookup = {entry["scenario"]: entry for entry in vanilla_journal}
        for label in sorted(mismatch_labels):
            lines.append(f"### {label}")
            lines.append("")
            scenario_messages = [msg for msg in mismatches if _extract_mismatch_label(msg) == label]
            if scenario_messages:
                lines.append("**Issues**")
                lines.append("")
                for msg in scenario_messages:
                    lines.append(f"- {msg}")
                lines.append("")

            api_entry = api_lookup.get(label)
            vanilla_entry = vanilla_lookup.get(label)
            if api_entry is not None:
                lines.append("**API Final State**")
                lines.append("")
                lines.append("```json")
                lines.append(json.dumps(api_entry["final_state"], indent=2, sort_keys=True))
                lines.append("```")
                lines.append("")
            if vanilla_entry is not None:
                lines.append("**Vanilla Final State**")
                lines.append("")
                lines.append("```json")
                lines.append(json.dumps(vanilla_entry["final_state"], indent=2, sort_keys=True))
                lines.append("```")
                lines.append("")
            else:
                lines.append("Vanilla result missing.")
                lines.append("")

    if not mismatch_labels:
        lines.append("All scenarios matched across API and vanilla harnesses.")

    PARITY_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
