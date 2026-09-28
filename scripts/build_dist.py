#!/usr/bin/env python3
"""Build deterministic per-skill ZIPs and the aggregate suite bundle."""

from __future__ import annotations

import argparse
import os
import stat
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import skill_rules as sr  # noqa: E402

SKILL_NAMES = (
    "competitor-scan",
    "content-ideas",
    "content-radar",
    "content-radar-setup",
    "newsjacking",
    "seo-aeo-geo",
    "trend-radar",
)
SUITE_NAME = "content-radar-skills"


def skill_roots() -> list[Path]:
    return [ROOT / "skills" / name for name in SKILL_NAMES]


def _write_file(zf: zipfile.ZipFile, arcname: str, path: Path) -> None:
    info = zipfile.ZipInfo(arcname, date_time=sr.ZIP_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | sr._mode(path)) << 16
    zf.writestr(info, path.read_bytes())


def build_bundle(out: Path) -> list[str]:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    written: list[str] = []
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root in skill_roots():
            for rel, path in sr.payload_files(root):
                arcname = f"{SUITE_NAME}/skills/{root.name}/{rel}"
                _write_file(zf, arcname, path)
                written.append(arcname)
        for path in sorted((ROOT / "resources").rglob("*")):
            if path.is_file():
                rel = path.relative_to(ROOT / "resources").as_posix()
                arcname = f"{SUITE_NAME}/resources/{rel}"
                _write_file(zf, arcname, path)
                written.append(arcname)
    os.replace(tmp, out)
    return written


def build_all(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for root in skill_roots():
        sr.build_zip(root, out_dir / f"{root.name}.zip", root.name)
    build_bundle(out_dir / f"{SUITE_NAME}.zip")


def check_all() -> list[str]:
    diffs: list[str] = []
    for root in skill_roots():
        for diff in sr.compare_zip(root, ROOT / "dist" / f"{root.name}.zip", root.name):
            diffs.append(f"{root.name}: {diff}")
    with tempfile.TemporaryDirectory(prefix="content-radar-dist-") as temp:
        expected = Path(temp)
        build_all(expected)
        for name in [*(f"{n}.zip" for n in SKILL_NAMES), f"{SUITE_NAME}.zip"]:
            actual = ROOT / "dist" / name
            if not actual.is_file():
                diffs.append(f"missing distribution: dist/{name}")
            elif actual.read_bytes() != (expected / name).read_bytes():
                diffs.append(f"distribution differs: dist/{name}")
    return sorted(set(diffs))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.check:
        diffs = check_all()
        if diffs:
            print("Distributions are out of date:")
            print("\n".join(f"- {diff}" for diff in diffs))
            return 1
        print("All distributions are up to date")
        return 0
    build_all(ROOT / "dist")
    print(f"Built {len(SKILL_NAMES)} skill ZIPs and dist/{SUITE_NAME}.zip")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
