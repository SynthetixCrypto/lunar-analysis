# Evidence index (session 2)

Study date: 2026-10-11. This index consolidates the findings in [java-internals.md](java-internals.md), [module-lifecycle.md](module-lifecycle.md), [launcher-internals.md](launcher-internals.md), [ipc-deep-dive.md](ipc-deep-dive.md) and [rendering-and-hud.md](rendering-and-hud.md). Codex's earlier evidence IDs (F-*, L-*, GUI-*, ME-*) remain valid and are referenced where relevant.

## Tools and reproducibility

| Tool | Version / identity | What it produced | Status in this session |
|---|---|---|---|
| REA MCP | rea-agents 6.4.0 | `binary_session`, `open_binary`, `inspect_artifact`, `analyze_javascript_application`, `trace_application_feature`, `get_evidence_bundle`, `export_evidence_bundle`, `close_binary` | Available for archive and JS work. Ghidra and IDA not configured, Hopper unsupported, no JVM decompiler. JS analysis of `main.js` hit the 4 GB worker heap limit. |
| JDK `javap` | Microsoft JDK 21.0.10 (preinstalled) | Bytecode disassembly (`-p -c`, plus `-v` for selected constant pools) | Used for all Java facts (JV-*) |
| Analyst Python | Python 3.11, protobuf 7.35.1 | Class index and alias rendering ([session2-tools/](session2-tools/)), Lombok-name recovery, protobuf descriptor decoding, ASAR member extraction, JSON key-structure listing | Static parsing only |
| Shell | Git-bash `unzip`, `sha256sum`, `grep` | Hashes, file lists, versions.conf reading | — |

**Aliases.** Short aliases (`L._88f3cf._cfe983`, …) come from an MD5-prefix rendering of each 30-character obfuscated segment. [session2-class-legend.md](session2-class-legend.md) gives the exact JVM class for every alias used, and `session2-tools/rev.py` reverses aliases.

**Bytecode offsets** are positions within the named method's `Code` attribute as printed by javap. **`main.js` offsets** are Python code-point indexes into the decoded `main.js` (SHA-256 `9781715e…`).

**Retained REA Evidence.** All five session records are exported to [rea-evidence-session2.json](rea-evidence-session2.json) (62,965,098 bytes).

| Evidence ID | Operation | Subject |
|---|---|---|
| `ev_3a3bda3688dc8b47b22d734d6f12c6d675194d7851c58355fc7168468ea328e4` | inspect_artifact | lunar.jar (`bf36e10e…`) |
| `ev_240074aaa2df47784569e96d463ee762f2ea067d31a72d4ca069a126bba4521a` | inventory_artifact | lunar.jar: 19,664 nodes, 19,685 occurrences, 0 integrity contradictions, manifest `agm_f3d5c476…` |
| `ev_1659849506e89465f14c31ebb3238138504cf5f46da341249cf0f2ee05d6ca0d` | analyze_javascript_application | Extracted `dist-electron/` (directory digest `96a2656f…`) |
| `ev_9d06583ee64e6faca63d9645da6e8af86332f59b6435d3e8df5338bbb2778b05` | inspect_analysis_view | Summary of the above |
| `ev_52e2ac38dd6a56de8696ba1e86afe9dfbf873a528291e71c2104bff1938301c3` | trace_application_feature | Seed channel `launch:launchGame` |

## Ledger

Confidence levels: **C** = Confirmed (directly observed), **S** = Strong inference, **T** = Tentative, **U** = Unknown.

### Java side (source: `.lunarclient/offline/multiver/*.jar`; tool: javap and analyst scripts)

