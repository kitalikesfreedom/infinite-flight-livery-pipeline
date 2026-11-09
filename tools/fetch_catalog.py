#!/usr/bin/env python3
"""Query the Infinite Flight package catalog and download individual packages.

Source: POST /auth/v2/login (guest) -> GET /live/v2/packages/aircraft.
Every entry carries a signed downloadUrl (CDN token, valid for 24 hours).

Useful for confirming which textures an aircraft's glTF expects, or for reading the
structure of an official livery package.

Usage
-----
    # list model packages
    python fetch_catalog.py --list --type AircraftModel --match a320

    # list every livery of the A320 family
    python fetch_catalog.py --list --type AircraftLivery --match a320

    # download an A320 model package (contains the glTF)
    python fetch_catalog.py --download --type AircraftModel --match a320 --out dl/

    # dump the whole catalog to JSON
    python fetch_catalog.py --dump-json catalog.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.infiniteflight.com"
LOGIN = f"{API}/auth/v2/login"
CATALOG = f"{API}/live/v2/packages/aircraft"
UA = "if-livery-pipeline/1.0"


def post_json(url: str, payload: dict, token: str | None = None, timeout: int = 30) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", UA)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def get_json(url: str, token: str, timeout: int = 180, retries: int = 4) -> dict:
    last: Exception | None = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, method="GET")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("User-Agent", UA)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except (TimeoutError, urllib.error.URLError, OSError) as exc:
            last = exc
            print(f"  catalog fetch failed (attempt {attempt}/{retries}): {exc}; retrying in 10s",
                  file=sys.stderr)
            time.sleep(10)
    raise SystemExit(f"catalog fetch failed: {last}")


def guest_token(app_version: str) -> str:
    body = post_json(LOGIN, {})
    # The field name observed in practice is "access" (a JWT); older or different entry
    # points may return token / access_token / result instead.
    token = body.get("access") or body.get("token") or body.get("access_token") or body.get("result")
    if isinstance(token, str) and "," in token and token.count(".") < 2:
        token = token.split(",", 1)[0]  # form: "<token>,<expiry>"
    if not token or not isinstance(token, str):
        raise SystemExit(f"no token in the login response: {json.dumps(body)[:300]}")
    return token


def fetch_packages(app_version: str) -> list[dict]:
    token = guest_token(app_version)
    body = get_json(f"{CATALOG}?appVersion={app_version}", token)
    packages = (body.get("data") or {}).get("packages") or body.get("packages") or []
    if not packages:
        raise SystemExit(f"empty catalog: {json.dumps(body)[:300]}")
    return packages


def matches(pkg: dict, *, kind: str | None, pattern: str | None) -> bool:
    if kind and pkg.get("contentType") != kind:
        return False
    if not pattern:
        return True
    haystack = " ".join(
        str(pkg.get(key) or "")
        for key in ("storagePath", "name", "id", "contentType", "metadataJson")
    )
    return re.search(pattern, haystack, re.I) is not None


def summarize(pkg: dict) -> dict:
    return {
        "id": pkg.get("id"),
        "contentType": pkg.get("contentType"),
        "storagePath": pkg.get("storagePath"),
        "sizeBytes": pkg.get("sizeBytes"),
        "sha256": pkg.get("sha256"),
        "urlExpiresAt": pkg.get("urlExpiresAt"),
    }


def download(url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", UA)
    with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as fh:
        total = 0
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            fh.write(chunk)
            total += len(chunk)
    return total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Query and download Infinite Flight content packages")
    parser.add_argument("--app-version", default="26.5")
    parser.add_argument("--type", help="AircraftModel / AircraftLivery / ...")
    parser.add_argument("--match", help="regex over storagePath/name, e.g. a320")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--dump-json", help="write the full catalog to this file")
    parser.add_argument("--out", default="dl", help="download directory (--download)")
    parser.add_argument("--limit", type=int, default=0, help="process at most N packages; 0 = no limit")
    args = parser.parse_args(argv)

    if not (args.list or args.download or args.dump_json):
        parser.error("give at least one action: --list / --download / --dump-json")

    try:
        packages = fetch_packages(args.app_version)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"request failed HTTP {exc.code}: {exc.read()[:300]!r}")
    except urllib.error.URLError as exc:
        raise SystemExit(f"network unreachable: {exc.reason}")

    selected = [p for p in packages if matches(p, kind=args.type, pattern=args.match)]
    if args.limit:
        selected = selected[: args.limit]

    if args.dump_json:
        Path(args.dump_json).write_text(json.dumps(packages, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"catalog written to {args.dump_json} ({len(packages)} packages)", file=sys.stderr)

    if args.list:
        print(json.dumps([summarize(p) for p in selected], ensure_ascii=False, indent=2))

    if args.download:
        out = Path(args.out)
        for pkg in selected:
            url = pkg.get("downloadUrl")
            if not url:
                print(f"skipped (no downloadUrl): {pkg.get('storagePath')}", file=sys.stderr)
                continue
            name = (pkg.get("storagePath") or pkg.get("id") or "package").replace("/", "_")
            if not name.lower().endswith(".zip"):
                name += ".zip"
            dest = out / name
            size = download(url, dest)
            print(json.dumps({"file": str(dest), "bytes": size, "from": pkg.get("storagePath")}, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
