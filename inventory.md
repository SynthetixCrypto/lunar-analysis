# Lunar Client inventory

Study date: 2026-10-11. Read-only static study of installed files. No Lunar executables, JARs, native libraries, application JavaScript, or anti-cheat components were executed. Only analysis outputs are written.

## Evidence convention

**Confirmed** means a specific filesystem, parser, or REA observation. **Inference** means an interpretation of that observation. **Unknown** means unavailable or unexamined evidence. Static code establishes declarations and possible behavior, not runtime execution. REA Evidence IDs and locally preserved record coverage are listed in findings.md; supplemental filesystem and parser records are identified by their output filenames.

## Verified locations

| Location | Status and observation |
|---|---|
| `C:\Users\Admin\AppData\Local\Programs\Lunar Client\Lunar Client.exe` | Confirmed by Start Menu shortcut strings and REA PE resource parsing. 235,252,216 bytes; PE32+; machine 0x8664 (AMD64). |
| `C:\Users\Admin\.lunarclient` | Confirmed directory; contains offline artifacts, Java runtimes, profiles, settings, shared assets, caches, and UI assets. |
| `C:\Users\Admin\.lunarclient\offline\multiver` | Confirmed Minecraft-side core JAR and native-library directory. |
| `C:\Users\Admin\.lunarclient\profiles` | Confirmed versioned mod/profile directories `1.21` and `26`. Names alone do not prove the currently selected Minecraft version. |
| `C:\Users\Admin\.lunarclient\settings` | Confirmed `launcher.json`, `cache.json`, `game`, and `game-backup` entries. Personal values not collected. |
| `C:\Users\Admin\.lunarclient\ui\2545e7fc28d10de3b6f9e5b8b66a4fc8931aece9` | Confirmed index.html and static/index.js (8,681,743 bytes), plus UI assets. Its relationship to the native game UI requires bridge evidence. |
| `C:\Users\Admin\AppData\Roaming\lunarclient` | Confirmed name in parent listing; direct filesystem enumeration returned EPERM. Contents unknown from that reader. |
| `C:\Users\Admin\AppData\Local\lunarclient-updater` | Confirmed name in parent listing; direct filesystem enumeration returned EPERM. Contents unknown from that reader. |
| `C:\Users\Admin\AppData\Roaming\.minecraft` | Confirmed name in parent listing; direct filesystem enumeration returned EPERM. Lunar ownership/use is unconfirmed without code evidence. |

Launcher identity evidence: `ev_54a5c81c3b5d0c5eb74874e623d2d26b1fc7ad238d084afc6c84c6f79c538623`. SHA-256 `e21d5ad61a3caec8e25948a52f3a0157b9e875ef6cd9a47cd1ee874a7e58f5e6`. Resource names include `INTEGRITY/ELECTRONASAR`, `OWEINTEGRITY/OWE`, and `OWEINTEGRITY/OWEASARSIG`. These are static resources, not evidence that enforcement ran.

## Filename inventory coverage

Supplemental evidence: `discovery-inventory.json` and `artifact-index.tsv`. The inspected Lunar data tree contains 6754 files and 636 directory entries, including 176 JARs, 269 DLLs, 39 EXEs, 7 ZIPs, and 3 JavaScript files. These are bounded counts, not a complete machine inventory.

Traversal recorded filenames and sizes, with depth at most 8 per traversed root, without following symlinks. Logs, databases, and textures were not descended; some nested directories named cache were skipped. File entries ending in .log, .db, or .pem were recorded by filename only. Their contents were not read. No personal setting values, credentials, tokens, or installation identifier values were collected. Access errors and the traversal scope are retained in the JSON. Parent-directory searches were limited to the current user, AppData Local/Roaming, Program Files, Program Files (x86), ProgramData, Desktop, and Start Menu locations; absence in those searches is not absence elsewhere.

## Minecraft core artifacts

| File | Bytes |
|---|---:|
| `C:\Users\Admin\.lunarclient\offline\multiver\client-natives-win-x86-v1_21_11.zip` | 460861 |
| `C:\Users\Admin\.lunarclient\offline\multiver\client-natives-win-x86-v26_1_2.zip` | 732106 |
| `C:\Users\Admin\.lunarclient\offline\multiver\client-natives-win-x86-v26_2.zip` | 732106 |
| `C:\Users\Admin\.lunarclient\offline\multiver\common-0.1.0-SNAPSHOT-all-nomappings.jar` | 55066 |
| `C:\Users\Admin\.lunarclient\offline\multiver\genesis-0.1.0-SNAPSHOT-all.jar` | 11319006 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar-fabric-mixins-0.1.0-SNAPSHOT-all.jar` | 823846 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar-flashback-mixins-0.1.0-SNAPSHOT-all.jar` | 22728 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar-lang.jar` | 1392220 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar-modmenu-mixins-0.1.0-SNAPSHOT-all.jar` | 8043 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar-platform-mappings-v1_21_11.jar` | 13924142 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar-platform-mappings-v26_1_2.jar` | 3052612 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar-platform-mappings-v26_2.jar` | 3163315 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar-replaymod-fabric-mixins-0.1.0-SNAPSHOT-all.jar` | 1095591 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar-skyhanni-mixins-0.1.0-SNAPSHOT-all.jar` | 8041 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar-sodium-mixins-0.1.0-SNAPSHOT-all.jar` | 916377 |
| `C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar` | 64582425 |
| `C:\Users\Admin\.lunarclient\offline\multiver\modern-0.1.0-SNAPSHOT-all-nomappings.jar` | 3166262 |
| `C:\Users\Admin\.lunarclient\offline\multiver\ul-natives-x86-win.zip` | 20150352 |
| `C:\Users\Admin\.lunarclient\offline\multiver\ul-resources.zip` | 2455080 |
| `C:\Users\Admin\.lunarclient\offline\multiver\webosr-natives-x86-win.zip` | 212115 |

