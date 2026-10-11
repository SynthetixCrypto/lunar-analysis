# Additional static module traces: Coordinates, Keystrokes and Waypoints

Study date: 2026-10-11. Scope: read-only bytecode study; no Lunar JAR, JavaScript, native library or other target code execution; no installation changes, credential reads, user settings values, anti-cheat/integrity investigation, dynamic testing or reimplementation.

## Evidence conventions and boundaries

- **Confirmed — provenance:** the supplied analyst `q.py` reads the existing `classes.pkl` disassembly index and prints class/method text; `idx.py` identifies `lunar_moonsworth.javap` as its first input. Both scripts were inspected before querying. Source: supplied scratchpad `q.py:1–45`, `idx.py:19–24`; analyst scripts, not target classes; javap offset **N/A**.
- **Confirmed — artifact locator:** the prior artifact inventory identifies `C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar`. All target citations below refer to this artifact's retained `lunar_moonsworth.javap` text, accessed through the supplied index. Source: `artifact-index.tsv:387`; class/method/offset **N/A** for inventory metadata. No fresh artifact hash or target execution was performed in this pass.
- **Confirmed — naming convention:** `L.` abbreviates `com.moonsworth.lunar.client.`, `ML.` abbreviates `com.moonsworth.lunar.`, and each `_xxxxxx` is the first six hexadecimal characters of the MD5 of its original 30-character obfuscated segment. Source: analyst `q.py:4–27`; javap offset **N/A**. Full JVM class locators are retained in [session3-class-locations.tsv](session3-class-locations.tsv). This is a locator convention, not a claim of original source names.
- **Confirmed — citation convention:** `@a–b` denotes javap instruction offsets in the named method, not file-line numbers or addresses. In tables, the class label expands using the following locator table; every row inherits artifact `lunar.jar`.

| Locator | Class alias |
|---|---|
| `Coordinates` | `L._88f3cf._bb4487._a140a8._1e73d7` |
| `CoordinatesHUD` | `L._88f3cf._bb4487._a140a8._1e73d7$_cfe983` |
| `BiomeService` | `L._ba7d98._590f69._d4ca6c` |
| `Keystrokes` | `L._88f3cf._bb4487._dd3308._590f69` |
| `Key` | `L._88f3cf._bb4487._dd3308._21aca6._cfe983` |
| `KeyHUD` | `L._88f3cf._bb4487._dd3308._21aca6$_cfe983` |
| `KeyLayout` | `L._88f3cf._bb4487._dd3308._21aca6._21aca6` |
| `Waypoints` | `L._88f3cf._bb4487._8c4693._590f69` |
| `WaypointManager` | `L._02d7ad._1253fc._81676d` |
| `WaypointGroup` | `L._88f3cf._bb4487._8c4693._21aca6` |
| `WaypointRenderConfig` | `L._88f3cf._bb4487._8c4693._1e73d7` |

Framework reference: [rendering-and-hud.md](rendering-and-hud.md), particularly JV-18–20. This report describes module-specific static paths, not a second verification of every shared HUD/framework detail.

## JV-47 — Coordinates

### Construction and static defaults

All values in this section are shipped bytecode constants, **not values read from a user's settings file**.