| ID | Artifact / class.method @offset | Finding | Conf. | Open question |
|---|---|---|---|---|
| JV-01 | modern: Minecraft Mixin `ML._d4ca6c._1e73d7._590f69._a140a8.impl$run` (Inject `Minecraft.run` HEAD) @120–128 | `new L._cfe983()` (client singleton), then log `LUNARCLIENT_STATUS_STARTED` | C | — |
| JV-02 | same Mixin `lunar$initMessage$v26_1` (min 36) and `…_88f3cf._2b0ee0.lunar$initMessage` (`VirtualScreen.newWindow` TAIL) | stdout `LUNARCLIENT_STATUS_INIT` at window creation | C | — |
| JV-03 | `L._cfe983.<init>` @38–1740 | Constructor order and log literals; event bus lock held across init | C | What `ML._cfe983._cfe983.start()` does |
| JV-04 | `L._cfe983.start()` | `"Lunar.start"`, manager `init()` loop with `"Manager Init"` error reporting, `"Launching"` | C | — |
| JV-05 | `L._d4ca6c._590f69` (register/post/static init) | Priority-sorted copy-on-write handler arrays, deferred registration during dispatch, lazy event construction, per-handler Throwable isolation, thread-check variant selection | C | Thread-check subclass semantics (T) |
| JV-06 | `L._88f3cf._cfe983.<init>(Z)` @0–118 | Trait container, `load_state=CONSTRUCTOR`, default-enabled flag | C | — |
| JV-07 | `L._88f3cf._02d7ad.<clinit>` | 21 named trait keys | C | Semantics of `panel`, `page`, `index` and `display` traits (T) |
| JV-08 | `L._88f3cf._cfe983.handle` → `L._88f3cf._1e73d7._429bf0` | Default priority 100; handlers attach to the bus only while active; propagation to children | C | — |
| JV-09 | `L._88f3cf._cfe983.updateEnabled` | Precedence: parent → support → restriction → intercept Optional → own | C | Which features carry support or restriction traits (U) |
| JV-10 | `L._02d7ad._1253fc._1eb51c` (`_a1ad6f`, `_a55711`, `_8d9bc5`, `_de9126`) | Hardcoded registry (119 feature constructions); file `settings/game/<Profile>/mods.json`; publishes `details` and `features` payloads | C | The `removeIf` filter in `_535838` (U) |
| JV-11 | `L._02d7ad._cfe983.load/_590f69` | Root `version`, migrator, per-feature objects, `LOADED_CONFIG`, empty objects omitted | C | Migration rules in `L._2b0ee0._cfe983._bb4487` (U) |
| JV-12 | `L._88f3cf._cfe983.load` / `_cfe983(JsonObject,List)` | Iterates serializable nodes; re-runs when traits grow | C | — |
| JV-13 | `L._ec7e36._13ea87.load/_590f69/_1e73d7` | DFU-style Codec parse and encode; `{value, children}` object form; only non-default values written; Apollo `ModSettingModule` broadcast on change | C | Apollo broadcast payload format (U) |
| JV-14 | `L._02d7ad._d4ca6c._5d96a0/_1f5a0f` | Gson load; read-merge-write save, synchronous, not atomic; `"Saved File: [%s]"` | C | — |
| JV-15 | `L._02d7ad._1253fc._3a14e3._145809/_d87130` | Save-on-change; publishes `general`, `performance` and `controls` payloads | C | — |
| JV-16 | `L._81676d._21aca6._d4ca6c._cfe983._ba7d98` (`@CallbackJS`) + `…_cfe983._88f3cf._cfe983(Scope,String,String)` | `update` → scope lookup → `setting._d2c28f(String)` | C | String→value parsing per type (T) |
| JV-17 | GameRenderer Mixin `…_13ea87._d4ca6c` (`lunar$renderGui$*`, `lunar$renderGameOverlay$v26_1`, `lunar$fireEvent2D`) | 2D event posting with HUD scale; 26.x strata splice; profiler `event2d` | C | — |
| JV-18 | `L._88f3cf._590f69._cfe983.<clinit>` and static handlers | Global HUD render loop over features and `hud_renderer` traits | C | Exact gate boolean (T) |
| JV-19 | `L._88f3cf._590f69._cfe983` (`_cfe983/_21aca6(anchor,double)`, `load`, `_590f69`, `_3a82ee`) + `$1` switch map | Anchor math table; persistence rules; ×2 UI coordinates | C (×2 meaning S) | — |
| JV-20 | `L._88f3cf._590f69._88f3cf` (`_52e8ee`, `_cfe983(event,…)`, `<clinit>`) | Per-frame content pull; String/Component/icon renderers; style settings | C | — |
| JV-21 | `L._88f3cf._bb4487._145809._cfe983` | FPS lifecycle | C | Preview-value helper (T) |
| JV-22 | `L._88f3cf._bb4487._6c713e._cfe983`, `$_cfe983`, `L._ba7d98._590f69._cfe983` | CPS: 1 s sliding window, three lists, divider drawing | C | Separator string literals (U) |
| JV-23 | MouseHandler Mixin `…_1e73d7._2f4182.lunar$onPress` | Post mouse event, cancellable; forward to GameUI; version gate max 32 / min 33 | C | — |
| JV-24 | `L._88f3cf._bb4487._136819._cfe983` | ZOOM: settings, defaults and ranges, FOV, tick, scroll and screen handlers | C | Consumer of `cameraSensitivity` (U) |
| JV-25 | genesis: `ML.ichor._cfe983._21aca6`, `ML.ichor._1253fc._1253fc`, `ML.ichor._1253fc._d4ca6c` | Version and condition annotations; ASM member removal and comparison folding (`_543b36` opcodes 153–164); Lorenz mappings | C (mapping source S) | Full pipeline order (U) |
| JV-26 | modern: Main Mixin `…_1e73d7._88f3cf` (`lunar$main$options$*`, `lunar$main$parse`) | joptsimple options for Lunar CLI keys, stored into `L.util._038392` | C | — (the `lunar$main$parse` store order confirms uiDir→`_8d6c5d`, webosrDir→`_155716`, ipcPort→`_0e3e07`, launchId→`_539ac8`, installationId→`_37ebd5`) |
| JV-27 | genesis: `ClientGameBootstrap.apply` @1041, @1094–1456 | `PREINIT` marker; `Class.forName(MinecraftVersion.launchClass)`; `getMethod("main")`; invoke | C | — |
| JV-28 | `L._81676d._21aca6._21aca6.<clinit>/<init>` | `lunar.webosr.url` (default `file:///index.html`) and other properties; Browser create; FunctionBus subscribe and registerChild; `loadURL` | C | — |
| JV-29 | `L._81676d._21aca6._590f69._1253fc` (FileSystem) | Root set, `.imgsrc`, ZIP entries, MC resource fallback, `WebOSR-REQ` | C | — |
| JV-30 | `L._81676d._21aca6._590f69._cfe983._cfe983` (TextureHandler) | `webosr:<n>` RGBA8 alloc, `bridge$uploadBgra` | C | Native call cadence (U) |
| JV-31 | `L._81676d._21aca6._21aca6._cfe983._21aca6` | `Browser.getTexture` → TextureManager → framebuffer quad, throttled | C | Meaning of throttle setting (T) |
| JV-32 | `L._81676d._21aca6._590f69._02d7ad` | `invokeIteration` ≥5 ms, model layer, browser draw | C | — |
| JV-33 | GameUI constant pool `#47` / `#25`; `L._81676d._21aca6._d4ca6c._590f69` | `window.lunarInternalAccept('<data:name>', <json>);` with dedup against the last sent value | C | — |
| JV-34 | `L._cb9292._cfe983` ctor and handlers; `L._cfe983._eb6c3c/_555303/_a61e7a` | `ws://127.0.0.1:<ipcPort>`, `lc-handshake` Base64 header (launch_id=`--launchId`, installation_id=`--installationId`; `installation-id` file fallback when no launch ID is supplied), 8 service stubs, push handlers, reconnect thread | C | Request timeout policy (U) |
| JV-35 | `L._2f4182._6c713e._cfe983` | Native HUD editor: shortcuts, undo/redo, box select, snapping toggle | C (algorithm S) | Snap thresholds (U) |
| JV-36 | Constant pools (all `com/moonsworth` classes) | 63 Lombok `toString` recipes revealing original class and field names ([recovered-original-names.txt](recovered-original-names.txt)) | C | — |
| JV-37 | genesis `ML.genesis._cfe983` | `LUNARCLIENT_STATUS_BUILD_CACHE` / `SAVING_CACHE` | C | — |
| JV-38 | modern Mixins (all) | 407 Mixin post sites mapped to target and injection ([mixin-event-post-map.tsv](mixin-event-post-map.tsv)); 101 core post sites ([client-event-post-sites.tsv](client-event-post-sites.tsv)) | C | Event semantics (S from hooks) |

