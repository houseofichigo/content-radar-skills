#!/usr/bin/env python3
"""Validate every Content Radar skill and its distributions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import build_dist  # noqa: E402
import skill_rules as sr  # noqa: E402

DEFAULT_TARGET = "all"


def run(target: str = DEFAULT_TARGET) -> dict:
    findings = []
    discovered = sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md"))
    expected = sorted(build_dist.SKILL_NAMES)
    if discovered != expected:
        findings.append(("blocker", "skill_set", f"Expected {expected}, found {discovered}", "skills/"))
    for root in build_dist.skill_roots():
        if not (root / "SKILL.md").is_file():
            continue
        _, skill_findings = sr.validate_skill_dir(root, target)
        findings.extend((sev, code, msg, f"skills/{root.name}/{path or ''}") for sev, code, msg, path in skill_findings)
    for diff in build_dist.check_all():
        findings.append(("blocker", "dist_out_of_sync", diff, "dist/"))
    if not (ROOT / "LICENSE").is_file():
        findings.append(("blocker", "missing_license", "Repository LICENSE is missing", "LICENSE"))
    status = "fail" if any(item[0] == "blocker" for item in findings) else "pass"
    return {"status": status, "target": sr.normalize_target(target), "skills": expected, "findings": findings}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=DEFAULT_TARGET)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = run(args.target)
    if args.json:
        output = dict(result)
        output["findings"] = [dict(zip(("severity", "code", "message", "path"), item)) for item in result["findings"]]
        print(json.dumps(output, indent=2))
    else:
        print(f"{result['status'].upper()}: {len(result['skills'])} skills (target: {result['target']})")
        if result["findings"]:
            print(sr.format_findings(result["findings"]))
    return 0 if result["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