| Classification | Observation | Class / method @javap offset |
|---|---|---|
| **Confirmed** | Module constructor passes `true` to the feature base; `getId()` returns `COORDINATES`. | `Coordinates.<init>() @0–2`; `getId() @0–2` |
| **Confirmed** | Boolean defaults: `showWhileTyping=true`, `textShadow=true`, `background=true`. | `Coordinates.<init>() @18–81` |
| **Confirmed** | `border=false`, `moveChildrenIndividually=false`, `decimalCoordinates=false`: those builders do not override their initial false value. | `Coordinates.<init>() @84–96,225–252`; `L._ec7e36._cfe983._cfe983._cfe983.<init>(String) @5–10`, `_1d4eda() @0–1` |
| **Confirmed** | `borderThickness=0.5`, range `[0.5,3]`; background color integer `0x6F000000`; border color integer `0x9F000000`; `mode=VERTICAL`. | `Coordinates.<init>() @99–193` |
| **Confirmed** | Creates `copyCoords` control and six children with preview text: X=`500`, Y=`62`, Z=`250`, C=`92/4269`, Biome=`Plains`, Direction=`N`. | `Coordinates.<init>() @196–222,255–348` |
| **Confirmed** | Child enumeration order is X, Y, Z, C, Direction, Biome, although construction creates Biome before Direction. | `Coordinates._0e0872() @0–27` |
| **Confirmed** | Parent HUD returns inactive when children are moved individually; when `showWhileTyping` is false, it also returns inactive while chat is open. | `CoordinatesHUD._52e8ee(boolean) @0–62` |

### Data-to-display and clipboard paths

| Classification | Trace / result | Class / method @javap offset |
|---|---|---|
| **Confirmed** | X supplier uses player `bridge$getPosX`; Y supplier uses `bridge$getBoundingBox().bridge$getMinY`; Z supplier uses `bridge$getPosZ`. Each calls the same string formatter. | `Coordinates._865f6b() @0–12`, `_ec6c75() @0–17`, `_60d5af() @0–12` |
| **Confirmed** | **Decimal mode is truncation, not floor:** for ordinary finite coordinate values it evaluates `(int)(value*100)/100.0`, then `String.valueOf(double)`. `d2i` is explicit at offset 21. This is not fixed two-decimal formatting. | `Coordinates._133367(double) @0–32` |
| **Confirmed** | Non-decimal supplier formatting uses mathematical floor for ordinary finite coordinate values; helper casts to int and subtracts one when the original value is less than the cast result. | `Coordinates._133367(double) @33–40`; `L.util._6247d7._ef5392(double) @0–17` |
| **Confirmed** | C supplier obtains unculled and maximum render counts from the level renderer, passing unculled first to the concatenation site. | `Coordinates._c2a530() @0–37` |
| **Confirmed** | Direction lookup table is N, NE, E, SE, S, SW, W, NW. Index is `floor(((wrap(yaw)+180+22.5)%360)/45)`. | `Coordinates._7e956b(float) @0–82`; floor helper `L.util._6247d7._ef5392(double) @0–17` |
| **Confirmed** | Grouped HUD obtains yaw from the render-view entity; if that entity is absent it falls back to the player. X/Y/Z here also use `posX/minY/posZ`. | `CoordinatesHUD._cfe983(Render2D,float,float,boolean) @47–197` |
| **Confirmed** | Biome service subscribes to tick; it resolves a known bridge biome enum or obtains the biome name, builds a localization-key candidate and invokes localization. If the resulting string contains `:`, it takes the suffix, replaces underscores with spaces and applies `capitalizeFully`; otherwise it retains the returned string. | `BiomeService.<init>() @19–28`; `lambda$new$0(Tick) @0–166`, especially `@22–147` |
| **Confirmed** | Clipboard handler formats `X: %s Y: %s Z: %s` from **integer casts** of `posX`, **posY**, `posZ`, calls the clipboard helper and requests the toast `Copied coordinates to clipboard!`. The clipboard path does not use the decimal setting or the HUD's `minY` supplier. | `Coordinates._76bef3() @16–90`; control callback registration `_cfe983(SettingsBuilder) @48–60` |
| **Unknown** | The meaning of the clipboard handler's early feature-state guard was deliberately not expanded. | `Coordinates._76bef3() @0–15` |
| **Unknown** | This pass does not establish whether every grouped numeric formatting branch exactly matches the separate-child formatter; the truncation finding above is specifically verified for `_133367(double)`. | `CoordinatesHUD._cfe983(drawCtx,double,double,double,float,int,int,float,float,boolean) @331–344` (layout branch); separate-child formatter `Coordinates._133367(double) @0–40` |

