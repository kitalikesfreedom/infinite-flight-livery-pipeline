# CRJ-900 — `infiniteflight-aircraft-crj9`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-crj9` |
| Model path in package | `Aircraft/CRJ-900` |
| Model package | `958486b0-1ef4-4efd-bee0-ea94e96f6c96` v25.3.47 · 7.7 MB |
| glTF files | 4 |
| Texture pipeline | **Multi-part (legacy shading)** |
| BaseColor images to paint | 4 |
| Entries in the official livery package | 5 |
| Livery packages | 14 named + 0 generic |
| Configuration package | `4af743ff-822b-484c-a792-0f237bc14e3c` · 25 KB |
| Sample livery parsed | Tunisair Express → `Aircraft/CRJ-900/Liveries/Tunisair Express` |

> 4 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `eng.webp` | 2048×2048 | 180 KB | surface | **yes** |
| `fuse.webp` | 2048×2048 | 195 KB | surface | **yes** |
| `wingLH (1).webp` | 4096×4096 | 275 KB | surface | keep |
| `wingLH.webp` | 2048×2048 | 113 KB | surface | **yes** |
| `wingRH.webp` | 2048×2048 | 127 KB | surface | **yes** |

## 2. Every baseColor texture the model references

The 4 glTF file(s) reference 14 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
CRJ_ovh_lamps.webp
Cockpit_Datails.webp
Cockpit_Environment.webp
Interior.webp
Pilot_01.webp
Pilot_02.webp
eng.webp
fuse.webp
glass.webp
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

## 4. Livery directories (14)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| Air Canada Express | `Air Canada` |
| AirOne | `AirOne` |
| American Eagle | `American Eagle` |
| Bombardier | `Bombardier House Colour` |
| China Express Airlines | `China Express Airlines` |
| Delta Air Lines | `Delta Air Lines` |
| Eurowings | `Eurowings` |
| Generic | `Generic` |
| Iraqi Airways | `Iraqi Airways` |
| Lufthansa CityLine- 2018 | `Lufthansa 2018` |
| Lufthansa CityLine | `Lufthansa Cityline` |
| Northwest Airlines | `Northwest Airlines` |
| Scandinavian Airlines | `SAS` |
| Tunisair Express | `Tunisair Express` |

## 5. Package it

**Format: Multi-part (legacy shading).** 4 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

### Files this aircraft needs

| file | dimensions | role | what to put there |
|---|---|---|---|
| `eng.webp` | 2048x2048 | surface / **paint** | your artwork |
| `fuse.webp` | 2048x2048 | surface / **paint** | your artwork |
| `wingLH.webp` | 2048x2048 | surface / **paint** | your artwork |
| `wingRH.webp` | 2048x2048 | surface / **paint** | your artwork |
| `wingLH (1).webp` | 4096x4096 | surface / keep | your artwork |

### Option A - explicit list (copy and run)

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-crj9 \
  --livery-dir "<a directory from the table above>" \
  --texture "eng.webp=art/eng.png" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  --texture "wingLH (1).webp=art/wingLH (1).png" \
  --out out/crj9.zip
```

### Option B - auto mode

```bash
python tools/build_slip_package.py --auto --art art/ \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-crj9 \
  --livery-dir "<a directory from the table above>" \
  --out out/crj9.zip
```

`--auto` reads `data/livery_files.json`, then looks for these stems in `art/`
(`.png`, `.webp`, `.jpg` are all accepted):

```
eng.png
fuse.png
wingLH.png
wingLH (1).png
wingRH.png
```

### Option C - reuse the companions from an official package

The `keep` rows above are not artwork: they are masks the vendor ships. Rather than
recreating them, pull them out of an official livery package:

```bash
python tools/fetch_catalog.py --download --type AircraftLivery \
  --match crj9 --out dl/
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-crj9 \
  --livery-dir "<a directory from the table above>" \
  --texture "eng.webp=art/eng.png" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  --keep-from dl/<downloaded package>.zip \
  --out out/crj9.zip
```

`--keep-from` copies every entry in that archive **except** the albedo files, so your own
artwork always wins and the companions stay byte-identical to the vendor's.

### Where the entries land

```
android: ../../files/aircraft/infiniteflight-aircraft-crj9/liveries/<directory>/<file>.webp
ios:     ../../Library/dlc/aircraft/infiniteflight-aircraft-crj9/liveries/<directory>/<file>.webp
```

`<directory>` must come from the table in section 4 - the folder name, not the name the app
shows.

### How to tell it worked

Each listed file is its own material, so the repaint is all-or-nothing per part: a wing still in
official colours means `wing_*.webp` did not land, a dark hull means the `_ORM` partner is missing.

## 6. Import

```bash
adb push out/crj9.zip /sdcard/Download/crj9.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

