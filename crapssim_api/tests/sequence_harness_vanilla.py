"""Vanilla engine sequence harness for CrapsSim."""
from __future__ import annotations

"""Vanilla-engine sequence harness for CrapsSim."""

from typing import Any, Dict, List

from crapssim.table import Table

from crapssim_api.actions import build_bet, compute_required_cash
from crapssim_api.errors import ApiError, ApiErrorCode
from crapssim_api.session import Session

from .sequence_harness_common import (
    VANILLA_JSON_PATH,
    VANILLA_REPORT_PATH,
    ActionResult,
    SequenceJournalEntry,
    SequenceRunConfig,
    ensure_results_dir,
    normalize_bets,
    write_json,
    write_sequence_report,
)
from .sequence_scenarios import SEQUENCE_SCENARIOS


def _ensure_player(session: Session):
    session._ensure_player()  # noqa: SLF001 - harness access
    player = session.player()
    if player is None:  # pragma: no cover - defensive
        raise RuntimeError("session player unavailable")
    return player


def _apply_initial_state(session: Session, *, bankroll: float, initial_bets: List[Dict[str, Any]]) -> None:
    player = _ensure_player(session)
    player.bets.clear()
    player.bankroll = float(bankroll)

    for bet in initial_bets:
        result = _apply_action(session, bet)
        if result["result"] != "ok":
            raise RuntimeError(f"initial bet {bet['verb']} failed with {result['error_code']}")


def _apply_action(session: Session, action: Dict[str, Any]) -> ActionResult:
    verb = action["verb"]
    args = dict(action.get("args", {}) or {})
    player = _ensure_player(session)
    table = session.table

    before_snapshot = session.snapshot()
    before_bets = normalize_bets(before_snapshot.get("bets", []))
    before_bankroll = float(before_snapshot.get("bankroll", 0.0))

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
        after_bets = normalize_bets(after_snapshot.get("bets", []))
        after_bankroll = float(after_snapshot.get("bankroll", 0.0))
        applied = (abs(after_bankroll - before_bankroll) > 1e-9) or (after_bets != before_bets)
        if not applied:
            raise ApiError(ApiErrorCode.TABLE_RULE_BLOCK, "engine rejected action")
        return {"verb": verb, "args": dict(args), "result": "ok", "error_code": None}
    except ApiError as exc:
        code = exc.code.value if isinstance(exc.code, ApiErrorCode) else str(exc.code)
        return {"verb": verb, "args": dict(args), "result": "error", "error_code": code}


def run_vanilla_sequence_harness(config: SequenceRunConfig | None = None) -> List[SequenceJournalEntry]:
    cfg = config or SequenceRunConfig()
    journal: List[SequenceJournalEntry] = []

    ensure_results_dir()

    for index, scenario in enumerate(SEQUENCE_SCENARIOS):
        seed = cfg.seed_base + scenario.get("seed_offset", index)
        table = Table(seed=seed)
        session = Session(table=table)
        initial_bankroll = float(scenario.get("initial_bankroll", 250.0))
        initial_bets = list(scenario.get("initial_bets", []))
        _apply_initial_state(
            session,
            bankroll=initial_bankroll,
            initial_bets=initial_bets,
        )

        initial_snapshot = session.snapshot()
        normalized_initial_bets = normalize_bets(initial_snapshot.get("bets", []))

        steps: List[Dict[str, Any]] = []
        last_result = "ok"
        last_error: str | None = None

        for step_index, step in enumerate(scenario.get("steps", [])):
            before_snapshot = session.snapshot()
            before_bankroll = float(before_snapshot.get("bankroll", 0.0))
            before_bets = normalize_bets(before_snapshot.get("bets", []))

            dice = step.get("dice")
            if dice is not None:
                session.step_roll(dice=[int(dice[0]), int(dice[1])])
                last_result = "ok"
                last_error = None

            actions = step.get("actions", []) or []
            action_results: List[ActionResult] = []
            for action in actions:
                result = _apply_action(session, action)
                action_results.append(result)
                last_result = result["result"]
                last_error = result.get("error_code")

            after_snapshot = session.snapshot()
            after_bankroll = float(after_snapshot.get("bankroll", 0.0))
            after_bets = normalize_bets(after_snapshot.get("bets", []))

            steps.append(
                {
                    "index": step_index,
                    "label": step.get("label", f"step_{step_index}"),
                    "dice": [int(dice[0]), int(dice[1])] if dice is not None else None,
                    "before_bankroll": before_bankroll,
                    "after_bankroll": after_bankroll,
                    "bets_before": before_bets,
                    "bets_after": after_bets,
                    "actions": action_results,
                }
            )

        final_snapshot = session.snapshot()
        final_bankroll = float(final_snapshot.get("bankroll", 0.0))
        final_bets = normalize_bets(final_snapshot.get("bets", []))

        journal.append(
            {
                "scenario": scenario["label"],
                "seed": seed,
                "initial_bankroll": initial_bankroll,
                "initial_bets": normalized_initial_bets,
                "steps": steps,
                "final_state": {
                    "bankroll": final_bankroll,
                    "bets": final_bets,
                    "result": last_result,
                    "error_code": last_error,
                },
            }
        )

        player = _ensure_player(session)
        player.bets.clear()

    write_json(VANILLA_JSON_PATH, journal)
    write_sequence_report(
        VANILLA_REPORT_PATH,
        journal,
        title="CrapsSim API — Roll-by-Roll Sequence Trace (Vanilla)",
    )
    return journal
