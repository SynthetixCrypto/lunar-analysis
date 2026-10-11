# Event payload catalog and cancellation validation

Study date: 2026-10-11, session 3. Static bytecode only. **Confirmed** = directly present in classes/disassembly/tables; **Strong inference** = interpretation of that evidence; **Tentative** = provisional semantic mapping; **Unknown** = not established. Decimal offsets are relative to the named method's JVM `Code` attribute.

## 1. Scope and base types (JV-43, FS-08)

**Confirmed.** The saved [event-catalog.tsv](event-catalog.tsv) contains **279 event classes**, **211 distinct posted types**, and **90 cancellable classes**. Of the posted types, **31** are under SkyBlock package `L._88f3cf._bb4487._23f752`. These are type counts, not numbers of invocations at runtime. Recalculated from the catalog by [session3-tools/verify.py](session3-tools/verify.py), with constructors cited in [event-bytecode-locations.tsv](event-bytecode-locations.tsv). Non-code aggregation offset: N/A.

**Confirmed.** `lunar.jar` event base is `L._d4ca6c._21aca6`. Cancellable base `L._d4ca6c._1e73d7` extends it and has one boolean `cancelled`; `cancel @0–5` sets true, `isCancelled @0–4` reads it, and `setCancelled(boolean) @0–5` replaces it. This state is not intrinsically a Mixin cancellation: a producer must consume it.

**Unknown.** Absence of a mapped post site is not proof of dead code. The catalog describes the saved class/post-map coverage, not every possible reflective or future producer. The full event-bus dispatch algorithm remains in [java-internals.md §3](java-internals.md) (JV-05).

## 2. Key payloads

For the following table, **E** abbreviates `L._d4ca6c._cfe983`. Each payload row is **Confirmed** from `lunar.jar` constructor/field bytecode. English role names are **Strong inference** from the Mixin hooks unless an original name is explicitly cited. Bridge type aliases identify the exact descriptor; their conceptual names are not claims about vanilla class identity.

| Role / event | Confirmed payload and mutability | Constructor / related method offset |
|---|---|---|
| Char: `E._bb4487._cfe983` | No subclass payload; inherits cancellation flag. In particular it does not store the typed character. | `<init>() @0–4` |
| FOV base: `E._d4ca6c._d4ca6c` | Four floats: mutable FOV `_3a82ee`, final partial tick `_cbdcd3`, final `fovModifierHandPrev` and `fovModifierHand`. The last two are surviving original field names. | `<init>(float,float,float,float) @0–25`; setter `_79e7e6(float) @0–5`; getters `@0–4` |
| Final-FOV variant: `E._d4ca6c._d4ca6c$_cfe983` | Inherits those four floats and cancellation. | `<init>(float,float,float,float) @0–9` (see constructor appendix) |
| Modifier variant: `E._d4ca6c._d4ca6c$_21aca6` | Same inherited payload; separate event type. | `<init>(float,float,float,float) @0–9` (see appendix) |
| Render2D: `E._1e73d7._cfe983` | Draw context `ML._590f69._bb4487._13ea87._a140a8`, resolution `L._81676d._1e73d7<?>`, and boolean. Two-argument convenience constructor delegates to the three-argument form. | `<init>(ctx,resolution) @0–7`; `<init>(ctx,resolution,boolean) @0–19` |
| Scaled Render2D-HUD: `E._1e73d7._21aca6` | Inherits Render2D fields; constructor takes draw context and `L._81676d._1e73d7$_cfe983` resolution. Scaling is done by the producer, not by a new payload field. | `<init>(ctx,resolution) @0–7`; producer below |
| Render3D: `E._1e73d7._590f69` | Final draw context and camera bridge `ML._590f69._bb4487._cfe983`, mutable float partial tick. | `<init>(ctx,camera,float) @0–19` |
| Tick pre/post: `E._2ce426._3a14e3` / `E._2ce426._ec7e36` | No subclass payload. | Both `<init>() @0–4` |
| Chat: `E._21aca6._21aca6$_590f69` | Component, derived plain-text String, int type. **Constructor takes only `(Component,int)`**, and computes the String using `PlainTextComponentSerializer`; a null component produces null text. | `<init>(Component,int) @0–35`, derivation `@9–27`; `getComponent/_c83130/getType @0–4` |
| Pre-attack: `E._2ce426._cfe983._02d7ad` | Original Lombok recipe names `EventPreAttackEntity(player,target,distance,hitPos)`. Constructor takes `(target,double,hitPos)` and obtains player through `_433a2f()`. Not cancellable. | `<init>(target,double,hitPos) @0–27`, player `@4–8`; `toString @0–30`; [recovered-original-names.txt](recovered-original-names.txt), recipe/constant-pool offset N/A |
| GUI closed: `E._590f69._1e73d7` | Two screen bridges: old and new screen. | `<init>(screen,screen) @0–14` |
| Screen-init variant: `E._590f69._429bf0$_cfe983` | Screen bridge, inherited from its parent. | `<init>(screen) @0–5`; parent constructor in appendix |

