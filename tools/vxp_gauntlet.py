from __future__ import annotations

import csv
import json
import pathlib
import time
from dataclasses import asdict, dataclass

import crapssim.bet as B
from crapssim.strategy.tools import NullStrategy
from crapssim.table import Table, TableUpdate

# ---------- Utilities ----------


def roll_fixed(table: Table, total: int) -> None:
    """Roll the dice to a fixed total while exercising full table lifecycle."""
    updater = TableUpdate()
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            if d1 + d2 == total:
                updater.run(table, dice_outcome=(d1, d2))
                return
    raise ValueError(f"Unsupported total {total}")


def establish_point(table: Table, point_total: int) -> None:
    """Ensure the table point is set to ``point_total`` for deterministic setups."""
    if table.point == "On":
        roll_fixed(table, 7)
    roll_fixed(table, point_total)


# ---------- Data model ----------


@dataclass
class RollRecord:
    scenario: str
    step: int
    total: int
    bankroll_before: float
    bankroll_after: float


@dataclass
class ScenarioResult:
    name: str
    settings: dict
    start_bankroll: float
    end_bankroll: float
    rolls: list[RollRecord]
    final_open_bets: list[str]


# ---------- Scenarios ----------


def scenario_horn_world() -> ScenarioResult:
    table = Table()
    player = table.add_player(bankroll=1000.0)
    start_bankroll = player.bankroll
    player.add_bet(B.Horn(5))
    player.add_bet(B.World(5))

    rolls: list[RollRecord] = []
    for i, total in enumerate([2, 3, 7, 11, 12]):
        before = player.bankroll
        roll_fixed(table, total)
        rolls.append(RollRecord("HornWorld", i + 1, total, before, player.bankroll))

    return ScenarioResult(
        name="HornWorld",
        settings=dict(table.settings),
        start_bankroll=start_bankroll,
        end_bankroll=player.bankroll,
        rolls=rolls,
        final_open_bets=[str(bet) for bet in player.bets],
    )


def scenario_props_isolated() -> ScenarioResult:
    table = Table()
    player = table.add_player(bankroll=1000.0, strategy=NullStrategy())

    # Defensive cleanup in case upstream defaults change before strategies run.
    player.bets = [
        bet for bet in player.bets if "PassLine" not in bet.__class__.__name__
    ]

    start_bankroll = player.bankroll
    player.add_bet(B.Horn(5))
    player.add_bet(B.World(5))

    rolls: list[RollRecord] = []
    for i, total in enumerate([2, 3, 7, 11, 12]):
        before = player.bankroll
        roll_fixed(table, total)
        rolls.append(RollRecord("PropsIsolated", i + 1, total, before, player.bankroll))

    return ScenarioResult(
        name="PropsIsolated",
        settings=dict(table.settings) | {"pass_line_suppressed": True},
        start_bankroll=start_bankroll,
        end_bankroll=player.bankroll,
        rolls=rolls,
        final_open_bets=[str(bet) for bet in player.bets],
    )


def scenario_big6_big8() -> ScenarioResult:
    table = Table()
    player = table.add_player(bankroll=1000.0)
    start_bankroll = player.bankroll
    player.add_bet(B.Big6(10))
    player.add_bet(B.Big8(10))

    sequence = [6, 8, 7]
    rolls: list[RollRecord] = []
    for i, total in enumerate(sequence):
        before = player.bankroll
        roll_fixed(table, total)
        rolls.append(RollRecord("Big6Big8", i + 1, total, before, player.bankroll))

    return ScenarioResult(
        "Big6Big8",
        dict(table.settings),
        start_bankroll,
        player.bankroll,
        rolls,
        [str(bet) for bet in player.bets],
    )


def scenario_buy_lay_matrix() -> list[ScenarioResult]:
    results: list[ScenarioResult] = []
    matrix = [
        {
            "name": "Default_on_win_none",
            "settings": {"vig_rounding": "none", "vig_paid_on_win": True},
        },
        {
            "name": "On_bet_ceil_floor25",
            "settings": {
                "vig_rounding": "ceil_dollar",
                "vig_floor": 25.0,
                "vig_paid_on_win": False,
            },
        },
    ]
    tests = [
        (
            "Buy4_then_hit_then_7",
            lambda table, player: player.add_bet(B.Buy(4, 25.0)),
            [4, 7],
        ),
        (
            "Buy6_then_hit_then_7",
            lambda table, player: player.add_bet(B.Buy(6, 30.0)),
            [6, 7],
        ),
        (
            "Lay10_then_7_then_10",
            lambda table, player: player.add_bet(B.Lay(10, 25.0)),
            [7, 10],
        ),
        (
            "Lay8_then_7_then_8",
            lambda table, player: player.add_bet(B.Lay(8, 30.0)),
            [7, 8],
        ),
    ]

    for cfg in matrix:
        for test_name, setup_fn, seq in tests:
            table = Table()
            player = table.add_player(bankroll=1000.0)
            start_bankroll = player.bankroll
            for key, value in cfg["settings"].items():
                table.settings[key] = value
            setup_fn(table, player)
            rolls: list[RollRecord] = []
            for i, total in enumerate(seq):
                before = player.bankroll
                roll_fixed(table, total)
                rolls.append(
                    RollRecord(
                        f"{cfg['name']}::{test_name}",
                        i + 1,
                        total,
                        before,
                        player.bankroll,
                    )
                )
            results.append(
                ScenarioResult(
                    f"{cfg['name']}::{test_name}",
                    dict(table.settings),
                    start_bankroll,
                    player.bankroll,
                    rolls,
                    [str(bet) for bet in player.bets],
                )
            )

    return results


