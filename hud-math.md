# HUD scale and editor snapping

Study date: 2026-10-11, session 3. Static disassembly only; this extends, rather than replaces, [rendering-and-hud.md](rendering-and-hud.md). **Confirmed** means directly present in bytecode; **Strong inference** is its interpretation; **Tentative** is a provisional mapping; **Unknown** is not established. Method offsets below are decimal JVM `Code` offsets, not file offsets. Class aliases follow [session2-class-legend.md](session2-class-legend.md).

## 1. Global HUD scale (JV-45)

**Confirmed.** In `lunar.jar`, `L._2f4182._1253fc._bb4487.getScale()` has three early-return cases:

| Case | Returned multiplier | Bytecode |
|---|---:|---|
| Scaled-resolution cache `_4dffb6` is absent, or client `_bb1b0c()` is false | 1 | `getScale @0–16` |
| Settings mode is `ALL` | 1 | `getScale @17–40` |
| Mode is `MODS`, and the current-screen class is null or the native HUD editor; also a version-gated screen-interface case on ordinals ≥7 | 1 | `getScale @41–95` |

**Unknown.** The user-facing identity of the extra `ML._590f69._bb4487._21aca6._429bf0` screen-interface case is not established here; the `instanceof` test itself is **Confirmed** (`getScale @62–81`). It must not be silently treated as every open GUI.

**Confirmed.** Otherwise the bytecode implements:

```text
dpr = _22e64f(true)
g = scaledResolution._ec40b4()       // Minecraft GUI scale
s = _58bb34                         // initialized to 2.0
if mode == AUTO and g / dpr > 4:
    s *= 2                         // normally 4.0
return s / int(g / dpr)
```

Sources: `getScale @96–155`, `_bb4487.<clinit> @41–42` for the initial 2.0, and `L.util._d0d09a._ec40b4 @0–4`. `f2i` at 152 truncates; for a positive quotient this is `floor`. **Unknown:** positivity of the denominator for every possible bridge/window state was not proven; this method does not clamp the denominator to one (`getScale @141–155`).

### HiDPI arithmetic and default

**Confirmed.** `_22e64f(true)` returns 1 unless the HiDPI predicate is true, display and logical heights are positive, and `_b36bc2()` permits the setting. On the enabled path:

```text
dpr = double(max(1, displayHeight / logicalHeight))
// IMPORTANT: the division is Java integer division, before conversion to double.
```

Source: `lunar.jar`, `L._2f4182._1253fc._bb4487._22e64f(boolean) @0–62`, specifically `idiv @57`, `Math.max @58`, `i2d @61`. **Correction to the handoff:** this is not an unrestricted floating-point display/logical ratio; a hypothetical 1.5 ratio yields 1 here.

**Confirmed.** `_b36bc2 @0–51` additionally requires its internal disable flag to be false, ordinal >5 (1.16+), a client and a settings manager, then reads `highDPIScale`. The default is hard-coded true in `L._02d7ad._1253fc._1253fc._590f69.<init> @177–196`. This is a constructor default, not the user's stored setting.

### Minecraft GUI scale

**Confirmed.** `L.util._d0d09a.<init>(MinecraftBridge,int,int)` uses `max(1, bridge$getGuiScale())` at ordinals ≥6 (`@14–46`). Earlier versions use a classic loop starting at scale 1: increase while below the configured limit and while the next division leaves at least 320×240 (`@49–164`); GUI scale zero becomes a limit of 1000 (`@99–107`). Unicode text adjusts an odd scale greater than one downward by one (`@165–194`); scaled dimensions are then calculated (`@197–249`). Artifact: `lunar.jar`; ordinal names are from `genesis.jar!versions.conf` (FS-04, resource offset N/A).

**Confirmed.** Migration v9→10 removes `useMinecraftScale` from general-settings JSON when `_22e64f(false)>1`, **or** the additional `_2683bc` platform flag is true: `L._2b0ee0._cfe983._cfe983._ec7e36._cfe983(ctx,target,json) @0–29`. False bypasses the `highDPIScale` opt-in check; the HiDPI/dimension checks remain. See [settings-persistence.md](settings-persistence.md).

## 2. Anchor assignment (JV-46)

**Confirmed.** `lunar.jar`, editor `L._2f4182._6c713e._cfe983._cfe983(point,screen)` divides the screen into thirds and returns top/middle/bottom and left/center/right anchors (`@0–280`). The bottom-middle region is split at `W/3+W/6 = W/2`: x≤W/2 gives `BOTTOM_CENTER_L`, x>W/2 gives `BOTTOM_CENTER_R` (`@224–276`). Comparisons determine the exact boundaries: x=W/3 belongs to the center column; on the bottom row x=2W/3 belongs to the right column; y=H/3 belongs to the middle row and y=2H/3 to the bottom row.

