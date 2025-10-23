#!/usr/bin/env python3
import json, hashlib, pathlib, xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = pathlib.Path(".")
BASE = ROOT / "baselines" / "phase4"
BASE.mkdir(parents=True, exist_ok=True)

def parse_junit(path: pathlib.Path):
    tree = ET.parse(str(path))
    root = tree.getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    total = sum(int(s.attrib.get("tests", 0)) for s in suites)
    failures = sum(int(s.attrib.get("failures", 0)) for s in suites)
    errors = sum(int(s.attrib.get("errors", 0)) for s in suites)
    skipped = sum(int(s.attrib.get("skipped", 0)) for s in suites)
    passed = total - failures - errors - skipped
    return {"total": total, "passed": passed, "failed": failures + errors, "skipped": skipped}

def sha(path: pathlib.Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

runs = [parse_junit(BASE / f"junit_run{i}.xml") for i in (1,2,3)]
identical_runs = all(r == runs[0] for r in runs[1:])
hashes = [sha(BASE / f"test_report_run{i}.txt") for i in (1,2,3)]
identical_hashes = (hashes[0] == hashes[1] == hashes[2])

manifest = {
    "api_phase": "4",
    "tag": "v0.4.0-api-p4",
    "tests": runs[0],
    "determinism": {
        "identical_runs": identical_runs,
        "identical_text_hashes": identical_hashes,
        "text_hashes": hashes
    },
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")
}

(BASE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps(manifest, indent=2))
