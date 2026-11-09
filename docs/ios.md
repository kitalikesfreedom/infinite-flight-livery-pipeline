# iOS

> Same logic, same import box, completely different container root and transport. An Android zip will
> not work here, and vice versa.

## 1. The root moves

```csharp
ContentRoot = Environment.GetFolderPath(SpecialFolder.LocalApplicationData);
```

| platform | ContentRoot | `GetTempFolder()` |
|---|---|---|
| Android | `/data/user/0/com.fds.infiniteflight/files/` | `.../cache/` |
| **iOS** | `<container UUID>/Library/dlc/` | `<container UUID>/tmp/` |

Container layout, read out of a backup's `Manifest.db`:

```
/private/var/mobile/Containers/Data/Application/<UUID>/
├── Library/
│   ├── dlc/                  ← the content root: aircraft / scenery / sounds
│   ├── Preferences/
│   ├── Settings.json
│   └── WeightAndBalance.json
├── tmp/                      ← where GetTempFolder() points
└── Documents/
```

Derivation: `tmp/if_zip_output` → `../` = `tmp/` → `../../` = container root → into `Library/dlc/`.

So the entry name is:

```
Android:  ../../files/aircraft/<repo>/liveries/<directory>/<file>.webp
iOS:      ../../Library/dlc/aircraft/<repo>/liveries/<directory>/<file>.webp
```

```bash
python tools/build_slip_package.py --platform ios \
  --aircraft-repo infiniteflight-aircraft-b789 \
  --livery-dir "<livery directory>" \
  --texture "Texture.webp=art/b789.png" \
  --fill-orm --fill-normal \
  --out out/ios_b789.zip
```

`--platform ios` only swaps the prefix; the file names and dimensions are identical per aircraft.

## 2. Getting the zip onto the device

Without a jailbreak there is exactly one route: the Files app.

```
1. send the zip to the iPhone (AirDrop / iCloud / any chat app)
2. "Open in another app" → "Save to Files"
3. save to "On My iPhone" or iCloud Drive
4. it becomes selectable in the app's Import Imagery picker
```

The picker call is `Platform.OpenFilePickerAsync(new string[] { "application/*" }, "Select a .zip file")`
(`AirportEditorControl.cs:1532`) — wildcard type, so a zip is accepted.

### Routes that do not work (verified)

| attempt | result |
|---|---|
| AFC into the app container | only reaches `/var/mobile/Media`, not the sandbox |
| "Open with Infinite Flight" on a zip | `CFBundleDocumentTypes` lists replay / geojson / fpl / dat only |
| backup → edit → restore | requires the device passcode; blocked repeatedly with `passcode prompt dismissed` |
| jailbreak | no bootrom exploit on A17 Pro, no current iOS jailbreak |

## 3. Cache clearing is easier on iOS

```
In-app settings → General → "Clear Cache"
→ swipe the app away (not Home)
→ relaunch
```

The in-app button is effective here. On Android it is quota-limited to a few MB; on iOS it clears the
tile cache properly.

### Alternative: offload, not delete

```
Settings → General → iPhone Storage → Infinite Flight → Offload App
```

| action | binaries | `Library/dlc/` data |
|---|---|---|
| **Offload App** | removed | **kept** |
| Delete App | removed | `dlc/` gone |

Offload, reinstall from the App Store: caches are empty, your repainted textures are still in place.

## 4. iOS only creates livery directories you have flown

A backup's `Manifest.db` for B787-9 shows eight livery directories, each containing a single
`UUID.json` — the package metadata — and **no `.webp`**:

```
liveries/Air China/8874908d-....json
liveries/Generic/20658961-....json
liveries/Juneyao Air/86f1c04f-....json
liveries/Lufthansa/6fce5ad8-....json
...
```

Textures are resolved at runtime from elsewhere on iOS. Missing directories are created by the write
itself, so you can target a livery you have never flown — one archive can carry every candidate
directory at once.

## 5. Verified on

```
device      iPhone (A17 Pro class) — no jailbreak available
iOS         27
app         26.5 (20148)
bundle id   com.flyingdevelopmentstudio.infiniteflight
container   <container UUID>  (per install; read it from Manifest.db or `apps list`)
```

## 6. Tooling

```bash
pip install pymobiledevice3

python -m pymobiledevice3 usbmux list                    # devices
python -m pymobiledevice3 lockdown info                  # system info
python -m pymobiledevice3 apps list --type User          # bundle id, container path, entitlements
python -m pymobiledevice3 backup2 backup <dir> --only-regex "<keyword>"
```

`Manifest.db` is SQLite with `Files(domain, relativePath, fileID)`. Even when the backup cannot copy
file contents, it still hands you the complete directory tree — which is how the iOS root above was
determined without ever reading a texture.
