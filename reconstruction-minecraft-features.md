# Minecraft feature reconstruction feasibility

This static evidence supports a feature catalog, shared setting contracts and a partial HUD/UI host interface. It does not supply a complete behavior specification for a compatible client. No shipped feature is marked behaviorally complete.

The machine-readable [catalog](reconstruction-minecraft-features.json) preserves all **379 feature identifiers**, their localization key paths, exact compiled-string/class correlations, candidate setting identifiers, evidence anchors, per-identifier readiness and missing host logic. It includes **5,780 localization leaf key names** across the language resource. Translation values and proprietary assets are excluded.

## Evidence and limits

**Confirmed:** The identifiers are keys in `C:/Users/Admin/.lunarclient/offline/multiver/lunar-lang.jar!lang/lunar/en_US.json`. In `lunar.jar`, 353 descendants of the shared feature base contain exact String constants matching 348 of those identifiers. The shared base has 403 direct children and 460 transitive descendants. There are 31 identifiers without a match in this limited correlation.

**Inference:** A matching identifier in a feature-base descendant is a useful class-to-feature lead. It does not establish registration, availability in a specific Minecraft version, activation, complete ownership, or the behavior of that feature. Child, legacy, debug and specialized identifiers are present; 379 is a catalog size, not an active feature count. Setting-name correlations likewise do not establish a schema or default.

All class relationships, member descriptors, annotations and constant-pool references below came from the supplemental inert ZIP/classfile parser. They are not REA decompilation. Previously retained REA Genesis inventory is anchored by `ev_3dfa373be43e21b36815c27464dbd7b08fa52a525ac0995bc2cfc9a6c7e378a7` and `ev_abd81f72db9d0318d3f5953315cfdcb138c8462fdbbea1dca5ed840efb52cb24`; see [retained evidence](rea-evidence-through-genesis.json). Current REA availability was checked: archive inspection/extraction are available, Java decompilation provider is missing and the current archive target does not support native batch decompilation. No active target was changed for this follow-up.

The artifact SHA-256 values are in the catalog. `lunar.jar`: `bf36e10e21154263ac16363f8c83bb08cff3a077cb788120954d3625b94a02e9`. Class entries are `<internal class name>.class` within this JAR. No client, Java program or native module was run; no mappings were applied, obfuscation altered, current user settings read, credentials collected or anti-cheat logic inspected.

## Readiness assignments

These groups are analyst planning inferences from identifier names and static links. Every catalog entry retains its individual assignment.

| Planning group | Identifiers | What the evidence can support | What remains missing |
| --- | ---: | --- | --- |
| Common HUD/data display | 42 | Names, some class relationships and shared layout/settings contracts; 28 have feature-class correlation | Runtime data adapter, event timing, renderer/layout, exact settings and lifecycle behavior |
| Domain or service dependent | 212 | Names, many class correlations and shared control contracts | Domain data interpretation, algorithms/state machines, service contracts, error handling and version-specific host behavior |
| Rendering/input/UI changes | 97 | Names and partial shared interfaces | Exact version hooks, rendering/input algorithms, state, persistence, defaults and interactions |
| Debug/specialized identifiers excluded from behavioral inspection | 28 | Identifier inventory only | Behavior deliberately not inspected |

Readiness totals: 28 have a partial contract useful for writing a fresh small-feature specification; 292 have partial interfaces insufficient for behavioral reconstruction; 31 are identifier-only in this correlation; 28 are scope-excluded inventory. These labels do not mean that any implementation can be copied or that parity has been demonstrated.

Common named candidates include `FPS`, `CPS`, `MEMORY`, `CLOCK`, `STOPWATCH`, `COORDINATES`, `KEYSTROKES`, `ARMORSTATUS`, `PING`, `DIRECTION_HUD`, `ITEM_COUNTER`, `POTION_COUNTER`, `TOTEM_COUNTER`, `SATURATION`, `POTION_EFFECTS`, `PACK_DISPLAY`, `SHADER_PACK_DISPLAY`, `PLAYTIME`, `REACH_DISPLAY` and `COMBO`. A familiar name alone does not specify a sampling window, unit, click/event definition, visibility rule, inventory interpretation or styling.

Complex examples include `MINIMAP`, `WAYPOINTS`, `MARKERS`, `REPLAYMOD`, `REWIND`, `WORLDEDIT_CUI`, `RADIO`, `MUMBLE_LINK`, `HYPIXEL_BEDWARS`, `SKYBLOCK`, `BETTERMAP_PRIMARY` and the numerous SkyBlock HUD, puzzle, farming, fishing, mining, dungeon and inventory identifiers. Names and shared settings do not recover their domain algorithms or server contracts.

## Shared feature contract

The following symbol prefixes are exact internal JVM names; concatenating prefix and suffix gives a class name:

- `F = com/moonsworth/lunar/client/RIHHCHHHROOHOOIOIIRIOOCRHHOOOR/`
- `H = F + RORCICOHRIOIIIOIOHIIIICRCIHRII/`
- `S = com/moonsworth/lunar/client/OHRHIRHIHIORRCHRHCCCOOOCORCRIR/`

**Confirmed:** Feature base `F + COOCHIRORIICRCIIRIROHIIRIRICCH` extends Object and implements two shipped interfaces. It contains `enabled:Z`, `mc:<Minecraft bridge reference>`, cache/client/event-related references, and named methods `isEnabled()Z`, `updateEnabled()V`, `load(JsonObject)V`, `handle(Class,Consumer)V`. Other overloads accept Class/Runnable or Class/Consumer with an integer priority. The catalog preserves exact interface, field and method descriptors.

**Inference:** This is a shared lifecycle/configuration/event boundary. Names, descriptors and JSON arguments do not establish default enablement, event ordering, conflict resolution, migration rules or every serialization field. No obfuscated methods were renamed or deobfuscated.

## HUD layout and renderer boundary

**Confirmed:** `H + COOCHIRORIICRCIIRIROHIIRIRICCH` extends Object and implements `H + OHOORCOHRORRIHROOCROOIIHHOOHRI`. It contains named `x:F`, `y:F`, `width:F`, `height:F` fields and `setScale(F)V`, `getScale()F`. Its String constants include the identifiers `position`, `scale`, `x` and `y`.

**Confirmed:** `H + RIHHCHHHROOHOOIOIIRIOOCRHHOOOR` extends that layout base. It has 66 direct children; the layout base has 37 direct children. Together the two bases and transitive descendants comprise 128 classes. Method descriptors accept shipped render-bridge references, float coordinates and boolean flags. The exact descriptors are retained in `confirmedFramework.hudBases`.

Compiled identifier names in the decorated HUD base include `alignment`, `background`, `backgroundColor`, `backgroundHeight`, `backgroundWidth`, `border`, `borderColor`, `borderThickness`, `bracketColor`, `brackets`, `showHudIcons`, `showText`, `staticBackgroundHeight`, `staticBackgroundWidth`, `textColor` and `textShadow`. **Inference:** These suggest reusable presentation controls. Their exact types, supported ranges and defaults are not proved by names.

The common feature mappings below are exact class/bytecode observations; assigning the feature responsibility is the explicitly limited String-correlation inference described above. Full names and fields are in `confirmedFramework.commonFeatureClassRelationships`.

