# Feature lifecycle traces: FPS, CPS, ZOOM

Study date: 2026-10-11. These traces are static bytecode only (javap disassembly of `lunar.jar` and `modern.jar`). Nothing was executed. Aliases are mapped in [session2-class-legend.md](session2-class-legend.md), and evidence IDs in [evidence-index.md](evidence-index.md).

## Why these three

Each feature exercises a different part of the framework while staying non-security-sensitive:

| Feature | Exercises |
|---|---|
| **FPS** | The minimal decorated text HUD, with a value pulled from Minecraft. |
| **CPS** | An input-event-driven shared service, a custom HUD subclass, and setting change listeners. |
| **ZOOM** | A non-HUD feature that combines keybind, tick, scroll, screen and FOV events with mutable state. |

All three were located by the exact string constant returned from their `getId()` method, at bytecode offset 0 (`"FPS"`, `"CPS"`, `"ZOOM"`).

## Shared lifecycle (applies to all three; JV-06…JV-18)

1. **Initialization.** The feature constructor calls `super(defaultEnabled)` on `L._88f3cf._cfe983` (the feature base).
2. **Registration.** It is constructed in `FeatureManager._de9126()`, a hardcoded list, while the client singleton is constructed. That happens in the `Minecraft.run()` HEAD injection.
3. **Configuration loading.** `FeatureManager.init()` loads `settings/game/<Profile>/mods.json`. The base `load(JsonObject)` passes each feature its own sub-object, `Feature.load` loads each setting node, and `load_state` becomes `LOADED_CONFIG`.
4. **Event handling.** Handlers declared with `handle()` in the constructor are stored in the `events` trait. They are attached to the global bus only while the feature is effectively enabled.
5. **Runtime.** Handlers run on whatever thread posts the event. Tick and input events come from Minecraft's client thread.
6. **Output.** HUD features attach a `hud_renderer` trait. The static handler in the HUD base renders it during the scaled 2D render event.
7. **Persistence.** A setting change triggers `SettingsManager._145809`, which writes the owning JSON file immediately. Only non-default values are written.

---

## FPS: `L._88f3cf._bb4487._145809._cfe983` (JV-21)

| Stage | Confirmed implementation |
|---|---|
| Initialization | `super(false)`, so the feature is **disabled by default**. One setting is created with `bool("reverseOrder")` and its default is unchanged (false). |
| Registration | Listed in `FeatureManager._de9126`. No event handlers are registered; FPS has no `handle()` calls. |
| Configuration | The `mods.json` object for `FPS` holds `enabled`, `x`, `y`, `position`, `options{scale}`, `seen`, `lastModified` and `panelIndex` (FS-03). `reverseOrder` is absent there, which matches the rule that defaults are not saved. |
| Event handling | Indirect only. The HUD base's static Render2D handler (JV-18) iterates the enabled features and calls FPS's `hud_renderer`. |
| Runtime | The HUD element is the factory-built `DecoratedTextHud(x=0, y=0, anchor=TOP_LEFT, HudSize(10,18,22,50,56,62), text=this::_e93d3c)`. Every frame, `_52e8ee(editing)` calls the text function (JV-20). The text function chooses the localization key `"reverse"` or `"fps"` according to `reverseOrder`, then formats it through the feature's cached message formatter. The `fps` argument is `mc.bridge$getDebugFPS()`, wrapped by `_590f69("fps", value)`. |
| Rendering | Through the decorated text HUD: optional background and border, then the text with color, shadow and alignment settings inherited from the decorated HUD base (section "Decorated HUD" in [rendering-and-hud.md](rendering-and-hud.md)). The size is clamped by `HudSize` (min, preferred and max width and height). |
| Persistence | `reverseOrder` is saved only when true. HUD position and scale are saved only when they differ from their defaults (JV-19). |

### What this establishes

- **The FPS value is Minecraft's own debug FPS counter**, read through the bridge (`Minecraft.fps` / `getFps()`). Lunar applies no separate sampling window.
- **Text is localized.** The display string comes from a language template keyed by feature details and `"fps"`/`"reverse"`, so the visible ordering ("120 FPS" versus "FPS: 120") is a translation-template choice.

**Tentative.** `_590f69(name, value)` delegates to an optional helper (`L._88f3cf._bb4487._590f69`), which is created only when `_f50b51()` is true. It likely substitutes preview or sample values, but its behavior was not traced.

---

## CPS: `L._88f3cf._bb4487._6c713e._cfe983` (+ `$_cfe983` HUD) (JV-22, JV-23)

