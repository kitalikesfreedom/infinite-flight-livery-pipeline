# MD-11F — `infiniteflight-aircraft-md11f`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-md11f` |
| Model path in package | `Aircraft/MD-11F` |
| Model package | `3f78766a-30c8-4d65-95ae-ebc2fb758aac` v25.3.30 · 5.3 MB |
| glTF files | 4 |
| Texture pipeline | **Multi-part (legacy shading)** |
| BaseColor images to paint | 6 |
| Entries in the official livery package | 6 |
| Livery packages | 11 named + 0 generic |
| Configuration package | `b843eaa4-56e5-499a-9fd3-764a4d613c91` · 30 KB |
| Sample livery parsed | Centurion Air Cargo → `Aircraft/MD-11F/Liveries/Centurion Air Cargo` |

> 6 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `engine.webp` | 2048×2048 | 144 KB | surface | **yes** |
| `fuse.webp` | 4096×4096 | 404 KB | surface | **yes** |
| `misc.webp` | 2048×2048 | 355 KB | surface | **yes** |
| `tail.webp` | 2048×2048 | 186 KB | surface | **yes** |
| `wingLH.webp` | 2048×2048 | 179 KB | surface | **yes** |
| `wingRH.webp` | 2048×2048 | 171 KB | surface | **yes** |

## 2. Every baseColor texture the model references

The 4 glTF file(s) reference 13 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
Cockpit_Datails.webp
Cockpit_Environment.webp
Cockpit_Text.webp
Korry_Legends.webp
Pilot_01.webp
Pilot_02.webp
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
Aircraft_LOD_1.gltf
Aircraft_LOD_3.gltf
Aircraft_LOD_2.gltf
```

## 4. Livery directories (11)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| Aeroflot Cargo | `Aeroflot Cargo` |
| Centurion Air Cargo | `Centurion Air Cargo` |
| Ethiopian Cargo | `Ethiopian Airlines` |
| FedEx | `Fedex` |
| Generic | `Generic` |
| Lufthansa Cargo | `Lufthansa Cargo` |
| Martinair Cargo | `Martinair Cargo` |
| Saudia | `Saudia` |
| UPS | `UPS` |
| Varig Log | `VARIG LOG` |
| World Airways | `World Airways` |

## 5. Package it

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-md11f \
  --livery-dir "<livery directory>" \
  --texture "engine.webp=art/engine.png" \
  --texture "fuse.webp=art/fuse.png" \
  --texture "misc.webp=art/misc.png" \
  --texture "tail.webp=art/tail.png" \
  --texture "wingLH.webp=art/wingLH.png" \
  --texture "wingRH.webp=art/wingRH.png" \
  --out out/md11f.zip
```

Resolves to, on Android:

```
../../files/aircraft/infiniteflight-aircraft-md11f/liveries/<livery directory>/<file name>
```

On iOS the root differs — replace `files` with `Library/dlc`:

```
../../Library/dlc/aircraft/infiniteflight-aircraft-md11f/liveries/<livery directory>/<file name>
```

## 6. Import

```bash
adb push out/md11f.zip /sdcard/Download/md11f.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