JAR/ZIP filename suffixes are discovery hints; archive format, packages and declarations are corroborated separately in the Minecraft report. Natives labeled x86 require PE header inspection before architecture claims.

## Bundled runtime directories

- `C:\Users\Admin\.lunarclient\jre\515e47c1d532181677af445d76add9cabc2317de\zulu25.30.17-ca-jre25.0.1-win_x64`
- `C:\Users\Admin\.lunarclient\jre\56e53accb20696f802d92bd011174126b5e3154e\zulu21.30.15-ca-jre21.0.1-win_x64`
- `C:\Users\Admin\.lunarclient\jre\d093c370fc8eaa3e6743d7f61fb633adac4344f2\zulu21.48.17-ca-jre21.0.10-win_x64`

Runtime version/architecture metadata and native dependencies are documented in `native-runtime-inventory.md`. Merely being installed does not establish which runtime a particular launch selects.

## Provider availability

See `provider-availability.json`. REA static JavaScript application analysis and portable PE resource inspection are available. Archive inspection becomes available after opening an archive. Ghidra is not configured; IDA is not configured; Hopper is unsupported on win32. JEB and JADX providers are unavailable. REA managed PE/CLI parsers target .NET, not JVM JAR classes, and are not used as Java substitutes. No engines were installed and no security protections were changed.

## Launcher archive and component inventory

**Confirmed by REA:** `C:/Users/Admin/AppData/Local/Programs/Lunar Client/resources/app.asar` is an ASAR archive, SHA-256 `506574f17a6b7aeb5a13fe5f53fc83329fa705141505dde30ec88e00aa03a9f4`. Its shipped manifest declares launcher 3.7.24-ow and Electron 42.7.1. Exact archive entries, formats, sizes, hashes and provenance are preserved in [launcher-asar-extraction-evidence.json](launcher-asar-extraction-evidence.json). REA materialized 1,324 regular-file occurrences, including 970 JavaScript-family files, seven HTML entry pages, four native .node addons and three Windows 7za helpers. These ASAR counts have a different scope from the data-tree filename counts above.

| Component | ASAR logical path / evidence |
|---|---|
| Electron main entry | `dist-electron/electron/main.js`, 5,739,762 bytes; package.json main field |
| Optional native-helper child entry | `dist-electron/electron/index.js`, distinct from package main |
| Launcher preload | `dist-electron/preload/launcher/index.js` |
| Launcher renderer | `dist/html/main.html` → `dist/assets/main.js` |
| Other renderer entry pages | embedded-browser, embedded-checkout, mission-control, satellite, updater, visualise-resolution |
| Native addons | bsdiff.node, better_sqlite3.node, diskusage.node, iselevated.node; all x64 from PE headers |
| Utility helpers | unpacked arm64/ia32/x64 7za members; declared-vs-observed integrity discrepancies recorded, never executed |

[launcher-module-index.jsonl](launcher-module-index.jsonl) contains 2,215 REA module observations, including duplicate/context-specific graph entries; this is not a count of unique source modules. [launcher-source-evidence.json](launcher-source-evidence.json) records manifest dependencies and focused entry/initialization/launch/IPC observations with exact source hashes and offsets. [launcher-native-addons.json](launcher-native-addons.json) records addon paths, hashes, headers, imports and exports.

## Detailed Minecraft and native inventories

[minecraft-artifacts.json](minecraft-artifacts.json) and [minecraft-jar-entries.tsv](minecraft-jar-entries.tsv) inventory 14 top-level core JARs and their entries. [minecraft-class-relationships.tsv](minecraft-class-relationships.tsv) records parsed class/superclass/interface relationships across 28,992 class entries. The broader 176-JAR filename inventory includes 153 profile JARs, three JRE JARs and 20 offline JARs including nested libraries; focused class parsing covers the 14 top-level core JARs, not every profile dependency.

[native-runtime-evidence.json](native-runtime-evidence.json) records all 14 native-directory DLLs, five native ZIP inventories, JRE metadata and selected REA resources. Thirteen installed game DLLs are x64; webp-imageio32.dll is x86. All ten DLL members in ul-natives-x86-win.zip are x64 despite the archive name. The v26_1_2/v26_2 client-native ZIPs have identical SHA-256 `a0c526513091c7feb64e223b8f84be9891b89a6ffb0a8962fdfed8edcfca58b8`. This establishes byte equality, not activation.

The initial discovery observation that the UI root's relationship required bridge evidence is now supplemented by Java/JavaScript host-contract corroboration in the Minecraft and game UI reports. Exact URL-to-root selection remains unresolved.
