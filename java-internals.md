# Minecraft-side Java internals (session 2)

Study date: 2026-10-11. This is a static, read-only study of the installed JARs. No Lunar JAR, class, or native library was executed or loaded. I did not apply deobfuscation, rename symbols, or bypass any protection. Every class name below is the exact shipped (ProGuard-obfuscated) name or a short alias for it. [session2-class-legend.md](session2-class-legend.md) maps each alias to its exact JVM name.

## How this was analyzed

| Tool | Used for | Notes |
|---|---|---|
| REA `binary_session` | Provider check | Ghidra was `not_configured`, IDA was `not_configured`, and Hopper was `unsupported_host`. JVM decompilation is not available in REA, so 111 tools reported unavailable and 59 available. |
| REA `open_binary` + `inspect_artifact` on `lunar.jar` | Archive identity and inventory | `ev_3a3bda3688dc8b47b22d734d6f12c6d675194d7851c58355fc7168468ea328e4` and linked inventory `ev_240074aaa2df47784569e96d463ee762f2ea067d31a72d4ca069a126bba4521a`. 19,664 nodes and 0 integrity contradictions. The complete records are exported to [rea-evidence-session2.json](rea-evidence-session2.json). |
| JDK 21.0.10 `javap -p -c` (local, already installed) | Bytecode disassembly of every `com/moonsworth` class in `lunar.jar` (6,485), `modern` (1,367), `common` (32), and the Ichor/Genesis subset (206) | javap is a disassembler; it does not execute classes. Scripts are in [session2-tools/](session2-tools/). |
| Analyst Python scripts | Indexing, alias rendering, constant-pool parsing, Lombok-name recovery, protobuf descriptor decoding | Static byte parsing only |

Evidence IDs (JV-*, FS-*, PB-*, JS-*) are defined in [evidence-index.md](evidence-index.md).

Artifact identity was re-verified (FS-06). `lunar.jar` is `bf36e10e…a02e9`, `genesis` is `c188afc0…1f046`, `modern` is `99df64c5…db02e`, and `common` is `440e1e6f…eee3`. These match the hashes Codex recorded. `lunar.jar!lunarBuildData.txt` declares `lunarVersion=2.22.31-2635`, `gitBranch=master`, `production=true`, and a `proguardUuid` (FS-01).

## 1. Package organization (confirmed by bytecode)

The client is split into a version-independent core in `lunar.jar` and version-specific adapters.

| Layer | Package (alias) | Role established by code |
|---|---|---|
| Bridge API | `com.moonsworth.lunar.RORCICOHRIOIIIOIOHIIIICRCIHRII.*` (`ML._590f69`) | Interfaces with `bridge$…` methods, such as `bridge$getGameSettings`, `bridge$getDebugFPS`, `bridge$uploadBgra` and `bridge$getPoseStack`. Core code only calls these interfaces. The `mc` field of every feature is typed to the Minecraft bridge `ML._590f69._bb4487._bb4487`. |
| Bridge implementations | `modern-…jar` Mixins | Mixin classes `implements` the bridge interfaces on Minecraft classes. For example, the Minecraft Mixin `ML._d4ca6c._1e73d7._590f69._a140a8` implements `ML._590f69._bb4487._bb4487`. |
| Core client | `com.moonsworth.lunar.client.*` (`L.*`) | Client singleton, managers, event bus, features, settings, HUD, GameUI and IPC. |
| Ichor | `com.moonsworth.lunar.ichor.*` (Genesis) | ASM transformer and version gating (section 6). |
| Genesis | `com.moonsworth.lunar.genesis.*` | Bootstrap, classloaders and the version registry `versions.conf` (FS-04). |

Main core sub-packages (aliases):

- `L._d4ca6c`: event bus.
- `L._d4ca6c._cfe983.*`: event classes.
- `L._88f3cf`: the feature framework. `L._88f3cf._bb4487.*` holds the individual features, and `L._88f3cf._590f69.*` holds the HUD.
- `L._55938e`: the trait system.
- `L._02d7ad._1253fc.*`: managers.
- `L._ec7e36`: settings.
- `L._81676d`: GameUI/WebOSR.
- `L._cb9292`: game IPC.
- `L._2f4182`: Lunar screens/GUI.
- `L._ba7d98`: shared listener services.

