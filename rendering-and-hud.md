# Rendering and HUD architecture

Study date: 2026-10-11. Static bytecode only. Each item is marked **Confirmed** (observed in bytecode or data), **Strong inference** or **Tentative**. Aliases are mapped in [session2-class-legend.md](session2-class-legend.md).

## 1. Where Lunar's 2D layer enters Minecraft's pipeline

**Confirmed (JV-17).** The GameRenderer Mixin `ML._d4ca6c._590f69._21aca6._1e73d7._13ea87._d4ca6c` provides one entry point per version family:

| MC family | Hook | Effect |
|---|---|---|
| 1.16–1.21.x | `lunar$renderGui$v1_16/v1_20/v1_21` **Redirect** of the `Gui.render(…)` call inside `GameRenderer.render`, plus `lunar$beforeHudRender$*` Inject before it | Lunar wraps the vanilla HUD call. On 1.21 it builds a draw context from `GuiGraphics` and `DeltaTracker` and calls `lunar$renderGui(gui, ctx, …, poseStack, partialTicks)`. From `MC_VERSION >= 30` (1.21.6) the work is deferred through `ML._d4ca6c._d4ca6c._a140a8._13ea87._3bf032(Runnable)`. |
| 26.1 / 26.2 (state-extraction renderer) | `lunar$renderGui$v26_1` Redirect of `Gui.extractRenderState`; `lunar$renderGameOverlay$v26_1` Inject at `GuiRenderer.render` | Shown in detail below |

**The 26.x path** (`lambda$lunar$renderGameOverlay$v26_1$0`) runs only when the world is loaded, the GUI is not hidden, and the screen is not a `LevelLoadingScreen`. It then:

1. Opens profiler section **`event2d`**.
2. Creates a new `GuiGraphicsExtractor` over the shared `GuiRenderState`.
3. **Splices strata.** It copies the strata after `bridge$getLastStratumBeforeOverlay()` aside, inserts a fresh stratum node for Lunar, renders, then re-appends the saved strata and fixes `firstStratumAfterBlur`. This places Lunar's HUD **above vanilla HUD elements but below overlays**, and keeps blur ordering correct.
4. Pushes the pose stack and translates by z=+1.5.
5. Builds a Lunar draw context through a builder: GUI graphics, GUI renderer, pose stack, buffer source, a z-level integer and partial ticks.
6. Calls `lunar$fireEvent2D(ctx, renderContext, bufferSource)`.
7. Draws the Lunar notification and overlay layer (`L._2f4182._cfe983._cfe983(ctx, drawCtx, scale)`).
8. Calls `bufferSource.endBatch()`, resets the shader color, and pops the profiler.

`lunar$fireEvent2D` (JV-17):

- If **F3 debug is not showing**, it posts **Render2D (unscaled)**, `L._d4ca6c._cfe983._1e73d7._cfe983`.
- It then always does `push`, `scale(s, s)` with `s = L._2f4182._1253fc._bb4487.getScale()` (the Lunar HUD scale), posts **Render2D-HUD (scaled)** `…_1e73d7._21aca6`, and calls `pop`.

**Strong inference.** The 3D layer is analogous. `LevelRenderer` `lunar$event3D*` posts `…_1e73d7._590f69` (from the Mixin event map) for world-space rendering such as waypoints and hitboxes.

## 2. HUD organization

### Type hierarchy (Confirmed)

```
HudElement interface  L._88f3cf._590f69._1253fc   (is a Serializable settings node)
 └ HudLayoutBase      L._88f3cf._590f69._cfe983   x,y,width,height, default x/y, anchor, scale setting
    └ DecoratedTextHud<T> L._88f3cf._590f69._88f3cf  background/border/text styling + content renderer
       ├ factory instances (FPS, CLOCK, …) via static _cfe983(x,y,anchor,HudSize,Boolean2ObjectFunction<T>)
       └ subclasses (CPS$_cfe983, …)
```

- **Attachment (Confirmed).** A feature exposes its HUD by setting the **`hud_renderer`** trait (`FeatureTraits._f845fa`). The renderer finds HUDs by walking the features, not through a separate HUD registry. Child features can carry their own `hud_renderer`, as `PING → PING_HUD` does.
- **Counts (Confirmed by Codex S1).** 37 direct children of the layout base and 66 of the decorated base; 128 classes including descendants.

### Render loop: the HUD base static handler (Confirmed, JV-18)

The HUD base's static initializer registers two **global** bus handlers, not per-feature handlers. One is for Render2D-HUD and one for its inner variant. Per frame the handler does the following:

