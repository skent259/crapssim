from __future__ import annotations

from functools import reduce
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence, Tuple

from crapssim.bet import (
    All,
    Any7,
    AnyCraps,
    Bet,
    Big6,
    Big8,
    Boxcars,
    Buy,
    CAndE,
    Come,
    DontCome,
    DontPass,
    Field,
    Fire,
    HardWay,
    Hop,
    Horn,
    Lay,
    Odds,
    PassLine,
    Place,
    Put,
    Small,
    Tall,
    Three,
    Two,
    World,
    Yo,
)
from crapssim.table import Player, Table

from .errors import ApiError, ApiErrorCode, bad_args
from .session import Session


AmountArgs = Mapping[str, Any]

_SIMPLE_AMOUNT_ONLY: Dict[str, type[Bet]] = {
    "pass_line": PassLine,
    "dont_pass": DontPass,
    "come": Come,
    "dont_come": DontCome,
    "field": Field,
    "any7": Any7,
    "c&e": CAndE,
    "horn": Horn,
    "world": World,
    "big6": Big6,
    "big8": Big8,
    "two": Two,
    "three": Three,
    "yo": Yo,
    "boxcars": Boxcars,
    "any_craps": AnyCraps,
    "fire": Fire,
    "all": All,
    "tall": Tall,
    "small": Small,
}

_NUMBER_REQUIRED: Dict[str, type[Bet]] = {
    "place": Place,
    "buy": Buy,
    "lay": Lay,
    "put": Put,
    "hardway": HardWay,
}

_ODDS_BASES: Dict[str, type[Bet]] = {
    "pass_line": PassLine,
    "dont_pass": DontPass,
    "come": Come,
    "dont_come": DontCome,
    "put": Put,
}

_BET_PLACEMENT_VERBS = frozenset(
    list(_SIMPLE_AMOUNT_ONLY) + list(_NUMBER_REQUIRED) + ["odds", "hop"]
)

_BET_MANAGEMENT_TYPE_MAP: Dict[str, type[Bet]] = {
    **_SIMPLE_AMOUNT_ONLY,
    **_NUMBER_REQUIRED,
    "odds": Odds,
    "hop": Hop,
}

_CENTER_ACTION_TYPES: Tuple[type[Bet], ...] = (
    Field,
    Any7,
    AnyCraps,
    CAndE,
    Horn,
    World,
    Two,
    Three,
    Yo,
    Boxcars,
    Hop,
    Fire,
    All,
    Tall,
    Small,
)

_PLACE_BUY_LAY_TYPES: Tuple[type[Bet], ...] = (Place, Buy, Lay)

_ATS_TYPES: Tuple[type[Bet], ...] = (All, Tall, Small)

_FIRE_TYPES: Tuple[type[Bet], ...] = (Fire,)

_BET_MANAGEMENT_VERBS = frozenset(
    {
        "remove_bet",
        "reduce_bet",
        "clear_all_bets",
        "clear_center_bets",
        "clear_place_buy_lay",
        "clear_ats_bets",
        "clear_fire_bets",
        "set_odds_working",
    }
)

SUPPORTED_VERBS = frozenset(_BET_PLACEMENT_VERBS | _BET_MANAGEMENT_VERBS)


def _coerce_amount(args: AmountArgs, verb: str) -> float:
    value = args.get("amount")
    if not isinstance(value, (int, float)):
        raise bad_args(f"{verb} requires numeric amount")
    amount = float(value)
    if amount <= 0:
        raise bad_args("amount must be greater than zero")
    return amount


def _coerce_number(args: AmountArgs, verb: str) -> int:
    number_value = args.get("number", args.get("box"))
    if number_value is None:
        raise bad_args(f"{verb} requires box/number argument")
    try:
        return int(number_value)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
        raise bad_args("number must be an integer") from exc


def _coerce_hop_result(args: AmountArgs, verb: str) -> tuple[int, int]:
    result = args.get("result")
    if not isinstance(result, (list, tuple)) or len(result) != 2:
        raise bad_args(f"{verb} requires result=[die1, die2]")
    try:
        die_1 = int(result[0])
        die_2 = int(result[1])
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
        raise bad_args("result values must be integers") from exc
    if not all(1 <= value <= 6 for value in (die_1, die_2)):
        raise bad_args("result values must be between 1 and 6")
    return die_1, die_2