**Correction (Confirmed).** “Chat `(Component,String,int)`” and “pre-attack `(player,target,distance,hitPos)`” describe payloads, not their constructor signatures. The saved descriptors and the actual bytecode distinguish them. Full original JVM class names and all constructor signatures/ranges are retained in the constructor appendix rather than expanded into unreadable obfuscated names in the table.

### Posting hooks and exact locations

**Confirmed.** These producers are in `modern-0.1.0-SNAPSHOT-all-nomappings.jar`; the saved Mixin inventory identifies the target/injection metadata. The aliases below name the Mixin, not the vanilla target class. Complete methods and Code ranges are in [event-hook-bytecode-locations.tsv](event-hook-bytecode-locations.tsv); join its exact class/method with [mixin-event-post-map.tsv](mixin-event-post-map.tsv) for the target and version annotation.

| Target / producer | Mixin alias, method @ Code range | Event relationship |
|---|---|---|
| KeyboardHandler.onCharPress | `ML._d4ca6c._1e73d7._590f69._429bf0.lunar$onCharPress @0–76` | Char event |
| Camera.calculateFov / GameRenderer.getFov version families | `ML._d4ca6c._590f69._21aca6._1e73d7._cfe983.lunar$getZoomLevel$v1_21_2 @0–60`; `…_13ea87._d4ca6c.lunar$getZoomLevel$v1_21_2 @0–68` | Final-FOV variant; hook metadata distinguishes version targets |
| Camera / GameRenderer modifier | Camera Mixin above / `…_13ea87._d4ca6c.lunar$fovModifier @0–30` | Modifier variant; see cancellation finding |
| GameRenderer HUD layer | `ML._d4ca6c._590f69._21aca6._1e73d7._13ea87._d4ca6c.lunar$fireEvent2D @0–89` | Posts unscaled Render2D, scales drawing context, posts Render2D-HUD |
| Gui variant | `ML._d4ca6c._590f69._21aca6._1e73d7._21aca6._1e73d7.lunar$fireEvent2D @0–253` | Alternative 2D producer |
| LevelRenderer | `ML._d4ca6c._590f69._21aca6._1e73d7._13ea87._88f3cf.lambda$lunar$event3D$core$0 @0–17` | Render3D |
| Minecraft tick | `ML._d4ca6c._1e73d7._590f69._a140a8.lunar$preRunTick @0–51` / `lunar$postRunTick @0–14` | Pre and post tick |
| ClientPacketListener player chat | `ML._d4ca6c._590f69._21aca6._2f4182._1e73d7.lunar$onPlayerChat @0–15` | Chat payload; system/legacy-chat variants also in catalog |
| MultiPlayerGameMode attack | `ML._d4ca6c._590f69._21aca6._1e73d7._bb4487._590f69.lunar$clickMouse$eventPreAttackEntityClient @0–38` | Pre-attack |
| Minecraft screen transition | `ML._d4ca6c._1e73d7._590f69._a140a8.impl$event$onGuiClosed @0–16` | Old/new-screen event |
| Screen initialization wrapper | `ML._d4ca6c._590f69._21aca6._1e73d7._21aca6._a140a8.lunar$wrapSetWorldAndResolution$v1_16_1 @0–61` | Screen-init variant |

