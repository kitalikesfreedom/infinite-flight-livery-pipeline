# Airbus A220-300 — `infiniteflight-aircraft-bcs3`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-bcs3` |
| Model path in package | `Aircraft/Airbus A220-300` |
| Model package | `710c84ae-6fdc-4c4a-ac3b-4031c3036e98` v25.3.52 · 18.0 MB |
| glTF files | 3 |
| Texture pipeline | **Multi-part (legacy shading)** |
| BaseColor images to paint | 5 |
| Entries in the official livery package | 5 |
| Livery packages | 23 named + 0 generic |
| Configuration package | `37a10f45-248b-43c5-b2c3-d168fdb5004d` · 25 KB |
| Sample livery parsed | Air Tanzania → `Aircraft/Airbus A220-300/Liveries/AirTanzania` |

> 5 baseColor images across fuselage, wings, engines, gear and details — each a separate PBR material, so a partial repaint shows up as a patchwork.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `Texture_01.webp` | 2048×2048 | 174 KB | surface | **yes** |
| `Texture_02.webp` | 2048×2048 | 232 KB | surface | **yes** |
| `Texture_03.webp` | 2048×2048 | 283 KB | surface | **yes** |
| `Texture_04.webp` | 2048×2048 | 167 KB | surface | **yes** |
| `Texture_05.webp` | 2048×2048 | 126 KB | surface | **yes** |

## 2. Every baseColor texture the model references

The 3 glTF file(s) reference 23 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
A220_ovh_lamps.webp
Pilot_01.webp
Pilot_02.webp
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
Texture_12.webp
Texture_13.webp
Texture_14.webp
Texture_15.webp
Texture_16.webp
Texture_17.webp
Texture_18.webp
screen_glass.webp
screen_glass_up.webp
```

## 3. glTF files inside the model package

```
Aircraft_LOD_0.gltf
Aircraft_LOD_1.gltf
Aircraft_LOD_2.gltf
```

## 4. Livery directories (23)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| Air Austral | `AirAustral` |
| Air Baltic | `AirBaltic` |
| Air Baltic - Estonian Flag | `AirBaltic2` |
| Airbus | `Airbus` |
| Air Canada | `AirCanada` |
| Air Canada - Retro | `AirCanadaRetro` |
| Air France | `AirFrance` |
| Air Manas | `AirManas` |
| Air Tanzania | `AirTanzania` |
| Air Vanuatu | `AirVanuatu` |
| Bombardier | `Bombardier` |
| Breeze Airways | `Breeze` |
| Delta Air Lines | `Delta` |
| EgyptAir | `Egyptair` |
| EgyptAir Express | `EgyptairExpress` |
| Generic | `Generic` |
| Ibom Air | `IbomAir` |
| Iraqi Airways | `IraqiAirways` |
| ITA Airways | `ITA Airways` |
| JetBlue | `JetBlue` |
| Korean Air | `KoreanAir` |
| QantasLink | `Qantas Link` |
| Swiss International Air Lines | `Swiss` |

## 5. Package it

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-bcs3 \
  --livery-dir "<livery directory>" \
  --texture "Texture_01.webp=art/Texture_01.png" \
  --texture "Texture_02.webp=art/Texture_02.png" \
  --texture "Texture_03.webp=art/Texture_03.png" \
  --texture "Texture_04.webp=art/Texture_04.png" \
  --texture "Texture_05.webp=art/Texture_05.png" \
  --out out/bcs3.zip
```

Resolves to, on Android:

```
../../files/aircraft/infiniteflight-aircraft-bcs3/liveries/<livery directory>/<file name>
```

On iOS the root differs — replace `files` with `Library/dlc`:

```
../../Library/dlc/aircraft/infiniteflight-aircraft-bcs3/liveries/<livery directory>/<file name>
```

## 6. Import

```bash
adb push out/bcs3.zip /sdcard/Download/bcs3.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

