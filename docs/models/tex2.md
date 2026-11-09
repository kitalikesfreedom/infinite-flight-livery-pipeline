# T6 Texan II — `infiniteflight-aircraft-tex2`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-tex2` |
| Model path in package | `Aircraft/T6 Texan II` |
| Model package | `acf7ff54-8ddc-465c-ba96-dc1c5fc204cd` v25.3.21 · 7.9 MB |
| glTF files | 1 |
| Texture pipeline | **Multi-part (legacy shading)** |
| BaseColor images to paint | 5 |
| Entries in the official livery package | 5 |
| Livery packages | 8 named + 3 generic |
| Configuration package | `5ff37d82-e563-4586-8dc0-24ba0163eda3` · 16 KB |
| Sample livery parsed | US Air Force → `Aircraft/T6 Texan II/Liveries/US Air Force` |

> 5 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `body_center.webp` | 4096×4096 | 627 KB | surface | **yes** |
| `body_front.webp` | 4096×4096 | 433 KB | surface | **yes** |
| `tail.webp` | 4096×4096 | 806 KB | surface | **yes** |
| `wing_left.webp` | 4096×4096 | 572 KB | surface | **yes** |
| `wing_right.webp` | 4096×4096 | 564 KB | surface | **yes** |

## 2. Every baseColor texture the model references

The 1 glTF file(s) reference 15 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
A10_Pilot.webp
A10_Pilot_head.webp
Glass.webp
Texture_01.webp
Texture_02.webp
Texture_03.webp
Texture_04.webp
Texture_05.webp
Texture_06.webp
Texture_07.webp
Texture_08.webp
Texture_09.webp
Texture_10.webp
Texture_11.webp
propeller.webp
```

## 3. glTF files inside the model package

```
Aircraft_LOD_0.gltf
```

## 4. Livery directories (8)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| Hellenic Air Force | `Hellenic Air Force` |
| Beechcraft | `House Livery` |
| Mexican Air Force | `Mexican Air Force` |
| Royal Air Force | `Royal Air Force` |
| Royal Canadian Air Force | `Royal Canadian Air Force` |
| Royal New Zealand Air Force | `Royal New Zealand Air Force` |
| US Air Force | `US Air Force` |
| US Navy | `US Navy` |

Generic packages: T6 Texan II → `?`, T6 Texan II → `?`, T6 Texan II → `?`

## 5. Package it

**Format: Multi-part (legacy shading).** 5 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

### Files this aircraft needs

| file | dimensions | role | what to put there |
|---|---|---|---|
| `body_center.webp` | 4096x4096 | surface / **paint** | your artwork |
| `body_front.webp` | 4096x4096 | surface / **paint** | your artwork |
| `tail.webp` | 4096x4096 | surface / **paint** | your artwork |
| `wing_left.webp` | 4096x4096 | surface / **paint** | your artwork |
| `wing_right.webp` | 4096x4096 | surface / **paint** | your artwork |

### Option A - explicit list (copy and run)

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-tex2 \
  --livery-dir "<a directory from the table above>" \
  --texture "body_center.webp=art/body_center.png" \
  --texture "body_front.webp=art/body_front.png" \
  --texture "tail.webp=art/tail.png" \
  --texture "wing_left.webp=art/wing_left.png" \
  --texture "wing_right.webp=art/wing_right.png" \
  --out out/tex2.zip
```

### Option B - auto mode

```bash
python tools/build_slip_package.py --auto --art art/ \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-tex2 \
  --livery-dir "<a directory from the table above>" \
  --out out/tex2.zip
```

`--auto` reads `data/livery_files.json`, then looks for these stems in `art/`
(`.png`, `.webp`, `.jpg` are all accepted):

```
body_center.png
body_front.png
tail.png
wing_left.png
wing_right.png
```

### Where the entries land

```
android: ../../files/aircraft/infiniteflight-aircraft-tex2/liveries/<directory>/<file>.webp
ios:     ../../Library/dlc/aircraft/infiniteflight-aircraft-tex2/liveries/<directory>/<file>.webp
```

`<directory>` must come from the table in section 4 - the folder name, not the name the app
shows.

### How to tell it worked

Each listed file is its own material, so the repaint is all-or-nothing per part: a wing still in
official colours means `wing_*.webp` did not land, a dark hull means the `_ORM` partner is missing.

## 6. Import

```bash
adb push out/tex2.zip /sdcard/Download/tex2.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

