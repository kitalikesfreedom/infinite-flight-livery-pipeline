# Mechanism

> Why a zip file can write into an app's private storage, and why the texture you just wrote does
> not appear. For the practical steps skip to [03](build-and-import.md).

## 1. The entry point

`AirportEditorControl.LoadOverlayTilesSource`, recovered with ILSpy from `Fds.InfiniteRunway`:

```csharp
string text = Path.Combine(FileSystem.GetTempFolder(), "if_zip_output");
if (Directory.Exists(text)) Directory.Delete(text, true);   // wiped before every import

foreach (var current in zip.Entries) {
    if (!current.FullName.StartsWith("__MACOSX/") && current.Length > 0) {
        string path = text + Path.DirectorySeparatorChar + current.FullName;
        path = FileSystem.FixPathForPlatform(path);           // slashes only, no .. check
        FileSystem.CreateDirectory(Path.GetDirectoryName(path));
        ZipFileExtensions.ExtractToFile(current, path, true);  // the important line
    }
}
```

Three properties have to hold at once:

1. the entry name is concatenated into a path with **no** `GetFullPath` normalisation and **no**
   `StartsWith` guard;
2. `FixPathForPlatform` only rewrites `\` to `/`;
3. `ExtractToFile(dest, overwrite: true)` overwrites silently.

.NET's own `ZipFile.ExtractToDirectory` rejects dot-segments, which is why the four places in the
client that use it (weather, replays, achievements, file manager) are not reachable this way. This
code path bypasses exactly that protection, by reimplementing extraction by hand.

## 2. Two levels up lands on the app root

```
FileSystem.GetTempFolder()        = /data/user/0/com.fds.infiniteflight/cache/
text                              = .../cache/if_zip_output
../../                            → /data/user/0/com.fds.infiniteflight/
../../files/aircraft/...          → .../files/aircraft/...      ← the livery tree
../../cache/...                   → .../cache/...               (works too; a profile picture lands here)
```

So every entry name starts with `../../`. One level short and you are still inside `cache/`; one
level more and you are outside the sandbox, where the write fails without an error.

## 3. The trigger condition (why nothing happens)

`Program.cs`, `ProcessDeepLinks`:

```csharp
else if (text2.EndsWith(".zip")) {
    if (InfiniteRunwayCore.Scenario.Mode == PlayMode.SceneryEditor
        && AirportEditorControl.SceneryDataModel != null)   // an airport must already be open
    {
        string text4 = FileSystem.GetTempFolder() + "Import.zip";
        // copy the content stream into text4
        AirportEditorControl.LoadOverlayTilesSource(text4);
    }
}
```

with `SceneryDataModel => SceneryEditor.CurrentAirport?.sceneryDataModel ?? null`.

**Consequence:** you must be inside the Scenery Editor *and* have an airport open. Otherwise the
import is dropped with no dialog, no log line and no toast. This is the first wall everybody hits.

## 4. Why a successful import can still show nothing

`AircraftModel.Load`:

```csharp
string texturePath = Path.Combine(FileSystem.ContentRoot,
                                  AircraftDataModel.Path,      // aircraft/<repo>
                                  "liveries",
                                  CurrentLivery.TexturePrefix); // the directory name
Renderer.ModelInstanceCreate(filePath, ..., texturePath, ModelLoadOptions.VirtualTextures, 1);
```

The fourth argument is a **directory**, and virtual textures are enabled. `Renderer.cs:21335`:

```csharp
string cacheRoot = FileSystem.CacheRoot;
string text = Path.Combine(cacheRoot, "vt.cache");     // preallocated, kept mapped
_vtDiskCache = VtCacheOpen(text);
```

The tile cache key is the directory path. Therefore:

| attempt | result |
|---|---|
| overwrite files in the same directory | no visual change — cache hit |
| truncate `vt.cache` to 0 bytes | no effect — the file is memory-mapped |
| system settings → clear cache | reclaims a token amount of the cache |
| `adb shell "pm trim-caches <bytes>"` | clears it to the target; cache rebuilds on next launch |

This is the root cause of "you can only repaint an aircraft once", and the reason step 5 of the
pipeline exists.

## 5. How much write surface this actually is

| can write | cannot write |
|---|---|
| any path under `files/` and `cache/` inside the app sandbox | anything outside the sandbox |
| overwrite existing textures, JSON, config | signatures, permissions, other apps' data |
| create directories that do not exist yet | — |

Sticking to textures is the minimal-blast-radius choice: no model package, no configuration package,
no `Settings.json`, therefore nothing but the render output changes.

## 6. Why role-less devices are stuck

*Import Imagery* lives inside the Scenery Editor, and entering the Scenery Editor requires the
`SceneryEditors` (68) role — a `r` claim in a server-signed JWT, stored under AndroidKeyStore
AES-GCM (`AuthManager`, `SecureStorage`). It cannot be forged locally.

On a device without that role the last link of the chain — handing a zip to
`LoadOverlayTilesSource` — is unreachable. All three write primitives remain open; what is missing is
the act of delivering bytes.

## Appendix · the other delivery surfaces

The same unguarded `ExtractToFile` pattern appears in:

| location | destination | trigger |
|---|---|---|
| `PackageManager.InstallPackage` (`PackageManager.cs:1912`) | `aircraft/<repo>/liveries/<fileName>` — *already* the livery tree | package install flow |
| `ScenarioManager.ImportScenarioPackage` (`:1583`) | `files/tutorials/<bundleGuid>/`, and `..\..\..\` reaches `files/` | scenario import |
| `ModelBankManager` (`:255`, `:953`, `:1738`) | `files/Content/Airport Assets/` | airport asset download |

All three are fed from server-provided URLs (`PackageRootURL`, `BundleUrl`, `AirportAssetsURL`), not
from a user file picker. They are not part of this pipeline; they are the reason a single
`GetFullPath` check will not be enough when the vendor finally looks.