## 2. Application entry and initialization: confirmed call chain

```
Genesis.main ─▶ ClientGameBootstrap.apply
   │  @1041 System.out.println("LUNARCLIENT_STATUS_PREINIT")               (JV-27)
   │  @1094-1101 Class.forName(MinecraftVersion.launchClass)               (JV-27, FS-04)
   │      launchClass default = "net.minecraft.client.main.Main" (versions.conf; no override present)
   ▼  @1456 Method.invoke(main, args)
net.minecraft.client.main.Main.main
   │  Mixin lunar$main$options$* (INVOKE OptionParser.allowsUnrecognizedOptions)  (JV-26)
   │     adds joptsimple options: launcherFeatureFlags, launcherVersion, installationId,
   │     overwolfMuid, texturesDir, jitDir, sentryTraceId, ipcPort, uiDir, webosrDir,
   │     tournamentServer, modrinth*/curseforge* ids, launchId, canaryToken, server, port
   │  lunar$main$parse copies parsed values into static fields of L.util._038392
   ▼
Minecraft.<init>  ── window created ──▶ stdout "LUNARCLIENT_STATUS_INIT"         (JV-02)
   (VirtualScreen.newWindow TAIL for older versions; for ordinal ≥36, i.e. 26.x, it is
    RenderSystem.initRenderer inside Minecraft.<init>)
   ▼
Minecraft.run  HEAD ── Mixin impl$run ─────────────────────────────────────── (JV-01)
   preload shaders → create loading-screen renderer L._2f4182._2ce426._590f69
   @120  new L._cfe983()          ← the client singleton is constructed here
   @128  log "LUNARCLIENT_STATUS_STARTED"
   @137  L._cfe983._e724a5()
```

**Correction to prior work.** `lunar$onInit` at the `Minecraft.<init>` TAIL is not where the client initializes. The singleton is created in the `Minecraft.run()` HEAD injection, so it starts on the render thread before the first frame.

### Client singleton constructor (`L._cfe983.<init>`; JV-03)

The order below is fixed by bytecode offsets and the log literals:

1. The constructor acquires the global event bus `ReentrantLock` (`EventBus._9e2624().lock()`, @38–44). It holds the lock until the end of the constructor (@1734–1740 `unlock`). Other threads therefore cannot dispatch while managers are being wired.
2. Bootstrap calls follow: `L.util._cb9292.bootstrap`, `L._767dc1._590f69.init`, setting the singleton, and `L._21aca6._cfe983.bootstrap`. The window title is then set through `bridge$setDisplayTitle`.
3. It logs `"Starting Lunar client..."` and starts `ML._cfe983._cfe983`.
4. It constructs the managers, each implementing `L._02d7ad._1253fc { init(); close(); }`. 52 are created inside the `ImmutableSet` builder, and several more are created just before it. It logs `"Failed to construct managers!"` on error and `"Finished making managers."` on success.
5. It logs `"Setting up listeners..."` and constructs 9 `L._ba7d98._21aca6.*` listener objects. At @1440 it calls `_555303()`, which starts a background `Thread` running `_a61e7a()`. That method closes any open game-IPC client (`closeBlocking`), builds the `gameipc` Handshake (logging `"Unable to construct IPC handshake."` on failure), constructs `L._cb9292._cfe983`, and calls `connect()` (JV-34).
6. It logs `"Init GameUI and GameUIRenderer..."` and calls `L._81676d._21aca6._21aca6._d82ff1()` and `L._81676d._21aca6._590f69.init()` (section 8).
7. It logs `"Setting up fixes..."`, then handles Emoticons registration and the Ichor pipeline. It logs `"Disabling ReplayMod because there is no valid link."` when no link is present.
8. `start()` (JV-04) logs `"Lunar.start"`, sets the language, initializes one priority manager, then loops over every manager's `init()` inside a try/catch that reports `"Manager Init"`. It then logs `"Launching"` and registers tick handlers.
9. The constructor logs `"Finished Lunar initialization."` and the elapsed time, then releases the lock.

