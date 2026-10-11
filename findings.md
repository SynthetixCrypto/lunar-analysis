# Findings and study limits

Study date: **2026-10-11**. Static, read-only study of locally installed Lunar Client. The six requested reports are present. The work answers the observable architecture questions and records where available providers, obfuscation, access restrictions or runtime selection prevent a complete answer.

## Read first

- [inventory.md](inventory.md): verified paths, artifact counts, search/access scope.
- [launcher-architecture.md](launcher-architecture.md): Electron entry points, initialization, modules, metadata, JVM launch and IPC.
- [minecraft-client-architecture.md](minecraft-client-architecture.md): JAR/package/class relationships, bootstrap, Mixin integration, UI and game IPC.
- [component-map.md](component-map.md): component boundaries, shared files/settings, local IPC and declared network dependencies.
- [startup-flow.md](startup-flow.md): evidence-qualified startup sequence.

Supporting focused reports: [game UI](game-ui-architecture.md), [native/runtime inventory](native-runtime-inventory.md), [launcher native addons](launcher-native-addons.md).

## Finding ledger

Every “confirmed” statement below is about local bytes, metadata or static code, unless explicitly identified as a filesystem observation. It does not mean that the code executed during a particular launch.

| ID | Confirmed evidence and anchors | Inference / unresolved boundary |
|---|---|---|
| F-01: Installed launcher | Shortcut strings and REA PE resources identify `C:/Users/Admin/AppData/Local/Programs/Lunar Client/Lunar Client.exe`; 235,252,216 bytes, PE32+, 0x8664. SHA-256 and Evidence ID in inventory/launcher-pe-resources.json | Desktop host confirmed; full original install-directory enumeration is incomplete |
| F-02: Separate game data | `C:/Users/Admin/.lunarclient` contains offline/multiver, profiles, jre, settings, shared, ui and cache trees. discovery-inventory.json + artifact-index.tsv | Verified current-user installation; searches do not prove machinewide uniqueness |
| F-03: Electron package entry | ASAR manifest version 3.7.24-ow, Electron 42.7.1, main dist-electron/electron/main.js; main tail invokes runApp/$9. L-INIT and launcher-source-evidence.json | Shipped versions; no running-version query. Manifest Node build constraint is not embedded runtime proof |
| F-04: Initialization and component lifecycle | Main source has single-instance lock, app.whenReady, stores, window/module setup and cleanup. zQe/BQe registry; L-INIT/L-REGISTRY/L-SINGLEINSTANCE | Ordering within asynchronous branches is partial; no observed startup |
| F-05: Launcher renderer boundary | HTML module entry, BrowserWindow preload preferences, contextBridge namespaces, ipcMain prefix:name handler and launch:launchGame/progress contract. L-WINDOW/L-RENDERERENTRY/L-PRELOADBRIDGE/L-PRELOADLAUNCH/L-IPCBASE | Static boundary only; no security-enforcement claim. Optional child helper is separate from package main |
| F-06: Metadata-driven Minecraft start | FKe version refresh; lRe POST launch; LUe preparation stages; g$ runtime path; bRe/yRe argument builders; zUe child_process.spawn. L-METADATA/L-LAUNCHREQUEST/L-STAGES/L-JREPATH/L-JVMARGS/L-ARGDIRS/L-SPAWN | Effective mainClass, selected runtime/profile, command line and environment remain unknown |
| F-07: Cached JVM choices | JRE release files and java.exe PE headers confirm Zulu 21.0.1, 21.0.10 and 25.0.1, all x64. native-runtime-evidence.json | Cached alternatives, not proof of historical or current selection |
| F-08: Minecraft artifact architecture | 14 core JARs, 28,992 parsed class entries including shaded/duplicate classes, zero parser errors. minecraft-artifacts.json, minecraft-jar-entries.tsv, minecraft-class-relationships.tsv | Not a count of unique Lunar feature classes or an exhaustive active dependency graph |
| F-09: Genesis bootstrap | Manifest Main-Class Genesis; main/run, Prelaunch/Game classloader references, bootstrap records and reflective main invocation in ClientGameBootstrap.apply. minecraft-bootstrap-metadata.json; REA Genesis evidence below | Installed entry candidate. Launcher metadata must select it; exact Minecraft reflective main target unresolved |
| F-10: Minecraft integration hooks | 184 Mixin configs, 2,332 class-level Mixin annotations; lifecycle/render/input/screen/options targets, accesswidener declarations. minecraft-mixin-metadata.json + minecraft-accesswidener-metadata.json | Declared transformations and compatibility layers; no proof of activation/success for any selected version |
| F-11: Game browser host bridge | Java Browser/NativeHandle/FunctionBus classes; bytecode loads lunarInternalInvoke at 58, obtains FunctionBus at 61, invokes Browser.bindFunction at 64. Document-ready IIFE injects lunar/lunarReady/lunarInternalAccept. Exact class paths in minecraft-ui-bridge-metadata.json | Directly corroborates JS host contract; full construction chain/threading and exact URL/root selection unresolved |
| F-12: Game React UI/feature boundaries | Hashed UI bundle includes React/Redux, ready polling, namespace provider calls, payload subscriptions, routes, settings/mod/HUD/model/input APIs. GUI-01–GUI-10 in game-ui-evidence.json | Feature-facing contracts are mapped; native feature algorithms and complete mod manager/config schema are not reconstructed |
| F-13: Paired launcher/game IPC | Main bLe declares 127.0.0.1 WebSocket server, initial 28190 with retries; --ipcPort passed; Java WebSocketClient constructs loopback URI and protobuf handlers. L-GAMEIPC/L-ARGIPC/L-PORTSELECT/L-GAMEIPCMESSAGES + minecraft-ipc-metadata.json | Matching static contracts strongly support pairing; no actual bound port, connection or payload recorded |
| F-14: Native boundaries | WebOSR JNI browser/texture/input exports align with Java methods and Ultralight/WebCore imports. MumbleLink imports file-mapping APIs. Native ZIP PE headers and hashes preserved | Embedded browser architecture strongly supported. Mumble shared-memory IPC is inference; no native disassembly or live calls |
| F-15: Architecture filenames are misleading | All 10 DLLs in ul-natives-x86-win.zip are x64; installed webp-imageio32.dll is x86 and webp-imageio64.dll x64. native-runtime-evidence.json | Filename “x86” is not sufficient to identify member architecture |
| F-16: Native launcher addons | bsdiff, SQLite, diskusage, iselevated are x64 PE; registration/import/export details in launcher-native-addons.json. First two export node_register_module_v146; iselevated has Node-API registration | ABI declarations do not prove runtime loading/compatibility; Node-API suffix is not the requested API level |
| F-17: Network dependencies | Static API/update/remote WebSocket/analytics helpers and game UI asset/font/proxy/iframe/Sentry declarations. L-APIBASE/L-REMOTEWS/L-UPDATEBASE, GUI-11–GUI-14 | Declared endpoints/conditional branches only; no traffic captured or remote resources fetched |
| F-18: Obfuscation limits | 4,421/4,439 com/moonsworth/lunar/client class entries have final segments matching the shipped CHIORS-alphabet pattern; JS bundles minified, source maps unavailable | Descriptive pattern, not obfuscator attribution. No deobfuscation, mapping application, protection bypass or protected-code recovery attempted |
| F-19: ASAR helper integrity discrepancy | REA records three unpacked 7za files whose observed hashes differ from declared ASAR metadata. Full expected/observed values below and in extraction evidence | Cause unknown; no tampering/security verdict. Helpers were not executed |
| F-20: Incomplete automatic graph | REA parsed 1,030 JS files/42,439,388 text bytes, but semantic expansion hit its result budget. launcher-rea-summary.json and focused source evidence preserve bounded coverage | Missing graph relationships are not evidence of absence; source inspection independently confirms windows and IPC contracts |

