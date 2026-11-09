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

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-dc10f \
  --livery-dir "<livery directory>" \
  --texture "engine.webp=art/engine.png" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "misc.webp=art/misc.png" \
  --texture "tail.webp=art/tail.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  # ship these unchanged (a solid fill also works) \
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

Resolves to, on Android:

```
../../files/aircraft/infiniteflight-aircraft-dc10f/liveries/<livery directory>/<file name>
```

On iOS the root differs — replace `files` with `Library/dlc`:

```
../../Library/dlc/aircraft/infiniteflight-aircraft-dc10f/liveries/<livery directory>/<file name>
```

## 6. Import

```bash
adb push out/dc10f.zip /sdcard/Download/dc10f.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