| Identifier | Correlated class suffix under F | Confirmed HUD reference anchor |
| --- | --- | --- |
| COORDINATES | `IRCROOHIIOOHIRCRRHOHIORHCOHIOR/RHCCHHHHIHHRIICRIHRRIHRORIIOHO/OHRORRHCHCRICORRRCIRIOCCIRCRII` | `<init>()V` bytecode 355 → `com/moonsworth/lunar/client/RIHHCHHHROOHOOIOIIRIOOCRHHOOOR/IRCROOHIIOOHIRCRRHOHIORHCOHIOR/RHCCHHHHIHHRIICRIHRRIHRORIIOHO/OHRORRHCHCRICORRRCIRIOCCIRCRII$COOCHIRORIICRCIIRIROHIIRIRICCH` |
| ARMORSTATUS | `IRCROOHIIOOHIRCRRHOHIORHCOHIOR/RROHOCRCCHCIORHICIHCOHRIRCIHCI/COOCHIRORIICRCIIRIROHIIRIRICCH` | `<init>()V` bytecode 810 → `com/moonsworth/lunar/client/RIHHCHHHROOHOOIOIIRIOOCRHHOOOR/IRCROOHIIOOHIRCRRHOHIORHCOHIOR/RROHOCRCCHCIORHICIHCOHRIRCIHCI/OHRORRHCHCRICORRRCIRIOCCIRCRII/RORCICOHRIOIIIOIOHIIIICRCIHRII` |
| CPS | `IRCROOHIIOOHIRCRRHOHIORHCOHIOR/ORHHCIHIOOCOOHOOIROIHHOCOOCIRH/COOCHIRORIICRCIIRIROHIIRIRICCH` | `<init>()V` bytecode 112 → `com/moonsworth/lunar/client/RIHHCHHHROOHOOIOIIRIOOCRHHOOOR/IRCROOHIIOOHIRCRRHOHIORHCOHIOR/ORHHCIHIOOCOOHOOIROIHHOCOOCIRH/COOCHIRORIICRCIIRIROHIIRIRICCH$COOCHIRORIICRCIIRIROHIIRIRICCH` |
| MEMORY | `IRCROOHIIOOHIRCRRHOHIORHCOHIOR/ORRCRHRIHHRRROHIHCHRHHRRHIRCOI/COOCHIRORIICRCIIRIROHIIRIRICCH` | `<init>()V` bytecode 112 → `com/moonsworth/lunar/client/RIHHCHHHROOHOOIOIIRIOOCRHHOOOR/IRCROOHIIOOHIRCRRHOHIORHCOHIOR/ORRCRHRIHHRRROHIHCHRHHRRHIRCOI/COOCHIRORIICRCIIRIROHIIRIRICCH$RROHOCRCCHCIORHICIHCOHRIRCIHCI` |
| KEYSTROKES | `IRCROOHIIOOHIRCRRHOHIORHCOHIOR/COHHOIRRCCCICHRHCOHRRCRHOIRIHI/RORCICOHRIOIIIOIOHIIIICRCIHRII` | `<init>()V` bytecode 665 → `com/moonsworth/lunar/client/RIHHCHHHROOHOOIOIIRIOOCRHHOOOR/IRCROOHIIOOHIRCRRHOHIORHCOHIOR/COHHOIRRCCCICHRHCOHRRCRHOIRIHI/RORCICOHRIOIIIOIOHIIIICRCIHRII$COOCHIRORIICRCIIRIROHIIRIRICCH` |
| FPS | `IRCROOHIIOOHIRCRRHOHIORHCOHIOR/HCOCRHCHRIHCHORRRRRHIOHHICHIII/COOCHIRORIICRCIIRIROHIIRIRICCH` | `<init>()V` bytecode 50 → `com/moonsworth/lunar/client/RIHHCHHHROOHOOIOIIRIOOCRHHOOOR/RORCICOHRIOIIIOIOHIIIICRCIHRII/RIHHCHHHROOHOOIOIIRIOOCRHHOOOR` |
| CLOCK | `IRCROOHIIOOHIRCRRHOHIORHCOHIOR/OIHRRCOOHRHIHICHRICIRIOCROHOCC/COOCHIRORIICRCIIRIROHIIRIRICCH` | `<init>()V` bytecode 111 → `com/moonsworth/lunar/client/RIHHCHHHROOHOOIOIIRIOOCRHHOOOR/RORCICOHRIOIIIOIOHIIIICRCIHRII/RIHHCHHHROOHOOIOIIRIOOCRHHOOOR` |
| STOPWATCH | `IRCROOHIIOOHIRCRRHOHIORHCOHIOR/CHCRCIRHCRCRIRHHIOCRRCHIOOCOOI/COOCHIRORIICRCIIRIROHIIRIRICCH` | No HUD-base/subclass reference found by the limited operand scan |
| PING | `IRCROOHIIOOHIRCRRHOHIORHCOHIOR/RIHCOHORHRIOICORHHIOOROOCIRRRO/RROHOCRCCHCIORHICIHCOHRIRCIHCI` | No HUD-base/subclass reference found by the limited operand scan |

These references establish coupling to shared HUD types, not exact rendered content. CPS constructor allocates a nested HUD subclass at bytecode 112 and invokes its constructor at 117; FPS constructor calls the decorated HUD factory at bytecode 50. The referenced CPS nested type inherits the decorated HUD base.

## Settings, controls, defaults and validation

**Confirmed:** Shared value classes extend `S + ORCOOOCHIICOIICCROCRCOOROORIHR`. The following suffixes expose a named `value` field and a `getDefaultValue()Object` method (primitive implementations also have compiler-generated bridge methods):

| Suffix under S | value descriptor |
| --- | --- |
| COOCHIRORIICRCIIRIROHIIRIRICCH | Z (boolean) |
| IRCROOHIIOOHIRCRRHOHIORHCOHIOR | I (int) |
| OHOORCOHRORRIHROOCROOIIHHOOHRI | J (long) |
| OHRORRHCHCRICORRRCIRIOCCIRCRII | F (float) |
| RORCICOHRIOIIIOIOHIIIICRCIHRII | D (double) |
| OIHRRCOOHRHIHICHRICIRIOCROHOCC | S (short) |
| RROHOCRCCHCIORHICIHCOHRIRCIHCI | B (byte) |
| RCRHOOHIOCHHHHOCRIOCHRICIRCRRR | Object; also named defaultValue:Object |

**Confirmed:** Builder/metadata class `S + COOCHIRORIICRCIIRIROHIIRIRICCH/COOCHIRORIICRCIIRIROHIIRIRICCH` has a `codec:Lcom/lunarclient/dfu/serialization/Codec;` field. Descendant classes with suffixes `IRCROOHIIOOHIRCRRHOHIORHCOHIOR`, `OHOORCOHRORRIHROOCROOIIHHOOHRI` and `OHRORRHCHCRICORRRCIRIOCCIRCRII` expose `min/max` pairs of float, int and double respectively. The `RCRHOOHIOCHHHHOCRIOCHRICIRCRRR` descendant exposes named `min:J`; its other bound is not named. Other setting types contain `options:List` and `elementCodec:Codec`.

**Inference:** Shared codecs, defaults and numeric boundary metadata make typed control models plausible. These observations do not establish per-feature values, slider increments, inclusive/exclusive limits, coercion, rejection, clamping, enum ordering, reset semantics, migration or save timing. Every feature catalog entry therefore marks actual defaults and per-feature validation as unresolved. Current user configuration values were not read.

