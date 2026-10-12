# TOGGLE_SNEAK and REACH_DISPLAY — static traces

Artifact: `lunar.jar`; no target execution. **Confirmed** = bytecode path, **Strong inference** = conditional interpretation, **Unknown** = remaining scope. Decimal offsets are method-local. Original JVM identities and aliases: [full-name-mappings.json](evidence-modules-b/full-name-mappings.json). Complete/verbose disassemblies and bounded references: [evidence-modules-b](evidence-modules-b/). Shared feature persistence/HUD framework is reused from session 3.

## TOGGLE_SNEAK — S4-MOD-03

### Root versus HUD child

**Confirmed.** Root is `L._88f3cf._bb4487._91398c._590f69`, **not** `_cfe983` (the latter is a display-state enum). Root `getId @0–2` returns TOGGLE_SNEAK. `_0e0872 @0–11` creates child `_21aca6`, ID TOGGLE_SNEAK_HUD_CHILD (`child.getId @0–2`), which holds rendering/labels. Root runtime booleans sneak/sprint/flying and timing fields are distinct from stored options and the child’s display text.

Root constructor `@5–195` declares toggleSprint default true; toggleSneak and sprint/sneak key override options; keybindSprint/keybindSneak; toggleSneakContainer; flyBoost default true; flyBoostAmount default 4, range 2–8; doubleTap default true. Explicit true/default/range are constructor constants, not installation values. `@210–255` binds keyboard, screen/container, player capability and mouse events; one extra tick callback is installed only for a specific version enum (`@258–276`), whose human-readable version is not asserted here.

### Tap/hold logic and key-state side effects

**Confirmed.** Root `_cfe983(inputAction,key) @0–396` rejects input without the relevant context/with another module gate (`@0–22`). Current-screen branch resets timers/held sprint marker and selectively preserves container sneak behavior (`@23–69`). DOWN stores wall-clock press time when matching enabled toggle key (`@70–145`). Non-DOWN clears held-sprint marker and, while not flying, toggles sneak if elapsed **<=200 ms** (`@191–281`); sprint uses **<=400 ms** (`@304–394`). Longer holds do not take those toggle branches. These are wall-clock thresholds, not game-tick counters or fixed double-tap periods.

On ordinary version path the method calls `_cfe983(keybind,state)`, which writes **both** `bridge$setKeyBindState @2` and `bridge$setKeyBindPressed @9`. Special version instead clears a one-shot synchronization flag, with tick callback `_21aca6(_3a14e3) @0–58` applying the stored toggle once. Keyboard/mouse event wrappers feed the shared input method; when it reports handled they can cancel the input event. Cancellation of a producer’s original operation requires that producer to honor the event flag; this report does not extend the session-3 bounded cancellation audit to every version.

**Confirmed.** Flight callback `_cfe983(_00e05b) @0–347` reads capabilities, checks creative/spectator paths and enabled boost/key condition, captures/restores base fly speed, sets boosted speed, and adjusts vertical motion for sneak/jump. This is behavior-changing client input code, not just a label HUD. No flight permissions or server acceptance are inferred. Exact motion multiplication and all permission branches are **partial**, despite full evidence retention.

### Display states and settings

**Confirmed.** Child constructor `@18–119` declares iconMode, custom sprintingText/sneakingText/flyingText, showRidingText default true and descendingText default true. It links parent trait and custom renderer (`@122–160`). Renderer `L._88f3cf._bb4487._91398c._21aca6$_cfe983.getText @0–…` samples flying/riding/physical-held keys/toggle state, then selects enum states and composes main/partition labels. Its source override keys include flying, riding, holdingSneak, holdingSprint, sneak, sprint; they are distinct inputs to the display, not all fields persisted on disk.

Display enum `L._88f3cf._bb4487._91398c._cfe983` declares FLYING, FLYING_BOOST, RIDING, DESCENDING, DISMOUNTING, SNEAKING_TOGGLED/HELD, SPRINTING_TOGGLED/HELD/VANILLA and HELD/TOGGLED/VANILLA (`<clinit> @0–224`). `getMainText(child) @0–111` prefers non-empty custom text only for matching sprinting/sneaking/flying main categories; otherwise localizes. `getPartition(args) @0–39` returns empty when absent or required boost arguments missing. Presence of an enum constant is not evidence every state is reachable on every version.

### Persistence and status

Options and child HUD position use shared typed-setting serialization. Runtime key state/timers/booleans are not shown as independently serialized. **Partial:** root/child distinction, input thresholds, state-writing bridge and display categories resolved; exact fly-speed/motion formula, all special-version sync/reset paths and every producer’s cancellation remain open. `event-producers.json` is an **empty bounded search result**, not proof there are no producers. Preserve that search limitation.

## REACH_DISPLAY — S4-MOD-04

### Settings and event chain

**Confirmed.** Root `L._88f3cf._bb4487._327414._cfe983.getId @0–2` returns REACH_DISPLAY. Constructor declares reverseOrder, hideZero, highlightAttackablePlayers and attackablePlayersHighlightColor (`@5–74`), installs generic text HUD and registers entity-status, reset-clock and attack-distance events (`@110–143`). Its tracked values are target entityId, candidate distance, sentTime, displayed distance and a reset-phase Boolean. sentTime is assigned from player bridge integer `_0be1fc`, widened to long: it is **not System.currentTimeMillis**.

Attack callback `_590f69(_02d7ad) @0–40` captures entity ID, event.getDistance and current player counter. Status callback `_cfe983(_c8175c) @0–64` requires status byte **2**, matching ID, and counter delta **<=4**; then:

`displayDistance = min(player.bridge$entityAttackRange(), capturedDistance)` (`@45–61`).

No lower-bound check on delta and no arbitrary raytrace-distance recalculation appears in this callback. **Strong inference:** distance is a correlated/clamped display sample, not an independently authoritative server-reported reach. Exact geometric distance production and the bridge counter’s original Minecraft field remain **Unknown in this report**; naming a four-tick/200-ms timeout without that mapping would overstate evidence.

### Reset, label and highlighting

**Confirmed.** `_bb4487(_1eb51c) @0–56` returns while player exists and delta<80; after that/without player, it zeroes display only if the reset phase is true, then flips phase. This is event-driven, alternating cleanup—not a scheduler firing exactly 80 ticks later. No new successful attack necessarily resets this phase in the shown capture callback.

Label `_e93d3c(boolean) @0–86` returns null for hideZero and displayed value exactly zero; formats value with static DecimalFormat `#.##` using **Locale.ENGLISH** (`<clinit> @0–22`); reverseOrder changes localized label/value placement, not sample arithmetic. Generic HUD framework owns text measurement/background/border/global scale; no second module-specific scaling pipeline is established.

Highlight predicate `_590f69(playerModel) @0–105` requires effective module enabled, option true, model/player/pointed target available, candidate not local player, auxiliary suitability predicate allowing it (Hypixel-specific parameter), and UUID equality with the pointed entity. `_78e403 @0–4` exposes highlight color. It is not an all-player unconditional tint.

### Persistence and status

Typed display options/color and generic HUD geometry use shared persistence; last target/distance/counter are ordinary runtime fields, not an established private file format. **Partial:** settings, sample/status correlation, clamp, reset and label/highlight conditions resolved. Next static steps: follow actual attack-event producer for getDistance’s geometry; identify `_0be1fc` implementation and `_1eb51c` producer timing; confirm highlight consumer. Bounded reference files are aids, not executed observations or whole-program guarantees.
