#!/usr/bin/env python3
"""Download every aircraft model package and mine its glTF for texture references.

This is what makes `docs/models/*.md` verifiable: for each aircraft it records every
`images[].uri` in the model's glTF files, which material/slot uses it, and — crucially —
which of them are `baseColorTexture` entries (the ones a repaint can touch).

Requires a catalog dump first:

    python tools/fetch_catalog.py --dump-json data/catalog.json
    python tools/extract_models.py            # all pending aircraft
    python tools/extract_models.py --limit 3  # smoke test

Output: data/model_textures.json
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


def load_catalog(path: Path) -> list[dict]:
    cat = json.loads(path.read_text(encoding="utf-8"))
    return cat if isinstance(cat, list) else cat["data"]["packages"]


def repo_of(pkg: dict) -> str | None:
    parts = (pkg.get("packageKey") or "").split("/")
    return parts[1] if len(parts) > 1 else None


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
            time.sleep(3 * attempt)
    raise RuntimeError(f"download failed: {last}")


def glb_json(blob: bytes) -> dict | None:
    if len(blob) < 20 or blob[:4] != b"glTF":
        return None
    offset = 12
    while offset + 8 <= len(blob):
        length, ctype = struct.unpack_from("<II", blob, offset)
        offset += 8
        chunk = blob[offset : offset + length]
        offset += length
        if ctype == 0x4E4F534A:  # 'JSON'
            return json.loads(chunk.decode("utf-8"))
    return None


def analyze(zip_path: Path) -> dict:
    result: dict = {"gltf": [], "images": [], "baseColor": [], "materials": []}
    with zipfile.ZipFile(zip_path) as zf:
        images: dict[str, set[str]] = {}
        base_colors: set[str] = set()
        materials: list[dict] = []
        for name in zf.namelist():
            low = name.lower()
            if not low.endswith((".gltf", ".glb")):
                continue
            try:
                blob = zf.read(name)
            except Exception:  # noqa: BLE001
                continue
            try:
                doc = json.loads(blob.decode("utf-8")) if low.endswith(".gltf") else glb_json(blob)
            except Exception:  # noqa: BLE001
                doc = None
            if not doc:
                continue
            result["gltf"].append(name)
            img_list = doc.get("images") or []
            tex_list = doc.get("textures") or []
            for mat in doc.get("materials") or []:
                pbr = mat.get("pbrMetallicRoughness") or {}
                refs = []
                for slot, tex in (
                    ("baseColor", pbr.get("baseColorTexture")),
                    ("metallicRoughness", pbr.get("metallicRoughnessTexture")),
                    ("normal", mat.get("normalTexture")),
                    ("emissive", mat.get("emissiveTexture")),
                    ("occlusion", mat.get("occlusionTexture")),
                ):
                    if not isinstance(tex, dict):
                        continue
                    idx = tex.get("index")
                    if idx is None or idx >= len(tex_list):
                        continue
                    src = (tex_list[idx] or {}).get("source")
                    if src is None or src >= len(img_list):
                        continue
                    uri = (img_list[src] or {}).get("uri")
                    if not uri:
                        continue
                    fname = uri.rsplit("/", 1)[-1]
                    refs.append({"slot": slot, "name": fname, "uri": uri})
                    images.setdefault(fname, set()).add(f"{mat.get('name') or '?'} ({slot})")
                    if slot == "baseColor":
                        base_colors.add(fname)
                if refs:
                    materials.append({"name": mat.get("name"), "refs": refs})
            for img in img_list:
                uri = (img or {}).get("uri")
                if uri:
                    images.setdefault(uri.rsplit("/", 1)[-1], set())
        result["images"] = [{"uri": n, "usedBy": sorted(r)} for n, r in sorted(images.items())]
        result["baseColor"] = sorted(base_colors)
        result["materials"] = materials[:250]
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="mine glTF texture references per aircraft")
    parser.add_argument("--catalog", default=str(ROOT / "data" / "catalog.json"))
    parser.add_argument("--out", default=str(ROOT / "data" / "model_textures.json"))
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--limit", type=int, default=0, help="process only N pending aircraft")
    parser.add_argument("--force", action="store_true", help="re-parse aircraft already present")
    args = parser.parse_args(argv)

    packages = load_catalog(Path(args.catalog))
    models: dict[str, tuple[str, int]] = {}
    for pkg in packages:
        if pkg.get("contentType") != "AircraftModel":
            continue
        repo = repo_of(pkg)
        if repo and pkg.get("downloadUrl"):
            models[repo] = (pkg["downloadUrl"], pkg.get("sizeBytes") or 0)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    existing: dict = {}
    if out.is_file() and not args.force:
        try:
            existing = json.loads(out.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            existing = {}

    todo = {k: v for k, v in models.items() if k not in existing or not existing[k].get("images")}
    if args.limit:
        todo = dict(list(todo.items())[: args.limit])

    print(f"aircraft {len(models)} | cached {len(existing)} | pending {len(todo)} "
          f"({sum(v[1] for v in todo.values()) / 1048576:.1f} MB)", flush=True)

    tmp = Path(tempfile.gettempdir()) / "if-models"
    tmp.mkdir(parents=True, exist_ok=True)
    results = dict(existing)
    lock = threading.Lock()
    done = 0

    def work(repo: str, url: str, size: int) -> tuple[str, dict | None]:
        nonlocal done
        dest = tmp / f"{repo}.zip"
        try:
            download(url, dest)
            info = analyze(dest)
            info["modelBytes"] = size
            try:
                dest.unlink()
            except OSError:
                pass
            with lock:
                done += 1
                print(f"[{done:>2}/{len(todo)}] {repo:44} gltf={len(info['gltf']):>2} "
                      f"baseColor={len(info['baseColor']):>2}", flush=True)
            return repo, info
        except Exception as exc:  # noqa: BLE001
            with lock:
                done += 1
                print(f"[{done:>2}/{len(todo)}] FAIL {repo}: {exc}", flush=True)
            return repo, None

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(work, repo, url, size) for repo, (url, size) in todo.items()]
        for fut in as_completed(futures):
            repo, info = fut.result()
            if info:
                results[repo] = info
            out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"done: {len(results)} aircraft -> {out}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
