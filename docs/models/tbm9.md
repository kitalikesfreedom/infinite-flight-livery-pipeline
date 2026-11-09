# TBM-930 — `infiniteflight-aircraft-tbm9`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-tbm9` |
| Model path in package | `Aircraft/TBM 930` |
| Model package | `3f17ca35-b384-4391-aa5e-5beececb0612` v25.3.34 · 13.0 MB |
| glTF files | 4 |
| Texture pipeline | **Multi-part (legacy shading)** |
| BaseColor images to paint | 5 |
| Entries in the official livery package | 10 |
| Livery packages | 12 named + 0 generic |
| Configuration package | `dca2bfd0-92a7-4e50-8c3b-8bef98c29c56` · 14 KB |
| Sample livery parsed | Sea Blue → `Aircraft/TBM 930/Liveries/Private 5` |

> 5 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `fuse.webp` | 2048×2048 | 114 KB | surface | **yes** |
| `fuse2.webp` | 2048×2048 | 92 KB | surface | **yes** |
| `fuse2_ORM.webp` | 2048×2048 | 2.9 MB | orm | keep |
| `fuse_ORM.webp` | 2048×2048 | 2.1 MB | orm | keep |
| `tail.webp` | 2048×2048 | 128 KB | surface | **yes** |
| `tail_ORM.webp` | 2048×2048 | 2.4 MB | orm | keep |
| `wingLH.webp` | 2048×2048 | 100 KB | surface | **yes** |
| `wingLH_ORM.webp` | 2048×2048 | 3.3 MB | orm | keep |
| `wingRH.webp` | 2048×2048 | 81 KB | surface | **yes** |
| `wingRH_ORM.webp` | 2048×2048 | 3.1 MB | orm | keep |

## 2. Every baseColor texture the model references

The 4 glTF file(s) reference 15 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
cockpit_01.webp
cockpit_02.webp
cockpit_03.webp
cockpit_04.webp
cockpit_05.webp
fuse.webp
fuse2.webp
glass.webp
interior_01.webp
pilot_03.webp
prop.webp
propeller.webp
tail.webp
wingLH.webp
wingRH.webp
```

## 3. glTF files inside the model package

```
Aircraft_LOD_0.gltf
Aircraft_LOD_1.gltf
Aircraft_LOD_3.gltf
Aircraft_LOD_2.gltf
```

## 4. Livery directories (12)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| French Army | `French Air Force` |
| Generic | `Generic` |
| Infinite Flight - Dark | `Infinite Flight 1` |
| Infinite Flight - Light | `Infinite Flight 2` |
| Maroon | `Private 1` |
| Navy Blue | `Private 2` |
| Black, Red & White | `Private 3` |
| Charcoal | `Private 4` |
| Sea Blue | `Private 5` |
| Red Stripe | `Private 6` |
| N930DH | `Private 8` |
| White, Red and Black | `Steveo1kinevo` |

## 5. Package it

**Format: Multi-part (legacy shading).** 5 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

### Files this aircraft needs

| file | dimensions | role | what to put there |
|---|---|---|---|
| `fuse.webp` | 2048x2048 | surface / **paint** | your artwork |
| `fuse2.webp` | 2048x2048 | surface / **paint** | your artwork |
| `tail.webp` | 2048x2048 | surface / **paint** | your artwork |
| `wingLH.webp` | 2048x2048 | surface / **paint** | your artwork |
| `wingRH.webp` | 2048x2048 | surface / **paint** | your artwork |
| `fuse2_ORM.webp` | 2048x2048 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `fuse_ORM.webp` | 2048x2048 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `tail_ORM.webp` | 2048x2048 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `wingLH_ORM.webp` | 2048x2048 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `wingRH_ORM.webp` | 2048x2048 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |

### Option A - explicit list (copy and run)

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-tbm9 \
  --livery-dir "<a directory from the table above>" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "fuse2.webp=art/fuse2.png" \
  --texture "tail.webp=art/tail.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  --texture "fuse2_ORM.webp=art/fuse2_ORM.png" \
  --texture "fuse_ORM.webp=art/fuse_ORM.png" \
  --texture "tail_ORM.webp=art/tail_ORM.png" \
  --texture "wingLH_ORM.webp=art/wingLH_ORM.png" \
  --texture "wingRH_ORM.webp=art/wingRH_ORM.png" \
  --out out/tbm9.zip
```

### Option B - auto mode

```bash
python tools/build_slip_package.py --auto --art art/ \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-tbm9 \
  --livery-dir "<a directory from the table above>" \
  --out out/tbm9.zip
```

`--auto` reads `data/livery_files.json`, then looks for these stems in `art/`
(`.png`, `.webp`, `.jpg` are all accepted):

```
fuse.png
fuse2.png
fuse2_ORM.png
fuse_ORM.png
tail.png
tail_ORM.png
wingLH.png
wingLH_ORM.png
wingRH.png
wingRH_ORM.png
```

### Option C - reuse the companions from an official package

The `keep` rows above are not artwork: they are masks the vendor ships. Rather than
recreating them, pull them out of an official livery package:

```bash
python tools/fetch_catalog.py --download --type AircraftLivery \
  --match tbm9 --out dl/
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-tbm9 \
  --livery-dir "<a directory from the table above>" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "fuse2.webp=art/fuse2.png" \
  --texture "tail.webp=art/tail.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  --keep-from dl/<downloaded package>.zip \
  --out out/tbm9.zip
```

`--keep-from` copies every entry in that archive **except** the albedo files, so your own
artwork always wins and the companions stay byte-identical to the vendor's.

### Where the entries land

```
android: ../../files/aircraft/infiniteflight-aircraft-tbm9/liveries/<directory>/<file>.webp
ios:     ../../Library/dlc/aircraft/infiniteflight-aircraft-tbm9/liveries/<directory>/<file>.webp
```

`<directory>` must come from the table in section 4 - the folder name, not the name the app
shows.

### How to tell it worked

Each listed file is its own material, so the repaint is all-or-nothing per part: a wing still in
official colours means `wing_*.webp` did not land, a dark hull means the `_ORM` partner is missing.

## 6. Import

```bash
adb push out/tbm9.zip /sdcard/Download/tbm9.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