1. **Gates on global state:** the HUD-hiding feature, F3 visibility (with a general setting that allows HUD while F3 is open), and `_cbdcd3()`. That method requires a loaded world, checks the GameUI overlay state, and compares the current screen class with the two HUD-editor screen classes (`L._2f4182._6c713e._cfe983` / `…_21aca6`). It also checks a Rewind feature flag. The exact boolean combination was only partly decoded.
2. Iterates `FeatureManager.getAll()`, skipping disabled features. In "vanilla-only" mode it keeps only features whose `details.isVanilla` is true. It recurses into `children`.
3. For each `hud_renderer`:
   - skip it if its "editor-only" flag (`_a003b6`) does not match;
   - call `hud._21aca6(editing, feature)`, which returns false when the `dynamic` trait says inactive, and otherwise refreshes content (`_52e8ee`);
   - if visible: `push`, `scale(hud.getScale())`, translate to the anchor-resolved position computed from the event's screen size (`_cfe983(screenSize)`), call `hud._cfe983(event, width, height, editing)`, then `pop`.

**Consequences.** Per-element scale multiplies the global Lunar HUD scale, because the event is already scaled. HUD content is recomputed every rendered frame (pull model). HUD draw order is the feature manager's set order, which is a `LinkedHashSet`, so insertion order from `_de9126`.

## 3. Layout, positioning and scaling (Confirmed, JV-19)

**Anchors.** The anchor enum (`L._88f3cf._590f69._bb4487`) has ids `topLeft`, `topCenter`, `topRight`, `middleLeft`, `middleCenter`, `middleRight`, `bottomLeft`, `bottomCenterLeft`, `bottomCenterRight` and `bottomRight`. Each pairs a horizontal and a vertical edge.

**Resolved position.** Let `W` and `H` be the screen size divided by the element scale, and `w` and `h` the element size. The x and y bases are:

| Anchor | x base | y base |
|---|---|---|
| `*_LEFT` | 2 | — |
| `TOP_CENTER`, `MIDDLE_CENTER` | W/2 − w/2 | — |
| `BOTTOM_CENTER_L` | W/2 − w + 30 | — |
| `BOTTOM_CENTER_R` | W/2 − 30 | — |
| `*_RIGHT` | W − w − 2 | — |
| `TOP_*` | — | 2 |
| `MIDDLE_*` | — | H/2 − h/2 |
| `BOTTOM_*` | — | H − h − 2 |

The stored `x` and `y` are offsets added to that base, divided by scale: `pos = base + x/scale`. The two bottom-center anchors sit 30 px either side of screen center. **Strong inference:** they flank the hotbar.

**Persistence.**

- `x` and `y` are written only when they differ from the element's default.
- `position` is written when x/y are non-default **or** the anchor differs from the default anchor.
- Load falls back to the defaults for missing keys, and `fromId` falls back to the default anchor for unknown ids.
- This matches `mods.json` on disk. For example, `DIRECTION_HUD` stores only `{y, position}` and `POTION_EFFECTS` only `{x, position}` (FS-03).

**UI payload form.** `_3a82ee()` emits `{x: X*2, y: Y*2, scale, position}`. **Strong inference:** the in-game web UI uses a doubled coordinate space for the HUD editor's property panel.

**Per-element scale.** The `scale` float setting is created in the base constructor through the setting builder with a default and range taken from interface defaults (`_b667ba`, `_0f113a`). It is saved under `options.scale`.

**Global Lunar HUD scale** (`L._2f4182._1253fc._bb4487.getScale()`). This is **partially resolved**. It depends on a general-settings enum with values `ALL`, `MODS` and `AUTO`, on Minecraft's GUI scale, and on whether a Lunar HUD editor screen is open. The `AUTO` branch uses constants 4.0 and 2.0 divided by the window's scale factor. The exact formula was not fully traced.

**Element size.** `HudSize(minHeight, height, maxHeight, minWidth, width, maxWidth)` (Lombok name) bounds the decorated HUD's computed width and height. FPS uses `(10,18,22,50,56,62)` and CPS `(10,18,22,40,56,62)`. The `staticBackgroundWidth/Height` settings choose fixed or content-sized boxes.

## 4. Text and content rendering (Confirmed, JV-20)

- **Content dispatch.** `DecoratedTextHud<T>` resolves a type-specific content renderer from a static `Class → renderer` map. Three renderers are registered: `String`, `net.kyori.adventure.text.Component`, and `L._88f3cf._590f69._13ea87` (strong inference: an icon-plus-text value). The renderer is chosen lazily from the first value's class.
- **Lists.** If `T` is an `Iterable`, each element is measured. The width is the maximum and the height is the sum of `(h + 1)`.
- **Drawing order:**
  1. background rectangle (`backgroundColor`);
  2. optional border (`borderColor`, `borderThickness`);
  3. text with `textColor` and `bracketColor`, `textShadow`, and `alignment`. Text metrics come from the bridge: `bridge$getStringWidth`, and a height derived from the 1.88 and 0.5 centering constants.
- **Setting names** (Confirmed): `background`, `brackets`, `staticBackgroundWidth`, `staticBackgroundHeight`, `backgroundWidth`, `backgroundHeight`, `border`, `textShadow`, `textColor`, `bracketColor`, `backgroundColor`, `borderColor`, `borderThickness`, `alignment`, `showHudIcons` and `showText`.
- **Custom drawing.** Subclasses override `_cfe983(ctx, x, y, editing, …)`. CPS draws its divider line this way, using utility `L._2f4182._1253fc._bb4487._1e73d7(ctx, x, y, w, h, argb)` for filled rectangles.

