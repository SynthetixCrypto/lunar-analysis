# ARMORSTATUS and POTION_EFFECTS — static traces

Artifact: `lunar.jar`. **Confirmed** means bytecode implementation, not observed execution. **Strong inference** means a consequence conditional on inputs; **Unknown** marks remaining coverage. Aliases resolve to actual JVM identities in [class-map.tsv](evidence-modules-a/class-map.tsv). Retained full/verbose dumps are authoritative; `short.compact.txt` files are reading aids that omit descriptors/constant-pool indices. Offsets below are decimal, local to the named method. Shared persistence/HUD algorithms were resolved in session 3; only module-specific wiring is added here.

## ARMORSTATUS — S4-MOD-01

### Identity, settings and child graph

**Confirmed.** Root `L._88f3cf._bb4487._21aca6._cfe983.getId @0–2` returns ARMORSTATUS. Constructor `@5–822` declares typed settings and installs its rendering helper; examples of shipped defaults, **not personal values**:

| Setting | Default | Constructor offsets |
|---|---|---|
| itemName / itemCount | false / true | 5–46 |
| showWhileTyping / moveArmorIndividually | false / false | 49–90 |
| textShadow / damageOverlay | true / true | 93–134 |
| itemDamage / armorDamage | true / true | 137–178 |
| maxDamage / hideUnbreakableDurability | false / true | 181–222 |
| durabilityPosition / listMode / damageDisplay | RIGHT / VERTICAL / VALUE | 225–276 |
| background / border | false / false | 279–320 |
| borderThickness | 0.5; range 0.5–3 | 323–353 |
| vanillaMode / hotbarAnchor / hotbarPosition | false / true / LEFT | 424–483 |

`_0e0872 @0–101` builds protection child (`_590f69._cfe983`), bars child (`_cfe983._21aca6`) and per-equipment children. OFF_HAND_HELD_ITEM is omitted for `MC_VERSION<5 @44–59`; children are indexed in a Map `@77–90`. This is a compound feature, not a single text HUD. Settings UI method `_cfe983(settings) @0–54` groups GENERAL/HUD/damageOptions/COLOR. Later color/threshold and equipment settings remain in the full constructor, not exhaustively tabulated here.

### Update and source selection

**Confirmed.** Root constructor `@786–803` registers helper.update as Runnable against event `L._d4ca6c._cfe983._2ce426._3a14e3`; verbose BootstrapMethods #0 binds that exact method. Helper `L._88f3cf._bb4487._21aca6._1e73d7._cfe983.update @0–172` clears live elements, marks editor cache dirty, and returns if player absent. It iterates enabled equipment children, resolves a stack, and keeps absent/invalid stacks only on the vanilla-mode branch (`@98–118`). Element construction is per-update, not accumulated forever. `_252625(false) @0–8` returns live map; `_252625(true) @9–29` lazily builds the preview map once per dirty cycle using `_89eec3 @0–176`, with synthetic item fallback. Preview contents are not live inventory observations.

Stack resolver `_cfe983(player,equipment) @0–73`: held item through `bridge$getCurrentEquippedItem`; offhand through `bridge$getEquipmentInSlot(OFFHAND)`; armor through inventory list. For `MC_VERSION>=29`, armor index becomes `3-slotId @31–45`; earlier versions use slotId unchanged. Correct slot ordering is explicitly version-sensitive.

### Durability math and rendering

**Confirmed.** Element `L._88f3cf._bb4487._21aca6._1e73d7._21aca6._23f752(boolean) @0–249` chooses armor/item damage visibility, requires damageability, and honors hideUnbreakableDurability. It computes:

`remaining = maxDamage - itemDamage`

`remainingPercent = (remaining * 100) / maxDamage` using integer multiplication/division (`@109–139`), **not floating point rounding**. VALUE/PERCENT/NONE switch `@141–233` produces text, with optional max suffix in VALUE. The color selector root `_920490 @0–80` uses inclusive thresholds 10, 25, 40, 60, 80 percent, unless a fixed-color mode selects the high/full color immediately. Separate threshold predicate root `_cfe983(stack,int) @0–54` guards `maxDamage>0` before the same integer ratio. The element’s denominator guard depends on bridge damageability contracts rather than an explicit local max>0 check.

Element renderer `_cfe983(matrix,itemRenderer,x,y) @0…` composes item, name and durability subcalls; `_21aca6(matrix,itemRenderer,x,y) @0–…` invokes `bridge$renderItemAndEffectIntoGUI @20`. Overlay helper `L._88f3cf._bb4487._21aca6._1e73d7._1e73d7._cfe983(matrix,stack,x,y)` computes damage fraction `itemDamage/maxDamage @51–66`, bar width `round(13-13*fraction) @68–82`, and remaining-color component `round(255-255*fraction) @84–98`, then draws bar rectangles. Legacy branches explicitly toggle GL state. Item-count rendering is a separate helper invocation; global HUD scaling/position remains the previously recovered framework.

### Persistence and remaining work

