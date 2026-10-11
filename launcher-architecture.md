# Desktop launcher architecture

## Scope and evidence

**Confirmed artifact identity:** installed launcher `C:\Users\Admin\AppData\Local\Programs\Lunar Client\Lunar Client.exe`; AMD64 PE32+; SHA-256 `e21d5ad61a3caec8e25948a52f3a0157b9e875ef6cd9a47cd1ee874a7e58f5e6`. REA PE Evidence: `ev_54a5c81c3b5d0c5eb74874e623d2d26b1fc7ad238d084afc6c84c6f79c538623`.

**Confirmed package metadata:** `resources/app.asar!package.json` names lunarclient, version **3.7.24-ow**, Electron **42.7.1**, branch master, commit `b9f6f4488584f73e8682c6b16f4f60e2af588f16`. These are shipped declarations; no running-version query was made. Its main field is `dist-electron/electron/main.js`. The manifest declares Overwolf packages overlay and crn. It declares Node >=24.x and pnpm@12.4.2 as build/package constraints; those fields do not independently establish the embedded Node runtime version.

REA JavaScript application parent: `ev_c5630573420a09f17aaa0bc744bdc75cf679447e3edc2dd6448ee48e2910ec5d`; summary projection: `ev_0cd9f37b4693713763406cca63ccb92d224ad484040db854b7dce49f2ea70c34`. REA parsed 1,030 JS files in the installed tree, read 42,439,388 text bytes, and inventoried 1,240 relevant files including one ASAR. Application/semantic coverage is partial; semantic expansion exhausted the result budget. Zero recovered BrowserWindow nodes and zero automatically paired launch IPC operations are **not evidence of absence**: supplemental source inspection below finds both.

REA safely materialized ASAR regular files into its own temporary directory, without changing the installation. Extraction Evidence `ev_31648b1ec89765d65a3cd9a6929cd7461fb4a5a4ab47e7da16d3ed9fbd42c71a`; ASAR SHA-256 `506574f17a6b7aeb5a13fe5f53fc83329fa705141505dde30ec88e00aa03a9f4`; inventory manifest `agm_db3eeb076b79554980752bd91c02488f7c62391a35cf86129edf853d5507b9cd`. The 1,324 materialized regular-file occurrences include 970 JS/MJS/CJS files, seven HTML entry pages, four native .node addons, and three Windows 7za helpers.

Supporting files: complete `launcher-asar-extraction-evidence.json`, complete `launcher-pe-resources.json`, compact `launcher-rea-summary.json`, `launcher-module-index.jsonl`, and **supplemental** `launcher-source-evidence.json`. L-* IDs below refer to the last file. It records exact source hashes, excerpts, UTF-16 character offsets, UTF-8 byte offsets, and line/column anchors. Original paths are ASAR logical members relative to `resources/app.asar`. Minified symbol names identify this exact build only.

## Entry points and initialization

**Confirmed static entry:** package.json selects main.js (5,739,762 bytes; SHA-256 `9781715efe843f763240bf27874f9604da9cb4a5b2959f5d6c1768a5e20540db`). The tail exports `runApp=$9` and invokes `$9()`. Pre-ready code validates the default Lunar directory, obtains a single-instance lock through `n1e`, constructs Redux/store and service factories, and sets DNS ordering. The root helper `a_` defaults to `path.join(os.homedir(), ".lunarclient")`; another setter can replace it, so this is a code default, not a universal immutable path. Evidence L-PATHS, L-SINGLEINSTANCE, L-INIT.

**Confirmed static ready branch:** `$9` registers an `app.whenReady().then(...)` callback. It configures production login/startup options and tray, processes launch arguments/deeplinks/pack imports, calls analytics setup, initializes windows with `K9.setup()`, and initializes modules with `$.setup()`. Profile migration finishes through a finally callback before one updater check. The before-quit handler calls cleanup on factories/stores; SIGINT/SIGTERM handlers request quit. This describes control flow in code, not an observed startup.