## Integrity discrepancy record

Archive: `C:/Users/Admin/AppData/Local/Programs/Lunar Client/resources/app.asar`, SHA-256 `506574f17a6b7aeb5a13fe5f53fc83329fa705141505dde30ec88e00aa03a9f4`.

REA initially rejected strict extraction because three unpacked 7za helpers contradicted archive integrity declarations. It then used its supported **record-and-continue** policy for inert static materialization. This preserved discrepancies rather than claiming validated integrity. No application integrity check was disabled or modified.

| Logical helper architecture | Declared SHA-256 | Observed SHA-256 |
|---|---|---|
| arm64 | `81f67048b7366870e5d49f00a8c570570c6a0dd11c05df7a09a8c52870cc83bd` | `43971691e77d5431fcdde393318b4d4c5abe74ff20f4140dc772fe03eb6fd3ad` |
| ia32 | `31fd52f8996986623cf52c3b4d0f7ac74a9dec63fc16c902cef673eed550c435` | `4e42ead072f8916066a3038e0108532288a280624a9d2e6b716d436564b21b57` |
| x64 | `b0cfdeaf429f5cc53f85123dd8f5a5feb92c19d31aa34df257edf9a26be05f95` | `f9dbc5f3a2c3508edf6eff866cebb09cf4a421519f05794b92a4724dfe82669e` |