## 3. Event dispatch: confirmed implementation (JV-05)

`L._d4ca6c._590f69` is a process-wide singleton.

- **Bus variant.** Its static initializer selects either the plain bus or the subclass `L._d4ca6c._cfe983`. The choice depends on a development flag and on internal feature flags named `THROW_ON_WRONG_THREAD_BETA`, `THROW_ON_WRONG_THREAD_DEV` and `IGNORE_EXTERNAL_THREAD_BETA`. Strong inference: the subclass enforces thread affinity.
- **Storage.** A `HashMap<Class<? extends Event>, HandlerRecord[]>` holds the handlers. `HandlerRecord` (`L._d4ca6c._bb4487`) is a Java `record(int priority, Consumer)`.
- **Registration** (`_590f69(Class,Consumer,int)`):
  - If a dispatch is in progress (`AtomicInteger` depth ≠ 0), the add is queued as a pending operation.
  - Otherwise the array is copied, the record is appended, and the array is re-sorted with `Comparator.comparingInt(r -> -r.priority())`. **Higher priority runs first.** The default priority from `handle()` is **100**.
- **Posting** (`post(Class<T>, Supplier<T>)`, used at 508 sites):
  - If no handlers are registered, the event object is **never constructed**. The supplier is lazy.
  - Otherwise the event is built once and each handler runs inside its own `try { … } catch (Throwable)`. A failing handler is reported through `_cfe983(Class,Throwable)` and does not stop the others.
  - Afterwards the pending registration operations are flushed (`_57e17e`).
- **Pre/post pairs.** An API `_cfe983(Class<PRE>, Class<POST>, Function, Runnable)` exists for wrapped pre/post event pairs. It is used at 8 Mixin sites.

**Event producers.** 407 Mixin methods in `modern` post events. They are listed with their Mixin target and injection point in [mixin-event-post-map.tsv](mixin-event-post-map.tsv). A further 101 post sites in core code are in [client-event-post-sites.tsv](client-event-post-sites.tsv). Examples:

| Minecraft hook (annotation) | Event alias |
|---|---|
| `Minecraft.tick()` HEAD (`lunar$preRunTick`) | `L._d4ca6c._cfe983._2ce426._3a14e3` (tick-pre), `…_1eb51c` |
| `Minecraft.tick()` RETURN | `…_2ce426._ec7e36` |
| `MouseHandler.onPress/onButton` HEAD, cancellable, version-gated | `…_bb4487._590f69` (mouse button) |
| `MouseHandler`/`ScrollWheelHandler` scroll | `…_bb4487._bb4487` (scroll) |
| `GameRenderer.getFov` RETURN / `Camera.calculateFov` (26.x) | `…_d4ca6c._d4ca6c$_cfe983` (FOV) |
| `GameRenderer.render` around GUI | `…_1e73d7._cfe983` / `…_1e73d7._21aca6` (2D render, scaled) |
| `LevelRenderer` (`lunar$event3D`) | `…_1e73d7._590f69` (3D render) |
| `ClientPacketListener.handle*` | Chat, title, scoreboard, ping, entity, inventory and similar events |
| `Options.save` TAIL | `…_590f69._00e05b` |

Event class names remain obfuscated. One original name survives through Lombok: `EventPreAttackEntity(player,target,distance,hitPos)` (JV-36). The role of each event is inferred from the hook that posts it.

## 4. Feature framework: trait-based composition (JV-06…JV-09)

The feature base `L._88f3cf._cfe983` (`F + COOCHIRORIICRCIIRIROHIIRIRICCH` in prior reports) does **not** store most capabilities as fields. Each feature owns a **trait container** (`L._55938e._1e73d7`) built from a frozen trait registry. Capabilities are attached under named keys. The static initializer of `L._88f3cf._02d7ad` creates 21 keys with literal names (JV-07):

