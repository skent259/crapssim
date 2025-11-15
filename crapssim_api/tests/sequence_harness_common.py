"""Common utilities for sequence harness tests."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, TypedDict

from .sequence_scenarios import NormalizedBet, SEQUENCE_SCENARIOS


RESULTS_DIR = Path(__file__).parent / "results"
API_JSON_PATH = RESULTS_DIR / "api_sequences_journal.json"
API_REPORT_PATH = RESULTS_DIR / "API_SEQUENCE_TRACE_API.md"
VANILLA_JSON_PATH = RESULTS_DIR / "vanilla_sequences_journal.json"
VANILLA_REPORT_PATH = RESULTS_DIR / "API_SEQUENCE_TRACE_VANILLA.md"
PARITY_REPORT_PATH = RESULTS_DIR / "API_SEQUENCE_TRACE_PARITY.md"


class ActionResult(TypedDict):
    """Outcome for an action applied in a sequence step."""

    verb: str
    args: Dict[str, Any]
    result: str
    error_code: str | None


class StepJournalEntry(TypedDict):
    """Roll-by-roll journal entry for a single step."""

    index: int
    label: str
    dice: List[int] | None
    before_bankroll: float
    after_bankroll: float
    bets_before: List[NormalizedBet]
    bets_after: List[NormalizedBet]
    actions: List[ActionResult]


class FinalState(TypedDict):
    """Summary of the final session state after a sequence finishes."""

    bankroll: float
    bets: List[NormalizedBet]
    result: str
    error_code: str | None


class SequenceJournalEntry(TypedDict):
    """Roll-by-roll journal captured for a full test scenario."""

    scenario: str
    seed: int
    initial_bankroll: float
    initial_bets: List[NormalizedBet]
    steps: List[StepJournalEntry]
    final_state: FinalState


@dataclass(frozen=True)
class SequenceRunConfig:
    """Configuration for sequence harness runs."""

    seed_base: int = 42000


def ensure_results_dir() -> None:
    """Ensure the results directory exists before writing artifacts."""

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def normalize_bets(bets: Iterable[Mapping[str, Any]]) -> List[NormalizedBet]:
    """Normalize bet dictionaries for stable comparisons and reporting."""

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
    """Persist JSON data with deterministic formatting."""

    ensure_results_dir()
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _summary_counts(journal: Sequence[SequenceJournalEntry]) -> tuple[int, int, int]:
    total = len(journal)
    ok_count = sum(1 for entry in journal if entry["final_state"]["result"] == "ok")
    error_count = total - ok_count
    return total, ok_count, error_count


def _format_bet_summary(bets: Sequence[NormalizedBet]) -> str:
    if not bets:
        return "(none)"
    fragments: List[str] = []
    for bet in bets:
        amount_value = float(bet["amount"])
        amount = f"${amount_value:.0f}" if amount_value.is_integer() else f"${amount_value:.2f}"
        number = bet.get("number")
        number_part = f" {number}" if number is not None else ""
        fragments.append(f"{bet['type']}{number_part}: {amount}")
    return "; ".join(fragments)


def _format_action(action: ActionResult) -> str:
    args = action.get("args", {})
    pieces: List[str] = []
    number = args.get("number")
    base = args.get("base")
    amount = args.get("amount")
    if number is not None and amount is not None:
        pieces.append(f"{number}:{amount}")
    elif amount is not None:
        pieces.append(str(amount))
    if base is not None:
        pieces.append(str(base))
    extra_keys = [key for key in sorted(args) if key not in {"number", "amount", "base"}]
    for key in extra_keys:
        pieces.append(f"{key}={args[key]}")

    detail = f" {' '.join(pieces)}" if pieces else ""
    if action.get("result") == "error":
        error = action.get("error_code") or "error"
        outcome = f"error ({error})"
    else:
        outcome = "ok"
    return f"{action['verb']}{detail} {outcome}".strip()


def _render_step_rows(entry: SequenceJournalEntry) -> List[str]:
    lines = [
        "| Step # | Label | Dice | Actions | Bankroll (before→after) | Bet Summary |",
        "| ------ | ----- | ---- | ------- | ------------------------ | ----------- |",
    ]
    for step in entry["steps"]:
        dice = step["dice"]
        dice_display = "—" if dice is None else f"{dice[0]}+{dice[1]}"
        actions_display = "; ".join(_format_action(action) for action in step["actions"]) or "(none)"
        bankroll_display = f"{step['before_bankroll']:.2f} → {step['after_bankroll']:.2f}"
        bets_display = _format_bet_summary(step["bets_after"])
        lines.append(
            "| {index} | {label} | {dice} | {actions} | {bankroll} | {bets} |".format(
                index=step["index"],
                label=step["label"],
                dice=dice_display,
                actions=actions_display,
                bankroll=bankroll_display,
                bets=bets_display,
            )
        )
    lines.append("")
    return lines


def write_sequence_report(path: Path, journal: Sequence[SequenceJournalEntry], *, title: str) -> None:
    """Write a human-friendly markdown trace report for the provided journal."""

    ensure_results_dir()
    total, ok_count, error_count = _summary_counts(journal)

    lines: List[str] = [f"# {title}", ""]
    lines.extend(["## Summary", ""])
    lines.append(f"- Total scenarios: {total}")
    lines.append(f"- Successful (final result ok): {ok_count}")
    lines.append(f"- With errors: {error_count}")
    lines.append("")

    for entry in journal:
        lines.append(f"## Scenario: {entry['scenario']}")
        lines.append("")
        lines.append(f"- Initial bankroll: {entry['initial_bankroll']:.2f}")
        lines.append(f"- Initial bets: {_format_bet_summary(entry['initial_bets'])}")
        lines.append("")
        lines.extend(_render_step_rows(entry))
        lines.append("```json")
        lines.append(json.dumps({"final_state": entry["final_state"]}, indent=2, sort_keys=True))
        lines.append("```")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def _extract_mismatch_label(message: str) -> str:
    prefix = message.split(":", 1)[0]
    if " step" in prefix:
        return prefix.split(" step", 1)[0]
    return prefix


def _build_parity_summary(
    api_journal: Sequence[SequenceJournalEntry],
    vanilla_journal: Sequence[SequenceJournalEntry],
    *,
    epsilon: float,
) -> Dict[str, MutableMapping[str, Any]]:
    vanilla_lookup = {entry["scenario"]: entry for entry in vanilla_journal}
    summary: Dict[str, MutableMapping[str, Any]] = {}

    for api_entry in api_journal:
        label = api_entry["scenario"]
        vanilla_entry = vanilla_lookup.get(label)
        record: MutableMapping[str, Any] = {
            "scenario": label,
            "api_final": api_entry["final_state"],
            "vanilla_final": vanilla_entry["final_state"] if vanilla_entry else None,
            "result_match": False,
            "error_match": False,
            "bankroll_match": False,
            "bets_match": False,
            "status": "❌",
        }

        if vanilla_entry is None:
            summary[label] = record
            continue

        api_final = api_entry["final_state"]
        vanilla_final = vanilla_entry["final_state"]
        record["result_match"] = api_final["result"] == vanilla_final["result"]
        record["error_match"] = (api_final.get("error_code") or "") == (
            vanilla_final.get("error_code") or ""
        )
        record["bankroll_match"] = (
            abs(api_final["bankroll"] - vanilla_final["bankroll"]) <= epsilon
        )
        record["bets_match"] = api_final["bets"] == vanilla_final["bets"]
        record["status"] = "✅" if all(
            (
                record["result_match"],
                record["error_match"],
                record["bankroll_match"],
                record["bets_match"],
            )
        ) else "❌"
        summary[label] = record

    for vanilla_entry in vanilla_journal:
        label = vanilla_entry["scenario"]
        if label not in summary:
            summary[label] = {
                "scenario": label,
                "api_final": None,
                "vanilla_final": vanilla_entry["final_state"],
                "result_match": False,
                "error_match": False,
                "bankroll_match": False,
                "bets_match": False,
                "status": "❌",
            }

    return summary


def compare_journals(
    api_journal: Sequence[SequenceJournalEntry],
    vanilla_journal: Sequence[SequenceJournalEntry],
    *,
    epsilon: float = 1e-6,
) -> tuple[bool, List[str]]:
    """Compare API and vanilla journals, returning mismatch messages."""

    mismatches: List[str] = []
    vanilla_lookup = {entry["scenario"]: entry for entry in vanilla_journal}

    parity_summary = _build_parity_summary(api_journal, vanilla_journal, epsilon=epsilon)
    for record in parity_summary.values():
        if not record["result_match"]:
            mismatches.append(
                f"{record['scenario']}: result mismatch"
                if record["vanilla_final"] is not None and record["api_final"] is not None
                else f"{record['scenario']}: scenario mismatch"
            )
        if record["vanilla_final"] is None or record["api_final"] is None:
            continue
        if not record["error_match"]:
            mismatches.append(
                f"{record['scenario']}: error code mismatch ({record['api_final'].get('error_code')} vs {record['vanilla_final'].get('error_code')})"
            )
        if not record["bankroll_match"]:
            mismatches.append(
                f"{record['scenario']}: bankroll mismatch ({record['api_final']['bankroll']:.2f} vs {record['vanilla_final']['bankroll']:.2f})"
            )
        if not record["bets_match"]:
            mismatches.append(f"{record['scenario']}: final bets mismatch")

    for api_entry in api_journal:
        label = api_entry["scenario"]
        vanilla_entry = vanilla_lookup.get(label)
        if vanilla_entry is None:
            continue

        vanilla_steps = vanilla_entry["steps"]
        api_steps = api_entry["steps"]
        if len(api_steps) != len(vanilla_steps):
            mismatches.append(f"{label}: step count mismatch")
            continue
        for idx, (api_step, vanilla_step) in enumerate(zip(api_steps, vanilla_steps)):
            if api_step["label"] != vanilla_step["label"]:
                mismatches.append(
                    f"{label} step {idx}: label mismatch ({api_step['label']} vs {vanilla_step['label']})"
                )
            if api_step["dice"] != vanilla_step["dice"]:
                mismatches.append(
                    f"{label} step {idx}: dice mismatch ({api_step['dice']} vs {vanilla_step['dice']})"
                )
            if abs(api_step["before_bankroll"] - vanilla_step["before_bankroll"]) > epsilon:
                mismatches.append(
                    f"{label} step {idx}: before bankroll mismatch ({api_step['before_bankroll']:.2f} vs {vanilla_step['before_bankroll']:.2f})"
                )
            if abs(api_step["after_bankroll"] - vanilla_step["after_bankroll"]) > epsilon:
                mismatches.append(
                    f"{label} step {idx}: after bankroll mismatch ({api_step['after_bankroll']:.2f} vs {vanilla_step['after_bankroll']:.2f})"
                )
            if api_step["bets_after"] != vanilla_step["bets_after"]:
                mismatches.append(f"{label} step {idx}: bets after mismatch")
            if len(api_step["actions"]) != len(vanilla_step["actions"]):
                mismatches.append(f"{label} step {idx}: action count mismatch")
                continue
            for action_idx, (api_action, vanilla_action) in enumerate(
                zip(api_step["actions"], vanilla_step["actions"])
            ):
                if api_action["verb"] != vanilla_action["verb"]:
                    mismatches.append(
                        f"{label} step {idx} action {action_idx}: verb mismatch"
                    )
                if api_action["result"] != vanilla_action["result"]:
                    mismatches.append(
                        f"{label} step {idx} action {action_idx}: result mismatch ({api_action['result']} vs {vanilla_action['result']})"
                    )
                if (api_action.get("error_code") or "") != (
                    vanilla_action.get("error_code") or ""
                ):
                    mismatches.append(
                        f"{label} step {idx} action {action_idx}: error code mismatch ({api_action.get('error_code')} vs {vanilla_action.get('error_code')})"
                    )

    ok = not mismatches
    return ok, mismatches


def write_parity_report(
    api_journal: Sequence[SequenceJournalEntry],
    vanilla_journal: Sequence[SequenceJournalEntry],
    mismatches: Sequence[str],
) -> None:
    """Write a parity report comparing API and vanilla journals."""

    ensure_results_dir()
    parity_summary = _build_parity_summary(api_journal, vanilla_journal, epsilon=1e-6)

    total = len(parity_summary)
    perfect_matches = sum(1 for record in parity_summary.values() if record["status"] == "✅")
    mismatch_count = total - perfect_matches

    lines: List[str] = ["# CrapsSim API — Sequence Trace Parity (API vs Vanilla)", ""]
    lines.extend(["## Summary", ""])
    lines.append(f"- Total scenarios: {total}")
    lines.append(f"- Perfect matches: {perfect_matches}")
    lines.append(f"- Mismatches: {mismatch_count}")
    lines.append("")

    lines.extend(["## Scenario Parity", ""])
    lines.append(
        "| Scenario | Result | Error Code | Bankroll (API) | Bankroll (Vanilla) | Bets Match? | Status |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for label in sorted(parity_summary):
        record = parity_summary[label]
        api_final = record.get("api_final")
        vanilla_final = record.get("vanilla_final")
        result = api_final["result"] if api_final else "—"
        error_code = api_final.get("error_code") if api_final else None
        lines.append(
            "| {scenario} | {result} | {error} | {api_bankroll} | {vanilla_bankroll} | {bets_match} | {status} |".format(
                scenario=label,
                result=result,
                error=error_code or "",
                api_bankroll=f"{api_final['bankroll']:.2f}" if api_final else "—",
                vanilla_bankroll=f"{vanilla_final['bankroll']:.2f}" if vanilla_final else "—",
                bets_match="✅" if record.get("bets_match") else "❌",
                status=record["status"],
            )
        )
    lines.append("")

    if mismatches:
        lines.extend(["## Mismatch Details", ""])
        seen_labels = set()
        for message in mismatches:
            label = _extract_mismatch_label(message)
            if label not in seen_labels:
                lines.append(f"### {label}")
                lines.append("")
                seen_labels.add(label)
            lines.append(f"- {message}")
        lines.append("")
    else:
        lines.append("All scenarios matched across API and vanilla harnesses.")

    PARITY_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
