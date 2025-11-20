## Phase 2 — Compatibility & Semantics

This phase introduces Python 3.11–3.13 compatibility, dependency cleanup,
and correct API-side push detection without introducing any game logic.

The API now reflects engine push outcomes either through explicit engine signals
or through lifecycle-based detection logic. No rules are inferred and the engine
remains the authoritative source of truth.

Error handling has also been aligned with CrapsSim v4.0 semantics, ensuring all
API error codes faithfully mirror core engine behavior.