**Confirmed renderer entry:** `dist/html/main.html` declares `../assets/main.js` as a module script, root/loading-screen elements, stylesheet links and module preloads. Other HTML pages are embedded-browser, embedded-checkout, mission-control, satellite, updater, and visualise-resolution. Renderer assets also include redux-hooks, topbar, input, theme-wrapper, hooks, and progress-bar. Filenames identify packaged components; UI responsibilities beyond inspected declarations are inference. Evidence L-RENDERERENTRY and ASAR extraction.

**Confirmed separate native-helper entry:** `dist-electron/electron/index.js` is **not** package.json's main entry. It implements child-process message dispatch, dynamically requires `native-modules/launcher.node` relative to the executable, sends load/return/error/callback messages, and registers a process message handler. The associated `fork` call in main.js and its log labels belong to the optional Badlion integration. Its presence does not establish that Lunar's ordinary launch uses this native bridge, nor that the external launcher.node exists. No protection bypass or addon loading was attempted. Evidence L-NATIVECHILD; source main.js near character 3,462,063.

## Stores, paths and version management

**Confirmed:** `ZM` constructs a `Gk` store named launcher at `KT()`; KT returns `.lunarclient/settings`. It supplies migration callbacks and clearInvalidConfig:true. Setting wrappers include allocated memory, game branch, game resolution, after-launch action, advanced mode, custom launch/environment behavior and many notification/UI options. `KSe` constructs the parallel cache store at the same directory. Filesystem discovery independently confirms launcher.json and cache.json. Values, account records and user preferences were not inspected. Evidence L-SETTINGS, L-CACHE, L-DIRS.

**Confirmed:** `FKe` is the metadata module. It registers branch/stream handlers, calls `fetchAndStore({init:true})` and schedules refresh. Helper `uWe` issues GET `/launcher/metadata/versions/lunar` with selected branch; adjacent helpers request metadata/layout and metadata/misc. Returned versions are converted into Redux state and subversion asset URL/SHA-1/index records. Metadata may replace the updater feed/channel. Evidence L-METADATA and FKe/NKe source anchors in this report.

**Confirmed:** `l0e` owns the launcher updater, generic feed URL/channel, listeners and checks. The bundled channel is latest-ow and the bundled production host is launcher-releases.lunarclientprod.com. Its interval uses metadata.refreshIntervals.updates with a 900,000ms fallback; it has development/test/migration/check-lock/downloaded-update branches. This establishes available update logic, not that any check/download/install occurred. Evidence L-UPDATER, L-UPDATEBASE.

**Inference:** launcher self-updates and Minecraft artifact/version updates are distinct subsystems. This is supported by the updater feed logic versus the launch metadata/artifact pipeline, not merely by directory names.

## Launching Minecraft

The Lunar-specific path is confirmed as static control flow:

1. Preload `lunar.launch.launchGame` invokes Electron IPC `launch:launchGame`. `SGe.onSetup` registers `handle("launchGame", ... this.launch(...))`. The module base `iE.handle` constructs `prefix + ":" + method`, resolving the otherwise dynamic handler channel. Evidence L-PRELOADLAUNCH, L-IPCBASE, L-LAUNCHHANDLER.
2. `lRe.call` POSTs to `/launcher/launch` with requested subversion, branch, flags, module and profile metadata. `zUe` reads returned JRE and launchTypeData; the latter supplies artifacts and **mainClass**. Missing fields produce explicit errors. Evidence L-LAUNCHREQUEST, launchPreparation observation from source.
3. `LUe` composes preparation stages: shared Minecraft assets, core artifacts and natives, licenses, textures, JRE, and UI, with additional modpack/Fabric checks when applicable. Core cache root is `.lunarclient/offline/multiver`; shared assets/libraries use `.lunarclient/shared`. These are the code's paths; no downloads were triggered. Evidence L-STAGES, L-DIRS.
4. JRE helper `g$` joins `.lunarclient/jre/<folderChecksum>` with returned executablePathInArchive. Therefore the selected Java executable is metadata driven. Three installed x64 Zulu runtimes corroborate the cache layout; selecting one for a specific version remains unknown. Evidence L-JREPATH and native-runtime-inventory.md.
5. `yRe` builds program flags for gameDir, assetsDir, texturesDir, UI directory, WebOSR directory, classpath cache, version, window dimensions and IPC port. Versioned UI selection appends metadata.ui.sourceSha1 when supplied. Artifacts marked CLASS_PATH/EXTERNAL_FILE become Ichor classpath/external-file lists. No runtime identity or authentication values were collected. Evidence L-ARGDIRS, L-ARGIPC.
6. `bRe` assembles JVM options, memory, native library path, classpath, selected mainClass and program arguments. On Windows the classpath separator is semicolon. It also constructs normal launch-time attach/core-dump options; this study did not change them. Evidence L-JVMARGS.
7. `zUe` resolves optional user prelaunch/wrapper/post-exit commands, then invokes Node `child_process.spawn(j,M,{cwd:h,detached:F,env:...})`. The returned object records JVM start time and PID; `kRe` attaches process stdout/stderr/exit/error callbacks. Optional user commands are code capabilities; none was executed and no configured command values were read. Evidence L-SPAWN, main.js character 4,782,092.

**Unknown:** the actual server response for this installation/session and therefore its exact selected mainClass, runtime, artifact set, command line and active profile. The installed Genesis JAR declares a main class and matches the bootstrap role, but static launcher code supplies the main class from remote metadata. It would be inaccurate to assert that the launcher always chooses Genesis or always launches one Minecraft version.

Vanilla, modpack, OptiFine/Forge processor, and Badlion-related branches coexist in the bundle. The primary trace above follows the Lunar branch; presence of other branches does not show they are active.

## Component boundaries and IPC

| Boundary | Confirmed declarations | Interpretation / limits |
|---|---|---|
| Renderer to Electron main | contextBridge exposes electron and lunar namespaces; explicit invoke/listen calls; iE creates namespaced ipcMain handlers | Electron IPC boundary. L-PRELOADBRIDGE, L-PRELOADLAUNCH, L-IPCBASE. |
| Redux state sharing | __ElectronReduxBridge exposes electron-redux state enhancers; synchronous/async initial state and action channels | State synchronization code is present; payload contents were not collected. |
| Launcher to Java game | bLe creates a ws server on host 127.0.0.1, initial port 28190, with port retries; selected port passed as --ipcPort | Matching Java client declarations independently confirm the protocol boundary. Actual bound port/traffic unknown. |
| Game RPC and pushes | LauncherboundIPCMessage.decode, service/method registry dispatch, GameboundIPCMessage responses and protobuf Any pushes | Confirmed static protobuf envelope flow. L-GAMEIPCMESSAGES, L-GAMEIPCPUSH. |
| Per-connection identification | gLe reads an lc-handshake header, decodes a Handshake, checks expected launch/installation fields and closes rejected connections | Code-level checks only; no header values or handshake contents collected; no security-enforcement claim. |
| Optional native child | process messages for native-call requests/returns/callbacks, forked index.js, launcher.node request | Optional Badlion-labeled boundary; actual addon existence/use unconfirmed. |
| Native utility addons | bsdiff.node, better_sqlite3.node, diskusage.node, iselevated.node | Confirmed packaged modules. Source requests or exports do not establish runtime calls. See launcher-native-addons.md. |

The preload includes an explicit allowlist for selected renderer listener channels and exposes grouped API methods rather than raw arbitrary invoke in the inspected lunar namespace. Window base code constructs contextIsolation:true, nodeIntegration:false, sandbox:false and webSecurity:app.isPackaged with the launcher preload. These are static option values; this study did not test security properties or runtime enforcement. L-WINDOW and L-PRELOADBRIDGE.

