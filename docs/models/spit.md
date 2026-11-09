# Spitfire — `infiniteflight-aircraft-spit`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-spit` |
| Model path in package | `Aircraft/Spitfire` |
| Model package | `8a62f1d0-bca9-494c-bc01-1fb8b7255f76` v25.3.31 · 375 KB |
| glTF files | 1 |
| Texture pipeline | **Few-part (legacy shading)** |
| BaseColor images to paint | 3 |
| Entries in the official livery package | 11 |
| Livery packages | 1 named + 0 generic |
| Configuration package | `038fdae9-f492-4c16-b8c7-a87b560f8b50` · 7 KB |
| Sample livery parsed | Royal Australian Air Force → `Aircraft/Spitfire/Liveries/Generic` |

> 3 baseColor images, one per body area, each its own PBR material.

## 1. Inventory of one official package

The per-livery package for this aircraft is metadata-only, so the inventory comes from
the aircraft's shared texture set (`AircraftSharedLiveryFiles`) — the complete file list
for the airframe, with real dimensions.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `Shadow.webp` | 256×256 | 5 KB | surface | keep |
| `Spitfire_Fan.webp` | 1024×1024 | 229 KB | surface | **yes** |
| `Spitfire_Fan_ORM.webp` | 512×512 | 111 KB | orm | keep |
| `Spitfire_Glass.webp` | 512×512 | 35 KB | glass | keep |
| `Spitfire_Glass_ORM.webp` | 512×512 | 237 KB | orm | keep |
| `SpitfireMk8_1.webp` | 1024×1024 | 103 KB | surface | **yes** |
| `SpitfireMk8_1_N.webp` | 1024×1024 | 306 KB | normal | keep |
| `SpitfireMk8_1_ORM.webp` | 1024×1024 | 860 KB | orm | keep |
| `SpitfireMk8_2.webp` | 1024×1024 | 107 KB | surface | **yes** |
| `SpitfireMk8_2_N.webp` | 1024×1024 | 321 KB | normal | keep |
| `SpitfireMk8_2_ORM.webp` | 1024×1024 | 888 KB | orm | keep |

## 2. Every baseColor texture the model references

The 1 glTF file(s) reference 4 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
SpitfireMk8_1.webp
SpitfireMk8_2.webp
Spitfire_Fan.webp
Spitfire_Glass.webp
```

## 3. glTF files inside the model package

```
Aircraft_LOD_0.gltf
```

## 4. Livery directories (1)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| Royal Australian Air Force | `Generic` |

## 5. Package it

**Format: Few-part (legacy shading).** 3 baseColor images, one per body area, each its own PBR material.

### Files this aircraft needs

| file | dimensions | role | what to put there |
|---|---|---|---|
| `Spitfire_Fan.webp` | 1024x1024 | surface / **paint** | your artwork |
| `SpitfireMk8_2.webp` | 1024x1024 | surface / **paint** | your artwork |
| `SpitfireMk8_1.webp` | 1024x1024 | surface / **paint** | your artwork |
| `Spitfire_Fan_ORM.webp` | 512x512 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `SpitfireMk8_2_ORM.webp` | 1024x1024 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `Spitfire_Glass.webp` | 512x512 | glass / keep | your artwork |
| `SpitfireMk8_2_N.webp` | 1024x1024 | normal / keep | solid `(128,128,255)` - flat normal |
| `SpitfireMk8_1_ORM.webp` | 1024x1024 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `Shadow.webp` | 256x256 | surface / keep | your artwork |
| `Spitfire_Glass_ORM.webp` | 512x512 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `SpitfireMk8_1_N.webp` | 1024x1024 | normal / keep | solid `(128,128,255)` - flat normal |

### Option A - explicit list (copy and run)

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-spit \
  --livery-dir "<a directory from the table above>" \
  --texture "Spitfire_Fan.webp=art/Spitfire_Fan.png" \
  --texture "SpitfireMk8_2.webp=art/SpitfireMk8_2.png" \
  --texture "SpitfireMk8_1.webp=art/SpitfireMk8_1.png" \
  --texture "Spitfire_Fan_ORM.webp=art/Spitfire_Fan_ORM.png" \
  --texture "SpitfireMk8_2_ORM.webp=art/SpitfireMk8_2_ORM.png" \
  --texture "Spitfire_Glass.webp=art/Spitfire_Glass.png" \
  --texture "SpitfireMk8_2_N.webp=art/SpitfireMk8_2_N.png" \
  --texture "SpitfireMk8_1_ORM.webp=art/SpitfireMk8_1_ORM.png" \
  --texture "Shadow.webp=art/Shadow.png" \
  --texture "Spitfire_Glass_ORM.webp=art/Spitfire_Glass_ORM.png" \
  --texture "SpitfireMk8_1_N.webp=art/SpitfireMk8_1_N.png" \
  --out out/spit.zip
```

### Option B - auto mode

```bash
python tools/build_slip_package.py --auto --art art/ \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-spit \
  --livery-dir "<a directory from the table above>" \
  --out out/spit.zip
```

`--auto` reads `data/livery_files.json`, then looks for these stems in `art/`
(`.png`, `.webp`, `.jpg` are all accepted):

```
Shadow.png
SpitfireMk8_1.png
SpitfireMk8_1_N.png
SpitfireMk8_1_ORM.png
SpitfireMk8_2.png
SpitfireMk8_2_N.png
SpitfireMk8_2_ORM.png
Spitfire_Fan.png
Spitfire_Fan_ORM.png
Spitfire_Glass.png
Spitfire_Glass_ORM.png
```

### Option C - reuse the companions from an official package

The `keep` rows above are not artwork: they are masks the vendor ships. Rather than
recreating them, pull them out of an official livery package:

```bash
python tools/fetch_catalog.py --download --type AircraftLivery \
  --match spit --out dl/
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-spit \
  --livery-dir "<a directory from the table above>" \
  --texture "Spitfire_Fan.webp=art/Spitfire_Fan.png" \
  --texture "SpitfireMk8_2.webp=art/SpitfireMk8_2.png" \
  --texture "SpitfireMk8_1.webp=art/SpitfireMk8_1.png" \
  --keep-from dl/<downloaded package>.zip \
  --out out/spit.zip
```

`--keep-from` copies every entry in that archive **except** the albedo files, so your own
artwork always wins and the companions stay byte-identical to the vendor's.

### Where the entries land

```
android: ../../files/aircraft/infiniteflight-aircraft-spit/liveries/<directory>/<file>.webp
ios:     ../../Library/dlc/aircraft/infiniteflight-aircraft-spit/liveries/<directory>/<file>.webp
```

`<directory>` must come from the table in section 4 - the folder name, not the name the app
shows.

### How to tell it worked

Each listed file is its own material, so the repaint is all-or-nothing per part: a wing still in
official colours means `wing_*.webp` did not land, a dark hull means the `_ORM` partner is missing.

## 6. Import

```bash
adb push out/spit.zip /sdcard/Download/spit.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

