# CRJ-700 — `infiniteflight-aircraft-crj7`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-crj7` |
| Model path in package | `Aircraft/CRJ-700` |
| Model package | `8f34680a-a4ad-4f21-91e9-3a932ab03ca4` v25.3.74 · 7.1 MB |
| glTF files | 4 |
| Texture pipeline | **Multi-part (legacy shading)** |
| BaseColor images to paint | 4 |
| Entries in the official livery package | 4 |
| Livery packages | 13 named + 0 generic |
| Configuration package | `e5eb84ee-aa21-4cc3-87c4-8362f9112df4` · 25 KB |
| Sample livery parsed | Alaska Airlines → `Aircraft/CRJ-700/Liveries/Alaska Airlines` |

> 4 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `eng.webp` | 2048×2048 | 192 KB | surface | **yes** |
| `fuse.webp` | 2048×2048 | 207 KB | surface | **yes** |
| `wingLH.webp` | 2048×2048 | 137 KB | surface | **yes** |
| `wingRH.webp` | 2048×2048 | 143 KB | surface | **yes** |

## 2. Every baseColor texture the model references

The 4 glTF file(s) reference 14 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
CRJ_ovh_lamps.webp
Cockpit_Datails.webp
Cockpit_Environment.webp
Pilot_01.webp
Pilot_02.webp
eng.webp
fuse.webp
glass.webp
interior.webp
misc.webp
screen_glass.webp
screen_glass_up.webp
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

## 4. Livery directories (13)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| Adria Airways | `Adria Airways` |
| Alaska Airlines | `Alaska Airlines` |
| American Eagle | `American Eagle` |
| British Airways | `British Airways` |
| Delta Air Lines | `Delta Air Lines` |
| Frontier | `Frontier Airlines` |
| Generic | `Generic` |
| HOP! | `HOP` |
| Infinite Flight - 2018 | `Infinite Flight` |
| Nordica | `Nordica` |
| Shandong Airlines | `Shandong Airlines` |
| SA Express | `South African Express` |
| United Express | `United Express` |

## 5. Package it

**Format: Multi-part (legacy shading).** 4 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

### Files this aircraft needs

| file | dimensions | role | what to put there |
|---|---|---|---|
| `eng.webp` | 2048x2048 | surface / **paint** | your artwork |
| `fuse.webp` | 2048x2048 | surface / **paint** | your artwork |
| `wingLH.webp` | 2048x2048 | surface / **paint** | your artwork |
| `wingRH.webp` | 2048x2048 | surface / **paint** | your artwork |

### Option A - explicit list (copy and run)

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-crj7 \
  --livery-dir "<a directory from the table above>" \
  --texture "eng.webp=art/eng.png" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  --out out/crj7.zip
```

### Option B - auto mode

```bash
python tools/build_slip_package.py --auto --art art/ \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-crj7 \
  --livery-dir "<a directory from the table above>" \
  --out out/crj7.zip
```

`--auto` reads `data/livery_files.json`, then looks for these stems in `art/`
(`.png`, `.webp`, `.jpg` are all accepted):

```
eng.png
fuse.png
wingLH.png
wingRH.png
```

### Where the entries land

```
android: ../../files/aircraft/infiniteflight-aircraft-crj7/liveries/<directory>/<file>.webp
ios:     ../../Library/dlc/aircraft/infiniteflight-aircraft-crj7/liveries/<directory>/<file>.webp
```

`<directory>` must come from the table in section 4 - the folder name, not the name the app
shows.

### How to tell it worked

Each listed file is its own material, so the repaint is all-or-nothing per part: a wing still in
official colours means `wing_*.webp` did not land, a dark hull means the `_ORM` partner is missing.

## 6. Import

```bash
adb push out/crj7.zip /sdcard/Download/crj7.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