**Strong inference.** The scaled/unscaled 2D types distinguish coordinate spaces for HUD and other drawing, as traced in [rendering-and-hud.md](rendering-and-hud.md). This static trace does not establish runtime handler order across different Minecraft families.

## 3. Cancellation audit (JV-44, FS-09)

**Confirmed.** Reproducing `session2-tools/canc.py`'s same-method check yields **185 mapped cancellable Mixin post-site rows**: **154** contain `isCancelled` in their producing method and **31** do not. These are rows in the saved map, not necessarily 185 individual bytecode invoke instructions or simultaneously active hooks. Some methods post more than once and version families coexist in the shipped archive.

**Confirmed.** [event-cancellation-audit.tsv](event-cancellation-audit.tsv) retains all 185 rows, event type, Mixin class alias, method Code range, post-call offsets, and whether the method reads `isCancelled`. Representative no-check sites:

| Target / Mixin method | Mixin class | Post @offset / Code range |
|---|---|---|
| SoundManager `lunar$playSoundEvent` | `ML._d4ca6c._1e73d7._590f69._cfe983._590f69` | `18 / 0–24` |
| ClientPacketListener `lunar$handleUpdateAttributes` | `ML._d4ca6c._590f69._21aca6._2f4182._1e73d7` | `28 / 0–32` |
| ClientPacketListener `lunar$handleSpawnObj` | Same as above | `38,58 / 0–62` |
| Camera `lunar$fovModifier` | `ML._d4ca6c._590f69._21aca6._1e73d7._cfe983` | `13 / 0–30` |
| GameRenderer `lunar$fovModifier` | `ML._d4ca6c._590f69._21aca6._1e73d7._13ea87._d4ca6c` | `13 / 0–30` |
| MouseHandler `lunar$onScroll` | `ML._d4ca6c._590f69._21aca6._1e73d7._2f4182` | `33 / 0–84` |
| FogRenderer `lunar$renderDistanceFogColorEvent` | `ML._d4ca6c._590f69._21aca6._1e73d7._13ea87._1253fc` | `11 / 0–48` |
| AbstractContainerScreen `lunar$renderGuiBeforeItems$v26_1` | `ML._d4ca6c._590f69._21aca6._1e73d7._21aca6._590f69._590f69._cfe983` | `16 / 0–20` |

Artifact for this table: `modern-0.1.0-SNAPSHOT-all-nomappings.jar`; raw class names are in the hook appendix. The full audit includes additional tooltip, entity, fog and before/after-container render variants.

**Strong inference, bounded.** Setting only the cancelled flag cannot directly stop the underlying operation through any of those 31 producing methods, since they do not inspect it. **Do not generalize this to “the event has no effect.”** Listeners may still mutate payloads or cause side effects, FOV producers can consume changed values, and downstream consumers have not all been exhaustively checked. Conversely, a same-method `isCancelled` read in the other 154 rows is not by itself proof that every path correctly cancels its vanilla operation.

## 4. Reproduction and limits

**Confirmed analyst procedure.** Run the static helper against the retained scratch index:

```powershell
python session3-tools/verify.py <scratchpad-directory> <research-directory>
```

It reads only `classes.pkl` (the saved analyst disassembly index), the event catalog and Mixin map, and writes derived TSV citations. The central test matches `canc.py`: select cancellable event rows with a Mixin target, select the producing method, and search its text for `isCancelled`. The helper includes all overloads sharing that method name; overloaded-method attribution and indirect cancellation reads are limitations of this deliberately reproduced test.

**Unknown.** Exhaustive semantic names for all 279 types, all inherited-field meanings, listener effects and runtime posting sequences remain open. U-06 is **partially resolved**: structural payload coverage is now available, not a complete behavioral specification.
