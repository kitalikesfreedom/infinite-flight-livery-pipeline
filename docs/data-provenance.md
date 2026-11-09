# Data provenance

> Every number in `docs/models/` came from downloading something and reading it. This page records
> what was downloaded, how big it was, and where the remaining gaps are — so the tables can be
> trusted, and re-generated when the catalog moves.

## 1. What the catalog contains

`GET /live/v2/packages/aircraft?appVersion=26.5` with a guest JWT, snapshot taken 2026-11-09:

| `contentType` | packages | total size |
|---|---|---|
| `AircraftLivery` | 1,260 | 1,554 MB |
| `AircraftSharedLiveryFiles` | 66 | 1,941 MB |
| `AircraftModel` | 65 | 681 MB |
| `AircraftConfiguration` | 66 | 1.5 MB |
| `AircraftGenericLivery` | 12 | ~0 |
| `AircraftSound` | 13 | 109 MB |
| **total** | **1,482** | **~4.3 GB** |

Each entry carries `packageId`, `packageKey` (`aircraft/<repo>/<class>/<id>`), `version`,
`sizeBytes`, `sha256`, `storagePath`, a signed `downloadUrl`, `urlExpiresAt` (24 h), and a
`metadataJson` blob holding `repositoryName`, `name`, `path`, and — for liveries — the
`livery` object with `isProOnly`, `visibleGroups`, `allowedRoles`, `modelId`.

That `metadataJson` is why livery directories can be listed exactly instead of guessed: `path` is
`Aircraft/<name>/Liveries/<directory>`, and the last segment is the write target.

## 2. What was downloaded for this repository

| step | scope | volume | output |
|---|---|---|---|
| catalog | all packages | 4.3 MB JSON | `data/catalog.json` |
| model packages | all 65 aircraft | **681 MB** | `data/model_textures.json` (6 MB) |
| livery packages | 1 per aircraft (largest) | **233 MB** | `data/livery_files.json` (31 KB) |
| shared texture sets | 4 aircraft only | **10 MB** | `data/shared_files.json` |
| **total** | | **~925 MB** | |

Nothing is vendored: no textures, no models, no APKs are stored in this repository — only the
inventories (file names, dimensions, byte sizes, hashes of the source packages).

## 3. Constraints discovered while collecting

**Many livery packages are 0 bytes.** Of the 1,260 livery packages, a large fraction are
metadata-only overlay updates (`sizeBytes: 0`). Picking "the smallest package per aircraft" therefore
returns an empty inventory for most aircraft. This repository downloads the **largest** livery
package per aircraft instead: `--pick largest`.

**Per-livery packages are deltas, not full sets.** A320neo's largest livery package carries 20
entries; the complete airframe texture list is larger. For four aircraft
(`c17`, `f16`, `f22`, `spit`) the livery package carries no textures at all, and the inventory comes
from their `AircraftSharedLiveryFiles` package instead.

**Model packages contain glTF only.** 681 MB of models yielded 65 glTF sets and *zero* embedded
textures — so texture dimensions cannot come from the model. They come from the livery packages
(§2), which is also why `docs/models/` dimensions are measured rather than assumed.

**One package has a broken key.** The catalog contains a livery with
`packageKey = aircraft/unknown/aircraftlivery/...` (`China Southern Airlines`, 5.1 MB). The vendor's
own manifest has an unresolved repository name. It is excluded from the per-aircraft pages because
there is no aircraft to attach it to.

## 4. Known gaps in the tables

| gap | count | effect |
|---|---|---|
| entries with no dimensions | 7 of 476 | `.ktx2` textures (NASA 747-SOFIA) and a few odd formats; name and bytes are still listed |
| aircraft whose inventory came from shared sets | 4 | marked on the page; file list is complete, but it is the airframe set rather than one livery's delta |
| aircraft with no parseable livery package at all | 0 | every aircraft has an inventory from one of the three sources |
| livery packages seen per aircraft | 1 | each aircraft page's directory list is complete (from the catalog), but the file inventory reflects a single official livery |

## 5. Device facts behind the "no root" claim

Collected read-only over `adb`. Every identifying value is removed — no model code, no serial, no
build fingerprint, no storage figures.

```
android            16 (SDK 36)
abi                arm64-v8a
bootloader         locked
verified boot      green
app                26.5.1 (targetSdk 36)
package flags      HAS_CODE ALLOW_CLEAR_USER_DATA ALLOW_BACKUP
private dir        ls .../files/aircraft     -> Permission denied
run-as             package not debuggable
```

The two denials are the reason the whole approach goes through the import box rather than through a
shell.

## 6. Regenerating

```bash
pip install -r tools/requirements.txt

python tools/fetch_catalog.py --dump-json data/catalog.json
python tools/extract_models.py      --catalog data/catalog.json
python tools/extract_liveries.py    --catalog data/catalog.json --type AircraftLivery --pick largest
python tools/extract_liveries.py    --catalog data/catalog.json --type AircraftSharedLiveryFiles \
                                    --pick smallest --only infiniteflight-aircraft-c17,infiniteflight-aircraft-f16,infiniteflight-aircraft-f22,infiniteflight-aircraft-spit
python tools/build_docs.py
```

All five steps are resumable: completed aircraft are cached in their `data/*.json`, a re-run only
fetches what is missing. Download URLs expire after 24 h, so refresh `data/catalog.json` first if a
run fails with `410 Gone`.

Then verify:

```bash
python tools/selftest.py
```