## JV-48 — Keystrokes

### Recovered settings, including previously clipped constructor details

| Classification | Static default / type / bounds | Class / method @javap offset |
|---|---|---|
| **Confirmed** | Module disabled by default; id `KEYSTROKES`; `keystrokesMode=GROUPED`. | `Keystrokes.<init>() @0–33`; `getId() @0–2` |
| **Confirmed** | `keyStrokesClicks=true`, `keyStrokesMovement=true`, `keyStrokesSpacebar=true`. | `Keystrokes.<init>() @36–55,88–129` |
| **Confirmed** | `leftCPS`, `rightCPS`, `useArrows`, `textShadow`, `border`, `innerBorder` all default false. | `Keystrokes.<init>() @58–85,132–189`; Boolean builder `L._ec7e36._cfe983._cfe983._cfe983._1d4eda() @0–1` |
| **Confirmed** | `borderColor` and `textColor` are integer `0xFFFFFFFF`; `textPressedColor=0xFF000000`; `backgroundColor=0x6F000000`; `backgroundPressedColor=0x6FFFFFFF`. | `Keystrokes.<init>() @192–302` |
| **Confirmed** | `boxSize` float `18 [10,32]`; `borderThickness` float `1 [0.5,3]`. | `Keystrokes.<init>() @305–367` |
| **Confirmed** | `keyFadeDelay` long `75 [0,500]`; renderer passes it to `setDurationMs`, establishing milliseconds. | `Keystrokes.<init>() @370–401`; `KeyHUD._2ce426(drawCtx) @186–238` |
| **Confirmed** | `spacebarThickness` float `1 [1,4.25]`; `animate=false`. | `Keystrokes.<init>() @404–447`; Boolean builder `_1d4eda() @0–1` in `L._ec7e36._cfe983._cfe983._cfe983` |
| **Confirmed** | `animationType=STACKED`, `timerType=HALF`, `animation=RIPPLE`, `animateColor=false`. | `Keystrokes.<init>() @450–516`; same Boolean builder `_1d4eda() @0–1` |
| **Confirmed** | `animationStartColor=0xC0FFFFFF`; `animationCenterColor=0x6FFFFFFF`; `animationEndColor=0x6FFFFFFF`; `duration` float `0.5 [0.1,1]`; `timingFunction=LINEAR`. | `Keystrokes.<init>() @519–635` |

### Render/input trace

