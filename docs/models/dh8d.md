# Bombardier Dash 8-Q400 — `infiniteflight-aircraft-dh8d`

[← all aircraft](index.md)

| field | value |
|---|---|
| Repository name | `infiniteflight-aircraft-dh8d` |
| Model path in package | `Aircraft/Dash-8 Q400` |
| Model package | `3098345e-1152-4441-96ec-40a71179a24f` v25.3.58 · 2.8 MB |
| glTF files | 1 |
| Texture pipeline | **Legacy (single texture)** |
| BaseColor images to paint | 1 |
| Entries in the official livery package | 2 |
| Livery packages | 29 named + 0 generic |
| Configuration package | `5d94c2e8-fef9-41db-adad-44124f38f4f3` · 22 KB |
| Sample livery parsed | Securite Civile → `Aircraft/Dash-8 Q400/Liveries/Securite Civile` |

> One 2048x2048 baseColor image. Replace it together with `Texture_ORM.webp` and `Texture_N.webp`, or the fuselage renders as black chrome.

## 1. Inventory of one official package

These are the exact entries that livery package ships, at their real dimensions. The
`paint` column marks the baseColor images — the ones you actually draw. Everything
else is a PBR companion (`_ORM`, `_comp`, `_norm`, `_emis`) that must be present so the
material does not fall back to a default channel value.

| file | dimensions | bytes | role | paint |
|---|---|---|---|---|
| `Texture.webp` | 2048×2048 | 265 KB | surface | **yes** |
| `Texture_Emissive.webp` | 128×128 | 0 KB | surface | keep |

## 2. Every baseColor texture the model references

The 1 glTF file(s) reference 9 distinct baseColor images in total.
Cockpit, glass, pilot and interior materials are included here for completeness — repainting
them changes the cockpit, not the airframe.

```
Cockpit_1.webp
Cockpit_2.webp
Cockpit_3.webp
Cockpit_4.webp
DH8D_ovh_lamps.webp
Glass.webp
PropellerQ400.webp
Texture.webp
screen_glass.webp
```

## 3. glTF files inside the model package

```
Aircraft_LOD_0.gltf
```

## 4. Livery directories (29)

The directory name is `Path.GetFileName(LiveryPackage.Path)` — **not** what the app shows.

| shown as | directory on disk |
|---|---|
| Air Baltic | `Air Baltic` |
| Air Berlin | `Air Berlin` |
| Air Canada Express | `Air Canada Jazz` |
| ANA | `ANA Nippon` |
| Austrian Airlines | `Austrian Airlines` |
| Bombardier | `Bombardier` |
| Congo Airways | `CongoAirways` |
| Croatia Airlines | `Croatia Airlines` |
| Ethiopian Airlines | `Ethiopian` |
| Flybe | `Flybe` |
| Infinite Flight - 2015 | `FlyingDevStudio2015` |
| Generic | `Generic` |
| Horizon Air | `Horizon Air` |
| Icelandair | `Icelandair` |
| Island Air | `Island Air` |
| Lufthansa Regional | `Lufthansa Regional` |
| Luxair | `Luxair` |
| Malev | `Malev` |
| PAL Express | `PAL Express` |
| Porter Airlines | `Porter Airlines` |
| QantasLink | `QantasLink` |
| SA Express | `SA Express` |
| Securite Civile | `Securite Civile` |
| SpiceJet | `SpiceJet` |
| Tassili Algeria | `Tasili Algeria` |
| United Express | `United Express` |
| WestJet Encore | `WestJet Encore` |
| Wideroe | `Wideroe` |
| Yakutia Airlines | `Yakutia` |

## 5. Package it

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-dh8d \
  --livery-dir "<livery directory>" \
  --texture "Texture.webp=art/Texture.png" \
  # ship these unchanged (a solid fill also works) \
  --texture "Texture_Emissive.webp=art/Texture_Emissive.png" \
  --out out/dh8d.zip
```

Resolves to, on Android:

```
../../files/aircraft/infiniteflight-aircraft-dh8d/liveries/<livery directory>/<file name>
```

On iOS the root differs — replace `files` with `Library/dlc`:

```
../../Library/dlc/aircraft/infiniteflight-aircraft-dh8d/liveries/<livery directory>/<file name>
```

## 6. Import

```bash
adb push out/dh8d.zip /sdcard/Download/dh8d.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

