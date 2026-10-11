# Launcher internals (session 2)

Study date: 2026-10-11. This is static text inspection of the installed ASAR; nothing was executed. No settings values, accounts or tokens were read.

## Sources and method

The ASAR is `C:/Users/Admin/AppData/Local/Programs/Lunar Client/resources/app.asar`. Selected members were copied to the scratchpad with a small Python ASAR reader ([session2-tools/asarx.py](session2-tools/asarx.py)). The original file was opened read-only.

| File | SHA-256 | Matches Codex? |
|---|---|---|
| `main.js` | `9781715efe843f763240bf27874f9604da9cb4a5b2959f5d6c1768a5e20540db` | Yes |
| `preload/launcher/index.js` | `d487d51504aa5ea42e3dde9cf92b08bc7baf511bcd163f43aa73e28587b3631b` | Yes |

The package declares version 3.7.24-ow.

### REA results

REA `analyze_javascript_application` (detail=summary, 4 GB worker heap) ran on `dist-electron/`. The parent Evidence is `ev_1659849506e89465f14c31ebb3238138504cf5f46da341249cf0f2ee05d6ca0d` and the summary view is `ev_9d06583ee64e6faca63d9645da6e8af86332f59b6435d3e8df5338bbb2778b05`.

- **Parsed:** 6 files, 1,234,282 AST nodes, 365 IPC operations, 353 literal channels, 4 contextBridge APIs, 36 exposed members, 0 parse failures.
- **Limitation:** the worker **exhausted its heap during semantic analysis of `main.js`**, so main-process handlers were not recovered (`main_handlers: 0`). This is a tool limit, not evidence of absence.
- The REA trace of `launch:launchGame` (`ev_52e2ac38dd6a56de8696ba1e86afe9dfbf873a528291e71c2104bff1938301c3`) matched the preload channel node. It expanded to 630 nodes and 152 paths, which are mostly containment relationships. It recovers no main-side handler.

The main-process facts below therefore come from direct text inspection of `main.js` (analyst `ctx.py`). Offsets are Python code-point indexes into the decoded file, and `main.js` is essentially ASCII. JS-* IDs are defined in [evidence-index.md](evidence-index.md). Minified identifiers apply to this build only.

## 1. Process structure and modules (verified, extending Codex)

- **Entry.** The tail of `main.js` runs `runApp` (`$9`). The renderer gets the preload `contextBridge` API. Main-process modules extend a base class `iE` whose `handle(name, fn)` registers `ipcMain.handle(prefix + ":" + name)`. This was confirmed again via the `launch` module `SGe`: `super("launch")`, then `handle("launchGame" | "cancel" | "respondMemoryWarning")` (JS-02).
- **State.** A Redux store `Z.store` (electron-redux bridged) holds `profiles`, `launch.phase` and `selectedProfileId`, `metadata.versions` with their subversion and module trees, `metadata.featureFlags`, `misc.logs`, and more.
- **Settings.** Settings are read through `Q.get(key)`, the `launcher` store. Keys used in the launch path include `game-branch`, `allocated-memory`, `game-resolution`, `jvm-args`, `garbage-collector`, `pre-launch-command`, `wrapper-command`, `post-exit-command`, `environment-variables`, `after-launch-action`, `mission-control-after-launch-action`, `game-update-preference`, `core-dump`, `enable-attach`, `log-retention`, `detach-game-process` and `include-snapshots`. **Per-profile `overrides` take precedence over global settings** for memory, resolution, JVM args, GC, hook commands and environment variables.
- **Windows.** The window manager `K9` handles `hideAll`, `getLunarWindow("main" | "mission-control")`, `switchRoute`, and `setGameFocused`/`setGameActive`.

## 2. Complete launch workflow: profile selection to Java start