| Classification | Trace / result | Class / method @javap offset |
|---|---|---|
| **Confirmed** | Ordinary labels use the binding's name uppercased with `Locale.ROOT`; mouse labels use localized `lmb`/`rmb`; movement keys have a `useArrows` branch. | `Key._b77881() @0–198` |
| **Unknown** | Exact arrow glyphs are not recoverable from this retained dump: the four strings print as `?`. Do not treat these characters as the shipped glyphs. | `Key._b77881() @176–196` |
| **Confirmed** | Layout width is `3*boxSize+2` for space and `(3*boxSize+1)/2` for each mouse tile; other tiles use `boxSize`. Enabled space height is `boxSize/2`, other enabled tile heights are `boxSize`, and disabled tile height is zero. | `KeyLayout._d4ca6c(KeyCode) @0–80`; `_13ea87(KeyCode) @0–51` |
| **Confirmed** | Grouped renderer evaluates movement/click/space visibility, temporarily installs parent-derived settings on each tile, computes dimensions, invokes the tile HUD, then restores tile state. | `KeyLayout._88f3cf(drawCtx) @0–149,209–255,1052–1066`; `Key._96f409(boolean) @0–413` |
| **Confirmed** | Per rendered tile, resolves the binding's actual key and calls `ML._590f69._21aca6._d043db()._cfe983(key)`. The directly polled pressed candidate is false whenever a current screen is present. That candidate then passes through the feature's `_be2139()._bb4487(description,candidate)` indirection. | `KeyHUD._2ce426(drawCtx) @0–120` |
| **Strong inference** | This is a per-render physical-input polling path, not solely the vanilla keybinding's logical pressed flag. The version-specific implementation behind the bridge poll and the intermediate state provider were not expanded. | `KeyHUD._2ce426(drawCtx) @72–112`; bridge target `ML._590f69._a140a8._590f69._cfe983(KeyCode)` callsite `@76` |
| **Confirmed** | A pressed-state transition invokes the animation dispatcher. With animation disabled, background uses the fade-color helper configured by `keyFadeDelay`; text selects pressed/unpressed color. | `KeyHUD._2ce426(drawCtx) @122–268`; `_d9fd0c(boolean) @0–210` |
| **Confirmed** | Mouse CPS calls the shared click service `_2ce426(isLeft,false)`; `isLeft` is true only for the left mouse tile. Optional CPS text is rendered on a 0.6 scale. | `Key._2ef37e() @0–23`; `KeyHUD._2ce426(drawCtx) @410–537` |
| **Confirmed** | Jump tile draws a short bar using `spacebarThickness`; when the box size is below 14, ordinary built-in labels are shortened to their first character. | `KeyHUD._2ce426(drawCtx) @270–388,570–618` |
| **Confirmed** | Loader recognizes keys ending `_CUSTOM`, derives an integer id, constructs custom key children and delegates to the feature loader. Custom child fields are `customKey` and `customText`; nonblank custom text wins, otherwise the assigned binding name is uppercased or `NONE` is used. | `Keystrokes.load(JsonObject) @27–169`; `L._88f3cf._bb4487._dd3308._cfe983.<init>(Feature,int) @6–36`, `_b77881() @0–54` |

## JV-49 — Waypoints

### Construction, controls and event entry points

| Classification | Static observation | Class / method @javap offset |
|---|---|---|
| **Confirmed** | Module enabled by default; id `WAYPOINTS`. | `Waypoints.<init>() @0–2`; `getId() @0–2` |
| **Confirmed** | `waypointBeams=true`, `boxBorder=true`, `highlightWaypointBlock=true`, `waypointShowDistance=true`, `deathWaypoint=true`, `limitDeathWaypoints=true`. | `Waypoints.<init>() @5–64,108–136,181–209,236–295` |
| **Confirmed** | `boxPadding` float `4 [1,8]`; `highlightWaypointBlockLineWidth` float `4 [1.5,7.5]`; `maxDeathWaypoints` integer `3 [1,20]`. | `Waypoints.<init>() @67–105,139–178,298–335` |
| **Confirmed** | `textShadow=false`, `onlyShowWhenLookingNear=false`, `showIcons=false`. | `Waypoints.<init>() @212–233,470–515`; Boolean builder `L._ec7e36._cfe983._cfe983._cfe983._1d4eda() @0–1` |
| **Confirmed** | `addWaypoint` binds N; `toggleWaypoints` binds M; `quickAddWaypoint` is created without an explicit key override in this constructor. | `Waypoints.<init>() @338–467` |
| **Confirmed** | `labelScale` float `1 [0.1,2]`; `iconScale` float `1.5 [0.1,3]`; `addWaypointsFromChat=true`; `confirmDelete=true`. | `Waypoints.<init>() @518–597,623–682` |
| **Confirmed** | Constructor's `quickWaypointNameFormat` is **`Quick Waypoint`**, not `Quick Waypoint $X/$Y/$Z/$W`. Settings setup subsequently replaces its default via localization key `quickWaypoint`. Name formatting supports `$X/$Y/$Z` using block coordinates and `$W` using a dimension-key suffix with its first character capitalized. | `Waypoints.<init>() @600–620`; `_cfe983(SettingsBuilder) @58–74`; `_79e7e6(Player) @0–106` |
| **Confirmed** | Six event registrations cover Render3D, a second render event, an inner Render2D variant, tick, death and a network/world-state event. | `Waypoints.<init>() @701–770`, with event class literals at `@702,714,726,738,750,762` |
| **Strong inference** | Human-readable event names are inherited from the established event/HUD mapping; the exact posted version-specific event cadence is not runtime-observed here. | Same six `Waypoints.<init>()` registration sites; framework reference JV-17–18 in `rendering-and-hud.md` |

