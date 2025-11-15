# CrapsSim HTTP API — Errors and Contract

This document describes the high-level error contract for the HTTP API and the meaning of the `ApiErrorCode` values returned from endpoints.

The concrete definitions live in `crapssim_api.errors.ApiErrorCode`. This file is a human-friendly summary of what clients should expect.

---

## 1. Error envelope

Most write endpoints (such as `/session/apply_action` and `/session/roll`) respond with a JSON document that may contain:

- the primary payload (session, roll, hand, bankroll, etc.)
- an `errors` list, where each entry includes:
  - a machine-readable `code`
  - a human-readable `message`
  - optional `details` or `field` information

Example shape:

```json
{
  "session_id": "session-uuid-or-token",
  "effects": [],
  "errors": [
    {
      "code": "ILLEGAL_BET",
      "message": "Bet amount does not match table increment rules.",
      "details": {
        "bet": "Place6",
        "amount": 7
      }
    }
  ]
}

Clients should treat the code as the primary discriminator and the message as a human-facing aid.

⸻

2. Common error codes

The exact enum values are defined in crapssim_api.errors.ApiErrorCode. Typical codes include (but are not limited to):

INVALID_ARGS
•Meaning: The request body or query parameters do not match the expected schema.
•Typical causes:
•missing required fields
•wrong types (string where an integer was expected)
•invalid enum values for fields such as bet or type
•Client action: Treat this as a client bug; fix the request formation before retrying.

⸻

UNKNOWN_SESSION
•Meaning: The server does not recognize the supplied session_id.
•Typical causes:
•typo in the session identifier
•client reusing an expired or never-created session
•Client action: Start a new session or correct the session_id value.

⸻

ILLEGAL_BET
•Meaning: The requested bet is not legal under the current table rules.
•Typical causes:
•wrong increment (e.g., $7 on Place 6/8 instead of a $6 multiple)
•bet type not supported by the underlying engine
•bet not allowed in the current phase (e.g., certain bets on the come-out)
•Client action: Validate bet types and increments against /capabilities before sending, or adjust UI constraints.

⸻

INSUFFICIENT_FUNDS
•Meaning: The player’s bankroll is too low to cover the requested bet.
•Typical causes:
•attempting to place a bet exceeding the current bankroll
•stacking multiple bets that together exceed remaining funds
•Client action: Reduce bet size or adjust strategy; this reflects game rules rather than server failure.

⸻

BAD_TIMING
•Meaning: The requested action is not allowed at this point in the hand or roll cycle.
•Typical causes:
•attempting to place or remove a bet outside its legal window
•trying to roll when no session is active
•Client action: Ensure that actions are aligned with the hand/roll state as reported by the API (e.g., phase, point, hand index).

⸻

INTERNAL_ERROR
•Meaning: An unexpected server-side exception occurred.
•Typical causes:
•bugs in the HTTP layer
•unhandled edge cases in the engine or adapters
•Client action: Treat as a server fault. Log details and consider retrying once. Do not attempt to guess a recovery strategy.

⸻

3. HTTP status codes

The HTTP layer strives to use conventional status codes:
•200 / 201 — request accepted and processed (even if some actions in the payload failed, in which case errors will be populated)
•400 — malformed request (INVALID_ARGS and similar input problems)
•404 — unknown path or UNKNOWN_SESSION depending on endpoint
•500 — unhandled server exceptions (INTERNAL_ERROR)

The response body should always be JSON for API routes, even in error cases.

⸻

4. Client expectations

Clients integrating with this API should:
1.Prefer checking errors in the response over attempting to infer failure from the HTTP status alone.
2.Use /capabilities to pre-validate bet types, increments, and supported features.
3.Treat INVALID_ARGS and related codes as code-level bugs to fix, not retry conditions.
4.Treat INTERNAL_ERROR and 5xx responses as temporary failures (log and optionally retry).

⸻

5. Backward compatibility

The error codes are designed to be:
•stable across minor versions
•extensible: new codes may be added in future versions, but existing codes should not change meaning

The engine and API version metadata (see crapssim_api.version) can be used to:
•detect when new codes or behaviors may be available
•gate client-side feature usage accordingly

---