### Files and data (tools: shell and Python; key names and types only, never values)

| ID | Source | Finding | Conf. |
|---|---|---|---|
| FS-01 | `lunar.jar!lunarBuildData.txt` | `lunarVersion=2.22.31-2635`, branch master, `proguardUuid` present, `uiGitHash` | C |
| FS-02 | `.lunarclient/settings/game/` listing | Profile directories (`Default`, `Arena PvP`, `UHC`, `Hypixel Skyblock`) holding `mods/general/performance/controls/staff_mods.json`; global files at the root | C |
| FS-03 | `settings/game/Default/mods.json` key structure | 90 root keys (`version` + 89 features). Sparse objects; nested child features; HUD keys `x/y/position/options.scale` | C |
| FS-04 | `genesis.jar!versions.conf` (HOCON, 4,765 lines) | 40 versions with ordinals 0–39; `launch-class` = `net.minecraft.client.main.Main` (only one occurrence); `java-version` per family; `deobfuscated` for 26.x | C |
| FS-05 | `lunar.jar!bridge/bridgeConfig.json` | List of bridge interface classes | C |
| FS-06 | sha256 of lunar, genesis, modern and common JARs, `main.js` and preload | All match the hashes Codex recorded | C |

### Protobuf (tools: javap ldc order, constant-pool bytes, protobuf `descriptor_pb2`)

