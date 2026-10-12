# Session 6 G-01 armor follow-up

This bounded pass resolves the retained list spacing, individual equipment layout, protection aggregation, and custom armor-bar point allocation. It also recovers the alternate vanilla-mode equipment tile dimensions. It does not re-investigate Session 4's headline ARMORSTATUS mechanisms. Evidence is static bytecode from installed artifacts; no Lunar code was executed.

## Scope and identity

G-01 in session5-deepseek/remaining-gaps.md explicitly asks for “ARMORSTATUS full list spacing, individually-positioned equipment, protection-enchantment aggregation, custom bars-layout formula.”

All fresh classes come from C:/Users/Admin/.lunarclient/offline/multiver/lunar.jar, SHA-256 bf36e10e21154263ac16363f8c83bb08cff3a077cb788120954d3625b94a02e9. The evidence-armor/*.json manifests map the stable aliases below to full original obfuscated class names and exact class SHA-256. Each .javap.txt preserves untouched javap -p -c -v output; .aliases.txt is only a name-shortened derivative. L expands to com.moonsworth.lunar.client; ML to com.moonsworth.lunar. Offsets are JVM bytecode offsets within the named method.

| Alias suffix after L._88f3cf._bb4487._21aca6 | Role | Class SHA-256 |
|---|---|---|
| _cfe983 | Root/options | 515041b49c3c84ffab9aa2fd2bed8939e3842157aa573f103d7b815fd79d5d4c |
| _590f69._cfe983 | Protection aggregate child | 054a8e346dba1f5da2e081bed41271d1f91f5d3a21ddae40d6d74a7e322ba44f |
| _cfe983._21aca6 | Custom armor icons child | 35222ad7774e20ab9dd9cb5dd64721da32204a7422a3b9977478dbf075af4b97 |
| _1e73d7._590f69 | Group list HUD | 6e8fe7fa3895887c624d4567021e8cdd2a1c57f9d83dc38d5de58dfd4afb8860 |
| _1e73d7._bb4487 | Alternate vanilla-mode equipment renderer | 6a3e87c5d72cfa9115db85b3605ef9b6b1bdc79ef8531ea21edc4a4552c69b70 |
| _1e73d7._cfe983._21aca6 | Per-equipment child mod | f35703cb9464f90a4fe7b03ada512e3f8958b239dbd233f90e2c274666982fa7 |
| _1e73d7._cfe983._cfe983 | Per-equipment HUD | 34ff1e98981e8b8a69ec679aa4a890e7523eb6c04a6090b6d4a20e9fa2dfc16f |
| _1e73d7._21aca6 | Element dimensions | 94e33ba763d9c8b12311282bf32d18e74e086075c1f068d49c2427d2d0453063 |

## S6-AR-01 — Exact list and element geometry

**High confidence, direct implementation.** Group HUD _1e73d7._590f69 private _cfe983(Collection, matrix, float x, float y) @8–217 chooses vertical iff listMode==VERTICAL. Vertical uses configured durabilityPosition. Horizontal forces LEFT when HUD horizontal anchor is RIGHT, otherwise RIGHT (@31–76).

For element sizes (wi,hi), nonempty vertical list W=max(wi), H=sum(hi)+2(n-1); horizontal W=sum(wi)+2(n-1), H=max(hi). More exactly the accumulator adds its 2-pixel gap only when its current sum is nonzero; a zero-size element is therefore a degenerate exception to the ordinary n-1 form. Final HUD size is (W+4,H+4). Rendering origin is (x+2,y+3) @319–328. Vertical cursor increases hi+2; horizontal cursor wi+2 @488–546.

Vertical X alignment: LEFT durability uses W-wi; RIGHT uses 0; TOP/BOTTOM uses 0 with itemName enabled and (W-wi)/2 otherwise (@407–480). The switch mapping is retained Session 4 evidence L__88f3cf__bb4487__21aca6__1e73d7__590f69__1.short.txt, static initializer @9–64. Background is optional; border is nested inside the background branch (@220–319), so border alone does not draw here.

Element _1e73d7._21aca6.init @4–124 caches item display name only with itemName enabled, durability label through _23f752, and integer-truncated font widths after stripping formatting. Define name width a, durability width b, font height f; N and D indicate nonempty name and durability strings. Null stack yields dimensions (0,0) in public _cfe983(position) @0–17.

For LEFT/RIGHT, _b92d51(boolean left) @9–82 computes m=max(a,b), t=f*(N+D), width=16+(m==0?0:2+m), height=max(16,t). Left durability moves the item to width-16 and right-aligns both text lines within m; right durability puts item at X=0 and both text origins at width-m. Text block Y=round((height-t)/2), durability line Y adds f only if the name is nonempty (@85–188).

For TOP/BOTTOM, _9451b3(boolean top) @9–67 computes r=16+(a==0?0:2+a), q=(D?2+f:0), width=max(r,b), height=16+q. Item X=round((width-r)/2), item Y=top?q:0; name X=itemX+18, name Y=itemY+round((16-f)/2). Durability X=0 and Y=top?3:16 (@70–142). Center rounding is Math.round(float) in _a1dd3a(II) @0–9. These are literal placements, including the asymmetric 3-pixel TOP durability Y.

## S6-AR-02 — Individual equipment is a separate child HUD

**High confidence, direct implementation.** Per-equipment mod _1e73d7._cfe983._21aca6._804335(boolean editor) @0–20 returns parent._cf6cb1(editor).get(its equipment enum). The static factory @0–20 builds a child with an ID derived from the equipment enum name. This is an independently configured HUD object per equipment key, with its own durabilityPosition (default RIGHT), background/border settings, and inherited placement/scale.

Per-equipment HUD _1e73d7._cfe983._cfe983._52e8ee(boolean) @8–105 requires !vanillaMode && moveArmorIndividually && (showWhileTyping || !chatOpen) && element!=null; failure resets its dimensions to zero. Group HUD _1e73d7._590f69._52e8ee @0–111 checks typing first, then vanillaMode returns true; outside vanilla mode moveArmorIndividually zeroes and suppresses the grouped HUD, otherwise it requires a nonempty parent element map.

Individual draw computes the element using its child durabilityPosition @11–26, sets dimensions (wi+4,hi+4) @29–46, draws optional background and nested border @55–154, then draws item at (x+2,y+2.5) @154–190. It saves/restores the shared item renderer Z level @164–197. Default anchor is BOTTOM_RIGHT. load(JsonObject) @5–36 changes durabilityPosition to LEFT when there is no saved placement and current horizontal anchor is RIGHT. Thus the constructor's default RIGHT is not necessarily the effective first-load position.

## S6-AR-03 — Protection estimate uses an integer XOR term

**High confidence, direct implementation; no claim of full Minecraft damage equivalence.** Protection child _590f69._cfe983._cc7511() @126–376 initializes armor sum A=0 and enchant sum E=0. For every nonnull armorValues slot stack, A adds bridge$getArmorValue only when its item bridge$isArmor (@182–206). It then scans the stack enchantment map regardless of that armor test. On the first enchant whose bridge$isProtection is true, let its integer level be l:

    E = (int)((double)E + floor(((6 + l) XOR 2) * 0.75 / 3.0))

The decisive instruction is ixor @286 after iadd @284; this must not be silently translated to a square. The goto @303 breaks this enchant loop after that first qualifying entry. The map's ordering can therefore matter if multiple keys qualify. The exact bridge implementation's accepted protection types was not followed in this bounded pass.

At @315–350:

    P = min(min(E,25) * 0.04f * 0.75f, 0.8f)
    R = 1 - (1 - A*0.04f) * (1-P)

The label is String.format("%3.1f%%", R*100) without an explicit locale (@352–373). For ordinary nonnegative levels, I–IV contribute floor(5/4)=1, floor(10/4)=2, floor(11/4)=2, floor(8/4)=2 respectively. This is a displayed estimate; the method takes no incoming damage parameter. It does not implement a modern damage-dependent armor/toughness calculation.

The optional showArmorToughness branch runs only when MC_VERSION>=6 and its setting is enabled (@17–35), sums armor toughness across armor item stacks (@35–109), and stores a separate float label @116–123. The later R formula does not use that toughness sum. No-player returns early and does not clear cached text in this method.

## S6-AR-04 — Custom armor bar consists of 20 point records and 10 paired icons

**High confidence, direct implementation.** Custom child _cfe983._21aca6 constructor @126–131 allocates 20 tuple slots. Defaults are smartArmorColors=true, showGlint=true, lowDurabilityIndicator=true, threshold=10 with allowed 1–100 (@5–100). Static initializer @0–28 fixes allocation order HEAD, CHEST, LEGS, FEET.

_8ca005 @0–329 clears all slots; if no player it returns. C=min(20,player.bridge$getTotalArmorValue()) @75–89. For each ordered equipment stack it skips null/nonarmor/nonpositive-armor-value stacks, constructs one tuple (material color, showGlint&&enchanted, lowIndicator&&thresholdPredicate), and repeats that tuple once per armor point while total assigned<C (@116–286). Remaining slots below C receive (-1,false,false) @295–325; slots >=C remain null. This handles a bridge total different from the explicitly summed equipment armor values without inventing material ownership.

Public _cfe983(matrix,int iconIndex,int x,int y) @0–94 returns false only when slot0 is null. An icon uses slots 2*i and 2*i+1. If the left slot is null OR equals the right tuple, it draws WHOLE with the left tuple; otherwise LEFT and RIGHT halves separately (@36–90). The draw helper always draws a base icon before returning on a null tuple (@0–17); thus an empty slot can still get its base icon once custom replacement is active. x,y are supplied by the caller; this class does not choose HUD screen coordinates.

Low-warning helper @36–98 modulates packed color alpha with f=0.5+0.5*ML._590f69._5b3f84._79e7e6._d4ca6c(2*pi*(currentTimeMillis%1200)/1200), retaining RGB and integer-truncating the alpha product. The glint overlay receives the same f @114–133. The exact identity of this math bridge and all material color table values were outside this bounded follow-up.

## S6-AR-05 — Alternate equipment tiles use fixed 20-pixel pitch

**High confidence for formulas, bounded for hotbar placement.** _1e73d7._bb4487 private _cfe983(groupHUD,Collection) @116–428 counts retained equipment as n, skipping null stacks only with hideEmptySlots. Base dimensions are vertical (22,2+20n), horizontal (2+20n,22) @275–322. Vertical text scale=1, extraTop=0 and returns @325–342.

For horizontal, let u be the maximum font width of element._23f752(false).key; scale s=1 if u<=20, else .75 if .75u<=20, else .5 (@343–374). ExtraTop=(any nonempty durability label ? round(fontHeight*s):0)+(any stack passes lowDurabilityIndicator && thresholdPredicate ?8:0) @377–425. Outside hotbar anchoring HUD dimensions become (baseWidth,baseHeight+extraTop); render translation is (x,y+extraTop), public draw @36–50,80–93. If hotbarAnchor is enabled and the external hotbar rectangle exists, HUD dimensions are set (0,0) while rendering continues through _590f69(matrix) @20–33,65–77. The latter anchoring method's full game-version placement branches were not modeled here.

Private _cfe983(Collection,matrix) @67–121 gives successive retained items 20-pixel pitch: vertical item origin (3,3+20i), horizontal (3+20i,3). Null slots with hideEmptySlots=false consume a tile and render a 16x16 equipment placeholder if mapped @123–171; populated slots use element rendering and per-item extras @177–199.

## Remaining bounded questions

The G-01 formulas and state gates above are resolved for these exact installed class bytes. Still open: all material-to-color values and texture UV/glint internals of custom icons; full hotbar anchoring across bridge versions; exact bridge$isProtection implementation and possible multi-qualifying enchant map order; saved individual child placement persistence outside these HUD classes; runtime visual parity. No runtime result is implied by static verification.

Reproduction: armor_fresh.py and analysis_helper.py perform read-only jar extraction/disassembly into evidence-armor. Focused method extracts are in evidence-armor/focused-excerpts.json. Existing Session 4 evidence remains intact.