`hud_renderer, staff_mod, ichor_keybind, intercept, children, enabled, enable_listener, load_state, index, panel, page, events, details, options, display, child, label, support, dynamic, restriction, toggle_keybind`

### Constructor (`protected Feature(boolean defaultEnabled)`, JV-06)

1. Creates a small Guava cache and an optional dynamic-state helper.
2. Sets `mc` from the global Minecraft bridge and the client singleton.
3. Creates the trait container and sets `load_state = CONSTRUCTOR`. `L._88f3cf._6c713e` has at least `CONSTRUCTOR` and `LOADED_CONFIG`.
4. Stores `defaultEnabled`.
5. If an `enabled` trait override is present, applies it.

### Event subscription (JV-08)

1. `handle(Class, Consumer)` delegates to `handle(Class, Consumer, 100)`. That gets or creates the `events` trait (`L._88f3cf._1e73d7._429bf0`), which records `Class → HandlerRecord` in a local map.
2. If the trait is currently **active**, the handler is also registered on the global bus immediately.
3. On activation (`_6e84a9`), every recorded handler is registered on the bus and the "on enable" runnables run.
4. On deactivation (`_4ee67b`), every handler is unregistered and the "on disable" runnables run.
5. Active means: the feature is enabled, AND the `dynamic` trait allows it, AND the parent/child condition holds. A change propagates to every child in the `children` trait.
6. A debug path prints `"enabled <id>"` / `"disabled <id>"` to stdout.

This is the confirmed mechanism behind "features only receive events while enabled": subscriptions are added to and removed from the bus as features toggle.

### Effective-enable precedence (`updateEnabled()`, JV-09)

The first rule that applies wins:

1. A `child` feature whose parent is disabled is forced off.
2. If the `support` trait reports unsupported for the current server/context (`L._dd3308._1e73d7._657fd1()`), the feature is off.
3. If the `restriction` trait denies it, the feature is off.
4. If the `intercept` trait returns an `Optional<Boolean>`, that value is used. Strong inference: this is for server or Apollo overrides.
5. Otherwise the feature uses its own `isEnabled()`.

After any outcome, the `dynamic`/listener update is fired.

## 5. Feature registration, settings and persistence

### Registration (JV-10, JV-11)

`FeatureManager` is `L._02d7ad._1253fc._1eb51c`. It extends the generic `L._02d7ad._cfe983<Feature>`, which in turn extends `L._02d7ad._21aca6<T>` (set-backed).

- **The registry is a hardcoded list.** `_de9126()` instantiates the feature classes directly with 119 `new` instructions, all in `L._88f3cf._bb4487.*`. Most are passed in one call to the varargs helper `_cfe983(Feature...) → LinkedHashSet`; 24 are added afterwards with direct `Set.add` calls. Some entries are added only conditionally, gated on a dev flag (`L._1e73d7._cfe983._c1461e`), on `MC_VERSION`, and on a server-feature enum (`RADIO`).
- No reflection or classpath scanning was observed for feature discovery.
- **Unresolved:** the effect of the `removeIf` filter applied in `_535838()` (section 9).
- The 379 language IDs are therefore a superset of what is registered. Child features live inside parents' `children` traits and are not top-level entries.

### Settings model (JV-12, JV-13)

`L._ec7e36._13ea87<T>` is the value-setting base. Each setting has:

- an id,
- a `com.lunarclient.dfu.serialization.Codec<T>` (a DataFixerUpper-style codec bundled under the `lunarclient` namespace),
- a default,
- child settings, and
- its own trait container.

Typed subclasses are created through a builder factory `L._ec7e36._81676d`. That factory exposes `bool(id)`, `float(id).default(…).range(min,max)`, `int(…)`, `color(…)` and `keybind(…)` builders. Each feature lists its settings for the UI in its `_cfe983(L._ec7e36._590f69._21aca6._21aca6)` override.

**Load** (`Setting.load(JsonObject)`):

