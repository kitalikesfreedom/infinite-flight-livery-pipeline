#!/usr/bin/env python3
"""Find an unknown path or filename with two rounds of probes.

Round 1 (--mode path): one distinct colour per candidate path, all written at once
        -> whichever colour shows on the fuselage names the winning path
Round 2 (--mode name): lock the path, write one big-numbered image per candidate filename
        -> whichever number shows names the winning file

Clear the virtual texture cache between rounds (Android):
        adb shell "pm trim-caches <bytes>"

--repo takes either a bare repository name (the `aircraft/` prefix is added) or a full
path relative to the content root when it contains a `/` — use the latter to test
historical candidates such as `Content/Aircraft/Airbus A320`.

Examples
--------
    python probe_matrix.py --mode path --platform android \
        --livery-dir "<livery directory>" --size 2048x2048 \
        --repo infiniteflight-aircraft-a320 \
        --repo "Content/Aircraft/Airbus A320" \
        --filenames Texture.webp --out out/probe_path.zip

    python probe_matrix.py --mode name --platform android \
        --repo infiniteflight-aircraft-a320 --livery-dir "<livery directory>" \
        --size 2048x2048 --filenames Texture.webp,Texture_0.webp,body.webp \
        --out out/probe_name.zip
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

from build_slip_package import PLATFORM_PREFIX, die, font_for, parse_size, solid, to_webp

# High-contrast colours, in order: red orange yellow green cyan blue purple magenta white black
PALETTE = [
    (255, 0, 0, 255),
    (255, 140, 0, 255),
    (255, 255, 0, 255),
    (0, 200, 0, 255),
    (0, 255, 255, 255),
    (0, 0, 255, 255),
    (160, 20, 190, 255),
    (255, 0, 255, 255),
    (255, 255, 255, 255),
    (0, 0, 0, 255),
]

COLOR_NAMES = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "magenta", "white", "black"]


def numbered(size: tuple[int, int], index: int, label: str) -> Image.Image:
    """Dark background, big yellow number, filename underneath — for name probes."""
    image = Image.new("RGB", size, (16, 16, 16))
    draw = ImageDraw.Draw(image)
    big = font_for(max(96, size[0] // 5))
    small = font_for(max(28, size[0] // 28))
    text = str(index)
    box = draw.textbbox((0, 0), text, font=big)
    draw.text(((size[0] - (box[2] - box[0])) // 2, size[1] // 3), text, fill=(255, 255, 0), font=big)
    draw.text((32, size[1] - 110), label, fill=(235, 235, 235), font=small)
    return image


def normalize(name: str) -> str:
    return name if name.lower().endswith(".webp") else f"{name}.webp"


def content_relative(repo: str) -> str:
    """Normalise --repo into a directory relative to the content root.

    A bare repository name gets the aircraft/ prefix; anything containing `/` is treated
    as a complete sub-path, so historical candidates can be tested as-is.
    """
    repo = repo.strip().strip("/")
    return repo if "/" in repo else f"aircraft/{repo.lower()}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Two-round probing for livery paths and texture names")
    parser.add_argument("--mode", choices=["path", "name"], required=True)
    parser.add_argument("--platform", choices=sorted(PLATFORM_PREFIX), default="android")
    parser.add_argument("--repo", action="append", default=[], help="candidate path (repeatable, mode=path)")
    parser.add_argument("--livery-dir", required=True)
    parser.add_argument("--filenames", required=True, help="comma-separated candidate filenames")
    parser.add_argument("--size", required=True, help="WxH; must match the target texture")
    parser.add_argument("--out", required=True)
    parser.add_argument("--quality", type=int, default=92)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    size = parse_size(args.size)
    names = [normalize(n) for n in (x.strip() for x in args.filenames.split(",")) if n]
    if not names:
        die("--filenames must not be empty")
    if not args.repo:
        die("at least one --repo is required")

    prefix_root = PLATFORM_PREFIX[args.platform]
    plan: list[tuple[str, int, str]] = []  # (entry name, colour index / number, label)

    if args.mode == "path":
        for idx, repo in enumerate(args.repo):
            base = f"{prefix_root}/{content_relative(repo)}/liveries/{args.livery_dir}".rstrip("/")
            for name in names:
                plan.append((f"{base}/{name}", idx, f"{COLOR_NAMES[idx % len(COLOR_NAMES)]} · {repo}"))
    else:
        base = f"{prefix_root}/{content_relative(args.repo[0])}/liveries/{args.livery_dir}".rstrip("/")
        for idx, name in enumerate(names, start=1):
            plan.append((f"{base}/{name}", idx, name))

    legend = [{"mark": mark, "meaning": label} for _, mark, label in plan]

    if args.dry_run:
        print(json.dumps({
            "mode": args.mode,
            "size": list(size),
            "legend": legend,
            "entries": [entry for entry, _, _ in plan],
        }, ensure_ascii=False, indent=2))
        return 0

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for entry, mark, label in plan:
            if args.mode == "path":
                image = solid(size, PALETTE[mark % len(PALETTE)])
            else:
                image = numbered(size, mark, label)
            bundle.writestr(entry, to_webp(image, args.quality))

    print(json.dumps({
        "out": str(out),
        "mode": args.mode,
        "legend": legend,
        "reminder": 'adb shell "pm trim-caches <bytes>"',
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