**Confirmed:** Scope enum `S + RHCHOCRHIOROIOCRHIHRCROOOHICCC` has `GENERAL`, `PERFORMANCE`, `CONTROLS`, `FEATURE` and `REWIND`. Category identifiers in another setting enum include `GENERAL`, `COLOR`, `SETTINGS`, `CONTROLS`, `HUD`, `RENDER`, `AUDIO`, `INVENTORY`, `CHAT`, `DUNGEONS`, `FARMING`, `MINING` and `FISHING`. They are shipped grouping names, not proof that every group is shown.

There are candidate setting-name String matches in 281 catalog identifiers' correlated classes. For example, the class correlated with `DIRECTION_HUD` contains `background`, `backgroundColor`, `boldDirections`, `border`, `borderColor`, `borderThickness`, `directionColor`, `externalMarkers`, `hudStyle`, `markerColor`, `renderOptions`, `showExternalMarkers`, `showMarker`, `showMarkerValue`, `showTeammates`, `showWaypoints`, `showWithTab`, `teammates` and `textShadow`. **Inference:** These are schema leads; registration, defaults and validation have not been established. The JSON stores exact constant-pool indexes for matches against shipped localization setting identifiers.

## Game UI host callbacks

**Confirmed:** The Java provider registry associates literal namespaces `settings`, `profiles`, `mods`, `hudModProperty` and `hudModMetadata` with shipped class literals. Exact class names and registry bytecode offsets are in `confirmedFramework.uiProviders`. The settings provider is:

`com/moonsworth/lunar/client/OHOORCCRHHHHROIICHOCRHOCRICROH/RROHOCRCCHCIORHICIHCOHRIRCIHCI/RCRHOOHIOCHHHHOCRIOCHRICIRCRRR/COOCHIRORIICRCIIRIROHIIRIRICCH/CCHRHCCCHRIHCICICIRCORHRORIOCI`

Its `@com.moonsworth.webosr.javascript.CallbackJS` annotations explicitly name the following callbacks. Scope means the exact enum above; strings are descriptor-level evidence, not an established payload schema.

| Callback | JVM argument types | Return |
| --- | --- | --- |
| setAdvancedMode | Boolean | void |
| update | Scope, String, String, String | void |
| reset | Scope, String, String | void |
| invokeAction | Scope, String, String | void |
| setEditingKeybind | Scope, String, String | void |
| stopEditingKeybind | none | void |

**Confirmed:** HUD metadata/property providers accept a String in their constructors and expose JsonElement-returning provider methods. The Java/UI bridge binds `lunarInternalInvoke` through `Browser.bindFunction`, and game UI initialization supplies proxy/namespace behavior. See [Minecraft architecture](minecraft-client-architecture.md), [UI bridge evidence](minecraft-ui-bridge-metadata.json) and the separate game UI reconstruction report for the JavaScript-facing side.

**Inference:** These contracts are sufficient to draft provider facades and settings command interfaces for a new host. They do not establish arbitrary JSON payload compatibility, subscriptions/change propagation, thread affinity, error encoding, persistence, callbacks' complete effects, or lifecycle teardown. No mock host was implemented.

## What a reconstruction still needs

The evidence supports designing independent interfaces for feature metadata, typed settings, HUD placement, provider dispatch and version adapters. Small display features can receive fresh specifications once data sources, units, update cadence and visibility behavior are chosen. Compatibility claims require additional lawful specifications or user-authorized observations.

Rendering, input, inventory, camera, map, replay and server-specific features need their own semantics and lifecycle specifications. Shared member descriptors and Mixin target lists do not recover pixel output, algorithm details, resource requirements, exact event order or all supported Minecraft versions. Minimap/waypoint, replay/rewind and SkyBlock/Hypixel logic remain substantially incomplete.

Obfuscation and missing Java decompilation providers limit the available explanations. No protection defeat, name recovery, hidden payload execution or anti-cheat investigation was attempted. Static confirmation is limited to the installed artifacts whose hashes are recorded.

## Complete identifier appendix

The following are identifier names only, grouped by the tentative planning category. The machine-readable catalog is authoritative for per-identifier evidence and readiness. No identifier here implies current activation.

### common_hud

