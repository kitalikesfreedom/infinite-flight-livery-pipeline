#!/usr/bin/env python3
"""Offline self-test: entry-name and dimension behaviour of the packager, plus docs links.

Touches no device and makes no network calls. Run locally or in CI:

    python tools/selftest.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
PY = sys.executable

# Placeholder directory name used by the tests; it points at no real airline.
TEST_DIR = "Test Livery Directory"

failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    print(f"[{'ok  ' if condition else 'FAIL'}] {name}{(' - ' + detail) if detail and not condition else ''}")
    if not condition:
        failures.append(name)


def dry_run(*args: str) -> list[str]:
    proc = subprocess.run(
        [PY, str(TOOLS / "build_slip_package.py"), *args, "--dry-run"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise SystemExit(f"build_slip_package.py failed: {proc.stderr or proc.stdout}")
    return json.loads(proc.stdout)["entries"]


def main() -> int:
    android = dry_run(
        "--platform", "android",
        "--aircraft-repo", "infiniteflight-aircraft-a320",
        "--livery-dir", TEST_DIR,
        "--tint", "FF00FF",
        "--texture", "Texture.webp",
        "--fill-orm", "--fill-normal",
        "--out", "unused.zip",
    )
    check("android prefix starts with ../../files", all(e.startswith("../../files/") for e in android), str(android))
    check("android path lands in aircraft/<repo>/liveries/<dir>/",
          all(f"/aircraft/infiniteflight-aircraft-a320/liveries/{TEST_DIR}/" in e for e in android), str(android))
    check("legacy aircraft get all three files (baseColor + ORM + normal)",
          {e.rsplit("/", 1)[-1] for e in android} == {"Texture.webp", "Texture_ORM.webp", "Texture_N.webp"}, str(android))
    check("entry names contain no backslashes", not any("\\" in e for e in android), str(android))

    ios = dry_run(
        "--platform", "ios",
        "--aircraft-repo", "infiniteflight-aircraft-b789",
        "--livery-dir", TEST_DIR,
        "--tint", "00FF00",
        "--texture", "Texture.webp",
        "--out", "unused.zip",
    )
    check("ios prefix starts with ../../Library/dlc",
          ios and all(e.startswith("../../Library/dlc/aircraft/") for e in ios), str(ios))

    # neo aircraft default to 4096; an explicit --size still wins, guarded by the dimension check
    mismatch = subprocess.run(
        [PY, str(TOOLS / "build_slip_package.py"),
         "--platform", "android",
         "--aircraft-repo", "infiniteflight-aircraft-a21n",
         "--livery-dir", TEST_DIR,
         "--tint", "112233",
         "--size", "2048x2048",
         "--texture", "M_Fuselage_01_albd.webp",
         "--out", "unused.zip", "--dry-run"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    check("--size overrides the per-aircraft default", mismatch.returncode == 0, mismatch.stderr)

    # relative documentation links across README translations, docs/ and docs/models/
    broken = []
    for md in ROOT.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for target in re.findall(r"\]\((?!https?://|#)([^)#]+)", text):
            if not (md.parent / target).resolve().exists():
                broken.append(f"{md.relative_to(ROOT)} -> {target}")
    check("documentation relative links resolve", not broken, "; ".join(broken[:6]))

    for name in ("README.md", "README.ja.md", "README.zh-Hant.md"):
        check(f"{name} present", (ROOT / name).is_file())

    index_path = ROOT / "data" / "models_index.json"
    if index_path.is_file():
        aircraft = json.loads(index_path.read_text(encoding="utf-8"))
        pages = {p.stem for p in (ROOT / "docs" / "models").glob("*.md")}
        missing = [r for r in aircraft if r.replace("infiniteflight-aircraft-", "") not in pages]
        check("every aircraft has a documentation page", not missing, ", ".join(missing[:6]))
        check("aircraft index page present", (ROOT / "docs" / "models" / "index.md").is_file())
        # each page must carry a packaging command for its own repository
        bad = []
        for repo in list(aircraft)[:8]:
            page = ROOT / "docs" / "models" / f"{repo.replace('infiniteflight-aircraft-', '')}.md"
            if page.is_file() and f"--aircraft-repo {repo}" not in page.read_text(encoding="utf-8"):
                bad.append(repo)
        check("aircraft pages carry a runnable packaging command", not bad, ", ".join(bad))
    else:
        check("data/models_index.json present", False)

    demo = ROOT / "examples" / "a320-demo" / "a320-demo.zip"
    if demo.is_file():
        with zipfile.ZipFile(demo) as bundle:
            names = bundle.namelist()
        check("example package contains webp entries only", all(n.endswith(".webp") for n in names), str(names))
        check("example package entries traverse into files/", all(n.startswith("../../files/") for n in names), str(names))
    else:
        check("example package present", False, str(demo))

    # no CJK text outside the documented translation files. Language-switcher labels are
    # stripped first, since they are written in their own script by design.
    # Written as escapes so this file stays pure ASCII.
    cjk_allowed = {
        "docs/preface.md", "README.ja.md", "README.zh-Hant.md",
    }
    labels = ("\u65e5\u672c\u8a9e", "\u7e41\u9ad4\u4e2d\u6587", "\u7b80\u4f53\u4e2d\u6587", "\u4e2d\u6587")
    cjk = re.compile(r"[\u4e00-\u9fff]")
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix in {".zip", ".png", ".webp"}:
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if rel in cjk_allowed or rel.startswith("data/") or rel.startswith("docs/models/"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for label in labels:
            text = text.replace(label, "")
        if cjk.search(text):
            offenders.append(rel)
    check("no CJK outside the translation files", not offenders, ", ".join(offenders[:8]))

    # nothing that could trace this repository back to a machine or a person.
    # Single-character classes keep the literal terms out of this file itself.
    trace_patterns = {
        r"[A-Za-z]:\\\\?Users": "a local user path",
        r"\bh[u]tao\b": "a local username",
        r"deepseek[-_ ]?harness|defaul[t]-workspace": "a workspace folder name",
        r"23117RK6[6]C|Redm[i]|HyperO[S]": "a device model",
        r"\bman[e]t\b|e85d75[c]\b": "an adb serial or codename",
        r"[A-Za-z]:\\\\?[^\"\n]*\\\\?Temp": "a temp directory path",
    }
    traced = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix in {".zip", ".png", ".webp"}:
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if rel.startswith("data/") or rel == "tools/selftest.py":
            continue  # vendor catalog data, and this file's own pattern table
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern, label in trace_patterns.items():
            if re.search(pattern, text, re.I):
                traced.append(f"{rel} ({label})")
                break
    check("no local paths or device identifiers", not traced, ", ".join(traced[:6]))

    # archives must not carry build timestamps
    if demo.is_file():
        with zipfile.ZipFile(demo) as bundle:
            stamps = {info.date_time for info in bundle.infolist()}
        check("example package uses a fixed timestamp", stamps == {(1980, 1, 1, 0, 0, 0)}, str(stamps))

    print()
    if failures:
        print(f"{len(failures)} check(s) failed: " + " | ".join(failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
