#!/usr/bin/env python3
"""Download one package per aircraft and record exactly what is inside it.

Three package classes matter for repainting:

  AircraftSharedLiveryFiles  the complete texture set for an aircraft
  AircraftLivery             one livery; usually a delta on top of the shared set
  AircraftGenericLivery      the "Generic" livery, often metadata only

The per-livery packages are the honest answer to "which files does a repaint need to
supply": that package ships exactly the entries the official liveries override. Note that
many of them are 0-byte metadata-only updates, so `--pick largest` is the useful default.

    python tools/extract_liveries.py --type AircraftLivery --pick largest
    python tools/extract_liveries.py --type AircraftSharedLiveryFiles --pick smallest

Output: data/<slug>.json  (default: livery_files.json)
"""
from __future__ import annotations

import argparse
import json
import struct
import sys
import tempfile
import threading
import time
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "if-livery-pipeline/1.0"

DEFAULT_OUT = {
    "AircraftLivery": "livery_files.json",
    "AircraftSharedLiveryFiles": "shared_files.json",
    "AircraftGenericLivery": "generic_files.json",
}


def load_catalog(path: Path) -> list[dict]:
    cat = json.loads(path.read_text(encoding="utf-8"))
    return cat if isinstance(cat, list) else cat["data"]["packages"]


def repo_of(pkg: dict) -> str | None:
    parts = (pkg.get("packageKey") or "").split("/")
    return parts[1] if len(parts) > 1 else None


def meta(pkg: dict) -> dict:
    """Package metadata: the raw API calls it metadataJson, the trimmed snapshot calls it metadata."""
    raw = pkg.get("metadataJson") or pkg.get("metadata")
    if isinstance(raw, dict):
        return raw
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:  # noqa: BLE001
        return {}


def download(url: str, dest: Path, retries: int = 3) -> None:
    last: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, method="GET")
            req.add_header("User-Agent", UA)
            with urllib.request.urlopen(req, timeout=300) as resp, dest.open("wb") as fh:
                while True:
                    chunk = resp.read(1 << 20)
                    if not chunk:
                        break
                    fh.write(chunk)
            if dest.stat().st_size == 0:
                raise RuntimeError("empty file")
            return
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(2 * attempt)
    raise RuntimeError(f"download failed: {last}")


def image_size(blob: bytes) -> list[int] | None:
    if blob[:4] == b"RIFF" and blob[8:12] == b"WEBP":
        fourcc = blob[12:16]
        try:
            if fourcc == b"VP8X":
                return [int.from_bytes(blob[24:27], "little") + 1, int.from_bytes(blob[27:30], "little") + 1]
            if fourcc == b"VP8 ":
                return [int.from_bytes(blob[26:28], "little") & 0x3FFF, int.from_bytes(blob[28:30], "little") & 0x3FFF]
            if fourcc == b"VP8L":
                bits = int.from_bytes(blob[21:25], "little")
                return [(bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1]
        except Exception:  # noqa: BLE001
            return None
    if blob[:8] == b"\x89PNG\r\n\x1a\n":
        try:
            w, h = struct.unpack(">II", blob[16:24])
            return [w, h]
        except Exception:  # noqa: BLE001
            return None
    return None


def classify(name: str) -> str:
    low = name.lower()
    stem = low.rsplit(".", 1)[0]
    if stem.endswith("_albd"):
        return "albedo"
    if stem.endswith("_comp"):
        return "composite"
    if stem.endswith("_norm") or stem.endswith("_n"):
        return "normal"
    if stem.endswith("_emis") or stem.endswith("_e"):
        return "emissive"
    if stem.endswith("_orm"):
        return "orm"
    if "glass" in stem:
        return "glass"
    if "pilot" in stem:
        return "pilot"
    if any(k in stem for k in ("cockpit", "panel", "interior", "seat", "cabin", "display")):
        return "interior"
    return "surface"


def analyze(zip_path: Path) -> dict:
    files = []
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename.rsplit("/", 1)[-1]
            entry = {"name": name, "path": info.filename, "bytes": info.file_size, "kind": classify(name)}
            if name.lower().endswith((".webp", ".png")) and info.file_size < (1 << 26):
                try:
                    with zf.open(info) as fh:
                        entry["size"] = image_size(fh.read(64))
                except Exception:  # noqa: BLE001
                    pass
            files.append(entry)
    return {"files": files}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="inventory one package class per aircraft")
    parser.add_argument("--catalog", default=str(ROOT / "data" / "catalog.json"))
    parser.add_argument("--type", default="AircraftLivery",
                        choices=sorted(DEFAULT_OUT), help="package class to download")
    parser.add_argument("--pick", default="largest", choices=["largest", "smallest"],
                        help="which package of that class to download per aircraft")
    parser.add_argument("--out", default=None, help="output json (default derives from --type)")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--only", default="", help="comma-separated repo names to restrict to")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    out = Path(args.out or str(ROOT / "data" / DEFAULT_OUT[args.type]))
    packages = load_catalog(Path(args.catalog))

    picks: dict[str, dict] = {}
    for pkg in packages:
        if pkg.get("contentType") != args.type or not pkg.get("downloadUrl"):
            continue
        repo = repo_of(pkg) or "unknown"
        size = pkg.get("sizeBytes") or 0
        key = -size if args.pick == "largest" else size
        if repo not in picks or key < picks[repo]["key"]:
            picks[repo] = {"pkg": pkg, "key": key}

    existing: dict = {}
    if out.is_file() and not args.force:
        try:
            existing = json.loads(out.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            existing = {}
    todo = {k: v for k, v in picks.items() if k not in existing or not existing[k].get("files")}
    if args.only:
        wanted = {x.strip() for x in args.only.split(",") if x.strip()}
        todo = {k: v for k, v in todo.items() if k in wanted}
        print(f"restricted to {len(wanted)} aircraft", flush=True)
    print(f"{args.type}: aircraft {len(picks)} | cached {len(existing)} | pending {len(todo)} "
          f"({sum(v['pkg'].get('sizeBytes') or 0 for v in todo.values()) / 1048576:.1f} MB)", flush=True)

    tmp = Path(tempfile.gettempdir()) / "if-pkgs" / args.type
    tmp.mkdir(parents=True, exist_ok=True)
    results = dict(existing)
    lock = threading.Lock()
    done = 0

    def work(repo: str, pkg: dict) -> tuple[str, dict | None]:
        nonlocal done
        dest = tmp / f"{repo}.zip"
        try:
            download(pkg["downloadUrl"], dest)
            info = analyze(dest)
            m = meta(pkg)
            info["sample"] = {
                "name": m.get("name"),
                "path": m.get("path"),
                "packageVersion": pkg.get("version"),
                "sizeBytes": pkg.get("sizeBytes"),
                "contentType": pkg.get("contentType"),
            }
            try:
                dest.unlink()
            except OSError:
                pass
            with lock:
                done += 1
                print(f"[{done:>2}/{len(todo)}] {repo:42} files={len(info['files']):>3} "
                      f"{[f['name'] for f in info['files']][:3]}", flush=True)
            return repo, info
        except Exception as exc:  # noqa: BLE001
            with lock:
                done += 1
                print(f"[{done:>2}/{len(todo)}] FAIL {repo}: {exc}", flush=True)
            return repo, None

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(work, repo, v["pkg"]) for repo, v in todo.items()]
        for fut in as_completed(futures):
            repo, info = fut.result()
            if info:
                results[repo] = info
            out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"done: {len(results)} aircraft -> {out}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
