# Independent Fabric client — proposed MVP architecture

Date: 2026-10-12. **Original design specification; no client implementation or runtime validation is claimed.** Companion documents: [build order](mvp-development-plan.md) and [readiness](development-readiness.md).

## 1. Product boundary and evidence

Deliver one client-only Fabric mod: startup/shutdown, module lifecycle, typed events/settings, local persistence, keybinds, FPS/CPS/coordinates/keystrokes HUD, movable HUD editor, native Minecraft settings screens and local configuration profiles. Install through an existing compatible Minecraft launcher. A new launcher is a later product milestone.

**Observed research:** [Session 7 summary](../session7-astra/session-summary.md) describes a native browser renderer worker, three CPU buffers, synchronous Java texture pulls and partial shutdown ownership. [Remaining gaps](../session7-astra/remaining-gaps.md) preserves unresolved texture deletion, queue/source lifetime, initialization/JNI cleanup and JS/promise behavior. These are observations about inspected artifacts, not requirements for this client. Native browser/JNI integration is absent from the proposed MVP. Use independently written code, schemas, UI and assets.

**Proposed stack:** Minecraft **1.21.11**, Java **21**, Fabric Loader/API/Loom, Gradle Wrapper, Mojang official mappings, native Minecraft screens and the Fabric HUD API. This is a provisional compatibility target, **not the latest Minecraft release**. Official docs currently default to 26.2. Exact toolchain coordinates must pass [Gate 0](mvp-development-plan.md#gate-0--lock-the-toolchain) before implementation depends on them.

## 2. Dependency and ownership model

```text
FabricClientEntrypoint
  -> ClientRuntime (composition, startup and shutdown)
     -> MinecraftAdapter (tick, input, HUD, screen, world/focus state)
     -> EventBus + ModuleManager + SettingsService
     -> InputRouter + TelemetryService
     -> HudRegistry + LayoutService -> MinecraftHudRenderer
     -> ScreenRouter -> SettingsScreen / HudEditorScreen / ProfilesScreen
     -> ProfileService -> ConfigStore -> single I/O executor

Pure core: module, event, setting, profile, geometry, metrics contracts
Adapters: Minecraft/Fabric callbacks, drawing, key mapping, filesystem, clock
Dependency direction: adapters depend on core; core never imports Minecraft.
```

- Client-thread ownership for mutable runtime state, event dispatch and profile transitions. Fabric callback thread assumptions are verified in Gate 1. A wrong-thread public mutation fails an assertion in development and is rejected with a diagnostic in production.
- HUD callbacks extract immutable draw data on their designated game thread; never retain game drawing contexts or access Minecraft objects on the I/O executor. Adapt to the pinned version's rendering/extraction contract rather than issuing direct OpenGL calls.
- One I/O executor receives immutable configuration snapshots. Completion messages return through the client executor with revision IDs. No disk access in HUD rendering or tick listeners.
- One permanent Fabric bridge per callback type; module toggles only manage internal subscriptions. No repeated registration of Fabric listeners.
- Inject a monotonic clock, storage and game snapshot provider. Metrics and geometry tests need no game runtime.

## 3. Original interface sketch

Names below are proposed application interfaces, not asserted Fabric method signatures.

```java
interface Module {
    ModuleDescriptor descriptor(); // stable ID, category, settings, default state
    void onEnable(ModuleContext context, ResourceScope scope) throws Exception;
    void onDisable() throws Exception;
}
interface ModuleManager {
    TransitionResult setEnabled(ModuleId id, boolean enabled);
    ModuleStatus status(ModuleId id);
}
interface EventBus {
    <E> Subscription subscribe(EventKey<E> key, ModuleId owner,
                                int priority, Consumer<E> listener);
    <E> void publish(EventKey<E> key, E event);
}
interface SettingsService {
    <T> ValidationResult<T> validate(SettingKey<T> key, T candidate);
    <T> ChangeResult set(SettingKey<T> key, T candidate);
}
interface HudWidget {
    WidgetId id();
    Size measure(HudSnapshot snapshot, TextMetrics text);
    DrawList draw(HudSnapshot snapshot, Rect bounds);
}
interface ConfigStore {
    CompletionStage<LoadResult> load();
    CompletionStage<SaveResult> save(ConfigSnapshot snapshot);
    CompletionStage<SaveResult> flush(long revision);
}
interface ProfileService {
    SwitchResult activate(ProfileId id);
    ProfileId create(String displayName);
    ProfileId cloneProfile(ProfileId source, String displayName);
    ChangeResult rename(ProfileId id, String displayName);
    ChangeResult delete(ProfileId id);
}
```

`EventKey<E>` carries a runtime payload class for boundary validation. `ResourceScope` owns subscriptions and other closeables, closes in reverse registration order, is idempotent and aggregates ordinary cleanup failures. Do not catch JVM-fatal `Error`s as recoverable module errors.

## 4. Startup, modules and event dispatch

| Subsystem | Responsibility, dependencies and interface | Failure policy | Tests and acceptance |
|---|---|---|---|
| Startup/shutdown | Entrypoint constructs services, registers module descriptors and one set of Fabric bridges, loads/validates config, then activates profile. Runtime states: NEW → LOADING → RUNNING → STOPPING → STOPPED; FAILED for invariant failures. During LOADING, only a loading/status UI is active. | Missing config creates defaults; corrupt config follows recovery below. Duplicate module/setting IDs fail initialization visibly. On partial startup, close acquired resources in reverse order. Shutdown stops input, captures final config, disables modules, closes subscriptions, flushes I/O with a proposed 2-second deadline, then closes executor; record a timeout rather than reporting saved. | Fresh start and restart; duplicate ID; load failure; failure after each acquisition; repeated stop. Acceptance: one runtime, deterministic initialization, no listeners after stop, actionable save status. |
| Module lifecycle | Registry has stable IDs such as `client:fps`; immutable descriptors. Manager owns DISABLED → ENABLING → ENABLED → DISABLING → DISABLED; failures end in FAULTED. All four modules depend only on core services, never each other. | Enable succeeds only after scope creation and hook completion. Enable failure closes partial scope. Disable always closes scope in `finally`, even if hook fails. A callback fault immediately mutes all subscriptions for its owner; cleanup runs at the safe dispatch boundary. FAULTED requires explicit retry and does not auto-retry every tick. | Repeated enable/disable, failure during enable/disable, callback failure and self-disable. Acceptance: idempotent requested transitions, exactly one active listener set, no rendering from a disabled/faulted module. |
| Typed event dispatch | Exact-key dispatch, no reflection/string payloads. Define tick, world-context, focus, physical-input and settings-changed records. Descending priority, then registration order. Synchronous on client thread; rendering uses the HUD registry rather than a global mutable render event. | Dispatch reads a snapshot; additions start next publish. Closed subscriptions are skipped immediately. Nested publish is rejected with a clear diagnostic; a listener can schedule a follow-up for next tick. Lifecycle changes are deferred until outer dispatch returns. One ordinary listener exception faults its module and allows other owners to run. | Ordering, payload rejection, unsubscribe during dispatch, additions, reentrancy and exception isolation. Acceptance: deterministic delivery and zero events to disabled owners. |

Startup sequence: install bridges → register descriptors/defaults → asynchronously read state → validate/migrate → apply snapshot on client thread → enable requested modules → mark RUNNING. World/player-dependent services publish an empty snapshot until a world exists. Shutdown also works from LOADING; late I/O completions cannot reactivate a stopped runtime.

## 5. Typed settings, persistence and profiles

### Schema and storage contract

Store **one atomic root document** at `<gameDir>/config/independent-client/state.json`; the folder name is provisional product naming. The root contains `schemaVersion`, monotonic `revision`, `activeProfileId` and `profiles` keyed by UUID. Each profile contains `displayName`, desired module enable flags, per-module typed settings, optional toggle bindings and HUD layout records. Global screen-opening bindings remain Minecraft Controls settings, not profile fields. Runtime FAULTED state, metrics, game objects and credentials are never serialized.

Typed `SettingDefinition<T>` owns its ID, default, codec, validator and UI metadata. MVP types: boolean, bounded integer, bounded decimal, enum, ARGB color and binding. Reject non-finite numbers; reject invalid GUI edits without changing live state. On load, default individual invalid known fields with diagnostics. Missing fields use defaults; retain unknown fields/module IDs when round-tripping the same schema. A newer schema is opened in read-only recovery mode; do not overwrite it with older defaults. Migrations are ordered pure transformations; schema 1 needs no invented legacy migration.

All changes go through services, update the in-memory snapshot and increment its revision. Debounce autosave by 500 ms after the last edit. One writer serializes revisions; retain at most one pending latest snapshot in addition to the in-flight write. Explicit save/flush waiters complete only after their revision or a newer revision is durable. Ignore stale completion notifications when reporting save state.

Write UTF-8 to a same-directory temporary file, flush it, preserve the previous validated root as `state.json.bak`, then replace the root with an atomic filesystem move. If atomic replacement is unsupported or fails, leave the previous root intact, retain pending changes and surface Retry/Save Failed; do not silently downgrade durability. On startup validate root, then backup; quarantine a corrupt root before replacing it. If quarantine cannot be completed, run in memory/read-only recovery mode. An interrupted temp write never takes precedence over a valid root. Limit input to 2 MiB and 100 profiles for the MVP. Acquire a process-lifetime lock for this config directory; another instance gets read-only settings rather than concurrent writes.

| Subsystem | Responsibilities and dependencies | Failure handling | Tests and acceptance |
|---|---|---|---|
| Settings | Definitions/codecs in core; `SettingsService` is the single mutation path for GUI, reset and profile application. Changes notify modules after validation. | An invalid edit retains the last valid value and displays a field error. A module failing to apply valid settings is faulted. Reset applies registered defaults, not an old serialized copy. | Boundary values, enum removal, NaN/infinity, reset and notification order. Acceptance: GUI/load use the same validation rules; no unchecked cast or untyped map reaches modules. |
| Persistence | `ConfigStore` handles file ownership, migration, snapshots, backups and save status. Depends on JSON codec, executor and filesystem adapter. | Recovery modes above; failed writes keep dirty state. Log file/revision/error, never claim success before replacement. Shutdown timeout may lose latest unsaved edits but preserves the last durable root. | Fault-inject full disk, access denial and failures before/after temp/backup/replace; corrupt/truncated root, valid backup, future schema and two instances. Acceptance: recovery loads a complete valid revision or enters explicit recovery; never a partial document. |
| Profiles | `ProfileService` owns create/clone/rename/delete/activate; profile IDs are UUIDs, names are 1–64 trimmed characters and never filesystem paths. Clone copies configuration, not runtime state. Reject duplicate normalized names and deletion of the last profile. | Prevalidate a candidate before changing anything. At next safe tick, mute input, disable current modules, install candidate settings/layout/bindings, clear telemetry, activate candidate modules, then resume input. Individual module failures yield an active but visibly degraded profile; desired enable flags remain intact, with no automatic retries. Save failure leaves this active state marked unsaved. | Clone independence, active deletion, invalid candidate, faulted candidate module, rapid switches and restart. Acceptance: no cross-profile subscriptions/pressed keys; switch displays failed modules and persistence status. |

When deleting the active profile, activate a selected remaining profile first and only remove the old profile after the transition completes. The resulting root mutation persists active ID and profiles together. Profile operations are disabled while a settings/editor draft is open; Done or Cancel resolves the draft first. Rename does not change an ID. Module keybind conflicts are validated before activation, so malformed stored conflicts cannot toggle multiple modules; later conflicting bindings in stable module-ID order become unbound with a diagnostic.

## 6. Input and telemetry semantics

`InputRouter` owns focus, screen gating, rising-edge detection and rebinding. Register global open-settings (default Right Shift) and open-editor (default unbound) through Fabric's key mapping helper; expose them in Minecraft Controls. Optional per-module toggle bindings live in the active profile and use the same edge stream. They start unbound. MVP bindings are one keyboard key or mouse button, with no chords/macros.

Settings can open in a world or title screen when no text-entry/modal screen owns input. Editor opens only with a world; the settings entry explains that requirement at the title screen. Module toggles and click telemetry are active only with world + focus + no ordinary screen. Key capture consumes its next input: Escape cancels, Backspace clears. Ignore auto-repeat. Clear held state on focus loss, screen opening, disconnect and profile change; require release before treating a still-held key as a new action.

Check conflicts against global actions, other module toggles and current vanilla bindings. Reject conflicting module assignments and identify the owner; users can first clear/change the other binding. Recheck after external Controls changes and suspend conflicting module bindings with a visible warning. Never cancel normal gameplay input merely to count it.

Prefer a supported Fabric raw input hook if available in the pinned API. Otherwise isolate minimal observational mouse/keyboard Mixins in the version adapter; verify exact descriptors against generated 1.21.11 sources. Tick polling alone is insufficient for CPS because a press and release can both occur between ticks. Do not replace GLFW callbacks.

| HUD module | Inputs/dependencies and defined output | Failure/reset behavior | Tests and acceptance |
|---|---|---|---|
| FPS | `GameSnapshotProvider` supplies Minecraft's reported FPS value; sample/copy on tick and refresh text at most every 250 ms. Label `FPS: N`. This is the game's counter, not a new average. | Before the first valid value show `FPS: —`. Disabled module has no formatting/draw work. | Fake snapshot changes and refresh boundary; in-game compare with debug counter allowing refresh lag. Acceptance: same source value, no claim of performance improvement. |
| CPS | Timestamp each left/right physical PRESS transition using monotonic nanoseconds. Separate deques count timestamps in `(now − 1 second, now]`. Holds/repeats do not count. Label `L: N  R: N`. | Clear on focus/screen/world/profile transitions. Cap each deque at 4096 entries; show `4096+` while saturated rather than silently reporting exact data. | Press/release between ticks, exact 1-second expiry, two buttons, holds, clock injection and saturation. Acceptance: synthetic press timeline matches specified counts; menu clicks never count. |
| Coordinates | Tick snapshot of local player's position and dimension; display floor-based block X/Y/Z plus dimension label. No interpolation in MVP. | Hide outside a world; editor uses labeled sample data. Never retain player/world references. | Negative fractions (`−0.1 → −1`), dimension change and disconnect. Acceptance: block values match game debug display and vanish after disconnect. |
| Keystrokes | Show forward/left/back/right/jump/sneak plus left/right mouse; use current vanilla action mappings and observed physical held state, not hardcoded WASD. Labels follow remapping. | Clear on focus/screen/world/profile transitions. This represents physical input, not inferred player velocity or auto-sprint state. | Remapped keyboard/mouse actions, simultaneous presses, missed releases on focus loss. Acceptance: no stuck highlights after Alt-Tab and correct labels after Controls edits. |

Input subsystem tests also cover held-key repeats, capture cancellation, binding conflicts and chat/inventory typing. Acceptance: one press causes at most one client action, typing never toggles a module, and opening a GUI does not leave gameplay input pressed.

## 7. HUD rendering and movable editor

Use Fabric `HudElementRegistry`, not the deprecated `HudRenderCallback`, with one original layer ordered relative to vanilla chat. Respect F1 and draw only in-world with no screen, except that the editor renders its own preview. Gate the exact layer insertion and drawing API through the version adapter.

`HudRegistry` maps enabled modules to widgets; `LayoutService` alone computes geometry. `HudSnapshot` contains copied metrics/settings; `DrawList` contains only bounded text/rectangle primitives. Scope matrix/scissor changes and restore them in `finally`. One bad widget faults only its owning module. Never allocate native textures or browser surfaces for these widgets.

**One coordinate space:** GUI-scaled logical pixels for drawing and Screen mouse positions. Convert raw window coordinates once at the adapter if used. Store each widget as normalized free-space placement `u,v ∈ [0,1]`, scale `s ∈ [0.5,3]`, and integer z-order. Given measured unscaled `w,h` and viewport `W,H`:

```text
displayWidth = s*w; displayHeight = s*h
x = u * max(0, W-displayWidth)
y = v * max(0, H-displayHeight)
```

Inverse drag mapping divides by the same available span; a zero span yields zero. Clamp before saving. Text/layout dimensions are recomputed after font/resource/GUI-scale changes. Oversized widgets pin to the origin and clip to the viewport; the editor still exposes scale/reset controls. Default widgets occupy separate top-left rows; draw order uses z-order then stable widget ID. Hit-testing walks reverse draw order.

| Subsystem | Responsibilities/interfaces/dependencies | Failure policy | Tests and acceptance |
|---|---|---|---|
| HUD renderer | `HudWidget.measure/draw`, layout and text metrics adapter; cache formatted strings until data/settings change. | Empty world snapshots hide gameplay widgets. Invalid stored geometry defaults with diagnostic; ordinary draw exception faults its owner and restores drawing state. | Geometry unit/property tests plus real scale/fullscreen/F1/resource reload checks. Acceptance: no HUD overlap caused by stale measurements and no lasting matrix/scissor corruption. |
| HUD editor | `HudEditorScreen` owns a layout draft, pointer capture, selection, drag offsets, arrows (1 GUI pixel; Shift 10), scale control, optional 4-pixel grid, reset and Done/Cancel. Preview disabled widgets dimmed with sample metrics without enabling them. | Escape/Cancel discards draft; Done commits one layout change and queues save. Focus loss cancels current drag but preserves draft. Resize recomputes bounds; non-editor forced screen close discards draft. | Drag hit-testing with overlap, normalized inverse round-trip, corner positions, zero span, GUI scale changes and cancel/save/restart. Acceptance: dragged widget follows pointer without jumping and remains reachable at 854×480, 1920×1080 and fullscreen. |

## 8. Settings and navigation

`ScreenRouter` manages parent screens; use native widgets, Minecraft fonts and original layout/colors. `SettingsScreen` includes category/search, module toggles, status/error badges, typed controls, reset, Profiles and Edit HUD buttons. All user-facing strings use this client's translation keys. Support Tab/Shift-Tab focus, Enter/Space activation, scroll and narrated labels.

Settings edits use a draft: field validation is immediate; Done submits one validated change set, updates desired module states and queues persistence; Escape/Cancel discards it. Live HUD previews read the draft without changing real module subscriptions. A callback failure during commit faults its module and leaves other valid settings applied; display this partial runtime failure explicitly. Rebinding belongs to the draft until Done. A pending save/error badge is outside the draft and reflects actual durability.

Dependencies: module descriptors, settings/profile services, input capture and screen adapter. Never let widgets write JSON directly. Tests: control-to-type validation, draft reset/cancel/commit, focus order, search, nested return path, title-screen access and scale clipping. Acceptance: all MVP settings, module switches and profile operations are usable without manual file edits; a save failure stays visible after the screen closes and on reopening.

## 9. Future launcher boundary

**Deferred proposed subsystem:** a separate process for installation profiles, official game/Fabric metadata resolution, verified downloads, Java selection, launch arguments, process monitoring and cancellation. Game configuration profiles above are not installation/accounts profiles. MVP relies on an existing launcher and has no launcher IPC dependency.

Reserve stable client/profile IDs and schema versioning. A later optional launch option may select an existing client profile ID; unknown IDs fall back visibly to the last selected profile. The launcher must not edit a running client's state file; hand over ownership only after exit or use a separately specified authenticated local protocol. Never put credentials in this settings schema.

Before launcher implementation: define `LaunchRequest`, staged `LaunchProgress`, cancellation and `LaunchResult` interfaces, then verify official metadata and authentication requirements separately. Failure handling covers corrupt downloads, unavailable metadata, incompatible Java, cancel during preparation and owned-process exit. Tests use fake metadata/process providers plus an authorized end-to-end launch. Acceptance: prepare → launch → observe exit → relaunch, with actionable errors and no dependency on proprietary services. This gate does not delay the client mod.

## Official integration references

Checked 2026-10-12: [versioned guides](https://docs.fabricmc.net/1.21.11/develop/), [JDK 21 setup](https://docs.fabricmc.net/1.21.11/develop/getting-started/setting-up), [HUD API](https://docs.fabricmc.net/1.21.11/develop/rendering/hud), [key mappings](https://docs.fabricmc.net/1.21.11/develop/key-mappings), [template generator](https://fabricmc.net/develop/template/). These establish integration guidance, not a successful build of this proposed design.