`COORDINATES`, `COORDINATES_X_CHILD`, `COORDINATES_Y_CHILD`, `COORDINATES_Z_CHILD`, `COORDINATES_C_CHILD`, `COORDINATES_DIRECTION_CHILD`, `COORDINATES_BIOME_CHILD`, `SERVER_ADDRESS`, `DIRECTION_HUD`, `REACH_DISPLAY`, `DAY_COUNTER`, `ARMORSTATUS`, `ARMORSTATUS_HELD_ITEM_CHILD`, `ARMORSTATUS_HELMET_CHILD`, `ARMORSTATUS_CHESTPLATE_CHILD`, `ARMORSTATUS_LEGGINGS_CHILD`, `ARMORSTATUS_BOOTS_CHILD`, `ARMORSTATUS_OFF_HAND_HELD_ITEM_CHILD`, `ARMORSTATUS_PROTECTION_CHILD`, `ARMORSTATUS_BARS_CHILD`, `TOTEM_COUNTER`, `TOTEM_COUNTER_HUD_CHILD`, `CPS`, `MEMORY`, `KEYSTROKES`, `SATURATION`, `SATURATION_HUD_CHILD`, `FPS`, `CLOCK`, `STOPWATCH`, `STOPWATCH_HUD_CHILD`, `PING`, `PING_HUD`, `PING_NAMETAG`, `ITEM_COUNTER`, `ITEM_COUNTER_CHILD`, `POTION_COUNTER`, `POTION_EFFECTS`, `COMBO`, `PACK_DISPLAY`, `SHADER_PACK_DISPLAY`, `PLAYTIME`.

### domain_or_service