**Confirmed scope.** Root/children declare typed settings and HUD traits consumed by the existing shared serialization lifecycle. No new private file write or module-specific persistence format is established here. The report does not read saved equipment/settings. **Partial:** live source, preview separation, child graph and durability/overlay math are recovered; exact full list spacing, individually positioned equipment, protection enchantment aggregation and custom bars-layout formulas still need a focused pass through retained helpers. Full helper dumps exist; retention alone does not make those branches resolved.

## POTION_EFFECTS — S4-MOD-02

### Identity and mode-specific options

**Confirmed.** Root `L._88f3cf._bb4487._52e8ee._1253fc.getId @0–2` returns POTION_EFFECTS; constructor `@802–814` installs HUD `L._88f3cf._bb4487._52e8ee._1e73d7`. Earlier constructor declares potionEffectsMode; minimal/vanilla horizontal/tiles-per-line options; names/duration/amplifier; inventory/chat visibility; blinking and blink duration; text/background/border/color controls; durationPosition/amplifierPosition and vanilla icon/text scale; infinite-effect exclusion. See [root compact dump](evidence-modules-a/L__88f3cf__bb4487__52e8ee__1253fc.short.compact.txt) for constructor offsets per key. No unverified universal defaults are asserted.

`_0b03da @0–415` creates ID→Boolean exclusion settings: legacy IDs 1–23, then version-gated newer IDs including glowing/levitation/luck, slow-falling/conduit/dolphins, dark/omen/trial effects, and `excludeBreathOfTheNautilus` only when `MC_VERSION>=35 @359–375`. HeroOfTheVillage ID is 31 or 32 based on version `@266–284`. This proves version-specific numeric mapping, not a stable cross-version registry identity for every effect. UI exclusion entries are sorted after registration `@375–415`.

### Tick, filters and editor behavior

**Confirmed.** HUD constructor `@61–73` registers Runnable tick against event `_d4ca6c._cfe983._2ce426._3a14e3`. `tick @0–115` clears effects each invocation, reads player `bridge$getActivePotionEffects @18`, rejects effects when root `_13ea87(effect)` is true, and adds static editor examples only when list empty and framework editor predicate true (`@74–103`). It then updates the selected renderer. No independent scheduler is shown.

Root `_13ea87 @0–67` excludes infinite effects if its option enabled or excludes by per-ID setting. `_2ce426(effect) @0–45` defines infinite-like duration: on `MC_VERSION<=5` the bridge max-duration flag qualifies; any version duration `-1` qualifies; duration **greater than 72000** qualifies. Exactly 72000 alone does not. These are duration units returned by the bridge, with rendering later dividing by 20.

HUD `_52e8ee @0–108` suppresses its custom HUD when hidePotionStatus is true (`@0–26`), suppresses while chat open unless allowed (`@27–80`), accepts editor request (`@81–86`), otherwise requires a non-empty filtered list. Suppression zeroes dimensions. Inventory integration is separate from this custom HUD gate; no blanket claim that an empty list means the entire vanilla inventory view is disabled.

### Renderer and duration formulas

**Confirmed.** HUD `_96ad72 @0–74` selects three renderer instances `_590f69`, `_21aca6`, `_d4ca6c` by mode. Draw `_cfe983(event,x,y,editor) @0–18` passes matrix/list/origin to the selected implementation. Shared renderer `L._88f3cf._bb4487._52e8ee._bb4487` handles icon bridge, text, amplifiers, colors and timing. Icon method `_cfe983(matrix,effect,potion,x,y)` uses effect icon bridge on its version branch (`@30`), otherwise status-index texture coordinates. JVM/LWJGL calls are evidence of implementation only; none was executed.

Shared duration `_1e73d7(effect) @0–179`:

- VANILLA: infinite-like → `?`; otherwise `seconds = int(duration/20)` (`@30–40`). At least 3600 seconds → integer hours; at least 600 → integer minutes; at least 60 → minutes and zero-padded seconds; less → integer seconds (`@41–116`). Exact concatenation suffixes are in verbose BootstrapMethods, not inferred from the short dump.
- Other modes with minute-format option: infinite-like → `**:**`; otherwise truncate duration/20 to long, multiply by 1000 and pass to formatter (`@117–169`).
- Otherwise delegate to version bridge formatter (`@170–179`).

Amplifier `_bb4487(effect)` maps normal levels to Roman numeral branches (II–X in retained dump), with a fallback beyond the small switch. Color `_cfe983(effect,potion)` uses bridge color/per-ID palette/bad-effect branch. Palette helper `_52e8ee._cfe983.<clinit> @0–358` builds immutable ID→color constants for IDs 1–27; it is not personal color storage.

### Persistence and remaining work

Typed options and HUD geometry use the shared settings lifecycle, not an established new potion file. Current active effects and synthetic editor samples are distinct from stored settings. **Partial:** update/filter/version rules, mode routing, duration conversion and icon/text boundaries resolved; exhaustive three-mode tile spacing, ordering, blink alpha curve and inventory-hook cancellation remain open. Next work should target those branches and producer annotations, not repeat effect-setting discovery.