| ID | Source | Finding | Conf. |
|---|---|---|---|
| PB-01 | `lunar.jar!com/lunarclient/gameipc/**/…Proto.class` (21 of 21 decoded) | Exact envelope, handshake, service and push schemas ([gameipc-protobuf-schema.txt](gameipc-protobuf-schema.txt)) | C |

### Launcher (source: `app.asar!dist-electron/electron/main.js`; tool: Python text context; REA for the preload)

| ID | Symbol @offset | Finding | Conf. |
|---|---|---|---|
| JS-01 | `iGe` @4,821,842; `nGe=/LUNARCLIENT_STATUS_\w+/` | stdout marker handling: progress, window hide, launch success, status timers | C |
| JS-02 | `SGe` @4,834,932; `startLaunch` | Launch module, profile and version resolution, error codes | C |
| JS-03 | `vGe` @4,828,770 | LaunchSession: `launchId=randomUUID`, branch selection, cancel | C |
| JS-04 | `zUe` @4,775,560; `LUe` @4,774,394; `lRe` @4,492,632; spawn @4,782,097 | POST `/launch`, JRE and launchTypeData checks, parallel stages, spawn options | C |
| JS-05 | `yRe` / `bRe` / `I$` @~4,498,264 | Full CLI and JVM argument construction, 26.1+ GC policy | C |
| JS-06 | `gLe` / `mLe` @~4,431,375 | Handshake check (close 4401), RPC dispatch, 9 service modules | C |
| JS-07 | `bLe` | Port 28190 + k (k < 30, 5 retries × 1 s), push broadcast and target, pending queue | C |
| JS-08 | `startLaunch` quick-join branch | `PlayServerPush` + `FocusGamePush` when a game is connected | C |
| JS-09 | `YQ` @4,440,972; `YWe` @4,819,284 | Error reporting; exit classification by code, signal and last status marker | C |

## Classification summary

### Confirmed

- The client initialization path and its order.
- The event bus algorithm.
- The feature trait system and enable precedence.
- Feature registration as a hardcoded list.
- Settings serialization and save-on-change.
- The HUD render loop, anchor math and persistence.
- The FPS, CPS and ZOOM implementations.
- Ichor version gating.
- The Java CLI option set.
- `versions.conf` and the vanilla `Main` launch class.
- The gameipc schemas and both handshake ends.
- UI URL resolution: `file:///index.html` → FileSystem root `--uiDir`.
- The launcher port policy, dispatch and stdout marker contract.
- WebOSR texture ownership and upload path.
- The Java→JS push template.