`HYPIXEL_BEDWARS`, `HYPIXEL_BEDWARS_STATS_CHILD`, `HYPIXEL_BEDWARS_RESOURCE_COUNTER_CHILD`, `HYPIXEL_BEDWARS_UPGRADE_DISPLAY_CHILD`, `HYPIXEL_BEDWARS_TEAM_DISPLAY_CHILD`, `HYPIXEL_BEDWARS_TIMERS_CHILD_HUD`, `RADIO`, `REPLAYMOD`, `REPLAYMOD_RECORDING_INDICATOR_CHILD`, `MARKERS`, `WAYPOINTS`, `HYPIXEL_MOD`, `WORLDEDIT_CUI`, `SKYBLOCK_TAB_WIDGET_CHILD`, `MUMBLE_LINK`, `QUICKPLAY`, `MINIMAP`, `REWIND`, `REWIND_RECORDING_INDICATOR_CHILD`, `REWIND_HANDLERS`, `SKYBLOCK`, `SKYBLOCK_HEALTH_HUD`, `SKYBLOCK_MANA_HUD`, `SKYBLOCK_KUUDRA_ARMOR_STACKS_HUD`, `SKYBLOCK_DEF_HUD`, `SKYBLOCK_SPEED_HUD`, `SKYBLOCK_VITALITY_HUD`, `SKYBLOCK_QUIVER_HUD`, `SKYBLOCK_VISITOR_HUD`, `SKYBLOCK_NETHER_BOSS_HUD`, `SKYBLOCK_POWDER_TRACKER_HUD`, `ETHERWARP_PREVIEW`, `SKYBLOCK_DAMAGE_SPLASH`, `SKYBLOCK_COMPOSTER_HUD`, `SKYBLOCK_VISITOR_ALERT`, `SPIRIT_LEAP_OVERLAY`, `SKYBLOCK_RARITY_BACKGROUND`, `SKYBLOCK_VANILLA_ITEM_MODELS`, `TIERS_AS_STACK_SIZE`, `SKYBLOCK_DUNGEON_SCORE_ALERT`, `BETTERMAP_PRIMARY`, `BETTERMAP_SECONDARY`, `SKYBLOCK_DUNGEON_BAT_HELPER`, `SKYBLOCK_LIVID_SOLVER_HUD`, `SKYBLOCK_TERMINAL_SOLVERS`, `SKYBLOCK_CHOCOLATE_FACTORY`, `SKYBLOCK_HOPPITY_EGG_HUD`, `SKYBLOCK_ARMOR_DYE_COLOR`, `DUNGEON_SECRET_WAYPOINTS`, `SKYBLOCK_ENDERMAN_SLAYER`, `SKYBLOCK_BLAZE_SLAYER`, `SKYBLOCK_DUNGEON_HIGHLIGHT_DOORS`, `STARRED_MOB_HIGHLIGHT`, `TEAM_CAKE_HIGHLIGHT`, `SKYBLOCK_DUNGEON_PUZZLES`, `SKYBLOCK_LOCK_MOUSE`, `SKYBLOCK_ANGLE_HUD`, `SKYBLOCK_EXPERIMENT_SOLVERS`, `GRAVITY_STORM_PREVIEW`, `SKYBLOCK_CHAT_COMMANDS`, `SKYBLOCK_FLOOR_FOUR`, `SKYBLOCK_CROESUS_CHESTS`, `SKYBLOCK_DUNGEON_TIMER`, `SKYBLOCK_DRAGON_FEATURES`, `SKYBLOCK_GLACITE_COMMISSIONS`, `SKYBLOCK_CRYSTAL_HOLLOWS_MAP`, `SKYBLOCK_CRITICAL_DUNGEON_TEAMMATE`, `SKYBLOCK_DUNGEON_BLOOD_CAMP_HELPER`, `SKYBLOCK_KUUDRA`, `DUNGEON_WAYPOINTS`, `SKYBLOCK_FARMING_HUD`, `SKYBLOCK_VISITOR_TRACKER_HUD`, `SKYBLOCK_VISITOR_SHOPPING_LIST_HUD`, `SKYBLOCK_CROP_TRACKER_HUD`, `SKYBLOCK_HARVEST_FEAST_TRACKER_HUD`, `SKYBLOCK_FARMING_TOOL_CROP_ICON`, `SKYBLOCK_GALATEA_MOB_HIGHLIGHT`, `SKYBLOCK_GARDEN_PESTS`, `SKYBLOCK_DNA_ANALYZER_SOLVER`, `SKYBLOCK_SEA_CREATURE_ALERT`, `SKYBLOCK_FISHING_MARKER`, `SKYBLOCK_POWDER_TRACKER`, `SKYBLOCK_DUNGEON_TEAMMATE_HIGHLIGHT`, `SKYBLOCK_FIRE_FREEZE_TIMER`, `SKYBLOCK_SKELETON_HELMET_HUD`, `SKYBLOCK_ARROW_POISON_HUD`, `SKYBLOCK_SPIDER_DEN_RAIN_HUD`, `SKYBLOCK_HIGHLIGHT_TRASH_DUNGEON_ITEMS`, `SKYBLOCK_HEALING_CIRCLE_OVERLAY`, `SKYBLOCK_DUNGEON_MILESTONE_HUD`, `SKYBLOCK_DUNGEON_BLESSING_HUD`, `SKYBLOCK_MYTHOLOGICAL_RITUAL`, `SKYBLOCK_PARTY_FINDER`, `SKYBLOCK_DUNGEON_COLORS`, `SKYBLOCK_WHISPER_TRACKER_HUD`, `SKYBLOCK_FORAGING_BEACON_SOLVER`, `SKYBLOCK_MUTE_BEEHEEMOTH_SOUNDS`, `SKYBLOCK_RAINBOW_BELL_WAYPOINTS`, `SKYBLOCK_CAUGHT_CRITTERS_HUD`, `SKYBLOCK_SPARKLING_CRITTER_ALERT`, `SKYBLOCK_UNFINISHED_TERMINALS`, `SKYBLOCK_COLLECTED_SECRET`, `SKYBLOCK_SPIRIT_LEAP_ANNOUNCE`, `SKYBLOCK_SKILL_XP_TRACKER_HUD`, `SKYBLOCK_SKILL_PROGRESS_HUD`, `SKYBLOCK_SKILL_GLOBE_HUD`, `SKYBLOCK_WITHER_HEALTH_HUD`, `SKYBLOCK_STORM_HUD`, `SKYBLOCK_ENCHANT_DISPLAY`, `SKYBLOCK_HIGHLIGHT_FILLED_BZ_ORDERS`, `SKYBLOCK_CALCULATOR_IN_SIGNS`, `SKYBLOCK_SKILL_PROGRESS_BAR_HUD`, `SKYBLOCK_MAGE_BEAM`, `SKYBLOCK_STACKING_ENCHANTS`, `SKYBLOCK_HIDE_CHUM_BUCKETS`, `SKYBLOCK_TROPHY_FISH_EXCHANGE_RATE`, `SKYBLOCK_LILY_PAD_HELPER`, `SKYBLOCK_HIDE_LOTUSFISH_NAMETAG`, `SKYBLOCK_FISHING_CIRCLE_OVERLAY`, `SKYBLOCK_FISHING_REEL_TIMER_HUD`, `SKYBLOCK_FISHING_INFO_HUD`, `SKYBLOCK_SEA_CREATURE_MESSAGES`, `SKYBLOCK_FISHING_BAIT_HUD`, `SKYBLOCK_INVINCIBILITY_HUD`, `SKYBLOCK_BITS_SHOP_HELPER`, `SKYBLOCK_SKYMART_HELPER`, `SKYBLOCK_CHOCOLATE_SHOP_HELPER`, `SKYBLOCK_CHOCOLATE_STATS`, `SKYBLOCK_RABBIT_COLLECTION_OVERLAY`, `SKYBLOCK_ENHANCED_MINION_MENU`, `SKYBLOCK_SMOOTH_TELEPORT`, `SKYBLOCK_VISITOR_PROFIT`, `SKYBLOCK_VISITOR_BAZAAR_HELPER`, `SKYBLOCK_WARDROBE_HOTKEYS`, `SKYBLOCK_HIDE_FAR_ENTITIES`, `SKYBLOCK_TERRACOTTA_TIMER`, `SKYBLOCK_TICK_TIMER_HUD`, `SKYBLOCK_LASSO_HELPER`, `HYPIXEL_TPS`, `SERVER_COMMAND_CONFIG`, `SKYBLOCK_TERMINAL_STATUS`, `SKYBLOCK_INVENTORY_BUTTONS`, `SKYBLOCK_CHEST_LOOTED`, `SKYBLOCK_AUTO_REQUEUE`, `SKYBLOCK_DUNGEON_BREAKER`, `SKYBLOCK_PRICE_IN_LORE`, `SKYBLOCK_DEATH_COUNTER_HUD`, `SKYBLOCK_REVIVE_HUD`, `SKYBLOCK_ENCHANTS`, `SKYBLOCK_DUNGEON_ROUTES`, `SKYBLOCK_CHAT_WAYPOINTS`, `SKYBLOCK_SEND_COORDS`, `SKYBLOCK_BURROW_SHARING`, `SKYBLOCK_BURROW_LOCATING`, `SKYBLOCK_BOSS_TIMER`, `SKYBLOCK_MINI_BOSS_ALERT`, `SKYBLOCK_FAIRY_SOULS`, `SKYBLOCK_INACTIVE_EFFIGY_DISPLAY`, `SKYBLOCK_GRAVITY_WELL_WAYPOINTS`, `SKYBLOCK_HIDE_FOOD`, `SKYBLOCK_HIDE_ARMOR`, `SKYBLOCK_VAMPIRE_SLAYER`, `SKYBLOCK_HIDE_FALLING_BLOCKS`, `SKYBLOCK_REPLACE_LAVA_TEXTURE`, `SKYBLOCK_STORAGE_HOVER_PREVIEW`, `SKYBLOCK_AUTO_COPY_RARE_DROPS`, `SKYBLOCK_WISHING_COMPASS`, `SKYBLOCK_GIANT_HP_AT_FEET`, `SKYBLOCK_PROFESSOR_GUARDIAN_HP`, `SKYBLOCK_KUUDRA_HEALTH`, `SKYBLOCK_METAL_DETECTOR`, `SKYBLOCK_COMPLETED_COMMISSIONS`, `SKYBLOCK_CREATION_DATE`, `SKYBLOCK_ITEM_ID_LORE`, `SKYBLOCK_DUNGEON_FEEDBACK`, `SKYBLOCK_FISHING_HIDE_PLAYERS`, `SKYBLOCK_FISHING_HOTSPOT_LOCATOR`, `SKYBLOCK_END_NODE_HIGHLIGHT`, `SKYBLOCK_GLOWING_MUSHROOM_HIGHLIGHT`, `SKYBLOCK_CUSTOM_MENU_CLICK`, `SKYBLOCK_MIDDLE_CLICK_GUI`, `SKYBLOCK_DUNGEON_QUALITY`, `SKYBLOCK_DUNGEON_NAMETAGS`, `SKYBLOCK_TERMINAL_SPLITS`, `SKYBLOCK_HIDE_EX_COOPS`, `SKYBLOCK_HIDE_MAGIC_SOUP_MESSAGES`, `SKYBLOCK_HIDE_PLAYERS_NEAR_NPC`, `SKYBLOCK_HIDE_OTHERS_GIFTS`, `SKYBLOCK_WEBSITE_ADBLOCK`, `SKYBLOCK_CHEST_PROFIT`, `SKYBLOCK_DIANA_MOB_HUD`, `SKYBLOCK_SPHINX_HELPER`, `SKYBLOCK_PROFILE_VIEWER`, `SKYBLOCK_KEY_GUARDIAN_TIMER`, `SKYBLOCK_TITANIUM_SPAWN_ALERT`, `SKYBLOCK_FOSSIL_EXCAVATION_SOLVER`, `SKYBLOCK_MINESHAFT_CORPSE_WAYPOINTS`, `SKYBLOCK_DIVAN_ALL_TOOLS_ALERT`, `SKYBLOCK_TREASURE_CHEST_HELPER`, `SKYBLOCK_MINING_SPEED_BOOST_ALERT`, `SKYBLOCK_SKY_MALL_BUFF_ALERT`, `SKYBLOCK_PROTECT_ITEM`, `SKYBLOCK_HIDE_MIDAS_BLOCKS`, `SKYBLOCK_PICKONIMBUS_DURABILITY`, `SKYBLOCK_WORM_SCATHA_ALERT`, `SKYBLOCK_RAFFLE_TASKS_HUD`, `SKYBLOCK_SCATHA_TRACKER_HUD`, `SKYBLOCK_GEMSTONE_PROFIT`, `KNOCKBACK_TRAINER`, `KNOCKBACK_JUMP_TIMING`, `KNOCKBACK_GROUND_GRAPH`, `KNOCKBACK_STATS`.