## Major module map

The registry `zQe` maps named modules to constructors; `BQe` constructs them, invokes setup in registry order, marks setup complete and invokes onFactorySetupComplete. Cleanup visits registered modules. `getModule` checks the setup flag. Evidence L-REGISTRY.

| Module / symbol | Responsibility supported by code | Confidence |
|---|---|---|
| launch / SGe | Launch/cancel/memory-warning lifecycle and launch sessions | Confirmed traced methods |
| gameipc / bLe, gLe | Loopback game connections, RPC responses and queued pushes | Confirmed traced methods |
| metadata / FKe | Remote layout/misc/version state and branch/stream refresh | Confirmed traced methods |
| profiles / HXe | Profile lookup/selection, mod directories and migration integration | Confirmed call boundaries; full implementation partial |
| auth / CAe | Account/login interface consulted by launch preparation | Confirmed boundary; secret-bearing files excluded |
| windows / A0e | Window creation, instance management, routes, focus/game state | Confirmed inspected methods; separate factory |
| updater / l0e | Launcher update checks/feed/channel/install lifecycle | Confirmed traced methods; separate factory |
| settings / ZM; cache / KSe | Typed settings and cached UI/metadata state | Confirmed construction; actual values excluded |
| assetserver / NR | Remote launcher service connection, heartbeat and push dispatch | Confirmed registry and protocol declarations; full service map partial |
| modrinth, curseforge, external-import, installs | Content/provider and installation workflows | Registry labels plus launch call sites; full behavior untraced |
| notifications, discord, cosmetics, promotions, styngr, socials | Named integration/service areas | Confirmed registry presence; responsibility largely inferred from names/call sites |
| servers, worlds, screenshots, notes, satellite, checkout, overwolf, badlion, connection, hosts-check, deeplink, logs, logupload | Additional named modules/integrations | Registry presence confirmed; only focused boundaries examined |

Declared package dependencies include fs-extra, chokidar, superstruct, ofetch, ws/socket.io-client, electron-redux, 7zip-bin/node-7z, extract-zip, @lunarclient/bsdiff-node, better-sqlite3, diskusage, native-is-elevated, prismarine-nbt, minecraft-server-util, smol-toml and shell-quote. Their manifest ranges are preserved in launcher-source-evidence.json. A declared dependency is not proof that every code path invokes it.

## Static network dependencies

Confirmed source declarations/call sites include production API base `https://api.lunarclientprod.com`, metadata and launch endpoints beneath /launcher, remote `wss://websocket.lunarclientprod.com/launcher-v3`, a separate authenticator WebSocket base, launcher update feed host, thirdpartycache helper, and analytics event-batch helper. Development/production choice is conditional in the code. Third-party provider, Microsoft/Xbox/Minecraft, Discord, Overwolf, payment and telemetry integrations also occur; not every literal URL is an automatically contacted dependency.

No destination was contacted, no network traffic captured, and no credentials/tokens/user payloads collected. See component-map.md for the bounded dependency interpretation.

## Integrity and remaining limits

REA found three unpacked 7za helpers whose observed bytes contradict declared ASAR integrity metadata (arm64, ia32, x64). The study used record-and-continue, preserved all expected/observed hashes, and treats those helpers as observed-untrusted. The cause is unknown. The discrepancy does not by itself establish tampering, nor did this study defeat integrity checks.

No source maps were materialized; sourceMappingURL comments are not evidence of available maps. The bundle is minified; original class/module names are mostly unavailable. Native disassembly providers are unavailable, and no native binary/addon was loaded. Semantic REA coverage is partial; supplemental inert text inspection fills specific questions and is labeled separately. The installed directory outside ASAR and selected inaccessible AppData data directories are not exhaustively enumerated. Dynamic startup, actual services, current defaults, selected metadata and runtime behavior remain unobserved.