def _combine_bets(bets: Iterable[Bet]) -> Bet:
    bets = list(bets)
    if not bets:
        raise ValueError("combine_bets requires at least one bet")
    return reduce(lambda acc, b: acc + b, bets[1:], bets[0])


def _ensure_odds_base(
    player: Player, base_cls: type[Bet], number: int | None, verb: str
) -> None:
    if base_cls in (PassLine, DontPass):
        if player.table.point.number is None:
            raise ApiError(
                ApiErrorCode.TABLE_RULE_BLOCK,
                "odds require an established point",
            )
        if not player.get_bets_by_type(base_cls):
            raise ApiError(
                ApiErrorCode.TABLE_RULE_BLOCK,
                f"odds require an active {base_cls.__name__} bet",
            )
        return

    target_number = number
    if target_number is None:
        raise ApiError(
            ApiErrorCode.TABLE_RULE_BLOCK,
            f"odds for {verb} require a resolved number",
        )

    matching = [
        bet
        for bet in player.get_bets_by_type(base_cls)
        if getattr(bet, "number", None) == target_number
    ]
    if not matching:
        raise ApiError(
            ApiErrorCode.TABLE_RULE_BLOCK,
            f"odds require an active {base_cls.__name__} bet on {target_number}",
        )


def build_bet(
    verb: str,
    args: AmountArgs,
    *,
    table: Table,
    player: Player,
) -> Bet:
    if verb not in _BET_PLACEMENT_VERBS:
        raise ApiError(ApiErrorCode.UNSUPPORTED_BET, f"verb '{verb}' not recognized")

    amount = _coerce_amount(args, verb)

    if verb in _SIMPLE_AMOUNT_ONLY:
        bet_cls = _SIMPLE_AMOUNT_ONLY[verb]
        try:
            return bet_cls(amount)
        except TypeError as exc:  # pragma: no cover - defensive
            raise bad_args(f"invalid arguments for {verb}") from exc

    if verb in _NUMBER_REQUIRED:
        number = _coerce_number(args, verb)
        bet_cls = _NUMBER_REQUIRED[verb]
        try:
            return bet_cls(number, amount)
        except (ValueError, KeyError) as exc:
            raise bad_args(f"invalid number '{number}' for {verb}") from exc

    if verb == "hop":
        dice_result = _coerce_hop_result(args, verb)
        return Hop(dice_result, amount)

    if verb == "odds":
        base_value = args.get("base")
        if not isinstance(base_value, str) or not base_value:
            raise bad_args("odds requires base bet identifier")
        base_key = base_value.lower()
        base_cls = _ODDS_BASES.get(base_key)
        if base_cls is None:
            raise bad_args(f"unsupported odds base '{base_value}'")

        if base_cls in (PassLine, DontPass):
            number = table.point.number
        else:
            number = None
            if "number" in args or "box" in args:
                number = _coerce_number(args, verb)

        always_working = bool(args.get("working"))
        _ensure_odds_base(player, base_cls, number, base_value)
        if number is None:
            raise ApiError(
                ApiErrorCode.TABLE_RULE_BLOCK,
                "odds require an established number",
            )
        return Odds(base_cls, number, amount, always_working=always_working)

    raise ApiError(ApiErrorCode.UNSUPPORTED_BET, f"verb '{verb}' not recognized")


def compute_required_cash(player: Player, bet: Bet) -> float:
    existing = list(player.already_placed_bets(bet))
    existing_cost = sum(x.cost(player.table) for x in existing)
    combined = existing + [bet]
    new_bet = _combine_bets(combined)
    new_cost = new_bet.cost(player.table)
    return float(new_cost - existing_cost)


def describe_vig(bet: Bet, table: Table) -> Dict[str, Any] | None:
    vig_method = getattr(bet, "vig", None)
    if callable(vig_method):
        vig_amount = float(vig_method(table))
        return {
            "amount": vig_amount,
            "paid_on_win": bool(table.settings.get("vig_paid_on_win", False)),
        }
    return None


def _ensure_session_player(session: Session) -> Player:
    player = session.player()
    if player is None:
        session._ensure_player()  # noqa: SLF001 - internal helper access
        player = session.player()
    if player is None:  # pragma: no cover - defensive
        raise ApiError(ApiErrorCode.INTERNAL, "session player unavailable")
    return player


