# Space Shuttle — `infiniteflight-aircraft-sshu`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-sshu` |
| Model path in package | `Aircraft/Shuttle` |
| Model package | `61bd47dc-e12b-4912-9d91-719e1f9298d7` v25.3.8 · 147 KB |
| glTF files | 1 |
| Texture pipeline | **Few-part (legacy shading)** |
| BaseColor images to paint | 2 |
| Entries in the official livery package | 2 |
| Livery packages | 0 named + 1 generic |
| Configuration package | `4a42e4e1-6ec1-40a8-923e-cd4ebb46375e` · 8 KB |

> 2 baseColor images, one per body area, each its own PBR material.

## 1. Inventory of one official package

No livery package could be parsed for this aircraft, so the inventory is the model's
own `baseColor` reference set taken from its glTF. Dimensions are not available here.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `spstob_1.webp` | ? | - | ? | **yes** |
| `wheels.webp` | ? | - | ? | **yes** |

## 2. Every baseColor texture the model references

The 1 glTF file(s) reference 2 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
spstob_1.webp
wheels.webp
```

## 3. glTF files inside the model package

```
Aircraft_LOD_0.gltf
```

## 4. Livery directories (0)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

No named liveries ship with this aircraft; only the Generic package exists.

## 5. Package it

**Format: Few-part (legacy shading).** 2 baseColor images, one per body area, each its own PBR material.

### Files this aircraft needs

| file | dimensions | role | what to put there |
|---|---|---|---|
| `spstob_1.webp` | ? | ? / **paint** | your artwork |
| `wheels.webp` | ? | ? / **paint** | your artwork |

### Option A - explicit list (copy and run)

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-sshu \
  --livery-dir "<a directory from the table above>" \
  --texture "spstob_1.webp=art/spstob_1.png" \
  --texture "wheels.webp=art/wheels.png" \
  --out out/sshu.zip
```

### Option B - auto mode

```bash
python tools/build_slip_package.py --auto --art art/ \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-sshu \
  --livery-dir "<a directory from the table above>" \
  --out out/sshu.zip
```

`--auto` reads `data/livery_files.json`, then looks for these stems in `art/`
(`.png`, `.webp`, `.jpg` are all accepted):

```
spstob_1.png
wheels.png
```

### Where the entries land

```
android: ../../files/aircraft/infiniteflight-aircraft-sshu/liveries/<directory>/<file>.webp
ios:     ../../Library/dlc/aircraft/infiniteflight-aircraft-sshu/liveries/<directory>/<file>.webp
```

`<directory>` must come from the table in section 4 - the folder name, not the name the app
shows.

### How to tell it worked

Each listed file is its own material, so the repaint is all-or-nothing per part: a wing still in
official colours means `wing_*.webp` did not land, a dark hull means the `_ORM` partner is missing.

## 6. Import

```bash
adb push out/sshu.zip /sdcard/Download/sshu.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

