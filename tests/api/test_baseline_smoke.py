from __future__ import annotations

import json
from subprocess import run

from crapssim_api import version
from crapssim_api.http import get_capabilities, start_session


def test_version_tag():
    assert version.ENGINE_API_VERSION.endswith("-api.p2")


def test_capabilities_contains_core_keys():
    body = json.loads(get_capabilities().body.decode())
    caps = body["capabilities"]
    assert isinstance(caps["schema_version"], int)
    for key in ["bets", "increments", "commission"]:
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