### Death, distance and rendering

| Classification | Trace / result | Class / method @javap offset |
|---|---|---|
| **Confirmed** | Death handler rejects events less than 1,000 ms after its preceding accepted event, updates the timestamp, combines localized `playerDeath` with the manager counter's `getAndIncrement`, constructs a waypoint at `posX/minY/posZ`, attaches world/dimension/server identity, marks it a death waypoint and adds it to the manager. | `Waypoints._21aca6(DeathEvent) @0–192`, especially `@0–55,58–118,154–187` |
| **Confirmed** | Death-limit helper filters, sorts by a long-valued accessor, computes `count-maxDeathWaypoints` and removes that many entries from the front when the limit is enabled. | `Waypoints._004e61() @0–117` |
| **Strong inference** | Sorting/removing the front is consistent with pruning oldest death markers; this pass did not resolve the invokedynamic predicate/accessor bootstrap, so it does not independently prove their identities. | `Waypoints._004e61() @30–53,91–107` |
| **Confirmed** | Tick gets the render-view entity, returns if absent, and refreshes distance only for waypoints whose `isVisible()` and `shouldRender()` both pass. Distance is Euclidean `sqrt(dx²+dy²+dz²)`, stored on the waypoint. | `Waypoints._21aca6(Tick) @0–92`; static `_cfe983(Waypoint,Entity) @0–71` |
| **Confirmed** | Render3D clears the projected-label list, requires the module's local visible flag, filters text and looking-near conditions, projects `(x,y+2,z)` and retains nonnull projected points with their waypoint. Beam rendering follows its global toggle and per-marker/group render configuration. | `Waypoints._1253fc(Render3D) @0–304`, projection `@126–176`; `_cfe983(drawCtx,Waypoint,double) @197–240` |
| **Confirmed** | Looking-near predicate checks both wrapped head-yaw difference and pitch difference against 20 degrees, aiming at the marker with an eye-height adjustment and +2 Y offset. | `Waypoints._cfe983(LivingEntity,Waypoint) @0–167` |
| **Confirmed** | Second render handler invokes block highlighting; highlighting is globally gated, then uses group override or waypoint configuration. The selected block is based on `floor(x),floor(y-1),floor(z)`. | `Waypoints._cfe983(SecondRenderEvent) @0–41`; `_cfe983(drawCtx,Waypoint) @0–61,104–143` |
| **Confirmed** | Render2D iterates the projected-label list; label builder appends nonblank name and optional integer-cast distance in `[Nm]` form. | `Waypoints._590f69(Render2D) @0–60`; `_cfe983(drawCtx,font,ProjectedWaypoint,double) @15–105` |
| **Confirmed** | Label rendering calls ZOOM's `_8c5fe4(float)` and scales by its reciprocal, then by the selected label scale; a per-waypoint text configuration can override module-level label scale/padding/shadow/icons. | `Waypoints._cfe983(drawCtx,font,ProjectedWaypoint,double) @159–268,519–647` |
| **Strong inference** | Reciprocal scaling compensates labels for the ZOOM/FOV factor; actual appearance across Minecraft versions remains unobserved. | Same label method `@159–191`, call to `L._88f3cf._bb4487._136819._cfe983._8c5fe4(float) @173` |
| **Confirmed** | Global distance toggle must pass; then an attached group with `renderOptionsOverrideMembers` supplies `showDistance`, otherwise the waypoint's own `renderConfig` supplies it. Similar group override selection exists for beam, color and highlighting. | `Waypoints._590f69(Waypoint) @0–53`; beam helper `_cfe983(drawCtx,Waypoint,double) @100–238`; highlight helper `_cfe983(drawCtx,Waypoint) @17–55` |