- A missing or `null` key resets the setting to `getDefaultValue()`.
- A primitive JSON value is decoded with `Codec.parse(JsonOps.INSTANCE, …)`. A decode error is logged and does not throw.
- An object value has the form `{ "value": …, <childId>: … }`, so nested child settings share one object.
- `Feature.load` iterates every serializable node in the trait container. If loading added new traits, it re-runs on the newly added nodes, so settings that appear dynamically are loaded too.

**Save** (`_590f69(JsonObject)`):

- A value is written **only when it differs from its default**. Otherwise the key is removed.
- `FeatureManagerBase.save` writes `{"version": CURRENT, <featureId>: {...}}` and **omits empty feature objects**.
- On load, the manager runs a migrator (`L._2b0ee0._cfe983._bb4487`), reads the root `version`, injects `version` into each feature object, calls `feature.load`, then sets `load_state = LOADED_CONFIG`.

**Change propagation** (`_1e73d7(T value, boolean force)`): when the value changes, the setting

1. applies the value,
2. broadcasts through the Apollo `ModSettingModule` when that module is present (`"Apollo broadcast failed"` on error),
3. fires change listeners (trait `_09bf1e`), and
4. notifies `SettingsManager._145809(setting)` (JV-15). That call **saves the owning file immediately** (`_8e99ad → _1f5a0f(false)`) when profiles are ready.

### File I/O (JV-14)

The config-file interface `L._02d7ad._d4ca6c` handles both directions.

- **Load** (`_5d96a0`) parses with Gson and logs `"Loaded File: [%s]"`. On failure it logs `"Couldn't load file %s [%s]"`.
- **Save** reads the existing file first, so unknown keys survive. It applies values, writes with a pretty or compact Gson writer through `FileWriter`, and logs `"Saved File: [%s]"`.
- The write is **synchronous on the caller's thread**. No temp-file rename was observed, so writes are not atomic.

### Storage locations (JV-10, JV-15, FS-02, FS-03)

| File | Owner | Scope |
|---|---|---|
| `settings/game/<Profile>/mods.json` | FeatureManager (`_a1ad6f()`: settingsDir/activeProfile.getName()/`mods.json`) | Per profile |
| `settings/game/<Profile>/general.json`, `performance.json`, `controls.json` | `L._02d7ad._1253fc._1253fc._590f69/_bb4487/_21aca6` | Per profile. Scope enum `GENERAL/PERFORMANCE/CONTROLS` |
| `settings/game/internal.json`, `features.json`, `global_options.json`, `rewind.json`, … | Other managers (40+ JSON names, JV-10 string scan) | Global |

**On-disk corroboration.** The key structure of `mods.json` was read without values (FS-03), and it matches the save rules exactly:

- the root has `version:int` plus 89 feature objects;
- most objects contain only `panelIndex` because defaults are omitted;
- child features nest under their parent's object (for example `PING → PING_HUD{options,position,x,y}`);
- HUD-bearing features carry `x`, `y`, `position` and `options{scale}`.

### UI ↔ settings (JV-16)

The settings provider `L._81676d._21aca6._d4ca6c._cfe983._ba7d98` is annotated `@CallbackJS("setAdvancedMode" | "update" | "reset" | "invokeAction" | "setEditingKeybind" | "stopEditingKeybind")`.

`update(scope, ownerId, settingId, valueString)` resolves the owning settings collection by `Scope`:

- `GENERAL`, `PERFORMANCE` or `CONTROLS` → the corresponding settings container;
- `FEATURE` → `FeatureManager`, find the feature by id, then its `options` trait.

It then finds the setting by id and calls `setting._d2c28f(String)`, which parses the string into a value. That enters the change-propagation path above, so a UI edit is persisted immediately.

**Reverse direction.** `FeatureManager._8d9bc5()` publishes the `details` and `features` payloads, and `SettingsManager._d87130()` publishes `general`, `performance` and `controls` into the UI payload store (section 8).

## 6. Version adaptation: Ichor (JV-25, FS-04)

