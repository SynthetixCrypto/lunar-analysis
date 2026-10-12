# Session 6 — G-02 potion follow-up

Date: 2026-10-11. Static-only follow-up to Session 4; no target execution. Scope is the remaining blink curve, inventory cancellation, ordering and three-mode spacing. Existing duration formatting and filter discovery were not repeated. **Confirmed** means class bytecode/annotations; **Strong inference** means branch consequences; **Unknown** means unmeasured/untraced behavior. Offsets are decimal and method-local. Fresh full/aliased javap and class/artifact SHA-256 manifests reside in [evidence-potion](evidence-potion/). Each alias maps to the exact original JVM class in its *.json file. Artifact identities match [reach-combo-findings.md](reach-combo-findings.md). [focused-excerpts.json](evidence-potion/focused-excerpts.json) preserves the decisive full methods.

## S6-PE-01 — blink alpha and text cadence

**Confirmed.** Shared renderer L._88f3cf._bb4487._52e8ee._bb4487._1253fc(effect) @0–70 qualifies blink only when root potionBlink is true, the effect is not ambient, and 0 <= int(duration) <= blinkDuration*20. The threshold includes its upper endpoint. Root constructor potionBlink @255–274 explicitly defaults true; blinkDuration @292–321 defaults 10 with declared range 2–20. No personal setting values were read.

Icon alpha method _d4ca6c(effect) @0–118 returns 1 unless potionBlinkIcon is enabled AND the above predicate qualifies. Otherwise, with d=int(duration) and T=blinkDuration*20:

~~~text
base = clamp(2*d/T, 0, 0.5)
amplitude = clamp((1-d/T)*0.25, 0, 0.25)
alpha = clamp(base + cos(d*pi/5)*amplitude, 0, 1)
~~~

This is directly transcribed from @29–118, using float arithmetic except the double cosine argument. Static math bridge ML._590f69._5b3f84._79e7e6._1253fc(double) carries runtime mapping value="cos", not sin (fresh verbose annotation). Shared icon drawing @15–30 or @91–106 packs int(alpha*255)<<24 | 0xFFFFFF for the modern icon bridge or legacy textured quad. The alpha curve depends on remaining duration ticks, not a separate elapsed-time oscillator.

Duration text has an independent gate in shared _cfe983(hud,effect) @0–109: effectDuration=false hides text; hideAmbientDuration=true plus ambient returns mode!=VANILLA (the exact mode exception must be preserved). Otherwise, if no blink qualifies, show. If blink qualifies, reset renderer field _712e6b to 0 when >20 (@81–92), and show only when counter<=10 (@95–109). Counter increments once per selected-renderer update in _e182e7(list) @0–10, wired by the already documented HUD pre-tick callback. Thus text blinks via a renderer counter; icons fade via remaining duration. Reset is performed during the text draw gate, not in tick. **Strong inference:** this is not a universal exact one-second duty cycle; mode switching, visibility and renderer selection can preserve or delay phase. At ordinary uninterrupted updates and draws it alternates a low-counter visible phase and high-counter hidden phase.

## S6-PE-02 — inventory hooks are concrete cancellable mixins

**Confirmed.** showInInventory is root private setting _2f9a8f; getter _0d4174() @0–4 returns it. In modern jar, two version-family mixins read the same getter directly:

| Alias suffix (under ML._d4ca6c._590f69._21aca6._1e73d7._21aca6._590f69._590f69) | Target / class gate | Hook and result |
|---|---|---|
| _d4ca6c | EffectRenderingInventoryScreen, max=25 | lunar$renderEffects @0–38 cancels HEAD renderEffects$v1_16_1 when module enabled && !showInInventory; hook max=9 |
| _d4ca6c | same | lunar$renderEffectsShifted @0–38 cancels HEAD renderEffects$v1_18_1 / renderEffects$v1_20_0; hook min=10 |
| _13ea87 | EffectsInInventory, min=26 | lunar$renderEffects @0–37 cancels HEAD renderEffects$v1_21_11 / extractEffects$v26_1; hook min=35 |
| _13ea87 | same | lunar$shiftEffectsPanel @0–38 cancels HEAD renderEffects$v1_21_2 / render$v1_21_11 / extractRenderState$v26_1 |
| _13ea87 | same | lunar$checkEffectRendering @166–202 returns false at canSeeEffects HEAD under enabled && !showInInventory |

All listed HEAD injections declare cancellable=true. These are direct Minecraft injection callbacks, not an assumed event-bus producer. Module-disabled and showInInventory=true branches do not perform this potion-based cancellation. Earlier _d4ca6c checkEffectRendering overloads implement the same gate in version-specific visibility/layout hooks; exact bodies and annotations are retained.

Inventory placement additionally interacts with local Apollo InventoryModule presence. The max=9 renderEffects lambda @8–25 cancels when an inventory-button shift is positive and leftPos-124-shift<0. Otherwise @29–41 temporarily subtracts the shift. This is an additional explicit fit guard separate from potion visibility. The min=26 family temporarily adds an inventory shift and undoes it at RETURN. No remote service calls or private behavior were investigated. Actual interception success and callback order remain runtime unknowns.

## S6-PE-03 — ordering

**Confirmed.** NORMAL (_590f69) and MINIMAL (_21aca6) index their input list from zero upward with no renderer-side sort (normal draw @119–138 and @553–556; minimal @267–378). The HUD tick creates that list in the iteration order of bridge$getActivePotionEffects, retaining accepted elements. Therefore those modes preserve the bridge collection's order; a universal alphabetical or duration-order claim would be false without a bridge-order guarantee.

