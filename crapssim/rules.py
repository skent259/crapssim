"""Rule variants and shared rule behavior for the craps table engine."""

from __future__ import annotations

from abc import ABC
from typing import Protocol


class Rules(Protocol):
    """Protocol for game-rule variants used by the table engine."""

    def point_numbers(self) -> list[int]:
        """Return all numbers that can become a table point."""
        ...

    def come_out_winners(self) -> list[int]:
        """Return come-out roll totals that win for pass/come-style bets."""
        ...

    def come_out_losers(self) -> list[int]:
        """Return come-out roll totals that lose for pass/come-style bets."""
        ...

    def point_winners(self, point: int | None) -> list[int]:
        """Return winning totals while a point is established.

        Args:
            point: Current point number, or None when point is off.
        """
        ...

    def point_losers(self, point: int | None) -> list[int]:
        """Return losing totals while a point is established.

        Args:
            point: Current point number, or None when point is off.
        """
        ...

    def allow_dont_pass(self) -> bool:
        """Return True when Dont Pass bets are allowed for this ruleset."""
        ...

    def allow_dont_come(self) -> bool:
        """Return True when Dont Come bets are allowed for this ruleset."""
        ...


class AbstractRules(ABC):
    """Shared default behaviors for craps rule variants."""

    def point_numbers(self) -> list[int]:
        """Return point numbers for the ruleset.

        Returns:
            list[int]: Empty list by default; subclasses define concrete values.
        """
        return []

    def point_winners(self, point: int | None) -> list[int]:
        """Return winning totals after a point is established.

        Args:
            point: Current point number, or None when point is off.

        Returns:
            list[int]: The current point number when set, otherwise an empty list.
        """
        if point is None:
            return []
        return [point]

    def point_losers(self, point: int | None) -> list[int]:
        """Return losing totals after a point is established.

        Args:
            point: Current point number, or None when point is off.

        Returns:
            list[int]: Seven, the default point-out total.
        """
        return [7]

    def allow_dont_pass(self) -> bool:
        """Return whether Dont Pass bets are legal in this ruleset."""
        return True

    def allow_dont_come(self) -> bool:
        """Return whether Dont Come bets are legal in this ruleset."""
        return True


class ClassicRules(AbstractRules):
    """Traditional craps rules.

    Uses six point numbers (4, 5, 6, 8, 9, and 10) and standard come-out outcomes.
    """

    def point_numbers(self) -> list[int]:
        """Return standard point numbers used in classic craps.

        Returns:
            list[int]: Valid point numbers: 4, 5, 6, 8, 9, and 10."""
        return [4, 5, 6, 8, 9, 10]

    def come_out_winners(self) -> list[int]:
        """Return classic pass-line winners on the come-out roll.

        Returns:
            list[int]: 7 and 11, the classic come-out winners.
        """
        return [7, 11]

    def come_out_losers(self) -> list[int]:
        """Return classic pass-line losers on the come-out roll.

        Returns:
            list[int]: 2, 3, and 12, the classic come-out losers.
        """
        return [2, 3, 12]


class CraplessRules(AbstractRules):
    """Crapless craps rules.

    In this variant, 2, 3, 11 and 12 are treated as points rather than immediate losses
    for the pass line and come family bets.
    """

    def point_numbers(self) -> list[int]:
        """Return Crapless point numbers, including 2, 3, 11, and 12.

        Returns:
            list[int]: Valid point numbers: 2, 3, 4, 5, 6, 8, 9, 10, 11, and 12.
        """
        return [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]

    def come_out_winners(self) -> list[int]:
        """Return come-out winners for Crapless rules.

        Returns:
            list[int]: 7, the only come-out winner in Crapless craps."""
        return [7]

    def come_out_losers(self) -> list[int]:
        """Return come-out losers for Crapless rules.

        Returns:
            list[int]: No come-out losers in Crapless craps.
        """
        return []

    def allow_dont_pass(self) -> bool:
        """Return False because Don't Pass is not supported in Crapless rules."""
        return False

    def allow_dont_come(self) -> bool:
        """Return False because Dont Come is not supported in Crapless rules."""
        return False