## FS-11 — Bytecode-derived waypoint persistence and import surfaces

**Confirmed — file destination:** `WaypointManager._a55711() @0–2` returns `waypoints.json`; interface `L._02d7ad._d4ca6c._a1ad6f() @0–16` joins the global game-settings directory, whose `L.util._cb9292.<clinit> @538–562` resolves `settings/game`. Thus the bytecode destination is global `settings/game/waypoints.json`, not a per-profile `mods.json` file. Artifact: `lunar.jar`. **No user waypoint file was read.**

### Serialized schema: keys and types only

| Classification | Schema path / types | Class / method @javap offset |
|---|---|---|
| **Confirmed** | Root `version`, `totalDeaths`, `sortIndex`: integers; `groups`, `waypoints`: objects. | `WaypointManager._590f69(JsonObject) @0–55`; `_728fa6(JsonObject) @0–78`; `_cfe983(JsonObject,Collection) @0–55` |
| **Confirmed** | `groups.<uuid-string>` is a group object. Its `id`, `name`: strings; `visible`, `isDefault`, `renderOptionsOverrideMembers`: booleans; `sortIndex`: integer; `addedAtMs`: long-valued number; optional `server`: string; `renderConfig`: object. | `WaypointManager._728fa6(JsonObject) @47–75`; `WaypointGroup._590f69(JsonObject) @0–130` |
| **Confirmed** | `waypoints.<server-key>.<world-key>.<name-key>` is a waypoint object; the three identities are nested object keys, not repeated fields in the serialized marker object. | `WaypointManager._cfe983(JsonObject,Waypoint) @8–104,401–409`; reader `_543b36(JsonObject) @8–181,299–309,348–365,465–479` |
| **Confirmed** | Waypoint `location` object contains numeric `x`,`y`,`z` written/read as doubles. | `WaypointManager._cfe983(JsonObject,Waypoint) @106–178`; `_543b36(JsonObject) @312–342` |
| **Confirmed** | `icon`, `skyBlockLocation`: strings; `addedAtMs`: long-valued number; `isDeathWaypoint`, `visible`, `isSkyBlockWaypoint`: booleans; `dimension`, `sortIndex`: integers; `renderConfig`: object. | `WaypointManager._cfe983(JsonObject,Waypoint) @181–293,346–374` |
| **Confirmed** | Optional `groupIndex`: integer; optional nonempty `dimensionKey`: string; optional `groupId`: UUID string. These fields supplement the supplied abbreviated schema. | `WaypointManager._cfe983(JsonObject,Waypoint) @296–343,377–398`; reader `_543b36(JsonObject) @484–553` |
| **Confirmed** | `renderConfig` writes `showBeam`, `showText`, `showDistance`, `highlightBlock`: booleans; `icon`: string enum name; delegates `color` to the color-setting serializer. | `WaypointRenderConfig._590f69(JsonObject) @0–73`; color key creation `<init>(boolean,Icon,boolean,boolean,boolean) @4–23` |
| **Unknown** | Exact inner JSON encoding of `color` was not expanded in this pass. Its Java setting value is an integer, but this is insufficient to assert that its persisted JSON is always a bare integer rather than the framework's setting envelope. | `WaypointRenderConfig._590f69(JsonObject) @65–70`; `L._ec7e36._e62626` member signature uses `Codec<Integer>`; serializer call is inherited, offset **N/A** for the signature |

### Import/chat surfaces, with bounded conclusions