```
Renderer: lunar.launch.launchGame(opts)  ── ipc "launch:launchGame" ──▶ SGe.launch(opts)
 └─ SGe.startLaunch(opts)                                                   (JS-02, @~4.84M)
     1. profile = profiles.find(id === launch.selectedProfileId) || default (OU()); else error NO_PROFILE_SELECTED
     2. require metadata loaded (Lunar / vanilla / Badlion variant) and no profile migration running
     3. QUICK-JOIN SHORTCUT: if opts.quickJoin.ip AND gameipc.hasConnectedClients():
            send PlayServerPush{autoJoinServerIp} + FocusGamePush to the running game and STOP   (JS-08)
     4. phase must be idle (else GAME_ALREADY_OPEN); optional migration-import prompt
     5. modpack/recommended-version resolution (Modrinth/CurseForge), content gate prompts
     6. claimProfile (prevents concurrent launch/delete of the same profile)
     7. resolve subVersion → major version → module (default module of the subversion);
        errors INVALID_VERSION / INVALID_MODULE / UNSUPPORTED_VERSION
     8. memory: opts.ram || profile.overrides.allocatedMemory || setting; modpack memory check/prompt
     9. branch/flags from setting "game-branch" (default "master"); AMD driver directory workaround
    10. collect overrides/settings (resolution, JVM args, GC, hooks, env vars, after-launch action…)
    11. launcherFeatureFlags = metadata.featureFlags split into enabled/disabled identifiers
    12. this.launchSession = new vGe({...})  ── LaunchSession                (JS-03, @4,828,770)
 └─ vGe constructor
     launchId = crypto.randomUUID(); Sentry transaction "launch-game"; analytics LaunchInit
     callbacks = {progress→aGe (sends "launch:onProgress"), log→iGe, exit→YWe, reset→oGe}
     startProcess(): Badlion → eRe | vanilla/modded → ZUe | Lunar → zUe
 └─ zUe (Lunar path)                                                        (JS-04, @4,775,560)
     a. lRe.call(): progress Authenticating "contacting-lc-servers";
        POST `${apiBase}/launch` {version, branch, args, module, canary_preference, profile{id,name,modrinth?}}
        server error → LauncherError(code, short, message)
     b. require response.jre (MISSING_JRE) and response.launchTypeData{artifacts, mainClass} (MISSING_LAUNCH_TYPE_DATA)
     c. LUe(response) builds stages, run as "parallel-stages" (progress Updating "downloading-lc-assets"):
          licenses (wUe) | textures index (AUe) | Minecraft assets (MRe) |
          group "artifacts-and-natives" [artifacts ARe, natives TUe] into .lunarclient/offline/multiver |
          JRE (CUe) | UI bundle (IUe)
        + Fabric loader stage (RUe/r0) for Fabric profiles
     d. ipcPort = gameipc.port || 28190; account = auth.getAccount()
     e. program args = yRe({... launchId, ipcPort, uiDir = <uiRoot>/<response.ui.sourceSha1> ...})   (JS-05)
     f. JVM args = bRe({allocatedMemory, artifacts, mainClass, programArguments, extraArguments,...})
     g. java = g$(jre)   (.lunarclient/jre/<folderChecksum>/<executablePathInArchive>)
     h. optional pre-launch / wrapper command resolution
     i. child_process.spawn(java, args, {cwd: launchDirectory, detached: setting "detach-game-process",
                                          env: {...process.env, ...attachEnv, ...userEnv}})   (@4,782,097)
     j. kRe(session, child) wires stdout/stderr → callbacks.log, exit → callbacks.exit
```

### Program arguments: exact key set (`yRe`, JS-05)

`--version`, `--launcherVersion`, `--launcherFeatureFlags` (JSON), `--installationId`, `--overwolfMuid`, `--sentryTraceId`, `--launchId`, `--canaryToken`, `--username`, `--uuid`, `--xuid`, `--accessToken`, `--userProperties` (`{}`), `--assetIndex`, `--gameDir`, `--assetsDir`, `--texturesDir`, `--uiDir`, `--webosrDir`, `--workingDirectory` (`.`), `--classpathDir`, `--modrinthModpackProjectId`, `--modrinthModpackVersionId`, `--curseforgeModpackModId`, `--curseforgeModpackFileId`, `--width`, `--height`, `--fullscreen`, `--server`, `--ipcPort`, and `--ichorClassPath` / `--ichorExternalFiles`. The last two are comma-joined artifact names of type `CLASS_PATH` / `EXTERNAL_FILE`. Keys with an undefined value are omitted.

