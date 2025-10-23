from __future__ import annotations

import hashlib
import json
import os

from crapssim_api.http import start_session
from crapssim_api.version import CAPABILITIES_SCHEMA_VERSION, ENGINE_API_VERSION


OUTDIR = "reports/baseline"
os.makedirs(OUTDIR, exist_ok=True)
SEED = 123456


resp = start_session({"spec": {"enabled_buylay": True}, "seed": SEED}).body.decode()
data = json.loads(resp)
identity = data["snapshot"]["identity"]
caps = data["snapshot"]["capabilities"]

blob = json.dumps({"identity": identity, "capabilities": caps}, sort_keys=True)
finger = hashlib.sha256(blob.encode()).hexdigest()

with open(os.path.join(OUTDIR, "fingerprint.txt"), "w", encoding="utf-8") as f:
    f.write(
        f"seed={SEED}\n"
        f"engine_api.version={ENGINE_API_VERSION}\n"
        f"capabilities.schema_version={CAPABILITIES_SCHEMA_VERSION}\n"
        f"fingerprint={finger}\n"
    )


print("Fingerprint:", finger)
