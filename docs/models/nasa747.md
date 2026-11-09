# Boeing 747-SOFIA — `infiniteflight-aircraft-nasa747`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-nasa747` |
| Model path in package | `Aircraft/Boeing 747-SOFIA` |
| Model package | `3ee45d20-1984-4d95-a753-3696e35cdf77` v25.3.37 · 1.7 MB |
| glTF files | 1 |
| Texture pipeline | **Few-part (legacy shading)** |
| BaseColor images to paint | 3 |
| Entries in the official livery package | 7 |
| Livery packages | 1 named + 1 generic |
| Configuration package | `538ac7be-08c0-4571-9048-aafcee7b6285` · 16 KB |
| Sample livery parsed | SOFIA → `Aircraft/Boeing 747-SOFIA/Liveries/Generic` |

> 3 baseColor images, one per body area, each its own PBR material.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `74SP.ktx2` | ? | 185 KB | surface | **yes** |
| `74SP_ORM.ktx2` | ? | 43 KB | orm | **yes** |
| `B747_Cockpit.ktx2` | ? | 198 KB | interior | keep |
| `B747_Cockpit_ORM.ktx2` | ? | 76 KB | orm | keep |
| `B747_Glass.ktx2` | ? | 2 KB | glass | keep |
| `B747_Glass_ORM.ktx2` | ? | 17 KB | orm | keep |
| `Shadow.ktx2` | ? | 51 KB | surface | **yes** |

## 2. Every baseColor texture the model references

The 1 glTF file(s) reference 3 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
74SP.webp
B747_Cockpit.webp
B747_Glass.webp
```

## 3. glTF files inside the model package

```
Aircraft_LOD_0.gltf
```

## 4. Livery directories (1)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| SOFIA | `Generic` |

Generic packages: Boeing 747-SOFIA → `?`

## 5. Package it

**Format: Few-part (legacy shading).** 3 baseColor images, one per body area, each its own PBR material.

### Files this aircraft needs

| file | dimensions | role | what to put there |
|---|---|---|---|
| `74SP.ktx2` | ? | surface / **paint** | your artwork |
| `74SP_ORM.ktx2` | ? | orm / **paint** | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `Shadow.ktx2` | ? | surface / **paint** | your artwork |
| `B747_Cockpit.ktx2` | ? | interior / keep | your artwork |
| `B747_Cockpit_ORM.ktx2` | ? | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `B747_Glass.ktx2` | ? | glass / keep | your artwork |
| `B747_Glass_ORM.ktx2` | ? | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |

### Option A - explicit list (copy and run)

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-nasa747 \
  --livery-dir "<a directory from the table above>" \
  --texture "74SP.ktx2=art/74SP.png" \
  --texture "74SP_ORM.ktx2=art/74SP_ORM.png" \
  --texture "Shadow.ktx2=art/Shadow.png" \
  --texture "B747_Cockpit.ktx2=art/B747_Cockpit.png" \
  --texture "B747_Cockpit_ORM.ktx2=art/B747_Cockpit_ORM.png" \
  --texture "B747_Glass.ktx2=art/B747_Glass.png" \
  --texture "B747_Glass_ORM.ktx2=art/B747_Glass_ORM.png" \
  --out out/nasa747.zip
```

### Option B - auto mode

```bash
python tools/build_slip_package.py --auto --art art/ \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-nasa747 \
  --livery-dir "<a directory from the table above>" \
  --out out/nasa747.zip
```

`--auto` reads `data/livery_files.json`, then looks for these stems in `art/`
(`.png`, `.webp`, `.jpg` are all accepted):

```
74SP.png
74SP_ORM.png
B747_Cockpit.png
B747_Cockpit_ORM.png
B747_Glass.png
B747_Glass_ORM.png
Shadow.png
```

### Option C - reuse the companions from an official package

The `keep` rows above are not artwork: they are masks the vendor ships. Rather than
recreating them, pull them out of an official livery package:

```bash
python tools/fetch_catalog.py --download --type AircraftLivery \
  --match nasa747 --out dl/
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-nasa747 \
  --livery-dir "<a directory from the table above>" \
  --texture "74SP.ktx2=art/74SP.png" \
  --texture "74SP_ORM.ktx2=art/74SP_ORM.png" \
  --texture "Shadow.ktx2=art/Shadow.png" \
  --keep-from dl/<downloaded package>.zip \
  --out out/nasa747.zip
```

`--keep-from` copies every entry in that archive **except** the albedo files, so your own
artwork always wins and the companions stay byte-identical to the vendor's.

### Where the entries land

```
android: ../../files/aircraft/infiniteflight-aircraft-nasa747/liveries/<directory>/<file>.webp
ios:     ../../Library/dlc/aircraft/infiniteflight-aircraft-nasa747/liveries/<directory>/<file>.webp
```

`<directory>` must come from the table in section 4 - the folder name, not the name the app
shows.

### How to tell it worked

Each listed file is its own material, so the repaint is all-or-nothing per part: a wing still in
official colours means `wing_*.webp` did not land, a dark hull means the `_ORM` partner is missing.

## 6. Import

```bash
adb push out/nasa747.zip /sdcard/Download/nasa747.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

