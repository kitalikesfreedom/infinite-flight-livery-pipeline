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

**Format: Legacy (single texture).** One 2048x2048 baseColor image. Replace it together with `Texture_ORM.webp` and `Texture_N.webp`, or the fuselage renders as black chrome.

### Files this aircraft needs

| file | dimensions | role | what to put there |
|---|---|---|---|
| `Texture.webp` | 2048x2048 | surface / **paint** | your artwork |
| `Texture_Emissive.webp` | 128x128 | surface / keep | your artwork |

### Option A - explicit list (copy and run)

```bash
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-dh8d \
  --livery-dir "<a directory from the table above>" \
  --texture "Texture.webp=art/Texture.png" \
  --texture "Texture_Emissive.webp=art/Texture_Emissive.png" \
  --fill-orm --fill-normal \
  --out out/dh8d.zip
```

### Option B - auto mode

```bash
python tools/build_slip_package.py --auto --art art/ \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-dh8d \
  --livery-dir "<a directory from the table above>" \
  --fill-orm --fill-normal \
  --out out/dh8d.zip
```

`--auto` reads `data/livery_files.json`, then looks for these stems in `art/`
(`.png`, `.webp`, `.jpg` are all accepted):

```
Texture.png
Texture_Emissive.png
```

`--fill-orm --fill-normal` synthesises the two PBR companions at the right size, so you do
not have to paint them. Drop the flags if you supply your own.

### Option C - reuse the companions from an official package

The `keep` rows above are not artwork: they are masks the vendor ships. Rather than
recreating them, pull them out of an official livery package:

```bash
python tools/fetch_catalog.py --download --type AircraftLivery \
  --match dh8d --out dl/
python tools/build_slip_package.py \
  --platform android \
  --aircraft-repo infiniteflight-aircraft-dh8d \
  --livery-dir "<a directory from the table above>" \
  --texture "Texture.webp=art/Texture.png" \
  --keep-from dl/<downloaded package>.zip \
  --out out/dh8d.zip
```

`--keep-from` copies every entry in that archive **except** the albedo files, so your own
artwork always wins and the companions stay byte-identical to the vendor's.

### Where the entries land

```
android: ../../files/aircraft/infiniteflight-aircraft-dh8d/liveries/<directory>/<file>.webp
ios:     ../../Library/dlc/aircraft/infiniteflight-aircraft-dh8d/liveries/<directory>/<file>.webp
```

`<directory>` must come from the table in section 4 - the folder name, not the name the app
shows.

### How to tell it worked

If only the baseColor had been replaced the fuselage would render as black chrome - so the
fact that it looks clean proves the ORM and normal companions are present. A dark, mirror-like
hull means one of the three did not land.

## 6. Import

```bash
adb push out/dh8d.zip /sdcard/Download/dh8d.zip
adb shell "pm trim-caches <bytes>"   # only when repainting the same directory again
```

Then: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip,
force-stop the app, reopen. Full walkthrough: [build-and-import.md](../build-and-import.md).

