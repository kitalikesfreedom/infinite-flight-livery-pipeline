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

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-spit \
  --livery-dir "<livery directory>" \
  --texture "Spitfire_Fan.webp=art/Spitfire_Fan.png" \
  --texture "SpitfireMk8_2.webp=art/SpitfireMk8_2.png" \
  --texture "SpitfireMk8_1.webp=art/SpitfireMk8_1.png" \
  # ship these unchanged (a solid fill also works) \
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

Resolves to, on Android:

```
../../files/aircraft/infiniteflight-aircraft-spit/liveries/<livery directory>/<file name>
```

On iOS the root differs — replace `files` with `Library/dlc`:

```
../../Library/dlc/aircraft/infiniteflight-aircraft-spit/liveries/<livery directory>/<file name>
```

## 6. Import

```bash
adb push out/spit.zip /sdcard/Download/spit.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