**Confirmed by the existing bytecode trace (JV-19).** Anchor-resolved offsets, persistence, doubled UI coordinates, per-element scale and `HudSize` remain as documented in [rendering-and-hud.md §3](rendering-and-hud.md#3-layout-positioning-and-scaling-confirmed-jv-19). Their source is `L._88f3cf._590f69._cfe983` (`_cfe983/_21aca6`, `load`, `_590f69`, `_3a82ee`) and its `$1` switch map; that report is the source for those method-level citations. This report changes only the previously partial global-scale and snap findings.

**Confirmed.** The shared HUD scale builder starts with default 1 and range from virtual helper methods: `L._88f3cf._590f69._cfe983.<init>(float,float,Anchor) @5–41`. Interface `L._88f3cf._590f69._1253fc._b667ba @0–2` returns 0.25 and `_0f113a @0–2` returns 5.0. These resolve the framework's default **0.25–5.0** setting range; subclasses can override the virtual helpers or customize the builder. The effective `getScale @0–18` also divides the stored scale by `_72340c()`, so the stored setting range should not be mistaken for a universal effective multiplier range.

## 3. Dragging and snapping

For this section, **D** means editor `_cfe983(DrawContext,point)` and **S** means editor `_cfe983(DrawContext,boolean,boolean,HudElement,Anchor,AtomicDouble,AtomicDouble)`. Both belong to `L._2f4182._6c713e._cfe983` in `lunar.jar`.

**Confirmed.** D reads `input._7fbb1e(0)` and `input._7fbb1e(1)` into separate booleans (`@14–34`). **Tentative:** their assignment to physical Mouse1/Mouse2 is not independently resolved by this interface trace; the editor help strings suggest left-drag and right-button suppression (JV-35), but strings are not an input implementation.

| Phase | Confirmed behavior | Citation |
|---|---|---|
| Screen edges | For a selected element being dragged, unless input boolean 1 is set: the left/top candidates at ≤4 editor units snap to nominal margin 2. Right/bottom tests use the screen extent minus 4; the right calculation also contains a +0.5 adjustment. Each snapped axis is marked unavailable to later snapping; a guide is drawn. | D `@1691–1702`, `@1791–2054` |
| Apply initial position | Calls `HudElement._429bf0(x,y)`. | D `@2057–2063` |
| Center/neighbour gate | Only when `selected.size()==1` **and** input boolean 0 is true does D call S. | D `@2068–2123` |
| Screen center | S tests a `MIDDLE` vertical/horizontal anchor; `abs(centerDelta)<5`, corrects that coordinate, draws a guide and disables further correction on that axis. `BOTTOM_CENTER_L/R` skip these center tests. | S `@58–248` |
| Candidate ordering | Sorts other HUD features by the rectangle distance metric, skips self and dimensions below 1. | S `@249–390` |
| Neighbour edges | Compares same and opposing edges on still-available axes; accepted interval is **−2≤d≤2**, then adds d, draws a guide and locks that axis. Stops when both axes are unavailable. | S `@399–1059`, exit/axis test `@327–335` |
| Apply final position | Calls `_429bf0` with the corrected `AtomicDouble` coordinates. | D `@2126–2140` |

**Correction (Confirmed).** The handoff's “all snapping requires one selected element” is too broad: the `size()==1` gate applies to the center/neighbour helper, **after** the screen-edge block. The latter is gated by input boolean 1 instead (D `@1797–1802`, `@2068–2083`). Likewise, the neighbour interval is inclusive: `iflt` at S 593 rejects below −2 and `ifgt` at 600 rejects above +2; the other edge tests repeat that pattern.

### Nearest-first metric

**Confirmed.** Editor `_cfe983(Rectangle a,Rectangle b) @0–60` returns:

```text
dx = max(0, abs(a.x-b.x) - (b.width / 2))
dy = max(0, abs(a.y-b.y) - (b.height / 2))
distance = dx*dx + dy*dy
```

The width/height halves use integer division (`@16–17`, `@41–42`). **Strong inference:** this is a proximity heuristic for prioritizing snap candidates, not a symmetric rectangle-to-rectangle minimum-distance formula; only b's size is subtracted. S sorts using its comparator at `@262–288`.

## 4. Limits

- **Unknown:** exact physical mouse-button mapping behind `_7fbb1e`, and subjective visual behavior at fractional edges. Sources above establish code, not runtime appearance.
- **Confirmed:** no target was executed and no user settings values were read in this continuation. Defaults and constants above come from shipped constructor bytecode.
