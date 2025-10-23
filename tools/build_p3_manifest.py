#!/usr/bin/env python3
import json, hashlib, pathlib, xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = pathlib.Path(".")
BASE = ROOT / "baselines" / "phase3"
BASE.mkdir(parents=True, exist_ok=True)

def parse_junit(path: pathlib.Path):
    tree = ET.parse(str(path))
    root = tree.getroot()
    # supports both <testsuite> and <testsuites>
    if root.tag == "testsuite":
        suites = [root]
    else:
        suites = list(root.iter("testsuite"))
    total = sum(int(s.attrib.get("tests", 0)) for s in suites)
    failures = sum(int(s.attrib.get("failures", 0)) for s in suites)
    errors = sum(int(s.attrib.get("errors", 0)) for s in suites)
    skipped = sum(int(s.attrib.get("skipped", 0)) for s in suites)
    passed = total - failures - errors - skipped
    return {"total": total, "passed": passed, "failed": failures + errors, "skipped": skipped}

runs = []
for i in (1,2,3):
    runs.append(parse_junit(BASE / f"junit_run{i}.xml"))

# Combine: require identical totals across runs
identical = all(runs[i] == runs[0] for i in range(1, len(runs)))

# Hash raw text reports to check byte-identical output
def sha(path: pathlib.Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

hashes = [sha(BASE / f"test_report_run{i}.txt") for i in (1,2,3)]
hash_identical = (hashes[0] == hashes[1] == hashes[2])

summary = {
    "runs": runs,
    "determinism_checks": {
        "junit_identical": identical,
        "text_hashes_identical": hash_identical,
        "text_hashes": hashes,
    }
}

# Manually set schema versions if available; otherwise default
cap_schema = "1.0"
err_schema = "1.0"

manifest = {
    "api_phase": "3",
    "tag": "v0.3.0-api-p3",
    "schema": {
        "capabilities_version": cap_schema,
        "error_schema_version": err_schema
    },
    "tests": {
        "total": runs[0]["total"],
        "passed": runs[0]["passed"],
        "failed": runs[0]["failed"],
        "skipped": runs[0]["skipped"]
    },
    "determinism": summary["determinism_checks"],
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")
}

(BASE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps(manifest, indent=2))
