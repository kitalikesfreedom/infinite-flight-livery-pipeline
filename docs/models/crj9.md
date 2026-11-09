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

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-crj9 \
  --livery-dir "<livery directory>" \
  --texture "eng.webp=art/eng.png" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  # ship these unchanged (a solid fill also works) \
  --texture "wingLH (1).webp=art/wingLH (1).png" \
  --out out/crj9.zip
```

Resolves to, on Android:

```
../../files/aircraft/infiniteflight-aircraft-crj9/liveries/<livery directory>/<file name>
```

On iOS the root differs — replace `files` with `Library/dlc`:

```
../../Library/dlc/aircraft/infiniteflight-aircraft-crj9/liveries/<livery directory>/<file name>
```

## 6. Import

```bash
adb push out/crj9.zip /sdcard/Download/crj9.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

