# COMBO and PACK_DISPLAY — static traces

Artifact: `lunar.jar`. **Confirmed** = bytecode path; **Strong inference** = conditional consequence; **Unknown** = unresolved coverage. Decimal offsets are method-local. [class-manifest.jsonl](evidence-modules-c/class-manifest.jsonl) maps aliases to actual JVM identities; [evidence-modules-c](evidence-modules-c/) retains full/verbose dumps and references. No code was executed, selected pack names were not read from personal settings, and texture loading is described from code only.

## COMBO — S4-MOD-05

**Confirmed.** Root `L._88f3cf._bb4487._429bf0._cfe983.getId @0–2` returns COMBO. Constructor `@5–38` installs generic text HUD anchored TOP_RIGHT, with factory dimensions tuple `(10,18,22,46,56,62)`; these tuple numbers are not reinterpreted as actual screen coordinates. `@42…` registers tick/hurt reset, entity-status and reset-clock callbacks, with verbose lambda bindings. No module-specific settings constructor is shown beyond inherited HUD options.

### Count and reset

Tick helper `_c817d8 @0–28` gets player; if present and `bridge$wasJustHurt` true, sets combo=0. Status helper `_cfe983(_c8175c) @0–36` accepts entities implementing the retained living-entity bridge, gets local player and uses last-attacker Optional. Lambda helper `_cfe983(status,player,attacker) @0–58` requires **reference identity** between Optional attacker and status event entity (`@0–8`), then samples `bridge$getLastAttackerTime`.

If timestamp differs from saved `_af72c5`, it stores timestamp **before** freshness test (`@17–29`). It increments only when `abs(timestamp - player._0be1fc()) <= 4 @32–55`. Identical timestamps cannot increment twice through this path. The method does **not** visibly test status byte==2, unlike REACH_DISPLAY; do not import that guard from the adjacent module. This records a specific bridge/event correlation, not proof of generic “every successful hit increments.” Bridge semantics and producer freshness require further mapping.

Reset handler `_bb4487(_1eb51c) @0–68`: absent local player returns unchanged; present last attacker with player counter minus attacker time <80 also returns; otherwise it clears combo only when reset-phase flag true, then toggles that flag. No timer/sleep exists. **Strong inference:** stale/no-attacker cleanup can occur on every other eligible reset event, not exactly 80 ticks/4 seconds on a timer. Java int subtraction/Math.abs also prevents a universal arithmetic-overflow-free claim.

### Render/persistence/status

Label supplier `_e93d3c(boolean) @0–54` calls inherited `_590f69("combo",currentCount)` override hook, then chooses localized noCombo for zero or combo label with integer argument. Rendering is shared text HUD, not a native/WebOSR widget. Runtime count/timestamp/reset flag are ordinary fields; no independent combo persistence file is established. **Partial:** count correlation, deduplication and reset paths resolved; actual Minecraft implementation of attacker/time/counter and event production/ordinary UI settings need narrower corroboration. No observed runtime correctness claims.

## PACK_DISPLAY — S4-MOD-06

### Options, update and child

**Confirmed.** Root `L._88f3cf._bb4487._59b0c6._cfe983.getId @0–2` returns PACK_DISPLAY. Constructor `@5–298` declares packIcon default true, packDescription, packExtension, packOrder default FIRST, titleReplacement, textColor, descriptionReplacement, descriptionReplacementColor, moveTitleDown and keepBold/Italic/Underline/Strikethrough/Obfuscated. It installs custom HUD `_cfe983$_21aca6`, captures default-pack thumbnail fallback and registers pack-update handling. Exact option defaults beyond those explicit constants are retained, not guessed.

Transition `_41ba55(true) @4–14` refreshes selected resource pack; false returns without equivalent clearing. Pack-update callback `_cfe983(_02d7ad)` delegates payload to refresh; changing packOrder also refreshes. `_0e0872 @0–11` adds child `_59b0c6._21aca6`; the child’s entire purpose/layout is not fully resolved here.

Refresh `_21aca6(pack) @0–73` with packOrder==FIRST gets all selected packs, and if nonempty uses **last list element** (`@13–49`), not index zero. It rebuilds thumbnail, description lines and retained pack reference (`@50–70`). **Strong inference:** FIRST refers to display/pack-priority semantics and cannot be interpreted as first returned list item. The bridge’s ordering contract remains Unknown.

### Texture and description boundary

Thumbnail `_590f69(pack) @0–52` asks bridge for Optional image, converts BufferedImage via version bridge and registers dynamic texture under `pack-display-thumbnail @39–42`; empty image uses cached default texture. Constructor default-image branch logs failure and registers `default-pack-display-thumbnail`. This proves Java/Minecraft texture-manager usage, **not** a native WebOSR paint path. The shown refresh does not explicitly destroy the previous dynamic texture; lifecycle/replacement behavior inside texture manager is Unknown.

Description `_1e73d7(pack) @0–89`: null pack or name `textures` uses localized defaultDescription; otherwise bridge$getDescription can return null or throw IOException (caught→null); successful rich text is wrapped to **256** units by font bridge (`@57–64`), mapped to strings and materialized. This is source-derived schema/control flow, not personal pack content. Null safety in thumbnail assumes supplied pack non-null; description’s null branch does not establish that all refresh entry points safely accept null.

### Title, formatting and draw

Custom HUD `L._88f3cf._bb4487._59b0c6._cfe983$_21aca6._cfe983(event,x,y,editor)` obtains pack name, normalizes textures/vanilla to localized default (`@78–…`), and if packExtension disabled removes `.zip` via **String.replace** (`@164–168`), not suffix-only stripping. It measures strings through font bridge, lays out icon/title/description and draws text; description rows are advanced within the same render method. Generic framework owns position/global scale.

Formatting helper `_2ce426(String,isDescription) @0–239` separately strips **lowercase** `§l/§o/§n/§m/§k` when their keep options are false (`@0–184`). Those are literal replacements, not a case-insensitive formatter. Selected FULL replacement mode strips color codes using root regex `(?i)§[0-9A-F]` (`@185–237`; root `<clinit> @0–8`). It does not universally strip every formatting/reset code: regex omits `§r`, and style stripping obeys its own flags. Exact FULL/PARTIAL/NONE modes are declared in retained enum; do not treat enum presence alone as exhaustive mode semantics.

### Persistence and remaining work

Options and HUD geometry use shared typed-setting persistence, not a new private pack database established by this trace. Dynamic texture, retained pack reference and description list are runtime/cache state. **Partial:** update/order selection, texture boundary, text wrapping and formatting resolved; full custom width/height formula, child HUD role, specialized mode color propagation, reload producer sequence and texture teardown remain open. Next useful work is these narrow helper/bridge paths, not resource-pack file contents or already-completed global HUD math.
