# Piper PA28 Archer — `infiniteflight-aircraft-pa28a`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-pa28a` |
| Model path in package | `Aircraft/PA28` |
| Model package | `b86afd1f-fa16-47e2-b803-8caaba5323a9` v25.3.33 · 15.2 MB |
| glTF files | 3 |
| Texture pipeline | **Multi-part (legacy shading)** |
| BaseColor images to paint | 5 |
| Entries in the official livery package | 18 |
| Livery packages | 10 named + 0 generic |
| Configuration package | `164a91e5-2625-4ce8-9dc4-f9a90cc8fc98` · 21 KB |
| Sample livery parsed | CAE Oxford Aviation Academy → `Liveries/04_CAE Oxford Aviation Academy` |

> 5 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `M_Fuselage_1_basecolor.webp` | 4096×4096 | 279 KB | surface | **yes** |
| `M_Fuselage_1_emissive.webp` | 2048×2048 | 8 KB | surface | keep |
| `M_Fuselage_1_normal.webp` | 2048×2048 | 1.8 MB | surface | keep |
| `M_Fuselage_1_orm.webp` | 1024×1024 | 387 KB | orm | keep |
| `M_Fuselage_2_basecolor.webp` | 4096×4096 | 392 KB | surface | **yes** |
| `M_Fuselage_2_emissive.webp` | 2048×2048 | 9 KB | surface | keep |
| `M_Fuselage_2_normal.webp` | 2048×2048 | 2.0 MB | surface | keep |
| `M_Fuselage_2_orm.webp` | 1024×1024 | 307 KB | orm | keep |
| `M_Fuselage_3_basecolor.webp` | 4096×4096 | 391 KB | surface | **yes** |
| `M_Fuselage_3_emissive.webp` | 2048×2048 | 8 KB | surface | keep |
| `M_Fuselage_3_normal.webp` | 2048×2048 | 1.7 MB | surface | keep |
| `M_Fuselage_3_orm.webp` | 1024×1024 | 412 KB | orm | keep |
| `M_Fuselage_4_basecolor.webp` | 4096×4096 | 307 KB | surface | **yes** |
| `M_Fuselage_4_normal.webp` | 2048×2048 | 1.5 MB | surface | keep |
| `M_Fuselage_4_orm.webp` | 1024×1024 | 464 KB | orm | keep |
| `M_Propeller_basecolor.webp` | 2048×2048 | 250 KB | surface | **yes** |
| `M_Propeller_normal.webp` | 2048×2048 | 2.4 MB | surface | keep |
| `M_Propeller_orm.webp` | 1024×1024 | 704 KB | orm | keep |

## 2. Every baseColor texture the model references

The 3 glTF file(s) reference 18 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
M_AnalogPanel_basecolor.webp
M_CockpitStructure_AIII_01_albd.webp
M_CockpitStructure_AIII_02_albd.webp
M_CockpitStructure_AIII_03_albd.webp
M_CockpitStructure_AIII_04_albd.webp
M_Cockpit_Controls_AIII_basecolor.webp
M_DigitalPanel_basecolor.webp
M_ExtraObjects_albd.webp
M_Fuselage_1_basecolor.webp
M_Fuselage_2_basecolor.webp
M_Fuselage_3_basecolor.webp
M_Fuselage_4_basecolor.webp
M_Glass_basecolor.webp
M_LandingGear_basecolor.webp
M_PanelStructure_basecolor.webp
M_Propeller_basecolor.webp
M_Seats_AIII_basecolor.webp
PropellerBlurred_basecolor.webp
```

## 3. glTF files inside the model package

```
Aircraft_LOD_0.gltf
Aircraft_LOD_1.gltf
Aircraft_LOD_2.gltf
```

## 4. Livery directories (10)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| ATP Flight School | `01_ATP Flight School` |
| Infinite Flight Academy | `02_Infinite Flight Academy` |
| L3 European Airline Academy | `03_L3 European Airline Academy` |
| CAE Oxford Aviation Academy | `04_CAE Oxford Aviation Academy` |
| Xian Aoxiang General Aviation | `05_Xian Aoxiang General Aviation` |
| University of North Dakota | `06_University of North Dakota` |
| AV8 Flight School | `07_AV8 Flight School` |
| DEKKP | `08_DEKKP` |
| N57MA | `09_N57MA` |
| Generic | `Generic` |

## 5. Package it

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-pa28a \
  --livery-dir "<livery directory>" \
  --texture "M_Fuselage_1_basecolor.webp=art/M_Fuselage_1_basecolor.png" \
  --texture "M_Fuselage_2_basecolor.webp=art/M_Fuselage_2_basecolor.png" \
  --texture "M_Fuselage_3_basecolor.webp=art/M_Fuselage_3_basecolor.png" \
  --texture "M_Fuselage_4_basecolor.webp=art/M_Fuselage_4_basecolor.png" \
  --texture "M_Propeller_basecolor.webp=art/M_Propeller_basecolor.png" \
  # ship these unchanged (a solid fill also works) \
  --texture "M_Fuselage_1_emissive.webp=art/M_Fuselage_1_emissive.png" \
  --texture "M_Fuselage_1_normal.webp=art/M_Fuselage_1_normal.png" \
  --texture "M_Fuselage_1_orm.webp=art/M_Fuselage_1_orm.png" \
  --texture "M_Fuselage_2_emissive.webp=art/M_Fuselage_2_emissive.png" \
  --texture "M_Fuselage_2_normal.webp=art/M_Fuselage_2_normal.png" \
  --texture "M_Fuselage_2_orm.webp=art/M_Fuselage_2_orm.png" \
  --texture "M_Fuselage_3_emissive.webp=art/M_Fuselage_3_emissive.png" \
  --texture "M_Fuselage_3_normal.webp=art/M_Fuselage_3_normal.png" \
  --texture "M_Fuselage_3_orm.webp=art/M_Fuselage_3_orm.png" \
  --texture "M_Fuselage_4_normal.webp=art/M_Fuselage_4_normal.png" \
  --texture "M_Fuselage_4_orm.webp=art/M_Fuselage_4_orm.png" \
  --texture "M_Propeller_normal.webp=art/M_Propeller_normal.png" \
  --texture "M_Propeller_orm.webp=art/M_Propeller_orm.png" \
  --out out/pa28a.zip
```

Resolves to, on Android:

```
../../files/aircraft/infiniteflight-aircraft-pa28a/liveries/<livery directory>/<file name>
```

On iOS the root differs — replace `files` with `Library/dlc`:

```
../../Library/dlc/aircraft/infiniteflight-aircraft-pa28a/liveries/<livery directory>/<file name>
```

## 6. Import

```bash
adb push out/pa28a.zip /sdcard/Download/pa28a.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