### Strong inference

- ProGuard as the obfuscator.
- `lunar-platform-mappings` as Ichor's Lorenz mappings.
- The launcher-supplied `mainClass` being Genesis.
- The ×2 HUD UI coordinate space.
- The bottom-center anchors flanking the hotbar.
- The HUD editor's re-anchoring and snapping.
- The external zoom compensation.

### Tentative

- The thread-check bus semantics.
- The FPS preview helper.
- The UI frame throttle setting.
- The global HUD scale formula details.

### Unknown

See [unresolved-implementation.md](unresolved-implementation.md).

## Previously undocumented behaviors now understood

1. Client construction point (`Minecraft.run` HEAD) and the init log sequence.
2. Event bus priority order and failure isolation.
3. Feature trait keys and when features (un)subscribe from the bus.
4. Setting JSON shape, sparse persistence, synchronous save-on-change and Apollo broadcast.
5. The HUD pipeline from the GameRenderer hook to element draw, including the 26.x strata splice.
6. HUD anchor geometry and persistence rules, corroborated by `mods.json`.
7. Three feature algorithms (FPS source, CPS window, ZOOM math).
8. Ichor version ordinals (from `versions.conf`) and branch folding.
9. Exact gameipc protobuf schemas, the `lc-handshake` header and close code 4401.
10. Launcher port selection, the quick-join shortcut, and the stdout marker → progress/exit contract.
11. UI URL and file resolution (`file:///index.html` → uiDir; `.imgsrc`; ZIP serving).
12. WebOSR textures: Java-owned RGBA8 with BGRA dirty-rect uploads drawn as a quad.
13. The Java→JS push expression `window.lunarInternalAccept('data:<name>', json)` with dedup.
14. The HUD editor is native Java, not the web UI.

## Corrections to earlier reports

| Earlier statement | Correction | Evidence |
|---|---|---|
| `lunar$onInit` at the `Minecraft.<init>` TAIL as a lifecycle/init hook | The client singleton is created in the `Minecraft.run()` HEAD (`impl$run`) | JV-01 |
| Runtime-resolved Minecraft main class unknown | `MinecraftVersion.launchClass` = `net.minecraft.client.main.Main` in this build's `versions.conf` | JV-27, FS-04 |
| Launcher "compares launch/installation identifiers" | Only `installation_id` is compared; `launch_id` must be non-empty and is used for push targeting | JS-06 |
| Port "28190 with retries" | 30 ports × 5 attempts at 1 s intervals; the bound port goes to `--ipcPort` | JS-07 |
| Obfuscator not attributed | `lunarBuildData.txt` carries `proguardUuid`, so ProGuard (S) | FS-01 |
| Platform-mapping JARs as inert "mapping-data carriers" | Consumed by Ichor's Lorenz-based remapper (S) | JV-25 |
| Exact UI URL/root selection unresolved | `file:///index.html` is served by Java FileSystem roots that include `--uiDir=<ui>/<sha1>` (C) | JV-28/29, JS-05 |
| Native texture ownership/composition unresolved (ME-09) | Java owns the textures; BGRA upload; framebuffer quad; ≥5 ms engine pumping | JV-30–32 |
| HUD editing implied via the web `/hud` route | The drag/scale editor is a native Java screen | JV-35 |
| Game settings defaults unresolved (ME-05) | Defaults and ranges are hardcoded in feature constructors (confirmed for FPS, CPS and ZOOM) | JV-21–24 |

## Session 3 — appended evidence ledger (2026-10-11)