## 5. Textures

### WebOSR browser textures (Confirmed, JV-30/31/32)

- `TextureHandler` (`L._81676d._21aca6._590f69._cfe983._cfe983`) is called by the native engine:
  - `createTexture(w, h, …)` registers a dynamic texture `webosr:<n>` with Minecraft's `TextureManager` and allocates **RGBA8** through `bridge$allocate`;
  - `uploadTexture(id, ByteBuffer, x, y, w, h, stride…)` calls **`bridge$uploadBgra`**, a sub-rectangle BGRA upload;
  - `resize`, `read` and `delete` are also implemented.
- **Pixel ownership is therefore Java/Minecraft-side.** Ultralight paints CPU bitmaps and Java uploads dirty rectangles.
- **Frame pacing.** `GameUIRenderer` calls `WebEngine.invokeIteration()` at most every **5 ms**, then renders 3D model widgets (the UI `addModel` support), then the browser.
- **Composition.** The browser blitter gets `Browser.getTexture()`, maps it to the `webosr` texture, registers it under a stable `lunar:<hash>` location, and draws a **framebuffer-sized textured quad** (4 position/UV vertices). It first sets a projection through a 6-double draw-context call using constants 1000.0, 21000.0 and 3000.0 (strong inference: orthographic near/far planes and z offset), sized from `bridge$getMainRenderTarget().framebufferWidth/Height`. An integer from performance settings (`_eeb804`) and a millisecond clock throttle redraws. **Tentative:** that integer is a UI frame-rate cap.
- **Device scale.** `Browser.setDeviceScaleFactor(max(guiScale, minimum))` is updated when the window or GUI scale changes ("Browser scale [w, h, lh, sd, sf]").

### Images inside the UI

`.imgsrc` requests return `IMGSRC-V1\n<id>`, which exposes game textures to HTML as Ultralight image sources (see [ipc-deep-dive.md](ipc-deep-dive.md) §2.3).

### Feature textures

HUD icons and Lunar assets use `lunar:` resource locations, for example `icons/mainmenu/cog-20x20.png` in the HUD editor. They are resolved through Minecraft's resource system via the bridge.

## 6. HUD editor and UI interaction

**Correction.** Codex inferred HUD editing from the web UI `/hud` route. The interactive drag/scale editor is in fact a **native Java screen**, `L._2f4182._6c713e._cfe983`. It extends a Lunar screen base and draws with the same bridge context.

**Confirmed from strings and Lombok names:**

| Item | Detail |
|---|---|
| Editor records | `SelectedHudMod(feature, dragX, dragY)`, `ScaleHudMod(feature, hudPosition, mouse, scaleRegion, scale, drawing)`, `HistoricalHudMod(feature, hudPosition, scale, x, y, groupingTime)` |
| Mouse1 | Hold: `addModsToRegion` (box select) and `selectDragMods` |
| Mouse2 | Click: `resetToClosest`. Hold: `dontLockDragging` (disables snapping) |
| CTRL+Mouse1 | `toggleModSelection` |
| CTRL+Z / CTRL+Y | `undoMovements` / `redoMovements` |
| Arrow keys | `moveWithPrecision` |
| Buttons | Help, mods, cosmetics, emotes, reportABug |

**Strong inference.** Static `_a140a8(point)` / `_cfe983(point, point)` return an anchor for a screen point, which re-anchors an element to the nearest region of the screen grid. `_cfe983(Rectangle, Rectangle)` computes an overlap or distance metric used for snapping. Thresholds were not extracted.

## 7. Configuration-driven rendering: an end-to-end example

A change to FPS `textColor` in the web UI flows as follows:

1. JS `settings.update(FEATURE, "FPS", "textColor", "<value>")` calls `@CallbackJS update`.
2. The `FEATURE` scope resolves to the FPS `options` trait, then the color setting, then `_d2c28f(str)`.
3. The value is applied, Apollo `ModSettingModule` is broadcast, listeners fire, and `settings/game/<Profile>/mods.json` is saved immediately.
4. Payloads `data:features` and `data:details` are re-published to the page if they changed.
5. On the next frame, the scaled Render2D event reaches the HUD base handler. `DecoratedTextHud` reads `textColor.get()` and draws with the new color. **There is no caching layer between a setting and the renderer.**

## 8. Verified versus inferred

| Claim | Status |
|---|---|
| Lunar HUD drawn through a GameRenderer Redirect/Inject, posting 2D events with HUD scale | Confirmed |
| 26.x strata splicing places the Lunar HUD between vanilla HUD and overlays | Confirmed as code; visual effect inferred |
| Anchor math, persistence rules, HudSize, content renderers | Confirmed |
| HUD editor is a Java screen with undo/redo, box select and snapping toggle | Confirmed from strings and fields; snapping algorithm details inferred |
| WebOSR CPU bitmap → Java RGBA8 texture (BGRA upload) → full-screen quad | Confirmed |
| Native paint and threading model of Ultralight | Unknown (no native decompiler) |
| Exact global HUD scale formula | Partial |
