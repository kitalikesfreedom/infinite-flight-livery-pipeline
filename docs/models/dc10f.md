# DC-10F — `infiniteflight-aircraft-dc10f`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-dc10f` |
| Model path in package | `Aircraft/DC-10F` |
| Model package | `e59fa7b4-b708-4480-aebd-26659a4f312b` v25.3.31 · 3.9 MB |
| glTF files | 1 |
| Texture pipeline | **Multi-part (legacy shading)** |
| BaseColor images to paint | 6 |
| Entries in the official livery package | 17 |
| Livery packages | 12 named + 0 generic |
| Configuration package | `c84dbbc0-339b-49ba-a110-00bca7dc087b` · 30 KB |
| Sample livery parsed | US Air Force - KC-10 Extender → `Aircraft/DC-10F/Liveries/KC-10 Extender USAF` |

> 6 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `engine.webp` | 2048×2048 | 124 KB | surface | **yes** |
| `engine_ORM.webp` | 2048×2048 | 1.2 MB | orm | keep |
| `fuse.webp` | 4096×4096 | 328 KB | surface | **yes** |
| `fuse_E.webp` | 2048×2048 | 10 KB | emissive | keep |
| `fuse_Emissive.webp` | 2048×2048 | 10 KB | surface | keep |
| `fuse_N.webp` | 2048×2048 | 518 KB | normal | keep |
| `fuse_ORM.webp` | 4096×4096 | 4.6 MB | orm | keep |
| `misc.webp` | 2048×2048 | 363 KB | surface | **yes** |
| `misc_ORM.webp` | 2048×2048 | 2.5 MB | orm | keep |
| `tail.webp` | 2048×2048 | 156 KB | surface | **yes** |
| `tail_E.webp` | 2048×2048 | 10 KB | emissive | keep |
| `tail_Emissive.webp` | 2048×2048 | 10 KB | surface | keep |
| `tail_ORM.webp` | 2048×2048 | 1.3 MB | orm | keep |
| `wingLH.webp` | 2048×2048 | 164 KB | surface | **yes** |
| `wingLH_ORM.webp` | 2048×2048 | 1.3 MB | orm | keep |
| `wingRH.webp` | 2048×2048 | 164 KB | surface | **yes** |
| `wingRH_ORM.webp` | 1024×1024 | 420 KB | orm | keep |

## 2. Every baseColor texture the model references