### render_input_ui

`TITLES`, `HEIGHT_LIMIT`, `HEIGHT_LIMIT_BEDWARS`, `HEIGHT_LIMIT_BRIDGE`, `HEIGHT_LIMIT_VANILLA`, `HEIGHT_LIMIT_SERVER`, `TAB`, `MOMENTUM`, `COLOR_SATURATION`, `SCOREBOARD`, `HIT_COLOR`, `UHC_OVERLAY`, `NAMETAG`, `TIER_TAGGER`, `AUDIO_SUBTITLES`, `ACTION_BAR`, `SHIELDS`, `PACK_ORGANIZER`, `ATTACK_INDICATOR`, `CROSSHAIR`, `CROSSHAIR_NORMAL`, `CROSSHAIR_ENEMY`, `CROSSHAIR_FRIENDLY`, `CROSSHAIR_ELYTRA`, `MOTION_BLUR`, `TNT_COUNTDOWN`, `ITEM_PHYSICS`, `AUTO_TEXT_HOTKEY`, `AUTO_TEXT_ACTIONS`, `FREELOOK`, `PVP_INFO_MELEE_CHILD`, `PVP_INFO_HEALTH_CHILD`, `PVP_INFO_PROJECTILE_CHILD`, `PVP_INFO`, `SNAPLOOK`, `FOV`, `LIGHTING`, `TIME_CHANGER`, `CHAT`, `CHAT_COMMAND_ALIASES_CHILD`, `MOB_SIZE`, `ITEM_TRACKER`, `GUI_SCALE`, `BLOCK_OUTLINE`, `GLINT_COLORIZER`, `ONE_SEVEN_VISUALS`, `ONE_SEVEN_ITEMS_LEGACY`, `ONE_SEVEN_ANIMATIONS_LEGACY`, `ONE_SEVEN_ITEMS_MODERN`, `ONE_SEVEN_ANIMATIONS_MODERN`, `SCREENSHOT`, `ZOOM`, `TEAM_VIEW`, `SHINY_POTS`, `3D_SKINS`, `BOSSBAR`, `SCROLLABLE_TOOLTIPS`, `NICK_HIDER`, `TOGGLE_SNEAK`, `TOGGLE_SNEAK_HUD_CHILD`, `PARTICLE_CHANGER`, `COOLDOWNS`, `2D_ITEMS`, `MENU_BLUR`, `HITBOX`, `WEATHER_CHANGER`, `CHUNK_BORDERS`, `FOG`, `SOUND_CHANGER`, `WAILA`, `HURT_CAM`, `DAMAGE_TINT`, `SHULKER_PREVIEW`, `HORSE_STATS`, `KILL_SOUNDS`, `KILL_SOUND_PLAYER_KILL_CHILD`, `KILL_SOUND_MELEE_KILL_CHILD`, `KILL_SOUND_BOW_KILL_CHILD`, `KILL_SOUND_ROD_KILL_CHILD`, `KILL_SOUND_THROWABLE_KILL_CHILD`, `KILL_SOUND_BEDWARS_WIN_CHILD`, `OVERLAY_MOD`, `TOTEM_ANIMATION_OVERLAY_CHILD`, `ITEM_CUSTOMIZER`, `CUSTOM_HELD_ITEMS`, `HELD_ITEM_ANIMATIONS`, `CUSTOM_DROPPED_ITEMS`, `LIGHT_OVERLAY`, `INVENTORY_MOD`, `SLOT_LOCKING`, `ITEM_DROP_PROTECTION`, `SLOT_BINDING`, `INVENTORY_HUD`, `ENCHANTMENT_SPRITE_TEXT_DECORATION`, `F3_DISPLAY`, `STORAGE_OVERLAY`, `INVENTORY_SEARCH`.

