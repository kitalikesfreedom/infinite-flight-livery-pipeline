# CRJ-200 — `infiniteflight-aircraft-crj2`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-crj2` |
| Model path in package | `Aircraft/CRJ-200-2018` |
| Model package | `24364e52-3788-487f-9f98-00f38b1f459c` v25.3.53 · 5.7 MB |
| glTF files | 4 |
| Texture pipeline | **Multi-part (legacy shading)** |
| BaseColor images to paint | 4 |
| Entries in the official livery package | 4 |
| Livery packages | 14 named + 0 generic |
| Configuration package | `66616dd7-9703-47ec-8666-22c3a1f26e04` · 24 KB |
| Sample livery parsed | Air Canada Express → `Aircraft/CRJ-200-2018/Liveries/Air Canada Express` |

> 4 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `eng.webp` | 2048×2048 | 176 KB | surface | **yes** |
| `fuse.webp` | 2048×2048 | 318 KB | surface | **yes** |
| `wingLH.webp` | 2048×2048 | 115 KB | surface | **yes** |
| `wingRH.webp` | 2048×2048 | 115 KB | surface | **yes** |

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
| Air Canada Express | `Air Canada Express` |
| American Eagle | `American Eagle` |
| Aruba Airlines | `Aruba Airlines` |
| Belavia | `Belavia Belarusian Airlines` |
| Delta Air Lines | `Delta Air Lines` |
| Generic | `Generic` |
| Infinite Flight - 2018 | `Infinite Flight` |
| J-Air | `J-Air` |
| Kendell Airlines | `Kendell Airlines` |
| MexicanaLink | `Mexicana Link` |
| Northwest Airlines | `Northwest Airlines` |
| SA Express | `South African Express` |
| United Express - Old | `United Express` |
| UTair Aviation | `UTair Aviation` |

## 5. Package it

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-crj2 \
  --livery-dir "<livery directory>" \
  --texture "eng.webp=art/eng.png" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  --out out/crj2.zip
```

Resolves to, on Android:

```
../../files/aircraft/infiniteflight-aircraft-crj2/liveries/<livery directory>/<file name>
```

On iOS the root differs — replace `files` with `Library/dlc`:

```
../../Library/dlc/aircraft/infiniteflight-aircraft-crj2/liveries/<livery directory>/<file name>
```

## 6. Import

```bash
adb push out/crj2.zip /sdcard/Download/crj2.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

