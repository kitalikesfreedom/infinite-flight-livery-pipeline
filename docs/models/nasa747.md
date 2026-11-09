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

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-nasa747 \
  --livery-dir "<livery directory>" \
  --texture "74SP.ktx2=art/74SP.ktx2" \
  --texture "74SP_ORM.ktx2=art/74SP_ORM.ktx2" \
  --texture "Shadow.ktx2=art/Shadow.ktx2" \
  # ship these unchanged (a solid fill also works) \
  --texture "B747_Cockpit.ktx2=art/B747_Cockpit.ktx2" \
  --texture "B747_Cockpit_ORM.ktx2=art/B747_Cockpit_ORM.ktx2" \
  --texture "B747_Glass.ktx2=art/B747_Glass.ktx2" \
  --texture "B747_Glass_ORM.ktx2=art/B747_Glass_ORM.ktx2" \
  --out out/nasa747.zip
```

Resolves to, on Android:

```
../../files/aircraft/infiniteflight-aircraft-nasa747/liveries/<livery directory>/<file name>
```

On iOS the root differs — replace `files` with `Library/dlc`:

```
../../Library/dlc/aircraft/infiniteflight-aircraft-nasa747/liveries/<livery directory>/<file name>
```

## 6. Import

```bash
adb push out/nasa747.zip /sdcard/Download/nasa747.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

