from __future__ import annotations

import json
import os

from crapssim_api.http import get_capabilities, start_session


OUTDIR = "reports/baseline"
os.makedirs(OUTDIR, exist_ok=True)


def dump(name: str, obj: dict):
    path = os.path.join(OUTDIR, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    print(f"Wrote {path} ({os.path.getsize(path)} bytes)")
    return path


def main():
    print("== GET /capabilities ==")
    cap = get_capabilities().body.decode()
    cap_data = json.loads(cap)
    dump("capabilities", cap_data)

    print("\n== POST /start_session (default) ==")
    spec_default = {"table_profile": "vanilla-default", "enabled_buylay": True}
    sess_default = start_session({"spec": spec_default, "seed": 42}).body.decode()
    dump("start_session.default", json.loads(sess_default))

    print("\n== POST /start_session (buylay disabled) ==")
    spec_disabled = {"enabled_buylay": False}
    sess_disabled = start_session({"spec": spec_disabled, "seed": 42}).body.decode()
    dump("start_session.disabled_buylay", json.loads(sess_disabled))


if __name__ == "__main__":
    main()