def _normalize_bets(bets: Sequence[Bet]) -> list[Dict[str, Any]]:
    normalized: list[Dict[str, Any]] = []
    for bet in bets:
        normalized.append(
            {
                "type": bet.__class__.__name__,
                "number": getattr(bet, "number", None),
                "amount": float(getattr(bet, "amount", 0.0)),
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


def _resolve_bet_type(type_key: str | None) -> type[Bet]:
    if not isinstance(type_key, str) or not type_key:
        raise bad_args("type must be provided")
    bet_cls = _BET_MANAGEMENT_TYPE_MAP.get(type_key.lower())
    if bet_cls is None:
        raise bad_args(f"unsupported bet type '{type_key}'")
    return bet_cls


def _matches_number(bet: Bet, number: Optional[int]) -> bool:
    if number is None:
        return True
    if not hasattr(bet, "number"):
        return False
    return getattr(bet, "number", None) == number


def _coerce_optional_number(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
        raise bad_args("number must be an integer") from exc


def remove_bets_matching(
    session: Session,
    *,
    bet_type: type[Bet] | None = None,
    number: Optional[int] = None,
) -> list[Bet]:
    player = _ensure_session_player(session)
    table = session.table
    removed: list[Bet] = []
    for bet in list(player.bets):
        if bet_type is not None and type(bet) is not bet_type:
            continue
        if not _matches_number(bet, number):
            continue
        if bet.is_removable(table):
            player.remove_bet(bet)
            removed.append(bet)
    return removed


def _construct_bet(
    bet_type: type[Bet],
    *,
    number: Optional[int],
    amount: float,
) -> Bet:
    try:
        if number is None:
            return bet_type(amount)
        return bet_type(number, amount)
    except TypeError as exc:  # pragma: no cover - defensive
        raise bad_args("invalid bet construction arguments") from exc


def set_bet_amount(
    session: Session,
    *,
    bet_type: type[Bet],
    number: Optional[int] = None,
    new_amount: float,
) -> tuple[list[Bet], list[Bet]]:
    if new_amount < 0:
        raise bad_args("new_amount must be non-negative")

    player = _ensure_session_player(session)
    matching = [
        bet
        for bet in player.bets
        if type(bet) is bet_type and _matches_number(bet, number)
    ]

    current_total = float(sum(getattr(bet, "amount", 0.0) for bet in matching))

    if new_amount > current_total + 1e-9:
        raise ApiError(ApiErrorCode.BAD_ARGS, "new_amount exceeds existing action")

    if current_total == 0:
        if new_amount == 0:
            return [], []
        raise ApiError(ApiErrorCode.BAD_ARGS, "no matching bets to modify")

    if abs(new_amount - current_total) <= 1e-9:
        return [], []

    removed = remove_bets_matching(session, bet_type=bet_type, number=number)
    removed_total = float(sum(getattr(bet, "amount", 0.0) for bet in removed))

    if new_amount < current_total and removed_total == 0:
        raise ApiError(
            ApiErrorCode.TABLE_RULE_BLOCK,
            "bet cannot be reduced while locked by table rules",
        )

    added: list[Bet] = []
    if new_amount > 0:
        new_bet = _construct_bet(bet_type, number=number, amount=new_amount)
        player.add_bet(new_bet)
        added.append(new_bet)

    return removed, added


def clear_all_bets(session: Session) -> list[Bet]:
    player = _ensure_session_player(session)
    removed: list[Bet] = []
    for bet in list(player.bets):
        if bet.is_removable(session.table):
            player.remove_bet(bet)
            removed.append(bet)
    return removed


def _clear_by_type(
    session: Session,
    bet_types: Tuple[type[Bet], ...],
) -> list[Bet]:
    player = _ensure_session_player(session)
    removed: list[Bet] = []
    for bet in list(player.bets):
        if type(bet) in bet_types and bet.is_removable(session.table):
            player.remove_bet(bet)
            removed.append(bet)
    return removed


def clear_center_bets(session: Session) -> list[Bet]:
    return _clear_by_type(session, _CENTER_ACTION_TYPES)


def clear_place_buy_lay(session: Session) -> list[Bet]:
    return _clear_by_type(session, _PLACE_BUY_LAY_TYPES)


def clear_ats(session: Session) -> list[Bet]:
    return _clear_by_type(session, _ATS_TYPES)


def clear_fire(session: Session) -> list[Bet]:
    return _clear_by_type(session, _FIRE_TYPES)


class BetManagementResult(Dict[str, Any]):
    """Typed dict-like result describing a bet management operation."""


def _session_snapshots(session: Session) -> Tuple[list[Dict[str, Any]], float]:
    player = _ensure_session_player(session)
    return _normalize_bets(player.bets), float(player.bankroll)


def apply_bet_management(
    session: Session,
    verb: str,
    args: Mapping[str, Any],
) -> BetManagementResult:
    before_bets, bankroll_before = _session_snapshots(session)
    result: BetManagementResult = BetManagementResult(
        result="ok",
        error_code=None,
        bets_before=before_bets,
        bets_after=before_bets,
        bankroll_before=bankroll_before,
        bankroll_after=bankroll_before,
        removed=[],
        added=[],
    )

    try:
        if verb == "remove_bet":
            bet_cls = _resolve_bet_type(args.get("type"))
            number_value = _coerce_optional_number(args.get("number"))
            removed = remove_bets_matching(
                session, bet_type=bet_cls, number=number_value
            )
            if not removed:
                raise ApiError(
                    ApiErrorCode.BAD_ARGS, "no matching removable bets found"
                )
            result["removed"] = removed

        elif verb == "reduce_bet":
            bet_cls = _resolve_bet_type(args.get("type"))
            number_value = _coerce_optional_number(args.get("number"))
            new_amount_raw = args.get("new_amount")
            if not isinstance(new_amount_raw, (int, float)):
                raise bad_args("new_amount must be numeric")
            new_amount = float(new_amount_raw)
            removed, added = set_bet_amount(
                session,
                bet_type=bet_cls,
                number=number_value,
                new_amount=new_amount,
            )
            if not removed and not added:
                # Nothing changed but the request is valid.
                result["removed"] = []
                result["added"] = []
            else:
                result["removed"] = removed
                result["added"] = added

        elif verb == "clear_all_bets":
            result["removed"] = clear_all_bets(session)
            if not result["removed"]:
                result["result"] = "ok"

        elif verb == "clear_center_bets":
            result["removed"] = clear_center_bets(session)

        elif verb == "clear_place_buy_lay":
            result["removed"] = clear_place_buy_lay(session)

        elif verb == "clear_ats_bets":
            result["removed"] = clear_ats(session)

        elif verb == "clear_fire_bets":
            result["removed"] = clear_fire(session)

        elif verb == "set_odds_working":
            base_value = args.get("base")
            bet_cls = _resolve_bet_type("odds")
            base_cls = _ODDS_BASES.get(str(base_value).lower()) if base_value else None
            if base_cls is None:
                raise bad_args("invalid odds base")
            number = _coerce_optional_number(args.get("number"))
            if number is None:
                raise bad_args("number must be provided for odds")
            working_value = args.get("working")
            if not isinstance(working_value, bool):
                raise bad_args("working must be a boolean")

            player = _ensure_session_player(session)
            updated: list[Bet] = []
            for bet in player.bets:
                if (
                    type(bet) is bet_cls
                    and bet.base_type is base_cls
                    and bet.number == number
                ):
                    bet.always_working = working_value
                    updated.append(bet)
            if not updated:
                raise ApiError(ApiErrorCode.BAD_ARGS, "no matching odds bets found")
            result["added"] = []
            result["removed"] = []

        else:  # pragma: no cover - defensive
            raise ApiError(
                ApiErrorCode.UNSUPPORTED_BET, f"verb '{verb}' not recognized"
            )

    except ApiError as exc:
        result["result"] = "error"
        result["error_code"] = (
            exc.code.value if isinstance(exc.code, ApiErrorCode) else str(exc.code)
        )
        result["error_hint"] = exc.hint
        # Do not alter bets if an ApiError was raised during processing.
        after_bets, bankroll_after = _session_snapshots(session)
        result["bets_after"] = after_bets
        result["bankroll_after"] = bankroll_after
        return result

    after_bets, bankroll_after = _session_snapshots(session)
    result["bets_after"] = after_bets
    result["bankroll_after"] = bankroll_after
    result["changed"] = (
        after_bets != before_bets or abs(bankroll_after - bankroll_before) > 1e-9
    )
    return result


def is_bet_placement_verb(verb: str) -> bool:
    return verb in _BET_PLACEMENT_VERBS


def is_bet_management_verb(verb: str) -> bool:
    return verb in _BET_MANAGEMENT_VERBS
