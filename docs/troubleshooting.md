# Troubleshooting

> Almost every failure in this pipeline is silent. Work down this page in order; it is sorted by how
> often each cause is actually the answer.

## 1. The three checks that solve most cases

| # | check | symptom it explains |
|---|---|---|
| 1 | entry names start with `../../` and continue `files/aircraft/<repo>/liveries/<directory>/` | nothing changes at all |
| 2 | an airport was **already open** in the Scenery Editor when you imported | nothing changes, with no error |
| 3 | you ran `pm trim-caches` and force-stopped the app before looking | first repaint worked, second did not |

## 2. Symptom → cause

### Nothing changes

| cause | how to confirm |
|---|---|
| directory name is the display name, not the folder name | check the aircraft's page in [models/](models/index.md) — `Delta Air Lines` → `Delta Airlines` |
| wrong case in the filename | `Texture.webp` ≠ `texture.webp`; `wing_lh` and `wingLH` both exist |
| not in Scenery Editor, or no airport open | redo step 4 with an airport loaded |
| wrote into `cache/` | one `../` short |
| target livery never downloaded | select that livery and fly once so the package lands |
| wrong aircraft | the same airline name is a different directory per aircraft; A320neo uses registration codes |

### Black patches, chrome sheen, "metallic" white areas

Only baseColor was replaced. `Texture_ORM.webp` still holds the official metallic mask, so white
areas render as mirrors. Fix:

```
Texture.webp      = your artwork
Texture_ORM.webp  = solid (255, 200, 0)      # no occlusion, fully rough, non-metal
Texture_N.webp    = solid (128, 128, 255)    # flat normal
```

`build_slip_package.py --fill-orm --fill-normal` appends both. On modern multi-part aircraft, ship the
`_comp` / `_norm` files the official livery ships and leave their channels untouched.

### Works once, then never again

`vt.cache` is keyed on the texture directory. Drop it:

```bash
adb shell "pm trim-caches <bytes>"
```

The in-app "clear cache" reclaims only a token amount of it; truncating `vt.cache` does nothing at
all because it is memory-mapped.

### `Error loading the imagery package`

The archive contains a `kml` or an entry the imagery loader rejects. The pipeline's archives contain
only `.webp` entries — if you hand-edited one, remove the extra entries.

### Dimension mismatch

The tool fails loudly when a texture does not match the model's expected size (2048², 4096², 1024²
depending on the part). `--resize` exists but softens the result; prefer re-exporting at the right
size.

### Partial repaint shows a patchwork

That aircraft is multi-part: several baseColor images, each its own material. Ship the complete set
listed on its page — 35 of the 65 aircraft are like this.

### Generic livery does not apply

The Generic texture root is not `liveries/Generic/` for every family:

```
A320neo  Generic → Aircraft/infiniteflight-aircraft-a20n            (model root)
A321neo  Generic → Aircraft/infiniteflight-aircraft-a21n/Liveries/Generic
```

Write both, or use `--entry-prefix` to hit the exact root.

## 3. Dead ends, already eliminated

Do not spend an evening on these. Each was tested and failed.

| idea | verdict | why |
|---|---|---|
| edit `files/GlobalConfig.json` | dead | the static constructor deletes the file; real config is SecureStorage + server |
| forge `FreeFlightScenario.json` to fake editor mode | dead | `PlayMode` is a projection of `Scenario.Mode`, rewritten before all 18 `Fly()` entry points |
| `adb run-as` into the sandbox | dead | `package not debuggable` |
| MITM the package downloads | dead | every URL is `https://`, the network security config trusts system CAs only, Android 7+ ignores user CAs, no root means no system CA |
| forge the role claim | dead | server-signed JWT, key material in AndroidKeyStore AES-GCM |
| set `livery` / `livery_id` in State Explorer | dead | both are read-only (`r`) |
| deep link a `.zip` to trigger the import | dead | requires `PlayMode == SceneryEditor && SceneryDataModel != null` |
| path traversal through forum image download | dead | filename is `if-markdown-{Guid:N}{ext}` — three independent blocks |
| repack the APK to skip the role check | dead | PairIP: `libpairipcore.so`, bytecode virtualisation, periodic licence checks |
| backup / restore injection | dead | Android 12+ restrictions; a 50 MB probe changed disk usage by 0.2 MB and no texture |

## 4. Still stuck: two-round probing

```bash
# round 1 — one colour per candidate root
python tools/probe_matrix.py --mode path --platform android \
  --livery-dir "<livery directory>" --size 2048x2048 \
  --repo infiniteflight-aircraft-a320 \
  --repo "Content/Aircraft/Airbus A320" \
  --filenames Texture.webp --out out/probe_path.zip

# round 2 — lock the root, one big number per candidate filename
python tools/probe_matrix.py --mode name --platform android \
  --repo infiniteflight-aircraft-a320 --livery-dir "<livery directory>" \
  --size 2048x2048 --filenames Texture.webp,Texture_0.webp,body.webp \
  --out out/probe_name.zip
```

Trim the cache between rounds. The colour tells you the root; the number tells you the filename. This
is exactly how the A320 answer was found — a handful of candidate roots against a handful of candidate
names, then a two-entry confirmation.