### excluded_inventory

`STAFF_XRAY`, `TICK_DEBUG`, `GECKOLIB_DEBUG_MOD`, `COMPANION_DEBUG`, `SHADER_DEBUG_MOD`, `SKYBLOCK_DEBUG_MOD`, `SKYBLOCK_DEBUG_GRAPHS`, `SKYBLOCK_CHILD_ENABLED_DEBUG`, `DEBUG_TIMER_HUD`, `SKYBLOCK_SPIRIT_LEAP_DEBUG`, `SKYBLOCK_METAL_DETECTOR_DATA_GEN`, `SKYBLOCK_RENDER_DEBUG_LAVA_WATER`, `SKYBLOCK_RENDER_DEBUG_BLOCK_COLORS`, `SKYBLOCK_RENDER_DEBUG_UTILITIES`, `SKYBLOCK_DEBUG_HUD`, `SKYBLOCK_DEBUG_HIDE_HUD`, `SKYBLOCK_DEBUG_RARITY_BACKGROUND`, `SKYBLOCK_DEBUG_HOTBAR_STACK_SIZE`, `SKYBLOCK_DEBUG_DISPLAY_ALERT`, `SKYBLOCK_DEBUG_RANDOM_LORE`, `SKYBLOCK_DEBUG_SECRET_CHIME`, `SKYBLOCK_DEBUG_HUD_SCROLLABLE`, `SKYBLOCK_DEBUG_HUD_INTERACTABLE`, `WATER_ROOM_SOLUTION_GENERATOR`, `MODS_ENABLED_DEBUG_MOD`, `OPTIMIZATION_DEBUG_MOD`, `PROFILER_DEBUG_MOD`, `FPS_DEBUG_MOD`.
