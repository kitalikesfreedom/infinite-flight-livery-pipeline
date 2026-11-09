#!/usr/bin/env python3
"""Package textures into a zip that Infinite Flight will import.

The entry names in the archive *are* the write targets (a relative path traversal), e.g. on Android:

    ../../files/aircraft/infiniteflight-aircraft-a320/liveries/<livery directory>/Texture.webp

iOS uses a different root (Library/dlc instead of files); switch with --platform ios.

Examples
--------
Print the entry names without writing anything:

    python build_slip_package.py --platform android \
        --aircraft-repo infiniteflight-aircraft-a320 \
        --livery-dir "<livery directory>" \
        --texture "Texture.webp=art/a320.png" --fill-orm --fill-normal \
        --out out/a320.zip --dry-run

Build a flat-colour probe package (to confirm a path or filename hits):

    python build_slip_package.py --platform android \
        --aircraft-repo infiniteflight-aircraft-a320 \
        --livery-dir "<livery directory>" \
        --tint FF00FF --texture "Texture.webp" --out out/probe.zip
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import zipfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    sys.exit("Pillow is required: pip install -r requirements.txt")

# How each platform's CacheRoot relates to its ContentRoot:
#   if_zip_output lives under GetTempFolder(); two levels up is the app private root
#   (Android) or the container root (iOS), from which you enter the content root.
PLATFORM_PREFIX = {
    "android": "../../files",
    "ios": "../../Library/dlc",
}

# Legacy pipeline (single Texture.webp) needs three files that must move together
OLD_PIPELINE_COMPANIONS = {
    "orm": "Texture_ORM.webp",   # R=AO G=Roughness B=Metallic -> (255,200,0)
    "normal": "Texture_N.webp",  # flat normal -> (128,128,255)
}

DEFAULT_SIZE = {"old": (2048, 2048), "new": (4096, 4096)}

# Fixed timestamp for archive entries: keeps output byte-reproducible and leaks no build time.
FIXED_DATE = (1980, 1, 1, 0, 0, 0)

ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "data" / "livery_files.json"
IMAGE_EXTS = (".png", ".webp", ".jpg", ".jpeg")


def auto_textures(repo: str, art_dir: Path) -> list[str]:
    """Build the --texture list from the recorded inventory plus a folder of artwork.

    The inventory is what an official livery package for that aircraft ships, so this is
    exactly the set of files a repaint has to provide. Artwork is matched by file stem:
    `Texture_ORM.webp` needs `art/Texture_ORM.png` (or .webp/.jpg).
    """
    if not INVENTORY.is_file():
        die(f"inventory not found: {INVENTORY} (run tools/extract_liveries.py first)")
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    entry = data.get(repo.strip().lower())
    if not entry:
        known = ", ".join(sorted(data)[:6])
        die(f"no inventory for {repo!r}; try one of: {known} ...")
    files = entry.get("files") or []
    if not files:
        die(f"inventory for {repo!r} is empty")

    found: list[str] = []
    missing: list[str] = []
    for item in files:
        name = item["name"]
        stem = name.rsplit(".", 1)[0]
        for ext in IMAGE_EXTS:
            candidate = art_dir / f"{stem}{ext}"
            if candidate.is_file():
                found.append(f"{name}={candidate}")
                break
        else:
            missing.append(name)

    print(f"auto: {len(found)}/{len(files)} file(s) matched under {art_dir}", file=sys.stderr)
    if missing:
        print(f"auto: no artwork for {', '.join(missing)}", file=sys.stderr)
        print("auto: add those files, or pass --fill-orm / --fill-normal to synthesise them",
              file=sys.stderr)
    if not found:
        die("auto mode matched nothing; check the artwork folder and file stems")
    return found


def die(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit(f"error: {msg}")


def parse_size(value: str) -> tuple[int, int]:
    try:
        w, h = value.lower().split("x")
        return int(w), int(h)
    except Exception:
        die(f"--size expects WxH, e.g. 2048x2048, got {value!r}")


def load_rgba(path: Path) -> Image.Image:
    if not path.is_file():
        die(f"texture not found: {path}")
    try:
        return Image.open(path).convert("RGBA")
    except Exception as exc:
        die(f"cannot decode {path}: {exc}")


def solid(size: tuple[int, int], rgba: tuple[int, int, int, int]) -> Image.Image:
    return Image.new("RGBA", size, rgba)


def hex_rgba(value: str) -> tuple[int, int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) == 6:
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (255,)  # type: ignore[return-value]
    if len(value) == 8:
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4, 6))  # type: ignore[return-value]
    die(f"--tint expects RRGGBB or RRGGBBAA, got {value!r}")


def to_webp(image: Image.Image, quality: int) -> bytes:
    buf = io.BytesIO()
    mode = "RGB" if image.mode == "RGBA" and image.getchannel("A").getextrema() == (255, 255) else image.mode
    image.convert(mode).save(buf, "WEBP", quality=quality, method=6)
    return buf.getvalue()


def font_for(size: int):
    """Pick an available font, used for numbered probe images."""
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size=size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow < 10.1
        return ImageFont.load_default()


def parse_texture_arg(value: str) -> tuple[str, Path | None]:
    """NAME=PATH, or a bare NAME (which needs --tint to become a flat colour)."""
    if "=" in value:
        name, path = value.split("=", 1)
        return name.strip(), Path(path)
    return value.strip(), None


def normalize_name(name: str) -> str:
    return name if name.lower().endswith(".webp") else f"{name}.webp"


def build_entries(args: argparse.Namespace) -> list[tuple[str, bytes]]:
    prefix = args.entry_prefix or (
        f"{PLATFORM_PREFIX[args.platform]}/aircraft/{args.aircraft_repo.strip().lower()}/liveries/{args.livery_dir}"
    )
    prefix = prefix.rstrip("/")

    explicit_size = parse_size(args.size) if args.size else None
    if explicit_size is None:
        explicit_size = DEFAULT_SIZE["new" if args.aircraft_repo.strip().lower().endswith(("a20n", "a21n")) else "old"]

    tint = hex_rgba(args.tint) if args.tint else None
    if tint is None and not args.texture:
        die("need at least one --texture, or --tint for a probe texture")

    entries: list[tuple[str, bytes]] = []
    base_image: Image.Image | None = None

    for raw in args.texture:
        name, path = parse_texture_arg(raw)
        name = normalize_name(name)
        if path is None:
            if tint is None:
                die(f"--texture {raw} has no =PATH; pair it with --tint")
            image = solid(explicit_size, tint)
        else:
            image = load_rgba(path)
            if args.resize and image.size != explicit_size:
                image = image.resize(explicit_size, Image.LANCZOS)
        if image.size != explicit_size:
            die(f"{name} is {image.size} but the target is {explicit_size} "
                f"(dimensions must match, or pass --resize)")
        base_image = base_image or image
        entries.append((f"{prefix}/{name}", to_webp(image, args.quality)))

    size = base_image.size if base_image else explicit_size
    if args.fill_orm:
        entries.append((f"{prefix}/{OLD_PIPELINE_COMPANIONS['orm']}", to_webp(solid(size, (255, 200, 0, 255)), args.quality)))
    if args.fill_normal:
        entries.append((f"{prefix}/{OLD_PIPELINE_COMPANIONS['normal']}", to_webp(solid(size, (128, 128, 255, 255)), args.quality)))

    return entries


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an importable Infinite Flight livery package")
    parser.add_argument("--platform", choices=sorted(PLATFORM_PREFIX), default="android")
    parser.add_argument("--aircraft-repo", required=True, help="e.g. infiniteflight-aircraft-a320")
    parser.add_argument("--livery-dir", required=True, help="livery directory name (not the display name); see docs/models/<aircraft>.md")
    parser.add_argument("--texture", action="append", default=[], metavar="NAME[=PATH]")
    parser.add_argument("--auto", action="store_true",
                        help="fill --texture from data/livery_files.json and the artwork folder")
    parser.add_argument("--art", default="art",
                        help="artwork folder for --auto (default: art)")
    parser.add_argument("--tint", help="RRGGBB[AA]: generate a flat colour texture (probe)")
    parser.add_argument("--quality", type=int, default=92)
    parser.add_argument("--size", help="WxH; defaults per aircraft (2048^2 legacy, 4096^2 neo)")
    parser.add_argument("--resize", action="store_true", help="scale on a dimension mismatch instead of failing")
    parser.add_argument("--fill-orm", action="store_true", help="append Texture_ORM.webp (prevents black/mirror shading)")
    parser.add_argument("--fill-normal", action="store_true", help="append Texture_N.webp (flat normal)")
    parser.add_argument("--entry-prefix", help="override the computed prefix (Generic liveries, custom roots)")
    parser.add_argument("--out", required=True)
    parser.add_argument("--dry-run", action="store_true", help="print entry names only")
    args = parser.parse_args(argv)

    if args.auto:
        if args.texture:
            die("--auto and --texture are mutually exclusive")
        args.texture = auto_textures(args.aircraft_repo, Path(args.art))

    entries = build_entries(args)
    if args.dry_run:
        print(json.dumps({"entries": [name for name, _ in entries]}, ensure_ascii=False, indent=2))
        return 0

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, data)

    print(json.dumps({
        "out": str(out),
        "bytes": out.stat().st_size,
        "entries": [{"name": name, "bytes": len(data)} for name, data in entries],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