- **Ordinals.** `genesis!versions.conf` (HOCON) defines 40 versions with ordinals from `v1_7`=0 to `v26_2`=39, a per-version `java-version` (26.x uses 25 and 1.20.5–1.21.11 use 21), `version-module: modern`, `deobfuscated: true` for 26.x, and `launch-class` (default `net.minecraft.client.main.Main`).
  - **This resolves the numbers in code.** `MC_VERSION >= 39` means 26.2, `>= 30` means 1.21.6, and Mixin `@…(min=33)` means 1.21.9 or later.
- **Version annotation.** The Ichor annotation `ML.ichor._cfe983._21aca6 {int[] value; int min; int max; boolean inverted; boolean onReturn}` marks members by version range. A separate conditional annotation `{String[] present; String[] absent; available}` gates on mod presence.
- **Transformer.** `ML.ichor._1253fc._d4ca6c` is an ASM `ClassNode` transformer built with two Cadix Lorenz `MappingSet`s.
  - It **removes methods and fields** whose version annotation excludes the running ordinal (`List.removeIf`).
  - It **constant-folds integer comparison branches**: `_543b36(a,b,opcode)` evaluates `IFEQ…IF_ICMPLE` (153–164). Strong inference: this prunes `if (MC_VERSION >= n)` code at load time.
  - It references `.ichor/inflight_merged.xsrg`.
  - Strong inference: `lunar-platform-mappings-v*.jar` supplies these mapping sets, translating names like `render$v1_16_1` to each version's names.
- **Bridge registration.** `lunar.jar!bridge/bridgeConfig.json` lists bridge interface classes (FS-05).

## 7. Original-name recovery (JV-36)

The obfuscation renames classes and members, but string-concatenation recipes generated by Lombok `@ToString` keep original class and field names in the constant pool. 63 such recipes were recovered and are listed in [recovered-original-names.txt](recovered-original-names.txt). Examples:

- `FeatureDetailsImpl(languagePath, categories, aliases, originalAuthors, isVanilla, allowsKeybind)`
- `HudSize(minHeight, height, maxHeight, minWidth, width, maxWidth)`
- `SelectedHudMod / ScaleHudMod / HistoricalHudMod` (the HUD editor)
- `KeyBind(alt, shift, control, value)`
- `Profile`, `Waypoint`, `WaypointGroup`
- `RewindProject`, `RewindMetadata`, `RewindRenderSettings`
- `MinecraftVersionBuilder(…, launchClass, coreOpenGL, latest, javaVer)`

These are shipped strings, not reversed obfuscation. I applied no mapping.

`lunarBuildData.txt` contains `proguardUuid`. Strong inference: the obfuscator is ProGuard with a custom `CHIOR` dictionary. Prior work had declined to attribute the obfuscator.

## 8. Native and rendering boundaries (summary)

Details are in [rendering-and-hud.md](rendering-and-hud.md) and [ipc-deep-dive.md](ipc-deep-dive.md).

- **GameUI (Ultralight) produces pixels, and Java owns the GPU textures.** The native engine calls the Java `TextureHandler` methods `create`, `resize`, `upload`, `read` and `delete`. These allocate RGBA8 textures through the bridge and upload BGRA dirty rectangles (JV-30).
- **The browser loads `file:///index.html`** (system property `lunar.webosr.url`), resolved by a Java `FileSystem` handler against root directories that include `--uiDir` (JV-28, JV-29). The option-to-field mapping is confirmed in `lunar$main$parse`.
- **IPC:** a WebSocket to `127.0.0.1:<--ipcPort>` with an `lc-handshake` header (JV-34).

## 9. Unresolved within this scope

- The predicate in `FeatureBase._535838()` (`removeIf`) that drops some constructed features. The lambda body was not traced.
- Exact `Event` semantics for most event classes. 279 classes transitively extend the event base (140 directly), and 211 distinct classes appear as posted types. Roles are inferred from hook sites only.
- How the thread-checked bus variant enforces affinity. The subclass body was not traced.
- Native code inside `WebOSR-Binding.dll` and Ultralight: threading, paint cadence and JS execution context. Ghidra and IDA are unavailable.
- Whether Lorenz mappings come only from `lunar-platform-mappings-*.jar`. That is strongly inferred, not traced to a file open.