| Classification | Observation | Class / method @javap offset |
|---|---|---|
| **Confirmed** | Constructor instantiates six named decoders: Badlion Client, JourneyMap, VoxelMap, Xaero's Minimap, Skytils and Coleweight, retaining them in `decoders`. | `WaypointManager.<init>() @4–66` |
| **Unknown** | Decoder existence is not verification of every supported upstream format/version or successful imports. No imported user files or target execution were used. | Same constructor `@4–66`; individual decoder methods not traced in this pass |
| **Confirmed** | Pattern initialization loads `waypoint-patterns.json`, compiles string entries with flag 2 (case-insensitive) and creates component transformers. Incoming chat transformation is gated on enabled WAYPOINTS and `addWaypointsFromChat`. | `WaypointManager._b9625d() @0–113`; `_79e7e6(ChatComponentEvent) @0–86` |
| **Confirmed** | `/lc_waypoint_chat` handler cancels the matching command event, parses coordinates from bracketed or alternate token forms, builds an X/Y/Z payload and dispatches a GameUI action; parse errors are caught. This is a UI handoff, not direct evidence that the waypoint is already persisted. | `WaypointManager._cfe983(ChatCommandEvent) @0–171`, especially `@0–12,13–127,129–164` |

## Compact ledger cross-reference

These entries are appended in [evidence-index.md](evidence-index.md); earlier reports and ledger entries remain preserved.

| ID | Classification | Artifact / class / method @offset | Finding and caveat |
|---|---|---|---|
| **JV-47** | **Confirmed** | `lunar.jar`; `Coordinates.<init>() @0–367`, `_133367(double) @0–40`, `_7e956b(float) @0–82`, `_76bef3() @16–90`; `CoordinatesHUD._52e8ee(boolean) @0–62` | Coordinates defaults/children, supplier data sources, decimal truncation versus integer floor, compass lookup, chat gate and clipboard/toast path. Clipboard uses integer-cast `posY`, not HUD `minY`; separate-child formatter must not be generalized to every grouped branch without further inspection. |
| **JV-48** | **Confirmed** | `lunar.jar`; `Keystrokes.<init>() @0–708`; `KeyHUD._2ce426(drawCtx) @0–710`; `KeyLayout._d4ca6c(KeyCode) @0–80`; `Key._2ef37e() @0–23` | Grouped default, recovered settings, key polling/current-screen candidate suppression, fades, geometry, shared mouse CPS and label/custom-key behavior. Exact arrow glyphs and version-specific input-bridge implementation remain Unknown. |
| **JV-49** | **Confirmed** | `lunar.jar`; `Waypoints.<init>() @0–814`, `_21aca6(DeathEvent) @0–192`, `_21aca6(Tick) @0–92`, `_1253fc(Render3D) @0–304`, label helper `_cfe983(drawCtx,font,ProjectedWaypoint,double) @15–268`, `_590f69(Waypoint) @0–53` | Defaults, event registrations, death debounce/builder, Euclidean distance cache, projection/render/config paths. Quick-name constructor default is `Quick Waypoint`; placeholders are supported, not included in that literal. Zoom compensation meaning is Strong inference, not observed rendering. |
| **FS-11** | **Confirmed** | `lunar.jar`; `WaypointManager._a55711() @0–2`, `_590f69(JsonObject) @0–55`, `_728fa6(JsonObject) @0–78`, `_cfe983(JsonObject,Waypoint) @8–409`; `WaypointGroup._590f69(JsonObject) @0–130`; `WaypointRenderConfig._590f69(JsonObject) @0–73` | Global waypoint path and bytecode-derived nested schema, including optional group/dimension fields; no user waypoint/settings values. Exact color envelope and upstream importer compatibility remain Unknown. |

**Unknown — execution boundary:** runtime appearance, default enablement after user configuration, active event cadence and successful disk/UI/import behavior were not observed. Source boundary: the named `lunar.jar` classes/methods/offsets above; there is no runtime offset/evidence for those questions.
