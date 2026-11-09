# Paths, filenames, and the three identifiers

> Get one of these three wrong and the import succeeds silently and changes nothing. There is no
> error path to guide you back.

## 1. The formula

```
<ContentRoot>/aircraft/<repo>/liveries/<livery directory>/<texture file>.webp
```

| platform | ContentRoot |
|---|---|
| Android | `/data/user/0/com.fds.infiniteflight/files/` |
| iOS | `<container UUID>/Library/dlc/` |

Concrete, both verified on hardware:

```
Android:  /data/user/0/com.fds.infiniteflight/files/aircraft/infiniteflight-aircraft-a320/liveries/<livery directory>/Texture.webp
iOS:      /private/var/mobile/Containers/Data/Application/<UUID>/Library/dlc/aircraft/infiniteflight-aircraft-b789/liveries/<livery directory>/Texture.webp
```

Inside the zip, the entry name is that path expressed relative to the extraction folder, two levels
up:

```
Android:  ../../files/aircraft/<repo>/liveries/<directory>/<file>.webp
iOS:      ../../Library/dlc/aircraft/<repo>/liveries/<directory>/<file>.webp
```

## 2. Identifier one: the repository name

`RepositoryName.Trim().ToLowerInvariant()`. All 65 in the catalog:

| aircraft | repo | aircraft | repo |
|---|---|---|---|
| A320 | `infiniteflight-aircraft-a320` | B787-9 | `infiniteflight-aircraft-b789` |
| A320neo | `infiniteflight-aircraft-a20n` | B787-10 | `infiniteflight-aircraft-b78x` |
| A321 | `infiniteflight-aircraft-a321` | B777-300ER | `infiniteflight-aircraft-b777w` |
| A321neo | `infiniteflight-aircraft-a21n` | B777-200ER | `infiniteflight-aircraft-b772` |
| A350-900 | `infiniteflight-aircraft-a359` | B757-200 | `infiniteflight-aircraft-b752` |
| A380 | `infiniteflight-aircraft-a388` | C172 | `infiniteflight-aircraft-c172` |
| B737-8 MAX | `infiniteflight-aircraft-b38m` | CRJ-200 | `infiniteflight-aircraft-crj2` |
| B737-800 | `infiniteflight-aircraft-b738` | E175 | `infiniteflight-aircraft-e75l` |

The complete list, with every livery directory per aircraft, is in
[models/index.md](models/index.md). Note the inconsistent suffixes: `b777w` (not `b773`),
`b77f`, `b77l`, `b38m` (not `b738max`), `crjx` for the CRJ-1000.

## 3. Identifier two: the livery directory

```csharp
livery.Path = Path.Combine(modelPackage.Path, "liveries", Path.GetFileName(FixPathForPlatform(livery.Path)));
```

`Path.GetFileName` of `LiveryPackage.Path`. It is **not** the name the app shows, and it is not
normalised to anything:

| shown in the app | directory on disk |
|---|---|
| Cathay Pacific | `CathayPacific` |
| Delta Air Lines | `Delta Airlines` |
| Korean Air | `Korean` |
| Scandinavian Airlines | `SAS` |
| Swiss International Air Lines | `Swiss` |
| TAP Air Portugal | `TAP` |
| Spirit Airlines | `Spirit` |
| VivaAerobus | `Viva` |
| Peach Aviation | `Peach` |
| Air New Zealand | `AirNewZealand` |
| Alaska Airlines | `Alaska` |
| American Airlines | `AmericanAirlines` |
| Air France | `AirFrance` |
| EasyJet | `easyJet` |
| Aegean Airlines - 2020 | `Aegean Airlines - 2020` |
| Aer Lingus - 2019 | `Aer Lingus 2019` |
| Transavia - Retro | `PH-YHD` |
| Middle East Airlines | `MEA` |

A320neo liveries are keyed by **airframe registration**: `OO-SBC`, `9H-NEB`, `B-326V`, `D-AINY`,
`G-UZLX`, `N308FR`. Every aircraft page in `docs/models/` lists its own mapping; do not extrapolate
from one family to another.

## 4. Identifier three: the texture file name

Fixed by the model's glTF: `images[].uri`, referenced from `materials[].pbrMetallicRoughness.baseColorTexture`.
Case matters — `Texture.webp` and `texture.webp` both exist in the catalog on different aircraft, and
`wing_lh.webp` coexists with `wingLH.webp`.

Two shading pipelines exist, and they are not interchangeable:

### Legacy · single texture

| file | size | channel |
|---|---|---|
| `Texture.webp` | 2048×2048 | baseColor |
| `Texture_ORM.webp` | 2048×2048 | R=AO, G=roughness, B=metallic |
| `Texture_N.webp` | 2048×2048 | normal |

Repaint only the first and the fuselage renders as black chrome: the ORM file still carries the
official livery's metallic mask, so white areas become mirrors. Replace all three, or use
`--fill-orm --fill-normal` with `(255,200,0)` and `(128,128,255)` solids.

*11 aircraft in the catalog are plain `Texture.webp`, 11 more use a single model-specific name
(`texture.webp`, `744GEN.webp`, `B717.webp`, `c17.webp`, `SR22.webp` …).*

### Modern · per-part albedo

```
M_<Part>_<channel>.webp        4096×4096
```

| suffix | meaning | repaint? |
|---|---|---|
| `_albd` | albedo / baseColor | **yes** |
| `_comp` | composite (metallic + roughness + occlusion) | keep |
| `_norm` | normal | keep |
| `_emis` | emissive | keep |

A320neo and A321neo ship 4096² parts; the rest of the modern fleet mixes 2048² engine maps with
4096² fuselage maps. Exact per-aircraft lists — file name, dimensions, byte size, role — are in each
aircraft page.

### Multi-part legacy shading

35 aircraft fall here: several baseColor images, one per body area (`fuselage_front`, `wing_lh`,
`tail`, `b757_RB211`, `b777_300er_uv8`, …). Every one is a separate PBR material, so replacing a
subset produces a patchwork aircraft. The page for each aircraft lists the full set that its official
livery ships.

## 5. Generic liveries are not in `liveries/Generic/`

| aircraft family | Generic texture root |
|---|---|
| A320neo | `Aircraft/infiniteflight-aircraft-a20n` (model root) |
| A321neo | `Aircraft/infiniteflight-aircraft-a21n/Liveries/Generic` |

Writing both is the safe move. `build_slip_package.py --entry-prefix` lets you target any root
explicitly:

```bash
python tools/build_slip_package.py --platform android \
  --aircraft-repo infiniteflight-aircraft-a21n --livery-dir "Liveries/Generic" ...
python tools/build_slip_package.py --platform android \
  --aircraft-repo infiniteflight-aircraft-a21n --livery-dir "." \
  --entry-prefix "../../files/aircraft/infiniteflight-aircraft-a21n" ...
```

## 6. When a path or filename is still unknown

Two rounds of probe, both scripted in [probe_matrix.py](../tools/probe_matrix.py):

```
Round 1 (path):    one distinct colour per candidate path, all written at once
                   → the colour on the fuselage names the winning path
Round 2 (filename): lock the path, write one numbered image per candidate name
                   → the number on the fuselage names the winning file
Between rounds:    adb shell "pm trim-caches <bytes>"
```

This is how A320's answer was pinned down: a fistful of candidate roots × a fistful of candidate
names, then a single-variable confirmation — a package with two entries and nothing else, after which
the fuselage turned orange.

Faster, if you have network access: read the model's glTF. `images[].uri` *is* the answer, and
`tools/extract_models.py` already did it for all 65 aircraft.