Earlier entries and classifications above are retained verbatim as the session-2 record. This appended ledger resolves or qualifies selected earlier questions; see [unresolved-implementation.md](unresolved-implementation.md#session-3--status-update-2026-10-11). No target execution, user settings-value reads, install changes, native-tool installation or anti-cheat/integrity analysis occurred in this continuation.

**Classification:** C = **Confirmed**, S = **Strong inference**, T = **Tentative**, U = **Unknown**. Confirmed code is not runtime-observed behavior. JVM citations are method-local decimal offsets; metadata/resource claims use N/A or explicit PE file offsets. Full alias-to-JVM mappings for newly cited classes are in [session3-class-locations.tsv](session3-class-locations.tsv); the prior legend is preserved.

### JV additions

All rows use `lunar.jar` unless a second artifact is explicitly named. Tables in each linked report expand abbreviated class locators and individual method citations.

| ID | Artifact / class.method @offset | Finding | Conf. / limit |
|---|---|---|---|
| JV-39 | FeatureManager `L._02d7ad._1253fc._1eb51c.<init> @0–15`, `_de9126 @1–1836`; base `L._02d7ad._21aca6.<init> @23–28` | Constructor-time ordered candidate list: 95 initial, non-production Panorama +16 specialized/debug, Radio flag, six unconditional tail entries | C; candidate sites, not a live member count. [feature-registration-deep-dive.md](feature-registration-deep-dive.md) |
| JV-40 | Generic manager `L._02d7ad._cfe983._535838 @5–16`, `_81676d @0–30`, `_cfe983(Support) @0–17`; BootstrapMethods #0/#5 | `removeIf` removes only a present static-unsupported support trait; U-01 closed | C; no assertion of exhaustive child pruning |
| JV-41 | `L._88f3cf._ba7d98$_cfe983._2b01f6 @0–111`, version/module/server setters; implementation `L._88f3cf._1e73d7._ba7d98`; feature `updateEnabled @39–90` | Version/module support versus runtime server gate; any-present/any-absent module semantics; development/JUnit overrides | C code; effective module/server/override state U |
| JV-42 | `L.util._c8175c` inclusive helpers; genesis `ML._cb9292._21aca6._601d9f` constant bindings; 17 consumer methods cited in report | Version-helper ranges, build-specific constants and per-feature constraint declarations | C; extra storage-preview summary discrepancy T |
| JV-43 | `L._d4ca6c._1e73d7.cancel @0–5`, `isCancelled @0–4`, `setCancelled @0–5`; all event constructors in event-bytecode-locations.tsv | Event bases and payloads; constructor descriptors distinguish Chat/attack payloads from arguments | C structure; English role names generally S. [event-payloads.md](event-payloads.md) |
| JV-44 | `modern-0.1.0-SNAPSHOT-all-nomappings.jar` Mixin methods/ranges/posts in event-cancellation-audit.tsv | 185 mapped cancellable rows: 154 read isCancelled, 31 do not | C reproduced same-method test; direct cancellation ineffectiveness S, not proof listeners have no effect |
| JV-45 | `L._2f4182._1253fc._bb4487.getScale @0–155`, `_22e64f @0–62`, `_b36bc2 @0–51`; `L.util._d0d09a.<init> @14–249`; HUD interface range helpers `@0–2` | Global HUD scale, early returns, integer HiDPI ratio and framework scale range 0.25–5.0; U-04 closed at framework level | C; subclass overrides/edge-state behavior not universally established. [hud-math.md](hud-math.md) |
| JV-46 | `L._2f4182._6c713e._cfe983`: draw `@1691–2140`, snap helper `@58–1059`, rectangle metric `@0–60`, anchor helper `@0–280` | Thirds-grid anchors; edge/center/neighbour snap algorithm; U-05 closed | C; physical mouse-button mapping T; inclusive ±2 and separate edge gate correct handoff |
| JV-47 | Coordinates `L._88f3cf._bb4487._a140a8._1e73d7.<init> @0–367`, `_133367 @0–40`, `_7e956b @0–82`, `_76bef3 @16–90`; HUD/chat gate and BiomeService cited in report | Defaults/children/data sources, decimal truncation, compass, chat gate, copy path | C; grouped-format parity U. [additional-module-traces.md](additional-module-traces.md) |
| JV-48 | Keystrokes `L._88f3cf._bb4487._dd3308._590f69.<init> @0–708`; KeyHUD `_2ce426 @0–710`; layout `_d4ca6c @0–80`; Key `_2ef37e @0–23` | Defaults/settings, physical-input candidate, screen suppression, fades, geometry, shared CPS/custom keys | C code / S physical interpretation; exact glyphs/input implementation U |
| JV-49 | Waypoints `L._88f3cf._bb4487._8c4693._590f69.<init> @0–814`, death `@0–192`, tick `@0–92`, Render3D `@0–304`, label helper `@15–268`, distance config `@0–53` | Death debounce/builder, Euclidean cache, projected labels/render/config paths | C; ZOOM compensation interpretation S; actual rendering/import outcomes U |
| JV-50 | Migrator `L._2b0ee0._cfe983._bb4487.<clinit> @0–18`, `_ad8b9c @0–26`, `_cfe983(Object,JsonObject) @0–83`; step signatures/ranges in migration appendix | CURRENT=list size=31; ordered lazy target-specific migration, context update before apply; U-13 closed at ledger/algorithm level | C; exhaustive outcomes for personal profiles U. [settings-persistence.md](settings-persistence.md) |
| JV-51 | Generic manager `_5d96a0 @0–104`, `load @44–183`, `_55938e @0–161`; file-I/O interface in appendix | Missing file skips LOADED_CONFIG but post-attempt setup/COMPLETE still runs; migration triggers re-save | C code; initial defaults retention S |
| JV-52 | `L._ec7e36._13ea87.get @0–39`, `_590f69(JsonObject) @21–98` | Dependency-tracked effective intercept read versus stored/nondefault save | C getter/save; complete Apollo/server/option source precedence U |
| JV-53 | Browser config `L._81676d._21aca6._21aca6._cfe983._cfe983(int,int,double,Listener) @9–12`, `_16aefb @15–22`; TextureHandler in bytecode appendix, JV-30 | Nonaccelerated Java browser configuration and installed Java upload handler | C; CPU-bitmap/native callback route S, native cadence U. [native-analysis-preparation.md](native-analysis-preparation.md) |
| JV-54 | `lunar.jar!com/moonsworth/webosr/**`; webosr-native-declarations.javap.txt; DLL export table (native declaration Code offset N/A); `WebEngine.<init> @5–9`, `invokeIteration @0–20` | 56 Java natives versus 58 exports; Session.name missing, three DLL-only names; Java owner-thread queue behavior | C names/Java code; version skew and ordinary-lookup UnsatisfiedLinkError S, alternate native registration U |
| JV-55 | Performance ctor `@303–390`, `_eeb804 @0–4`; GameUI listener `<init> @392–412`, `_bb4487(Integer) @0–62`; blitter `_cfe983 @11–61` | menuFpsLimit identifies UI throttle; engine argument clamp 67–240 separate from setting 30–500 | C; actual/native FPS behavior U; prior JV-31 throttle T upgraded |

### FS additions and retained supporting files

| ID | Source | Finding | Conf. / boundary |
|---|---|---|---|
| FS-07 | Retained handoff Default/mods.json key-order observation; feature-registry.tsv; prior FS-03; serializer JV-40/11 | Saved order matches registry subsequence; REPLAYMOD absent | C retained structural observation, S interpretation; not newly re-read, absence not proof of module filtering |
| FS-08 | event-catalog.tsv; event-bytecode-locations.tsv; event-hook-bytecode-locations.tsv | 279 classes / 211 posted / 90 cancellable / 31 posted SkyBlock types; descriptors and constructor/hook ranges | C within saved inventory; no runtime counts |
| FS-09 | event-cancellation-audit.tsv; inspected canc.py and session3-tools/verify.py | Reproducible same-method cancellation test and all 185 mapped rows | C text test; overload/indirect-consumer caveats in report |
| FS-10 | settings-migration-steps.tsv; settings-migration-bytecode-locations.tsv; migrator supplier-list class | 31 ordered transitions with key strings/full JVM classes/method ranges | C implementation; handoff's personal profile/version scalar observations T, not re-read |
| FS-11 | Bytecode only: waypoint manager `_a55711 @0–2`, serializers `@0–55`, `@0–78`, `@8–409`; group `@0–130`, render-config `@0–73` | Global waypoints.json schema, group/dimension fields, six importer surfaces and chat pattern route | C; no user waypoint file read; color envelope/upstream format success U |
| FS-12 | native-pe-session3.json; native-jni-session3-verification.json | Six snapshot DLLs x64; supplementary WebP32 x86, Machine 0x014c at file offset 0x84; hashes retained | C static metadata; JVM offsets N/A |
| FS-13 | WebOSR-Binding imports/exports in native-pe-session3.json | JNI families, Ultralight/JSC/JVM/DWrite/USER32 dependencies; no normal OpenGL imports | C bounded table; window subclassing/CPU route S, dynamic imports U |
| FS-14 | native-signatures-session3-verification.json; rea-evidence-session3.json | Four Moonsworth-signed Valid images, three unsigned; version/UA string offsets; four manifest-only resource trees, no VERSIONINFO | C verifier/parser observation, S distribution-version interpretation; no target-integrity analysis |
| FS-15 | provider-availability.json, Ghidra diagnostics; native-analysis-preparation.md checklist | Recorded Ghidra not configured / JDK 21.0.10 accepted; approval-gated setup proposal | C retained diagnosis; installation/configuration not performed |

**Confirmed provenance / reproducibility.** Derived TSVs were generated from the retained analyst javap index, not by loading Lunar classes. `session3-tools/verify.py` regenerates event/migration/class/method citations; `verify-jni.py` runs JDK javap as a disassembler, compares declarations to saved exports, and reads only WebP32 PE bytes. [session3-bytecode-locations.tsv](session3-bytecode-locations.tsv) provides full original class names and method ranges for the shared HUD/settings/WebOSR traces. [webosr-fps-listener-binding.json](webosr-fps-listener-binding.json) retains the freshly checked BootstrapMethods #1 binding. Metadata offsets N/A except the identified Code/PE locations.

### Retained session-3 REA Evidence

The complete four-record export [rea-evidence-session3.json](rea-evidence-session3.json) is 12,873 bytes and has no newly added unknown records. No native analysis session was opened; these are target-free portable static PE-resource calls, not native decompilation.

| Evidence ID | Image | Operation / coverage |
|---|---|---|
| `ev_1754d1892de23136481a3896993038130ace56740dd41b5f11c0f502fb1b7a0e` | WebOSR-Binding.dll | inspect_pe_resources; one manifest at file offset 552032, 381 B |
| `ev_99d6f9e19db301702248dd3d31a16c69fc358a0fafc95f4f0d894aebddcb626a` | Ultralight.dll | inspect_pe_resources; one manifest at 598624, 323 B |
| `ev_db8a8cff158fc7524fa171d357c3aa138aae3e21100d0b39942d19cd8aeb1a29` | UltralightCore.dll | inspect_pe_resources; one manifest at 2481248, 323 B |
| `ev_0ef9f04a55e935408a7dd6cdd3d1c14a23adaaf975ea4ca520d68be5bdc72bf7` | WebCore.dll | inspect_pe_resources; one manifest at 47837280, 323 B |

### Session-3 classification corrections

- **Confirmed:** JV-10 registry filter is now resolved by JV-40; registered, statically supported and actively enabled are separate states.
- **Confirmed:** prior partial global HUD math and snap algorithm upgraded by JV-45/46, with integer ratio, inclusive neighbour thresholds and separate edge gate.
- **Confirmed:** migration version/list/load algorithm upgraded by JV-50/51; effective versus stored setting values distinguished by JV-52.
- **Confirmed:** UI FPS-throttle identity upgraded by JV-55; setting range, engine clamp, texture refresh cadence and native paint cadence are not interchangeable.
- **Strong inference, not Confirmed native behavior:** CPU rendering/callback path and JNI version-skew interpretation. **Unknown:** native thread/paint model, actual launch response/mainClass and live stdout/IPC ordering remain unresolved.