The `--accessToken`, `--uuid` and `--xuid` flags exist, but their values are account data and were not read.

**Java-side counterpart (confirmed).** A Mixin on `net.minecraft.client.main.Main` registers matching joptsimple options for the Lunar-specific keys: `ipcPort`, `uiDir`, `webosrDir`, `launchId`, `installationId`, `launcherFeatureFlags` and others. It stores them in static fields of `L.util._038392` (JV-26). The vanilla keys (`--gameDir`, `--width` and so on) are parsed by Minecraft itself.

### JVM arguments (`bRe` and the GC policy `I$`, JS-05)

The order is:

1. metadata extra arguments;
2. `-Xmx<mem>m`;
3. `-Dichor.fabric.localModPath=` or `-Dichor.fabric.profileModPath=` (the mods directory);
4. `-Djava.library.path=<natives>`;
5. an optional `-Dichor.fabricLoaderVersion=`. The loader version is accepted only if it is at least `0.18.0`; otherwise the log says "Ichor cannot boot loader … using its recommended version";
6. `-Dlog4j.configurationFile=<profileLogs>/config.xml`, `-Dichor.logsFile=<profileLogs>/ichor-boot.log` and `-Dichor.usingIsolatedProfiles=true`, plus `-Dichor.usingIsolatedModpack=true` for provider modpacks;
7. `-XX:+DisableAttachMechanism`, unless the `enable-attach` setting is on;
8. `-XX:±CreateCoredumpOnCrash` and `-XX:±CreateMinidumpOnCrash`;
9. user JVM args;
10. `-cp <artifacts>`, then `mainClass`, then the program args.

GC policy for **26.1 and later only**:

- Metadata GC flags are dropped if the user selected G1/ZGC or passed their own `-XX:+Use*GC`.
- G1 appends `-XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M` and removes `-XX:+AlwaysPreTouch`.
- ZGC appends `-XX:+UseZGC`.

### Main class: closing the loop

- **Launcher side:** `mainClass` comes from `response.launchTypeData` returned by `POST /launch`. That response is unknown, because no network call was made.
- **Installed artifacts:** the Genesis manifest Main-Class is `com.moonsworth.lunar.genesis.Genesis`. Genesis' `ClientGameBootstrap` reflectively calls `MinecraftVersion.launchClass`, which `versions.conf` sets to `net.minecraft.client.main.Main` for every version in this build (FS-04, JV-27).
- **Conclusion.** It is a strong inference that the launcher's `mainClass` is Genesis. The final game entry is confirmed statically as vanilla `net.minecraft.client.main.Main`, which Lunar's Mixins extend.

## 3. Progress, state and the Java stdout contract (JS-01; confirmed across the process boundary)

The `log` callback (`iGe`, @4,821,842) parses every stdout and stderr line. It strips the `[HH:MM:SS]` prefix and `INFO]`/`WARN]`/`ERROR]` tags, batches lines into the Redux log store and a FlexSearch index, and reacts to markers that the **Java side prints**:

| Marker | Java emitter (JV-*) | Launcher reaction |
|---|---|---|
| `LUNARCLIENT_STATUS_PREINIT` | `ClientGameBootstrap.apply` @1041, before the reflective `main` | Generic: `timings.createStatusTimer("PREINIT")` |
| `LUNARCLIENT_STATUS_BUILD_CACHE` / `…_SAVING_CACHE` | Genesis cache builder `ML.genesis._cfe983` | `BUILD_CACHE` sets progress `BuildingCache` and marks `launch.cacheGenerated` |
| `LUNARCLIENT_STATUS_INIT` | Minecraft window creation: `VirtualScreen.newWindow` TAIL, or `RenderSystem.initRenderer` for 26.x | Progress `Launching "starting-game"`. If the after-launch action is `Hide` and no promotion holds the "play lock", it calls `K9.hideAll`, optionally keeping mission-control |
| `LUNARCLIENT_STATUS_STARTED` | `Minecraft.run` HEAD, after `new LunarClient()` | Progress `Launched "game-launched"`, `setGameFocused(true)`, `setGameActive(true)`, `sendLaunchSuccess()` |

Each marker also creates a status timer. `session.getLaunchStage()` returns the last recorded marker, or `PRE_LAUNCH` if none has arrived.

## 4. Error handling and recovery

**Launch errors** go through `YQ(session, code, subcode, short, description, classification?)` (JS-09). It resets callbacks and shows toasts or prompts. Codes seen on this path include `ABORTED`, `GAME_ALREADY_OPEN`, `NO_PROFILE_SELECTED`, `INVALID_VERSION`, `INVALID_MODULE`, `UNSUPPORTED_VERSION`, `MODPACK_REQUIRED/RESOLVE_FAILED`, `MISSING_JRE`, `MISSING_LAUNCH_TYPE_DATA`, `INVALID_ASSETS_URL`, `NO_SPACE_LEFT`, `UNEXPECTED_ERROR` and `UNKNOWN_ERROR/CLASSIFICATION_FAILED`. Server-side `response.error` becomes a `LauncherError(code)`.

**Exit classification** is done by `YWe(session, code, signal)` (JS-09):

| Exit | Treatment |
|---|---|
| code `0`, `SIGTERM` or `143`, and launch stage `STARTED` | Normal close. Optional "game closed" toast, then reset to ready. |
| Same exit, earlier stage | Treated as `ABORTED`. |
| Any other exit | Collects Windows application events (`JWe`), then runs crash classification `bWe(session, code, signal)`. The result supplies the analytics group/subgroup and user message passed to `YQ`. If no classification is found, the error is `UNKNOWN_ERROR`. |

**What this means in practice.** The Java stdout marker `STARTED` decides whether a clean exit counts as "game closed" or as an aborted launch.

**Cancel.** `vGe.cancel()` fires the `AbortController`. Every stage races against the abort signal (`cancelIfAborted`), and a toast distinguishes "closing" from "cancelling" according to the phase.

## 5. Local resource management

| Path | Purpose |
|---|---|
| `.lunarclient/offline/multiver` | Core artifacts and natives |
| `.lunarclient/shared` (`zz()`) | Minecraft assets and libraries |
| `.lunarclient/jre/<checksum>` | Java runtimes |
| `<uiRoot>/<ui.sourceSha1>` | The UI bundle passed as `--uiDir` (`Rz()` is the UI root) |
| `<webosrDir>` (`Lz()`) | Also used as `java.library.path` for natives |
| Per-profile log directory | log4j config and `ichor-boot.log` |

Archived game logs (`YYYY-MM-DD-N.log.gz`) are listed, read, searched and deleted by the `logs` module (`DGe`).

## 6. Corrections and additions to `launcher-architecture.md`

- **Added: the quick-join shortcut.** If a game is already connected over game IPC, launching with a server address does not spawn a new JVM. It sends `PlayServerPush` and `FocusGamePush` instead.
- **Added:** `launchId` is a per-session random UUID, passed as `--launchId`. The game echoes it in its IPC handshake (see [ipc-deep-dive.md](ipc-deep-dive.md)).
- **Added:** the full program-argument key set, the JVM argument order and the 26.1+ GC policy.
- **Clarified:** the stage set and concurrency. Six stage kinds run in parallel; artifacts then natives run sequentially inside one group; Fabric profiles add a loader stage.
- **Clarified:** stdout markers also drive exit classification, not only progress.
