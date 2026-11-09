# Quickstart

Five commands from nothing to a repainted aircraft. The long version is in
[build-and-import.md](build-and-import.md); this page is the one you hand to somebody who has not
read anything yet.

**Requirements:** the app, a PC with `adb` (Android) or the Files app (iOS), Python 3.10+, and
Pillow. Your account needs the `SceneryEditors` role — the import button lives inside the Scenery
Editor, so without it there is nowhere to put the bytes.

## 1. Pick your aircraft

Open [models/index.md](models/index.md) and find the airframe. Its page tells you three things you
cannot guess: the repository name, the livery directory names, and the exact texture files with
their dimensions.

```
Airbus A320  →  infiniteflight-aircraft-a320
                liveries/Aegean Airlines/Texture.webp   2048x2048
```

## 2. Paint at the same size

Export WebP (quality 90–95) at exactly the listed dimensions. Put the files in `art/` using the same
stems:

```
art/Texture.png        (2048x2048)   your artwork
```

Legacy single-texture aircraft also read `Texture_ORM` and `Texture_N`. Do not paint those — let the
tool synthesise them, or the fuselage renders as black chrome.

## 3. Build the zip

```bash
pip install -r tools/requirements.txt

python tools/build_slip_package.py --auto --art art/ \
  --aircraft-repo infiniteflight-aircraft-a320 \
  --livery-dir "Aegean Airlines" \
  --fill-orm --fill-normal \
  --out out/a320.zip
```

`--auto` reads the aircraft's file list and matches your artwork by name. It names anything it could
not find. Multi-part aircraft (A321neo: 11 files, C172: 5) work the same way — no extra flags.

## 4. Import it on the device

```bash
adb push out/a320.zip /sdcard/Download/a320.zip
```

In the app: **Scenery Editor → open an airport → Satellite → Import Imagery** → pick the zip.
The airport must already be open or the import is dropped silently. There is no progress bar and no
confirmation — that is normal.

Then force-stop the app (swipe it out of recents, not Home) and reopen it.

## 5. If you repaint the same livery twice

```bash
adb shell "pm trim-caches <bytes>"
```

Pass a value larger than the texture cache. Only needed when the target directory is one you have
already written to; a new directory always shows up on the first try.

## It did not work

| what you see | what it is |
|---|---|
| nothing at all | airport was not open, or the livery directory name is wrong (section 4 of the aircraft page) |
| black hull with mirror highlights | only the baseColor landed — build with `--fill-orm --fill-normal` |
| one part still in official colours | that `_albd` / `part` file is missing from the zip |
| worked once, now never | the tile cache — run step 5 |
| `Error loading the imagery package` | something other than `.webp` is in the archive |

Full symptom table: [troubleshooting.md](troubleshooting.md).

## Where things are

| I want to… | go to |
|---|---|
| know which files my aircraft needs | [models/index.md](models/index.md) → your aircraft |
| understand why a zip can write into the app | [mechanism.md](mechanism.md) |
| see all 65 recipes side by side | [models/packaging-matrix.md](models/packaging-matrix.md) |
| download models, packages, templates | the two releases linked from the README |