Exact logical paths and contradictions are in [launcher-asar-extraction-evidence.json](launcher-asar-extraction-evidence.json). No cause was established. Signing/packaging differences and modification are possibilities, not findings.

## Provider and evidence accounting

REA availability was checked before dependent analysis. Static JavaScript, archive and portable PE-resource providers were usable. Ghidra/IDA were not configured, Hopper was unsupported on Windows, and JEB/JADX were unavailable. Managed PE/CLI support was not treated as a Java parser. No engine was installed or configured. [provider-availability.json](provider-availability.json) preserves the availability observations.

REA directly supplied launcher JavaScript analysis, archive materialization/inventory, PE resources and Genesis archive evidence. Read-only filesystem, ZIP, JVM-classfile and PE-header parsing supplemented missing providers. These supplemental outputs are identified as analyst evidence, never presented as REA decompilation.

| Evidence | Retained identifier | Locally preserved form |
|---|---|---|
| Launcher PE resources | ev_54a5c81c3b5d0c5eb74874e623d2d26b1fc7ad238d084afc6c84c6f79c538623 | launcher-pe-resources.json, complete bounded record |
| Launcher JS application parent | ev_c5630573420a09f17aaa0bc744bdc75cf679447e3edc2dd6448ee48e2910ec5d | Compact analyst summary, module index, entry projections and selected source excerpts; **not** the full parent graph |
| Launcher JS summary view | ev_0cd9f37b4693713763406cca63ccb92d224ad484040db854b7dce49f2ea70c34 | launcher-rea-summary.json, compact projection |
| Launcher ASAR materialization | ev_31648b1ec89765d65a3cd9a6929cd7461fb4a5a4ab47e7da16d3ed9fbd42c71a | launcher-asar-extraction-evidence.json, complete bounded extraction record |
| Genesis archive | ev_3dfa373be43e21b36815c27464dbd7b08fa52a525ac0995bc2cfc9a6c7e378a7 | rea-evidence-through-genesis.json, full two-record export |
| Genesis linked inventory | ev_abd81f72db9d0318d3f5953315cfdcb138c8462fdbbea1dca5ed840efb52cb24 | Same export |
| MumbleLink PE resources | ev_ce47b2c1768f5fdd35a762b2fc69b9cf8694d50d1f53e0fce8c7b185c6153001 | Complete inline record in native-runtime-evidence.json |
| WebOSR PE resources | ev_1754d1892de23136481a3896993038130ace56740dd41b5f11c0f502fb1b7a0e | Complete inline record in native-runtime-evidence.json |

The roughly 2.04GB launcher parent graph was not exported wholesale. Focused local evidence preserves the report's observations, but does not substitute for full graph reproducibility. Temporary ASAR materialization paths are provenance, not permanent source dependencies; hashes and excerpts remain in the analysis folder. Evidence IDs are session locators and may cease to resolve after session cleanup.

## Coverage and unanswered questions

| Requested area | Result |
|---|---|
| Discovery, separation, formats/runtime/dependency inventory | Answered within documented bounded search; inaccessible directories and skipped private/cache trees recorded |
| Launcher entry, initialization, configuration/version management, Minecraft start | Focused static paths traced; major registry mapped; full internal graph partial |
| Minecraft packages/classes/interfaces, initialization and integration | Core archive inventory/relationships and focused bootstrap/Mixin/UI/IPC paths recorded; obfuscated feature internals partial |
| Launcher/game integration, startup, shared settings/files and dependencies | Matching code contracts mapped; effective runtime choices and active network state unknown |
| Six analysis documents | Created, with companion evidence files and source anchors |

Still unresolved: exact effective Minecraft main class; selected JRE/profile/artifact/Mixin set; full core feature/module/event architecture; game configuration filenames/schema and values; native rendering thread/texture composition; exact UI URL hosting; all reflective targets; active IPC/network/service state; inaccessible AppData directories and remaining install-tree files.

No Lunar executable, JAR or native addon was executed; no application JavaScript was evaluated. No Lunar files were modified, protections bypassed, anti-cheat mechanisms inspected/interfered with, credentials/tokens extracted, or runtime/network collection performed. Dynamic analysis was not undertaken and would require separate user approval.