def scenario_put_with_and_without_odds() -> list[ScenarioResult]:
    output: list[ScenarioResult] = []

    # A) allow odds (default True)
    table = Table()
    player = table.add_player(bankroll=1000.0)
    start_bankroll = player.bankroll
    establish_point(table, 6)
    player.add_bet(B.Put(6, 10))
    player.add_bet(B.Odds(B.Put, 6, 20, True))

    sequence = [6, 7]
    rolls: list[RollRecord] = []
    for i, total in enumerate(sequence):
        before = player.bankroll
        roll_fixed(table, total)
        rolls.append(
            RollRecord("PutOddsAllowed", i + 1, total, before, player.bankroll)
        )
    output.append(
        ScenarioResult(
            "PutOddsAllowed",
            dict(table.settings),
            start_bankroll,
            player.bankroll,
            rolls,
            [str(bet) for bet in player.bets],
        )
    )

    # B) illegal Put while point OFF gets stripped pre-roll
    table3 = Table()
    player3 = table3.add_player(bankroll=1000.0)
    start_bankroll3 = player3.bankroll
    player3.bets.append(B.Put(6, 10))
    before = player3.bankroll
    roll_fixed(table3, 7)
    record = [RollRecord("PutIllegalGuard", 1, 7, before, player3.bankroll)]
    output.append(
        ScenarioResult(
            "PutIllegalGuard",
            dict(table3.settings),
            start_bankroll3,
            player3.bankroll,
            record,
            [str(bet) for bet in player3.bets],
        )
    )

    return output


# ---------- Runner ----------


def main() -> None:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    outdir = pathlib.Path("reports") / "vxp_gauntlet" / timestamp
    suffix = 1
    while outdir.exists():
        outdir = outdir.parent / f"{timestamp}_{suffix:02d}"
        suffix += 1
    outdir.mkdir(parents=True, exist_ok=True)

    results: list[ScenarioResult] = []
    results.append(scenario_horn_world())
    results.append(scenario_props_isolated())
    results.append(scenario_big6_big8())
    results.extend(scenario_buy_lay_matrix())
    results.extend(scenario_put_with_and_without_odds())

    data = [asdict(result) for result in results]
    (outdir / "gauntlet.json").write_text(json.dumps(data, indent=2))

    with (outdir / "gauntlet_rolls.csv").open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "scenario",
                "step",
                "total",
                "bankroll_before",
                "bankroll_after",
                "delta",
            ]
        )
        for result in results:
            for record in result.rolls:
                delta = record.bankroll_after - record.bankroll_before
                writer.writerow(
                    [
                        record.scenario,
                        record.step,
                        record.total,
                        f"{record.bankroll_before:.2f}",
                        f"{record.bankroll_after:.2f}",
                        f"{delta:.2f}",
                    ]
                )

    markdown_lines = ["# VXP Gauntlet Summary\n"]
    markdown_lines.append(
        "> Note: Table defaults include a $5 Pass Line on come-out. Some scenarios reflect "
        "PL outcomes (e.g., come-out 2/3/7/11). An isolated-props scenario below disables "
        "PL to show pure Horn/World net.\n"
    )
    for result in results:
        markdown_lines.append(f"## {result.name}")
        settings_json = json.dumps(result.settings, separators=(",", ":"))
        markdown_lines.append(f"- Settings: `{settings_json}`")
        markdown_lines.append(f"- Start bankroll: {result.start_bankroll:.2f}")
        markdown_lines.append(f"- End bankroll: {result.end_bankroll:.2f}")
        if result.final_open_bets:
            markdown_lines.append(
                f"- Final open bets: {', '.join(result.final_open_bets)}"
            )
        else:
            markdown_lines.append("- Final open bets: (none)")
        if result.rolls:
            markdown_lines.append("")
            markdown_lines.append("| step | total | before | after | Δ |")
            markdown_lines.append("|---:|---:|---:|---:|---:|")
            for record in result.rolls:
                delta = record.bankroll_after - record.bankroll_before
                markdown_lines.append(
                    f"| {record.step} | {record.total} | {record.bankroll_before:.2f} | "
                    f"{record.bankroll_after:.2f} | {delta:.2f} |"
                )
        markdown_lines.append("")

    (outdir / "summary.md").write_text("\n".join(markdown_lines))

    print(f"[VXP-GAUNTLET] Artifacts in: {outdir}")


if __name__ == "__main__":
    main()
