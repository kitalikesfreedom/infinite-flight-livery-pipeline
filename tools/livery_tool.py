#!/usr/bin/env python3
"""Offline artwork helper: inspect, compose, archive. Touches no installed application.

  inspect  report an image's dimensions and format
  compose  stack overlays at given coordinates, optionally with text
  package  write a manifest-based livery folder plus a zip (archival, not for import)

For the package that Infinite Flight itself imports, use build_slip_package.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}


@dataclass
class Overlay:
    path: Path
    x: int
    y: int
    opacity: int


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def load_rgba(path: Path) -> Image.Image:
    if not path.is_file():
        fail(f"file not found: {path}")
    if path.suffix.lower() not in SUPPORTED:
        fail(f"unsupported image format: {path.suffix}; use PNG/JPEG/WebP")
    try:
        return Image.open(path).convert("RGBA")
    except Exception as exc:
        fail(f"cannot decode image {path}: {exc}")


def apply_opacity(image: Image.Image, opacity: int) -> Image.Image:
    opacity = max(0, min(100, opacity))
    if opacity == 100:
        return image
    alpha = image.getchannel("A").point(lambda value: value * opacity // 100)
    image = image.copy()
    image.putalpha(alpha)
    return image


def parse_overlay(value: str) -> Overlay:
    # Split from the right so a Windows drive letter stays part of PATH
    parts = value.rsplit(":", 3)
    if len(parts) == 1:
        path, x, y, opacity = parts[0], 0, 0, 100
    elif len(parts) == 3:
        path, x, y = parts
        opacity = 100
    elif len(parts) == 4:
        path, x, y, opacity = parts
    else:
        fail("overlay must be PATH or PATH:X:Y[:OPACITY]")
    x, y, opacity = int(x), int(y), int(opacity)
    if not 0 <= opacity <= 100:
        fail("overlay opacity must be 0..100")
    return Overlay(Path(path), x, y, opacity)


def font_for(size: int):
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size=size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def compose(args: argparse.Namespace) -> None:
    image = load_rgba(Path(args.template))
    for raw_overlay in args.overlay:
        overlay = parse_overlay(raw_overlay)
        layer = apply_opacity(load_rgba(overlay.path), overlay.opacity)
        image.alpha_composite(layer, dest=(overlay.x, overlay.y))

    if args.text:
        draw = ImageDraw.Draw(image)
        font = font_for(args.text_size)
        x, y = args.text_position
        draw.text((x + 2, y + 2), args.text, fill=(0, 0, 0, 170), font=font)
        draw.text((x, y), args.text, fill=tuple(args.text_color), font=font)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)
    print(json.dumps({"output": str(output), "size": list(image.size), "sha256": sha256(output)}, indent=2))


def package(args: argparse.Namespace) -> None:
    texture = Path(args.texture)
    image = load_rgba(texture)
    if args.width and args.height and image.size != (args.width, args.height):
        fail(f"texture size {image.size} does not match requested {(args.width, args.height)}")

    package_dir = Path(args.directory)
    package_dir.mkdir(parents=True, exist_ok=True)
    texture_dest = package_dir / "textures" / f"{args.aircraft_id}.png"
    texture_dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(texture_dest, format="PNG", optimize=True)

    manifest = {
        "format": "local-livery-v1",
        "aircraftId": args.aircraft_id,
        "liveryId": args.livery_id,
        "displayName": args.display_name,
        "networkLiveryId": args.network_livery_id,
        "textures": {"albedo": str(texture_dest.relative_to(package_dir)).replace("\\", "/")},
        "renderOnly": True,
        "upload": False,
    }
    manifest_path = package_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    archive = Path(args.output)
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(package_dir.rglob("*")):
            if path.is_file():
                bundle.write(path, path.relative_to(package_dir).as_posix())
    print(json.dumps({"output": str(archive), "manifest": manifest, "sha256": sha256(archive)}, ensure_ascii=False, indent=2))


def inspect(args: argparse.Namespace) -> None:
    image = load_rgba(Path(args.texture))
    print(json.dumps({"path": args.texture, "size": list(image.size), "mode": image.mode, "format": image.format}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local livery artwork helper")
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_cmd = sub.add_parser("inspect", help="report dimensions and format")
    inspect_cmd.add_argument("texture")
    inspect_cmd.set_defaults(func=inspect)

    compose_cmd = sub.add_parser("compose", help="stack overlays and export PNG")
    compose_cmd.add_argument("--template", required=True)
    compose_cmd.add_argument("--output", required=True)
    compose_cmd.add_argument("--overlay", action="append", default=[], help="PATH[:X:Y[:OPACITY]]")
    compose_cmd.add_argument("--text")
    compose_cmd.add_argument("--text-position", nargs=2, type=int, default=[32, 32], metavar=("X", "Y"))
    compose_cmd.add_argument("--text-size", type=int, default=48)
    compose_cmd.add_argument("--text-color", nargs=4, type=int, default=[255, 255, 255, 255], metavar=("R", "G", "B", "A"))
    compose_cmd.set_defaults(func=compose)

    package_cmd = sub.add_parser("package", help="write a local-livery-v1 archive")
    package_cmd.add_argument("--texture", required=True)
    package_cmd.add_argument("--aircraft-id", required=True)
    package_cmd.add_argument("--livery-id", required=True)
    package_cmd.add_argument("--display-name", required=True)
    package_cmd.add_argument("--network-livery-id", default="official-default")
    package_cmd.add_argument("--directory", required=True)
    package_cmd.add_argument("--output", required=True)
    package_cmd.add_argument("--width", type=int)
    package_cmd.add_argument("--height", type=int)
    package_cmd.set_defaults(func=package)
    return parser


if __name__ == "__main__":
    try:
        command = build_parser().parse_args()
        command.func(command)
    except ValueError as exc:
        fail(str(exc))
