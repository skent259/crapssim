from __future__ import annotations

from crapssim_api.determinism import DeterminismHarness, compute_hash


def _exercise(h: DeterminismHarness) -> None:
    # Deterministic series of calls
    for _ in range(5):
        h.randint(1, 6)
    h.choice([4, 5, 6, 8, 9, 10])
    for _ in range(3):
        h.randint(1, 6)


def test_same_seed_same_tape():
    h1 = DeterminismHarness(seed=123)
    h2 = DeterminismHarness(seed=123)
    _exercise(h1); _exercise(h2)
    t1 = h1.export_tape(); t2 = h2.export_tape()
    assert t1["entries"] == t2["entries"]
    assert t1["run_hash"] == t2["run_hash"]
    assert t1["seed"] == 123 and t2["seed"] == 123


def test_mismatch_detected():
    h1 = DeterminismHarness(seed=321)
    h2 = DeterminismHarness(seed=321)
    _exercise(h1)
    # introduce a divergence
    h2.randint(1, 6)
    _exercise(h2)
    t1 = h1.export_tape(); t2 = h2.export_tape()
    assert t1["run_hash"] != t2["run_hash"]


def test_replay_works():
    h = DeterminismHarness(seed=777)
    _exercise(h)
    tape = h.export_tape()
    # Should not raise
    DeterminismHarness(seed=None).replay_tape(tape)
    # Hash should be stable
    assert tape["run_hash"] == compute_hash({"seed": tape["seed"], "entries": tape["entries"]})