| Stage | Confirmed implementation |
|---|---|
| Initialization | `super(false)` (disabled by default). Settings: `rightClick` (bool, false), `showCPSText` (bool, **true**), `reverseText` (bool), `ignoreCancelledClicks` (bool) and `lineColor` (color, default int `-14671840`, i.e. `0xFF202020`). |
| Registration | Obtains the shared listener service with `_c8175c(L._ba7d98._590f69._cfe983.class)`, which is the click counter. It sets `hud_renderer` to a new inner class `$_cfe983` that extends the decorated text HUD with `TOP_LEFT` and `HudSize(10,18,22,40,56,62)`. It attaches a change listener to `rightClick` that calls `counter._f4d7d6()` to clear the right-click list. |
| Configuration | `mods.json` key `CPS` holds `x`, `y`, `position` and `panelIndex` (FS-03). |
| Event handling | Done by the **counter service**, not by the feature. In its constructor the service calls `handle(tickPreEvent, prune)` and `handle(mouseButtonEvent, record)`. The service base `L._ba7d98._1e73d7` is a per-class singleton map (`_1eb51c(Class)`) with a dependent-feature set and a counter. **Strong inference:** it is active only while at least one dependent feature is enabled. |
| Runtime | **Record** (mouse button event, posted from the `MouseHandler.onPress` HEAD, cancellable, ≤1.21.8, or the `onButton` HEAD, ≥1.21.9): if no screen is open and the action is `DOWN`, then button 0 adds `currentTimeMillis` to list A, and also to list B when the player is **not** using an item; button 1 adds to list C. **Prune** (every client tick, from the `Minecraft.tick` HEAD): `removeIf(t < now − 1000)` on all three lists. **Value:** CPS is the number of presses in the last 1000 ms. Left CPS reads list B when `ignoreCancelledClicks` is set and list A otherwise; right CPS reads list C. |
| Rendering | The text is built with one 5-part `makeConcatWithConstants`: the left count, a separator and the right count when `rightClick` is set, and a suffix constant (`L._e62626._cfe983._0d1625`) when `showCPSText` is set. `reverseText` changes the part order. The literal separator strings were not decoded; javap printed them as blank, so they are likely formatting or control characters. A custom `_cfe983(ctx, x, y, …)` draws a 1×9 px divider between the two numbers when `rightClick` is on: a shadow in `0x6F000000`, then a line in `lineColor`. The divider is positioned from string widths measured with `bridge$getStringWidth`. |
| Persistence | Same rules as FPS. Toggling `rightClick` also clears the stored right-click timestamps at runtime. |

### What this establishes

- **Click-counting definition:** a 1-second sliding window of press timestamps, sampled per click and pruned per tick. It is not an average. Clicks made while a GUI screen is open are ignored.
- **"Ignore cancelled clicks"** really means "exclude clicks while using an item" (`bridge$isUsingItem`). That is the only filter on list B.
- **Ordering relative to the bus:** the mouse Mixin posts the event *before* vanilla handles it. If any handler cancels it, vanilla processing is cancelled. The click is also forwarded to the GameUI browser, which can consume it.

---

## ZOOM: `L._88f3cf._bb4487._136819._cfe983` (JV-24)

| Stage | Confirmed implementation |
|---|---|
| Initialization | `super(true)`, so the feature is **enabled by default**. Settings and defaults: `zoomKeybind` keybind (default `KEY_C`; it re-binds to Minecraft's own zoom key when the bridge exposes one through `bridge$getZoomKey`), `smoothCamera` true, `smoothZoom` true, `variableZoom` false, `zoomScrollSpeed` float 1.0 in [0.25, 5.0], `toggleKeyZoom` false, `zoomDivisor` int 4 in [2, 10], `cameraSensitivity` float 1.0 in [0.1, 2.0]. |
| Registration | Six `handle()` subscriptions: scroll, tick-pre, screen-init, screen-closed, FOV-modifier and FOV. The keybind's press and release callbacks call `_e6d2f9` (activate or toggle) and `_cb47d7(released)` (deactivate unless toggle mode). |
| Configuration | `mods.json` key `ZOOM` holds only `panelIndex` (FS-03), so every setting is at its default. |
| Event handling | The **FOV event** is posted from the `GameRenderer.getFov` RETURN (1.16–1.21) or `Camera.calculateFov` (26.x). The **scroll event** comes from `MouseHandler`/`ScrollWheelHandler`. The **screen init event** comes from wrapping `Screen.init`. **Tick** comes from the `Minecraft.tick` HEAD. |
| Runtime | **Enter zoom** (first FOV event while `active`): remember the vanilla `smoothCamera` option, enable cinematic camera if `smoothCamera` is set, and request a full chunk re-cull with `bridge$setNeedsFullRenderChunkUpdate(true)`. **Each FOV event:** fov × `lerp(partialTick, prev, cur)` when `smoothZoom` is set, otherwise fov ÷ (`zoomDivisor` × variable factor). If an external zoom integration (`ML._590f69._21aca6._f02b61()` → `getConfig().isZooming()`) reports zooming, the result is additionally multiplied by 4.0. Strong inference: this compensates for the other mod's zoom. **Tick:** `cur += (1/divisor − cur) × 0.75` (exponential approach). **Scroll** while zooming with `variableZoom`: the factor changes by ±`zoomScrollSpeed`. **Screen opened:** `active = false`. **Exit:** restore `smoothCamera`, re-cull chunks, and reset the factor to 1. |
| Rendering | No HUD. The visible effect is the modified FOV and, optionally, the cinematic camera. `_907dcf()` exposes `cameraSensitivity`; the consumer was not traced. |
| Persistence | Settings persist through the normal path. The runtime `active` and smoothing state are transient. |

### What this establishes

The zoom algorithm is now explicit: a divisor of 2–10 (default 4), smoothed per tick with a 0.75 factor and interpolated per frame. Chunk re-culling is triggered on enter and exit. Opening any screen cancels zoom.

---

## Cross-feature observations

- **Settings UI listing.** Each feature implements `_cfe983(OptionsBuilder)` to declare its options page: FPS lists `[reverseOrder]`, CPS groups its settings under `SETTINGS`, and ZOOM lists 8 settings. This is the `options` trait payload the GameUI settings screen renders.
- **Defaults live in bytecode constructors.** No external defaults file was found for these features. Previously, defaults were described as unresolved; for these three they are now confirmed.
- **Gating precedence.** Even an enabled feature can be forced off by server or Apollo `intercept`, `support` or `restriction` traits (JV-09). No `restriction`/`support` attachment was observed for these three in their own constructors; attachments made elsewhere were not searched exhaustively.