VANILLA (_d4ca6c) update _e182e7(list) @0–172 clears two lists, skips effects whose bridge$shouldShowIcon is false, and splits bad effects into a second list only when vanillaGroupEffects is true and potion object is non-null/isBadEffect (@86–130). When grouping is false, all accepted effects enter the first list. Both lists sort through the same bound comparator (@142–167; BootstrapMethods #0).

Comparator _cfe983(a,b) @0–164, dA/dB=int(duration), ambientA/B=ambient flags:

~~~text
if (dA>32147 && dB>32147) || (ambientA && ambientB):
    compare(b.ambient,a.ambient), then compare(color(b),color(a))
else:
    compare(b.ambient,a.ambient),
    then compare(dB<0,dA<0),
    then compare(dB,dA),
    then compare(color(b),color(a))
~~~

Consequently ambient sorts first; in the ordinary branch negative duration sorts first, then descending duration and color. The long-duration special threshold is exactly 32147 and requires BOTH durations above it. Color helper _88f3cf @0–40 uses bridge$getColor for MC_VERSION>=6; earlier uses static per-potion palette &0xFFFFFF or zero fallback. These are exact comparator conditions, not a generalization from vanilla Minecraft.

## S6-PE-04 — three-mode spacing and geometry

All geometry below is in renderer-local HUD coordinates before the shared HUD scale; k is the configured tiles-per-line integer, n a nonempty list count. The three renderer instances map NORMAL→_590f69, MINIMAL→_21aca6, VANILLA→_d4ca6c through retained HUD enum-switch metadata.

**NORMAL, confirmed.** _590f69 draw @103–108 starts y+3. Effects form a vertical list, row offset=22*i (@546–551). Name/amplifier text sits on the row baseline. Duration baseline adds 10 when either name or amplifier enabled, else 5 (@467–484), and width is still measured when duration is in its blink-hidden phase (@417–430,511–518). Each measured line width includes a 20-unit icon allowance; final width=max(maxMeasuredWidth,20)+7 and height=22*n+2 (@559–574). Optional flip setting swaps LEFT and RIGHT alignment, leaving MIDDLE unchanged (@27–75). Nonmiddle x-origin adjustment is +3 on LEFT, -2 on RIGHT. Text offset helpers: LEFT=20; RIGHT=HUDWidth-lineWithIconWidth; MIDDLE=HUDWidth/2-lineWithIconWidth/2+20. Icon offsets: LEFT=0; RIGHT=HUDWidth-20; MIDDLE=HUDWidth/2-nameLineWithIconWidth/2. The helpers use current HUD width before the final dimension write.

**MINIMAL, confirmed.** _21aca6 draw @0–45 computes padding p=3 unless border enabled, then p=3+2*borderThickness. Origin adds max(0,p-6) on both axes (@47–73). Tile side s=41 when background OR border enabled, else 30 (@139–184). Stride q=s+p (@204–210). Let row=floor(i/k), col=i%k. Ordinary wrapping positions are col*q on the primary axis and row*q on the secondary axis. Horizontal mode uses primary=x; vertical mode primary=y. Reverse wrapping is selected when horizontal mode anchored BOTTOM or vertical mode anchored RIGHT (@93–137). In reverse mode secondary offset=B-row*q, where B=floor(n/k)*q only if n>k, else zero (@220–245); **the source uses n/k, not (n-1)/k**, so exact multiples above one line retain the extra reverse-origin step.

MINIMAL dimension helper @0–81 defines lines=floor((n-1)/k)+1, columns=min(n,k), primary=s+(columns-1)*q+p-3, secondary=s+(lines-1)*q+p-3; swaps them for vertical mode. Duration is centered at x+s/2-textWidth/2 and y+s-s/3+1; icon origin is x+s/2-9.5, y+s/2-13 (tile helper @52–143).

**VANILLA, confirmed.** _d4ca6c draw @67–155 sets group line counts r1=ceil(n1/k), r2=ceil(n2/k) via helper _6fc5d5=(n+k-1)/k @0–7. Primary extent W=27*max(min(n1,k),min(n2,k))-3; secondary extent H=27*(r1+r2)-3. Horizontal dimensions=(W,H), vertical=(H,W), @157–190. Both lists empty yields dimensions zero and return @0–30. First group starts at secondary line 0, second at line r1 (@207–247); tiles have 27-unit stride and 24-unit extent, i.e. 3-unit gaps. Group iteration helper @14–70 computes within-line i%k and line floor(i/k), with each line's actual item count to align a short last line.

For horizontal mode, helper _cfe983(hud,horizontal,index,lineCount,W) @0–86 lets lineWidth=27*lineCount-3 and A=lineWidth for LEFT, (W+lineWidth)/2 for MIDDLE, W otherwise. Primary offset=A-24-27*index: fill right-to-left within each aligned line. Secondary offset=27*(groupLineStart+row). For vertical mode @87–157, A=0 for TOP, (W-lineWidth)/2 for MIDDLE, W-lineWidth otherwise; primary offset=A+27*index and secondary uses the same group-line offset. The input lists are sorted as above before this geometric placement.

## Disposition and boundaries

G-02's named remaining items are **resolved in the retained renderer and modern inventory families**: three outer layout/spacing formulas, exact renderer ordering, icon alpha/text blink mechanisms, and cancellable inventory hooks. Remaining unrelated limits: live bridge collection order for NORMAL/MINIMAL, runtime injection/ordering behavior, selected version, and every internal vanilla icon/text scaling/position option were not exhaustively modeled. No target binaries, credentials, personal profiles, network services or protection mechanisms were accessed/executed. Further work should not repeat these formulas; use them when drafting the independent client specification, with explicit design decisions where Lunar's quirks are undesirable.