The 1 glTF file(s) reference 14 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
Cockpit_Datails.webp
Cockpit_Environment.webp
Cockpit_Text.webp
Korry_Legends.webp
Pilot_01.webp
Pilot_02.webp
boom.webp
engine.webp
fuse.webp
glass.webp
misc.webp
tail.webp
wingLH.webp
wingRH.webp
```

## 3. glTF files inside the model package

```
Aircraft_LOD_0.gltf
```

## 4. Livery directories (12)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| 10 Tanker Air Carrier | `10 Air Tanker Carrier` |
| Arrow Air | `Arrow Air` |
| Avient | `Avient` |
| DAS Air Cargo | `DAS Air Cargo` |
| Emery Worldwide | `Emery Worldwide` |
| FedEx | `Fedex` |
| Gemini Air Cargo | `Gemini Air Cargo` |
| Generic | `Generic` |
| US Air Force - KC-10 Extender | `KC-10 Extender USAF` |
| Royal Netherlands Air Force - KDC-10 | `KDC-10 RNAF` |
| Kelowna Flightcraft Air Charter | `Kelowna Flightcraft Air Charter` |
| Solar Cargo | `Solar Cargo` |

## 5. Package it

**Format: Multi-part (legacy shading).** 6 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

### Files this aircraft needs

| file | dimensions | role | what to put there |
|---|---|---|---|
| `engine.webp` | 2048x2048 | surface / **paint** | your artwork |
| `fuse.webp` | 4096x4096 | surface / **paint** | your artwork |
| `misc.webp` | 2048x2048 | surface / **paint** | your artwork |
| `tail.webp` | 2048x2048 | surface / **paint** | your artwork |
| `wingLH.webp` | 2048x2048 | surface / **paint** | your artwork |
| `wingRH.webp` | 2048x2048 | surface / **paint** | your artwork |
| `engine_ORM.webp` | 2048x2048 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `fuse_E.webp` | 2048x2048 | emissive / keep | ship as-is unless you want glowing panels |
| `fuse_Emissive.webp` | 2048x2048 | surface / keep | your artwork |
| `fuse_N.webp` | 2048x2048 | normal / keep | solid `(128,128,255)` - flat normal |
| `fuse_ORM.webp` | 4096x4096 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `misc_ORM.webp` | 2048x2048 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `tail_E.webp` | 2048x2048 | emissive / keep | ship as-is unless you want glowing panels |
| `tail_Emissive.webp` | 2048x2048 | surface / keep | your artwork |
| `tail_ORM.webp` | 2048x2048 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `wingLH_ORM.webp` | 2048x2048 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |
| `wingRH_ORM.webp` | 1024x1024 | orm / keep | solid `(255,200,0)` - no occlusion, fully rough, non-metal |

### Option A - explicit list (copy and run)

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-dc10f \
  --livery-dir "<a directory from the table above>" \
  --texture "engine.webp=art/engine.png" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "misc.webp=art/misc.png" \
  --texture "tail.webp=art/tail.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  --texture "engine_ORM.webp=art/engine_ORM.png" \
  --texture "fuse_E.webp=art/fuse_E.png" \
  --texture "fuse_Emissive.webp=art/fuse_Emissive.png" \
  --texture "fuse_N.webp=art/fuse_N.png" \
  --texture "fuse_ORM.webp=art/fuse_ORM.png" \
  --texture "misc_ORM.webp=art/misc_ORM.png" \
  --texture "tail_E.webp=art/tail_E.png" \
  --texture "tail_Emissive.webp=art/tail_Emissive.png" \
  --texture "tail_ORM.webp=art/tail_ORM.png" \
  --texture "wingLH_ORM.webp=art/wingLH_ORM.png" \
  --texture "wingRH_ORM.webp=art/wingRH_ORM.png" \
  --out out/dc10f.zip
```

### Option B - auto mode

```bash
python tools/build_slip_package.py --auto --art art/ \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-dc10f \
  --livery-dir "<a directory from the table above>" \
  --out out/dc10f.zip
```

`--auto` reads `data/livery_files.json`, then looks for these stems in `art/`
(`.png`, `.webp`, `.jpg` are all accepted):

```
engine.png
engine_ORM.png
fuse.png
fuse_E.png
fuse_Emissive.png
fuse_N.png
fuse_ORM.png
misc.png
misc_ORM.png
tail.png
tail_E.png
tail_Emissive.png
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
  --match dc10f --out dl/
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-dc10f \
  --livery-dir "<a directory from the table above>" \
  --texture "engine.webp=art/engine.png" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "misc.webp=art/misc.png" \
  --texture "tail.webp=art/tail.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  --keep-from dl/<downloaded package>.zip \
  --out out/dc10f.zip
```

`--keep-from` copies every entry in that archive **except** the albedo files, so your own
artwork always wins and the companions stay byte-identical to the vendor's.

### Where the entries land

```
android: ../../files/aircraft/infiniteflight-aircraft-dc10f/liveries/<directory>/<file>.webp
ios:     ../../Library/dlc/aircraft/infiniteflight-aircraft-dc10f/liveries/<directory>/<file>.webp
```

`<directory>` must come from the table in section 4 - the folder name, not the name the app
shows.

### How to tell it worked

Each listed file is its own material, so the repaint is all-or-nothing per part: a wing still in
official colours means `wing_*.webp` did not land, a dark hull means the `_ORM` partner is missing.

## 6. Import

```bash
adb push out/dc10f.zip /sdcard/Download/dc10f.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

