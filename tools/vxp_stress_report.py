import sys
import json
import time
import platform
import pathlib
import subprocess
import xml.etree.ElementTree as ET

OUTDIR = pathlib.Path("reports/vxp_stress")
OUTDIR.mkdir(parents=True, exist_ok=True)

JUNIT_SMOKE = OUTDIR / "junit_smoke.xml"
JUNIT_STRESS = OUTDIR / "junit_stress.xml"
LOG_SMOKE = OUTDIR / "smoke.log"
LOG_STRESS = OUTDIR / "stress.log"
SUMMARY_MD = OUTDIR / "summary.md"
SUMMARY_JSON = OUTDIR / "summary.json"


def parse_junit(path: pathlib.Path):
    if not path.exists():
        return {
            "tests": 0,
            "errors": 0,
            "failures": 0,
            "skipped": 0,
            "time": 0.0,
            "suites": [],
        }
    tree = ET.parse(path)
    root = tree.getroot()
    agg = {
        "tests": 0,
        "errors": 0,
        "failures": 0,
        "skipped": 0,
        "time": 0.0,
        "suites": [],
    }
    for ts in root.iter("testsuite"):
        suite = {
            "name": ts.attrib.get("name", ""),
            "tests": int(ts.attrib.get("tests", "0")),
            "errors": int(ts.attrib.get("errors", "0")),
            "failures": int(ts.attrib.get("failures", "0")),
            "skipped": int(ts.attrib.get("skipped", "0")),
            "time": float(ts.attrib.get("time", "0") or 0.0),
            "cases": [],
        }
        for tc in ts.iter("testcase"):
            case = {
                "classname": tc.attrib.get("classname", ""),
                "name": tc.attrib.get("name", ""),
                "time": float(tc.attrib.get("time", "0") or 0.0),
                "status": "passed",
            }
            for child in list(tc):
                tag = child.tag.lower()
                if tag in ("failure", "error", "skipped"):
                    case["status"] = tag
                    case["message"] = (child.attrib.get("message") or "").strip()
            suite["cases"].append(case)
        agg["tests"] += suite["tests"]
        agg["errors"] += suite["errors"]
        agg["failures"] += suite["failures"]
        agg["skipped"] += suite["skipped"]
        agg["time"] += suite["time"]
        agg["suites"].append(suite)
    return agg


def read_text(path: pathlib.Path, limit=200000):
    try:
        return path.read_text(errors="ignore")[:limit]
    except Exception:
        return ""


def get_git_info():
    def cmd(args):
        try:
            return (
                subprocess.check_output(args, stderr=subprocess.DEVNULL)
                .decode()
                .strip()
            )
        except Exception:
            return ""

    return {
        "commit": cmd(["git", "rev-parse", "HEAD"]),
        "branch": cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "dirty": bool(cmd(["git", "status", "--porcelain"])),
    }


def main():
    env = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "git": get_git_info(),
    }

    smoke = parse_junit(JUNIT_SMOKE)
    stress = parse_junit(JUNIT_STRESS)

    summary = {
        "environment": env,
        "smoke": smoke,
        "stress": stress,
        "artifacts": {
            "junit_smoke": str(JUNIT_SMOKE),
            "junit_stress": str(JUNIT_STRESS),
            "log_smoke": str(LOG_SMOKE),
            "log_stress": str(LOG_STRESS),
            "summary_md": str(SUMMARY_MD),
        },
        "notes": "Stress includes randomized multi-session torture test over varied commission policy settings.",
    }

    # Markdown summary
    md = []
    md.append("# CrapsSim-Vanilla Expansion — Stress Test Summary\n")
    md.append(f"- Timestamp: {env['timestamp']}")
    md.append(f"- Python: {env['python']}")
    md.append(f"- Platform: {env['platform']}")
    if env["git"]["commit"]:
        md.append(
            f"- Git: {env['git']['branch']} @ {env['git']['commit']}{' (dirty)' if env['git']['dirty'] else ''}"
        )
    md.append("\n## Smoke (default test run)\n")
    md.append(
        f"- Tests: {smoke['tests']}  | Failures: {smoke['failures']}  | Errors: {smoke['errors']}  | Skipped: {smoke['skipped']}  | Time: {smoke['time']:.2f}s"
    )
    md.append("\n## Stress (@stress marker)\n")
    md.append(
        f"- Tests: {stress['tests']}  | Failures: {stress['failures']}  | Errors: {stress['errors']}  | Skipped: {stress['skipped']}  | Time: {stress['time']:.2f}s"
    )
    md.append("\n### Slowest Stress Cases (top 15)\n")
    cases = []
    for s in stress["suites"]:
        for c in s["cases"]:
            cases.append(
                (c["time"], f"{c['classname']}::{c['name']}  —  {c['status']}")
            )
    cases.sort(reverse=True)
    for t, label in cases[:15]:
        md.append(f"- {t:.3f}s  {label}")
    md.append("\n### Artifacts\n")
    for k, v in summary["artifacts"].items():
        md.append(f"- **{k}**: `{v}`")
    md_text = "\n".join(md)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_MD.write_text(md_text)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
