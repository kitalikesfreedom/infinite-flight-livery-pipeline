# Build and import (Android)

> Pick your aircraft in [models/index.md](models/index.md), copy its packaging command, run it.
> This page explains what that command is doing and how to verify the result.

## 1. Paint

| requirement | detail |
|---|---|
| dimensions | must equal the original exactly — 2048², 4096², 1024² depending on the part; never scale |
| format | WebP, quality 90–95 |
| colour | RGB is fine for legacy; keep RGBA where the original has alpha (`M_*_albd`) |
| content | follow the part's UV layout — start from the blank template and the UV sheet for that part |

Compose and inspect locally:

```bash
python tools/livery_tool.py inspect art/a320.png
python tools/livery_tool.py compose \
  --template art/a320_blank.png \
  --overlay "art/logo.png:820:640:100" \
  --text "B-3201" --text-position 180 1500 --text-size 96 \
  --output art/a320.png
```

`compose` writes a lossless PNG; compression happens once, at packaging time.

## 2. Package

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-a320 \
  --livery-dir "<livery directory>" \
  --texture "Texture.webp=art/a320.png" \
  --fill-orm --fill-normal \
  --out out/a320.zip
```

Flags that matter:

| flag | meaning |
|---|---|
| `--texture NAME=PATH` | repeatable; one entry per file the aircraft needs |
| `--fill-orm` / `--fill-normal` | append solid `Texture_ORM` / `Texture_N` (legacy pipeline only) |
| `--size WxH` | override the expected dimensions (2048² legacy / 4096² neo by default) |
| `--resize` | scale instead of failing on a dimension mismatch — softens the result, avoid |
| `--entry-prefix` | replace the computed prefix entirely (Generic liveries, model root) |
| `--dry-run` | print entry names, write nothing |
| `--tint RRGGBB` | generate a flat colour probe instead of a real texture |

Always dry-run first:

```json
{
  "entries": [
    "../../files/aircraft/infiniteflight-aircraft-a320/liveries/<livery directory>/Texture.webp",
    "../../files/aircraft/infiniteflight-aircraft-a320/liveries/<livery directory>/Texture_ORM.webp",
    "../../files/aircraft/infiniteflight-aircraft-a320/liveries/<livery directory>/Texture_N.webp"
  ]
}
```

Multi-part modern aircraft take one `--texture` per albedo file — copy the block from the aircraft's
page, e.g. A321neo needs 11 entries, A320neo 20:

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-a21n \
  --livery-dir "<livery directory>" \
  --texture "M_Fuselage_01_albd.webp=art/f1.png" \
  --texture "M_Fuselage_02_albd.webp=art/f2.png" \
  --texture "M_Fuselage_03_albd.webp=art/f3.png" \
  --texture "M_Wings_01_albd.webp=art/w1.png" \
  --texture "M_Wings_02_albd.webp=art/w2.png" \
  --texture "M_LandingGear_02_albd.webp=art/g1.png" \
  --texture "M_PW1100G_Left_albd.webp=art/e1.png" \
  --texture "M_PW1100G_Right_albd.webp=art/e2.png" \
  --out out/a21n_lufthansa.zip
```

## 3. Push

```bash
adb push out/a320.zip /sdcard/Download/a320.zip
```

Not into the app's private directory — you have no permission there, that is the whole point.

## 4. Import

1. Open the app
2. **Scenery Editor**
3. **Open an airport** — skipping this makes the import vanish silently
4. **Satellite → Import Imagery**
5. Pick the zip (the picker takes `application/*`, so a zip is selectable)
6. Wait 2–3 seconds (no progress indicator, no confirmation)
7. Force-stop the app — swipe it out of recents, not Home — then reopen
8. Select the aircraft and the livery you targeted, spawn in

## 5. Drop the texture cache

```bash
adb shell "pm trim-caches <bytes>"
```

| approach | effect |
|---|---|
| in-app / system "clear cache" | reclaims a token amount of the tile cache |
| truncate `vt.cache` | nothing, it is memory-mapped |
| `pm trim-caches <bytes>` | clears down to the target; rebuilds on next start |

Root not required. The large file that reappears afterwards is the freshly preallocated empty
`vt.cache` (`VtCacheCapacityInBytes`), not a failure.

You only need this when repainting **the same livery directory** a second time. First write into a
new directory always shows up.

## 6. Verification

| what you see | what it means |
|---|---|
| fuselage repainted, no mirror highlights | success — all baseColor + ORM/N present |
| black patches, chrome sheen | baseColor only; add ORM and normal |
| absolutely nothing changed | wrong path / wrong directory / airport not open / cache |
| works once, then never again | `vt.cache` still hot — trim it |
| `Error loading the imagery package` | a `kml` or malformed entry is in the zip; keep the archive to webp |

## 7. The repeat loop

```
1) adb shell "pm trim-caches <bytes>"
2) Scenery Editor → open airport → Satellite → Import Imagery → new zip
3) force-stop, reopen, fly
```

Verified across consecutive rewrites of the same directory (purple → teal).

---

## Appendix · confirming a filename from the official packages

If an aircraft's page still leaves a name ambiguous, or a new aircraft ships before this repository
is regenerated, two routes remain.

### A. Read the model's glTF (authoritative)

```bash
python tools/fetch_catalog.py --dump-json data/catalog.json
python tools/extract_models.py --only <repo>     # or no --only for all 65
python - <<'PY'
import json
d = json.load(open("data/model_textures.json"))
print(d["infiniteflight-aircraft-a320"]["baseColor"])
PY
```

### B. Inspect an official livery package

```bash
python tools/extract_liveries.py --type AircraftLivery --pick largest --only infiniteflight-aircraft-a320
```

`--pick largest` is not cosmetic: many livery packages in the catalog are 0-byte metadata-only
updates, and choosing the smallest one returns an empty inventory. Signed download URLs carry
`urlExpiresAt` (24 h); re-fetch the catalog to refresh them.

### C. Neither is available: probe

See [02 §6](paths-and-textures.md#6-when-a-path-or-filename-is-still-unknown) and
[probe_matrix.py](../tools/probe_matrix.py).
