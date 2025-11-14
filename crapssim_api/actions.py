from __future__ import annotations

from functools import reduce
from typing import Any, Dict, Iterable, Mapping

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

SUPPORTED_VERBS = frozenset(
    list(_SIMPLE_AMOUNT_ONLY) + list(_NUMBER_REQUIRED) + ["odds", "hop"]
)


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
    if verb not in SUPPORTED_VERBS:
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
