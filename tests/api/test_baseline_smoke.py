from __future__ import annotations

import json
from subprocess import run

from crapssim_api.http import get_capabilities, start_session


def test_engine_version_tag():
    from crapssim_api import version as version
    v = version.ENGINE_API_VERSION
    # Accept both Phase 2 and Phase 3 tags for cross-compatibility
    suffixes = (
        "-api.p2",
        "-api-p2",
        "-api.p3",
        "-api-p3",
        "-api-p3-sync",
        "-api-p4",
    )
    assert any(v.endswith(s) for s in suffixes), f"unexpected tag {v}"


def test_capabilities_contains_core_keys():
    body = json.loads(get_capabilities().body.decode())
    caps = body["capabilities"]
    assert isinstance(caps["schema_version"], int)
    for key in ["bets", "increments", "vig"]:
        assert key in caps


def test_start_session_echoes_profile_and_seed():
    req = {"spec": {"table_profile": "vanilla-default"}, "seed": 99}
    body = json.loads(start_session(req).body.decode())
    ident = body["snapshot"]["identity"]
    assert ident["table_profile"] == "vanilla-default"
    assert ident["seed"] == 99


def test_fingerprint_script_runs(tmp_path):
    r = run(["python", "tools/api_fingerprint.py"], capture_output=True, text=True)
    assert "fingerprint" in r.stdout.lower() or r.returncode == 0
