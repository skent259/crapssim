"""Run the CrapsSim API surface stress scenarios directly against the engine."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, List

from crapssim.table import Table

from crapssim_api.actions import build_bet, compute_required_cash
from crapssim_api.errors import ApiError, ApiErrorCode
from crapssim_api.session import Session

from .api_surface_scenarios import SCENARIOS, Scenario

DEFAULT_JSON = Path("build/api_surface_vanilla.json")
DEFAULT_MARKDOWN = Path("docs/API_SURFACE_STRESS_VANILLA.md")


def _ensure_player(session: Session) -> Any:
    session._ensure_player()  # noqa: SLF001 - harness needs direct access
    player = session.player()
    if player is None:  # pragma: no cover - defensive
        raise RuntimeError("session player unavailable")
    return player


def _normalize_bets(bets: Iterable[dict]) -> List[dict]:
    normalized: List[dict] = []
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


def _apply_bet(session: Session, verb: str, args: dict) -> tuple[str, str | None, float, float, List[dict], List[dict]]:
    player = _ensure_player(session)
    table = session.table

    before_snapshot = session.snapshot()
    before_bankroll = float(before_snapshot.get("bankroll", 0.0))
    before_bets = _normalize_bets(before_snapshot.get("bets", []))

    try:
        bet = build_bet(verb, args, table=table, player=player)
        required_cash = compute_required_cash(player, bet)
        if required_cash > player.bankroll + 1e-9:
            raise ApiError(
                ApiErrorCode.INSUFFICIENT_FUNDS,
                f"bankroll ${player.bankroll:.2f} < required ${required_cash:.2f}",
            )
        player.add_bet(bet)

        after_snapshot = session.snapshot()
        after_bankroll = float(after_snapshot.get("bankroll", 0.0))
        after_bets = _normalize_bets(after_snapshot.get("bets", []))
        applied = (abs(after_bankroll - before_bankroll) > 1e-9) or (after_bets != before_bets)
        if not applied:
            raise ApiError(ApiErrorCode.TABLE_RULE_BLOCK, "engine rejected action")
        return "ok", None, before_bankroll, after_bankroll, before_bets, after_bets
    except ApiError as exc:
        after_snapshot = session.snapshot()
        after_bankroll = float(after_snapshot.get("bankroll", 0.0))
        after_bets = _normalize_bets(after_snapshot.get("bets", []))
        code = exc.code.value if isinstance(exc.code, ApiErrorCode) else str(exc.code)
        return "error", code, before_bankroll, after_bankroll, before_bets, after_bets


def _ensure_output_dirs(*paths: Path) -> None:
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, data: Any) -> None:
    _ensure_output_dirs(path)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_markdown(path: Path, journal: list[dict]) -> None:
    _ensure_output_dirs(path)
    total = len(journal)
    ok_count = sum(1 for entry in journal if entry["result"] == "ok")
    error_count = total - ok_count
    scenario_lookup = {scenario["label"]: scenario for scenario in SCENARIOS}

    lines = ["# CrapsSim Vanilla Engine Surface Stress Report", ""]
    lines.append("## Summary")
    lines.append("")
    lines.append(f"* Total scenarios: **{total}**")
    lines.append(f"* Successful actions: **{ok_count}**")
    lines.append(f"* Errors: **{error_count}**")
    lines.append("")

    lines.append("## Scenario Results")
    lines.append("")
    lines.append("| Scenario | Verb | Result | Error Code | Expected |")
    lines.append("| --- | --- | --- | --- | --- |")
    for entry in journal:
        expected = scenario_lookup.get(entry["scenario"], {}).get("expect", {})
        expected_desc = expected.get("result")
        expected_code = expected.get("error_code")
        if expected_code:
            expected_desc = f"{expected_desc} ({expected_code})"
        lines.append(
            "| {scenario} | {verb} | {result} | {error_code} | {expected} |".format(
                scenario=entry["scenario"],
                verb=entry["verb"],
                result=entry["result"],
                error_code=entry["error_code"] or "",
                expected=expected_desc or "",
            )
        )
    lines.append("")

    lines.append("## Full Journal")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(journal, indent=2, sort_keys=True))
    lines.append("```")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def run(*, limit: int | None = None, json_path: Path = DEFAULT_JSON, markdown_path: Path = DEFAULT_MARKDOWN) -> list[dict]:
    journal: list[dict] = []
    scenarios: Iterable[Scenario]
    if limit is not None:
        scenarios = SCENARIOS[:limit]
    else:
        scenarios = SCENARIOS

    for idx, scenario in enumerate(scenarios):
        table = Table(seed=10_000 + idx)
        session = Session(table=table)
        player = _ensure_player(session)
        player.bets.clear()

        bankroll = scenario["pre_state"].get("bankroll")
        if bankroll is not None:
            player.bankroll = float(bankroll)

        for bet_spec in scenario["pre_state"].get("existing_bets", []):
            bet_verb = bet_spec.get("verb")
            bet_args = bet_spec.get("args", {}) or {}
            if not isinstance(bet_verb, str):
                raise RuntimeError(f"invalid pre-state bet verb: {bet_spec!r}")
            result, error_code, *_ = _apply_bet(session, bet_verb, bet_args)
            if result != "ok":
                raise RuntimeError(f"pre-state bet {bet_verb} failed with {error_code}")

        for dice in scenario["pre_state"].get("rolls_before", []):
            session.step_roll(dice=[int(dice[0]), int(dice[1])])

        result, error_code, before_bankroll, after_bankroll, before_bets, after_bets = _apply_bet(
            session, scenario["verb"], scenario["args"]
        )

        journal.append(
            {
                "scenario": scenario["label"],
                "verb": scenario["verb"],
                "args": scenario["args"],
                "result": result,
                "error_code": error_code,
                "before_bankroll": before_bankroll,
                "after_bankroll": after_bankroll,
                "bets_before": before_bets,
                "bets_after": after_bets,
            }
        )

    _write_json(json_path, journal)
    _write_markdown(markdown_path, journal)
    return journal


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run the CrapsSim vanilla engine stress scenarios")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of scenarios to execute")
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON, help="Path to write the JSON journal")
    parser.add_argument(
        "--markdown", type=Path, default=DEFAULT_MARKDOWN, help="Path to write the markdown report"
    )
    args = parser.parse_args()

    run(limit=args.limit, json_path=args.json, markdown_path=args.markdown)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
