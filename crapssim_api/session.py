from __future__ import annotations
import importlib
from typing import Callable, Optional, Any

from crapssim.table import Table, TableUpdate

class Session:
    """
    Lightweight wrapper around a CrapsSim Table.
    Provides a minimal surface for orchestration, recording, and replay.
    Does not change engine behavior.
    """

    def __init__(self, table: Optional[Table] = None, *, record_callback: Callable[[dict], None] | None = None):
        self._table = table or Table()
        self._ensure_player()
        self._record = record_callback
        self._running = False
        self.roll_id = 0
        self._pending_fixed_dice: tuple[int, int] | None = None

    # internal util
    def _emit(self, event: dict) -> None:
        if self._record:
            self._record(event)

    def start(self) -> None:
        self._running = True
        self._emit({"type": "run_started"})

    def stop(self) -> None:
        self._running = False
        self._emit({"type": "run_finished"})

    def apply_command(self, command: dict) -> dict:
        """
        Supported commands:
          {"type":"place_bet", "bet":<name>, "args":{...}}
          {"type":"remove_bet", "bet_id":...}
          {"type":"set_dice", "dice":[d1,d2]}
        """
        ctype = command.get("type")

        if ctype == "place_bet":
            bet_name = command["bet"]
            bet_args = command.get("args", {}) or {}
            ok = self._place_bet(bet_name, bet_args)
            self._emit({"type": "bet_placed", "bet": bet_name, "args": bet_args, "ok": ok})
            return {"ok": ok}

        if ctype == "remove_bet":
            bet_id = command.get("bet_id")
            ok = self._remove_bet(bet_id)
            self._emit({"type": "bet_removed", "bet_id": bet_id, "ok": ok})
            return {"ok": ok}

        if ctype == "set_dice":
            dice = command["dice"]
            self._pending_fixed_dice = (int(dice[0]), int(dice[1]))
            self._emit({"type": "dice_fixed", "dice": dice})
            return {"ok": True}

        return {"ok": False, "error": "UNKNOWN_COMMAND"}

    def step_roll(self, dice: list[int] | None = None) -> dict:
        """
        Roll once. If dice is provided, uses fixed dice for this roll.
        """
        self._ensure_player()

        if dice is not None:
            roll_values = (int(dice[0]), int(dice[1]))
        elif self._pending_fixed_dice is not None:
            roll_values = self._pending_fixed_dice
            self._pending_fixed_dice = None
        else:
            roll_values = None

        before = self.snapshot()

        updater = TableUpdate()
        updater.update_table_stats(self._table)
        updater.roll(self._table, fixed_outcome=roll_values)
        updater.update_bets(self._table)
        updater.set_new_shooter(self._table)
        updater.update_numbers(self._table, verbose=False)

        self.roll_id += 1

        dice_values = list(self._table.dice.result or (0, 0))
        after = self.snapshot()

        event = {
            "type": "roll",
            "roll_id": self.roll_id,
            "dice": dice_values,
            "before": before,
            "after": after,
        }
        self._emit(event)
        return event

    def snapshot(self) -> dict:
        """
        JSON-safe dict of the current table state.
        Does not compute statistics.
        """
        t = self._table
        player = self._first_player()
        bets = []
        if player:
            for idx, bet in enumerate(player.bets):
                bets.append(
                    {
                        "id": idx,
                        "type": bet.__class__.__name__,
                        "number": getattr(bet, "number", None),
                        "amount": float(getattr(bet, "amount", 0.0)),
                    }
                )

        point_value = getattr(t.point, "number", None)
        bankroll = float(getattr(player, "bankroll", 0.0)) if player else 0.0
        shooter = int(getattr(t, "n_shooters", 0))

        return {
            "point": point_value,
            "bets": bets,
            "bankroll": bankroll,
            "shooter": shooter,
        }

    # ------------------------------------------------------------------
    def _ensure_player(self) -> None:
        if not getattr(self._table, "players", []):
            self._table.add_player(bankroll=1000, strategy=None, name="Session Player")

    def _first_player(self):
        return self._table.players[0] if getattr(self._table, "players", []) else None

    def _bet_signature(self) -> list[tuple[str, Optional[int], float]]:
        player = self._first_player()
        sig: list[tuple[str, Optional[int], float]] = []
        if player:
            for bet in player.bets:
                sig.append(
                    (
                        bet.__class__.__name__,
                        getattr(bet, "number", None),
                        float(getattr(bet, "amount", 0.0)),
                    )
                )
        return sig

    def _place_bet(self, bet_name: str, bet_args: dict) -> bool:
        try:
            bet_module = importlib.import_module("crapssim.bet")
        except ImportError:
            return False

        bet_cls = getattr(bet_module, bet_name, None)
        if bet_cls is None:
            return False

        player = self._first_player()
        if player is None:
            return False

        before = self._bet_signature()
        bankroll_before = float(player.bankroll)

        try:
            bet_obj = bet_cls(**bet_args)
        except TypeError:
            return False

        player.add_bet(bet_obj)

        after = self._bet_signature()
        bankroll_after = float(player.bankroll)
        return after != before or abs(bankroll_after - bankroll_before) > 1e-9

    def _remove_bet(self, bet_id: Any) -> bool:
        player = self._first_player()
        if player is None:
            return False

        bet_type: Optional[str] = None
        bet_number: Optional[int] = None

        if isinstance(bet_id, dict):
            bet_type = bet_id.get("type")
            bet_number = bet_id.get("number")
        elif isinstance(bet_id, str):
            bet_type = bet_id
        elif isinstance(bet_id, (tuple, list)) and bet_id:
            bet_type = str(bet_id[0])
            if len(bet_id) > 1:
                try:
                    bet_number = int(bet_id[1])
                except (TypeError, ValueError):
                    bet_number = None

        if not bet_type:
            return False

        target = None
        for bet in player.bets:
            if bet.__class__.__name__ != bet_type:
                continue
            number = getattr(bet, "number", None)
            if bet_number is None or number == bet_number:
                target = bet
                break

        if not target:
            return False

        before = self._bet_signature()
        bankroll_before = float(player.bankroll)

        player.remove_bet(target)

        after = self._bet_signature()
        bankroll_after = float(player.bankroll)
        return after != before or abs(bankroll_after - bankroll_before) > 1e-9


