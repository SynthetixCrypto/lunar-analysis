# Feature registration and support gating — static deep dive

Study date: 2026-10-11. Scope: the retained Lunar Java disassembly and saved registration/constraint inventories. **Static, read-only analysis; no Lunar code, JAR, JavaScript or native library was executed.** No installation changes, credential collection, settings-value reads, integrity analysis or anti-cheat analysis were performed. Existing reports and indexes are preserved.

## Evidence conventions and source boundary

- **Confirmed**: an instruction, declaration, resource inventory or explicitly retained structural observation supports the statement. This does not mean runtime-observed.
- **Strong inference**: the interpretation follows from multiple static facts, but an effective runtime outcome was not observed.
- **Tentative**: retained secondary evidence is incomplete or not corroborated by the inspected class body.
- **Unknown**: the stated question is not answered by this bounded static evidence.

Java citations below use method-local decimal **javap bytecode offsets**, not text-file line numbers or archive byte positions. Resources and retained structural observations use **offset N/A**. BootstrapMethods entries are classfile metadata, not instructions; their associated `invokedynamic` instruction offsets are supplied separately.

**Confirmed — source identities.** `lunar` means `C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar`; `genesis` means the adjacent `genesis.jar`. Short aliases follow the existing MD5-prefix convention documented in [session2-class-legend.md](session2-class-legend.md), not recovered original names; newly cited full class names are in [session3-class-locations.tsv](session3-class-locations.tsv). The inventories used here are [feature-registry.tsv](feature-registry.tsv), [feature-support-constraints.txt](feature-support-constraints.txt) and the prior JV/FS ledger in [evidence-index.md](evidence-index.md). Source: saved inventory/legend/ledger, offset N/A.

**Confirmed — reproducibility boundary.** Cached class text was queried with the inspected, read-only `q.py` (`meth`, `show`, `sig`) and small read-only Python selectors. The retained scratch directory is `C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad`. Relevant files are `classes.pkl`, `lunar_moonsworth.javap`, `genesis.javap`, `de.txt`, `vmeth.txt` and `verfields.json`. A focused local JDK `javap -p -v` read of the extracted generic manager class verified its lambda bindings. No new REA binary session or broad artifact reanalysis was opened. Source: inspected scripts, cached dumps and tool operations, offset N/A.

## 1. The registration path begins inside construction

**Confirmed — JV-39.** The complete superclass chain matters: the feature manager does not call `_535838()` directly in its own constructor.

| Step | Confirmed operation | Artifact / class.method @ javap offset |
|---|---|---|
| 1 | FeatureManager invokes its immediate superclass constructor. | lunar / `L._02d7ad._1253fc._1eb51c.<init>()` @0–3 |
| 2 | Generic feature-manager constructor invokes the set-backed manager constructor. | lunar / `L._02d7ad._cfe983.<init>()` @0–3 |
| 3 | Set-backed constructor invokes virtual `_535838()`, then stores its result in `_d00250`. | lunar / `L._02d7ad._21aca6.<init>()` @23–28 |
| 4 | Final generic `_535838()` invokes the FeatureManager override `_de9126()` to obtain the candidate set. | lunar / `L._02d7ad._cfe983._535838()` @0–4 |
| 5 | It removes unsupported candidates, processes each survivor, invokes `_6c713e(set)`, then returns the set. | lunar / `L._02d7ad._cfe983._535838()` @5–35 |
| 6 | Only after superclass construction returns does FeatureManager allocate/store `_b82659`, its UI payload helper. | lunar / `L._02d7ad._1253fc._1eb51c.<init>()` @4–15 |

**Strong inference — construction-order implication.** Feature instantiation and registration filtering occur during the superclass constructor's virtual call, before the FeatureManager constructor body creates its UI helper. A reconstruction should not move this filtering into later config loading merely because the concrete constructor looks short. Sources: JV-39 instruction sequence above, especially set-backed `<init>` @23–28 and FeatureManager `<init>` @4–15. This is control-flow interpretation, not a measured startup trace.

## 2. Candidate order and conditional additions

**Confirmed — JV-39.** `_de9126()` contains **119 feature-construction sites**, not an unconditional 119-member effective registry. Its initial array has length **95**, and the remaining **24** additions are individual `Set.add` sites. The saved TSV has 119 rows with distinct IDs and continuous zero-based order 0–118. Sources: lunar / `L._02d7ad._1253fc._1eb51c._de9126()` @1–3, @9–1415, @1427–1829; `feature-registry.tsv`, offset N/A; read-only counts against `de.txt`, offset N/A.

| Phase | Confirmed candidates and condition | `_de9126()` offsets in lunar |
|---|---|---|
| Initial ordered batch | 95 candidates, TSV order 0–94, from `REPLAYMOD` to `KNOCKBACK_TRAINER`; the array is handed to `_cfe983(Feature...)`. “Always” means an unconditional construction site here, **not exemption from support filtering**. | @1–1415 |
| Non-production additions | `PANORAMA_MAKER` plus 16 debug/specialized candidates, TSV order 95–111; skipped when `_c1461e` is true. | production test @1419–1422; additions @1427–1687 |
| Additional Turbo condition | `TURBO_RENDERING_DEBUG_MOD`, within the non-production block, additionally requires `MC_VERSION >= 8`. | comparison @1549–1554; construction/add @1558–1565 |
| Radio | `RADIO`, TSV order 112, added only if `L._02d7ad._bb4487._21aca6.RADIO.isEnabled()` is true. | test @1693–1699; construction/add @1704–1715 |
| Unconditional tail | Six debug-named candidates, TSV order 113–118, appended outside both the production and Radio branches. | @1723–1829 |

**Confirmed — production flag identity.** `_c1461e` is the Boolean-parsed `PRODUCTION` build-data entry, not a guessed developer-mode flag. Source: lunar / `L._1e73d7._cfe983.<clinit>()` @343–358. **Unknown — effective values.** This pass did not evaluate the running flag or Radio flag, or read user-configured values; the branches describe static conditions only. Source boundary: the same initializer and `_de9126()` @1419–1422, @1693–1699.

**Confirmed — ordinal, not a version number.** `MC_VERSION` is assigned from `getOrdinal()` in the non-JUnit initialization branch; the JUnit branch sets it to zero. Source: lunar / `L.util._e93d3c.<clinit>()` @33–58. In the retained 40-version table, ordinal 8 denotes `v1_17_0`, not Minecraft 1.8. Source: genesis / `versions.conf`, offset N/A (FS-04), and `ML._cb9292._21aca6._601d9f(Path)` @1100–1119 for the `v1_17_0` constant binding.

### Non-production insertion order

**Confirmed — declaration/inventory scope only.** These are the ordered additions and their construction/`Set.add` offsets in lunar / `L._02d7ad._1253fc._1eb51c._de9126()`. IDs and corresponding aliases are retained in `feature-registry.tsv` (offset N/A). No debug-feature behavior is analyzed here.

| Order | Identifier | `new` / `Set.add` offsets |
|---:|---|---|
| 95 | `PANORAMA_MAKER` | @1427 / @1439 |
| 96 | `HUD_DEBUG` | @1446 / @1453 |
| 97 | `MC_DEBUG_RENDERER` | @1461 / @1473 |
| 98 | `RAYCAST_DEBUG` | @1480 / @1487 |
| 99 | `TRANSFORMATION_DEBUG` | @1494 / @1501 |
| 100 | `FEATURE_FLAG_DEBUG` | @1508 / @1515 |
| 101 | `SETTINGS_OVERRIDE_DEBUG` | @1522 / @1529 |
| 102 | `GRAPH_DEBUG_MOD` | @1536 / @1543 |
| 103 | `TURBO_RENDERING_DEBUG_MOD` | @1558 / @1565; also ordinal >=8 |
| 104 | `BASIC_DEBUG_MOD` | @1573 / @1584 |
| 105 | `EVENT_DEBUG_MOD` | @1591 / @1598 |
| 106 | `APOLLO_DEBUG_MOD` | @1606 / @1617 |
| 107 | `DYNAMICLISTENER_DEBUG_MOD` | @1624 / @1631 |
| 108 | `TICK_DEBUG` | @1638 / @1645 |
| 109 | `PATHFINDING_DEBUG` | @1652 / @1659 |
| 110 | `COSMETIC_DEBUG_MOD` | @1666 / @1673 |
| 111 | `OPTION_DUMP_MOD` | @1680 / @1687 |

### The six unconditional debug-named additions

**Confirmed — JV-39.** All six full identifiers must remain distinct from the 16 non-production debug/specialized additions. “Unconditional” applies to this insertion phase; the generic support filter still follows. Source: lunar / FeatureManager `_de9126()` at the offsets below; ID mapping in `feature-registry.tsv`, offset N/A.

| Identifier | Class alias | `new` / `Set.add` offsets |
|---|---|---|
| `MODS_ENABLED_DEBUG_MOD` | `L._88f3cf._bb4487._a1dd3a._429bf0` | @1723 / @1734 |
| `OPTIMIZATION_DEBUG_MOD` | `L._88f3cf._bb4487._a1dd3a._bb4487._590f69` | @1742 / @1753 |
| `SKYBLOCK_DEBUG_MOD` | `L._88f3cf._bb4487._23f752._cfe983` | @1761 / @1772 |
| `FPS_DEBUG_MOD` | `L._88f3cf._bb4487._a1dd3a._21aca6._cfe983` | @1780 / @1791 |
| `GECKOLIB_DEBUG_MOD` | `L._88f3cf._bb4487._a1dd3a._590f69._21aca6` | @1799 / @1810 |
| `SHADER_DEBUG_MOD` | `L._88f3cf._bb4487._a1dd3a._1253fc._cfe983` | @1818 / @1829 |

**Confirmed — insertion order.** The varargs helper uses `Sets.newLinkedHashSet()`, `Arrays.asList(array)` and `LinkedHashSet.addAll`. Source: lunar / `L._02d7ad._cfe983._cfe983(F...)` @0–14. **Strong inference — effective-order implication.** Conditional omissions and the subsequent `removeIf` leave an insertion-order subsequence of the candidate list, subject to ordinary set equality/deduplication semantics; this is not a claim that all candidates survive. Sources: the helper @0–14, `_de9126()` @1415–1836, `_535838()` @5–16.

## 3. The formerly unresolved `removeIf` filter

**Confirmed — JV-40.** The filter removes a feature exactly when its optional `support` trait is present and its static supported Boolean is false. A feature without that trait is not removed by this predicate.

| Predicate stage | Confirmed detail | Artifact / class.method @offset |
|---|---|---|
| Bind removal predicate | BootstrapMethods entry 0 binds to `_81676d(Feature)`; its call site supplies the predicate to `removeIf`. | lunar / `L._02d7ad._cfe983._535838()` @6–11; BootstrapMethods #0, metadata offset N/A |
| Read support trait | Fetch optional trait key `_290b8b`, map its present value, default the removal decision to false. | lunar / `L._02d7ad._cfe983._81676d(Feature)` @0–30 |
| Bind mapped function | BootstrapMethods entry 5 binds to `_cfe983(Support)`. | same class / `_81676d(Feature)` @9–14; BootstrapMethods #5, metadata offset N/A |
| Negate static support | `_cfe983(Support)` returns `!support._951ef4()`. | lunar / `L._02d7ad._cfe983._cfe983(L._88f3cf._ba7d98)` @0–17 |
| Read immutable result | `_951ef4()` returns final `_2cc01e`, supplied at construction. | lunar / `L._88f3cf._1e73d7._ba7d98._951ef4()` @0–4; `<init>(boolean,server)` @4–13 |
| Process survivors | BootstrapMethods entry 1 binds the survivor consumer to virtual `_df21a7(Feature)`; `_6c713e(set)` follows. | lunar / `L._02d7ad._cfe983._535838()` @17–31; BootstrapMethods #1, metadata offset N/A |

**Confirmed — server is not tested here.** Neither the removal predicate nor its mapped function calls the support trait's server-comparison method. Sources: lunar / generic manager `_81676d(Feature)` @0–30 and `_cfe983(Support)` @0–17. **Strong inference — lifecycle distinction.** A server-bound, statically supported feature can remain registered while being disabled outside its target server; registration and active enablement are separate decisions. Sources: those predicate bodies plus `L._88f3cf._cfe983.updateEnabled()` @39–90, detailed below.

## 4. Support builder semantics

**Confirmed — JV-41.** `L._88f3cf._ba7d98._a37102()` creates `L._88f3cf._ba7d98$_cfe983`. The builder starts with supported=true, modules=null and server=null. Building returns `L._88f3cf._1e73d7._ba7d98(supported,server)` through its `_cfe983(boolean,server)` factory. Sources: lunar / support interface `_a37102()` @0–7; builder `<init>()` @4–16; builder `_2b01f6()` @103–111; implementation factory @0–9 and constructor @4–13.

| Builder operation | Confirmed semantics | lunar / builder method @offset |
|---|---|---|
| `_21aca6(int...)` | Supported iff the current `getMinecraftVersion().getOrdinal()` occurs in the supplied list. An empty allowed list produces false. | @0–54 |
| `_590f69(int...)` | Supported iff the current ordinal does not occur in the supplied denied list. An empty denied list produces true. | @0–54 |
| `_88f3cf(String...)` | Store modules and set `_34410f=true`: require at least one listed module to be present. | @0–28 |
| `_2ce426(String...)` | Store modules and set `_34410f=false`: require at least one listed module to be absent. This is **not** an all-modules-absent rule for multi-element lists. | @0–28 |
| Either module setter again | Throw `UnsupportedOperationException` if the modules field is already non-null. | both setters @0–16 |
| `_21aca6(server)` | Store one optional server; throw if the field is already non-null. | @0–23 |
| `_2b01f6()` ordinary path | Start with the version-derived supported flag. Only if true and modules is non-null/nonempty, scan modules; retain support iff any `hasModule(name)` result equals `_34410f`. Return that Boolean and the stored server. | @27–111, especially @78–102 |

**Confirmed — version setters overwrite, rather than accumulate.** Each allowed/denied setter directly writes `_a1a585` on both its match and no-match paths. Successive calls therefore replace that Boolean; the module test is combined later during build. Sources: lunar / builder `_21aca6(int...)` @35–50, `_590f69(int...)` @35–50 and `_2b01f6()` @27–102. A reconstruction must not automatically turn repeated version setter calls into an intersection.

**Confirmed — module delegation.** `L.util._e93d3c.hasModule(String)` returns false when `_2683bc` is true; otherwise it delegates to `ML.ichor._13ea87.hasModule(String)` and returns that result. Source: lunar / `L.util._e93d3c.hasModule(String)` @0–21. **Unknown — effective module membership.** No running Ichor pipeline/module set was queried. Source boundary: this delegation body and builder `_2b01f6()` @78–102.

### Static generation and JUnit-context overrides

**Confirmed — JV-41, not a bypass recommendation.** The support builder contains two declared development/test-context branches; their existence does not prove either was active in the user's launch.

| Branch | Confirmed source behavior | Artifact / class.method @offset |
|---|---|---|
| Generation path present | A non-null `_44f211` makes build return `(true,null)`, skipping ordinary version/module checks and discarding the optional server for this result. | lunar / builder `_2b01f6()` @0–11 |
| Generation-path source | `_44f211` is derived from a nonempty `System.getProperty("lunar.generateModClasses")`, otherwise null. This is a source-declared property name, not a collected settings value. | lunar / `L._02d7ad._13ea87._bb4487.<clinit>()` @14–43 |
| JUnit-context flag | A true `_2683bc` makes build return `(true,storedServer)`, also skipping ordinary checks. | lunar / builder `_2b01f6()` @12–26 |
| JUnit detection | `_4d6574()` tests whether any current-thread stack-frame class name starts with `org.junit.`; its result initializes `_2683bc`. | lunar / `L.util._e93d3c._4d6574()` @0–42; `<clinit>()` @0–3 |

**Unknown — active overrides.** Property contents and the running stack were not read or generated. Sources: the declared static branches above; no runtime evidence was collected.

## 5. Version helpers and constant resolution

**Confirmed — JV-42.** The common builder interface converts version objects to ordinals and builds inclusive ordinal lists. The meaning of `LATEST` is resolved from shipped version metadata, not the current calendar date.

| Helper | Confirmed meaning | Artifact / class.method @offset |
|---|---|---|
| `_83cb4e(n)` | Allow ordinal n through `LATEST.getOrdinal()`, inclusive. | lunar / `L.util._c8175c._83cb4e(int)` @0–14; `_2ce426(int,int,boolean)` @0–56 |
| `_bb4487(v)` | Allow from version v through `LATEST`; delegated through the version-range overload and ordinal conversion. | lunar / `L.util._c8175c._bb4487(version)` @0–11; `_cfe983(version,version,boolean)` @0–24; `_cfe983(version...)` @0–35 |
| `_0a1c78()` | Allow exactly the 1.8 ordinal, plus every ordinal from 1.21.2 through `LATEST`, inclusive; it is **not** a general 1.8-and-newer range. | lunar / `L.util._c8175c._0a1c78()` @8–60 |
| Enum allowed list | Convert each version to its ordinal, then invoke `_bb4487(int[])`, whose builder bridge delegates to allowed-list `_21aca6(int...)`. | lunar / `L.util._c8175c._cfe983(version...)` @13–30; builder `_bb4487(int[])` @0–5 |
| Enum denied list | Convert each version to its ordinal, then invoke `_1e73d7(int[])`, whose builder bridge delegates to denied-list `_590f69(int...)`. | lunar / `L.util._c8175c._21aca6(version...)` @13–30; builder `_1e73d7(int[])` @0–5 |

**Confirmed — named constants.** Genesis `ML._cb9292._21aca6._601d9f(Path)` binds `_d6bc66` to `v1_12` @1034–1053, `_76344d` to `v1_8` @946–965, `_071482` to `v1_21_2` @1496–1515 and `_6626d0` to `v1_7` @924–943. `_817c06` is assigned from the version marked latest @865–905. Source: `genesis.jar`, retained `vmeth.txt`; `versions.conf` metadata (offset N/A, FS-04) and `verfields.json` (offset N/A). In this retained table `LATEST` corresponds to `v26_2`, ordinal 39; ordinal 30 is `v1_21_6`, and ordinal 33 is `v1_21_9`. These are build-specific constants, not future compatibility promises.

## 6. Per-feature constraint declarations

**Confirmed — JV-42, declaration scope.** The following 17 entries have matching support-builder consumer bodies in the retained class disassembly. Each cited method takes `L._88f3cf._ba7d98$_cfe983`; offsets are local to that consumer method. All classes in this table are from **lunar.jar**. The saved ID/alias correlations are in `feature-support-constraints.txt` (offset N/A). These declarations do not establish complete feature algorithms, successful rendering or effective runtime state.

| Identifier | Confirmed declared constraint | Class / consumer method @offset |
|---|---|---|
| `2D_ITEMS` | Deny 1.7. | `L._88f3cf._bb4487._000018._cfe983._cfe983(builder)` @1–11 |
| `ATTACK_INDICATOR` | Allow 1.12 through latest. | `L._88f3cf._bb4487._590f69._21aca6._cfe983(builder)` @1–4 |
| `AUDIO_SUBTITLES` | Allow 1.12 through latest. | `L._88f3cf._bb4487._ef5392._cfe983._cfe983(builder)` @1–4 |
| `HYPIXEL_MOD` | Allow {1.8} plus 1.21.2 through latest; optional server=HYPIXEL. | `L._88f3cf._bb4487._32565b._1e73d7._21aca6(builder)` @1–10 |
| `INVENTORY_SEARCH` | Allow ordinal 1 through latest (1.8+ in this table). | `L._88f3cf._bb4487._767dc1._cfe983._cfe983._21aca6._590f69(builder)` @1–2 |
| `ONE_SEVEN_VISUALS` | Deny 1.7. | `L._88f3cf._bb4487._3bf032._590f69._cfe983(builder)` @1–11 |
| `PANORAMA_MAKER` | Allow 1.17.0 through latest; separate registry gate requires non-production. | `L._88f3cf._bb4487._4cf8c3._cfe983._cfe983(builder)` @1–4; FeatureManager `_de9126()` @1419–1439 |
| `QUICKPLAY` | Allow {1.8} plus 1.21.2 through latest; optional server=HYPIXEL. | `L._88f3cf._bb4487._41e3dc._21aca6._cfe983(builder)` @1–10 |
| `REPLAYMOD` | Require module `replaymod` to be present. | `L._88f3cf._bb4487._b03e9c._cfe983._cfe983(builder)` @1–10 |
| `SERVER_COMMAND_CONFIG` | Allow ordinal 30 through latest (1.21.6+ in this table). | `L._88f3cf._1253fc._21aca6._cfe983._cfe983(builder)` @1–3 |
| `SHIELDS` | Allow 1.12 through latest. | `L._88f3cf._bb4487._381fad._cfe983._cfe983(builder)` @1–4 |
| `SHULKER_PREVIEW` | Deny 1.7 and 1.8. | `L._88f3cf._bb4487._d930e6._cfe983._cfe983(builder)` @1–17 |
| `SKYBLOCK` | Allow ordinal 33 through latest (1.21.9+ in this table). | `L._88f3cf._bb4487._23f752._590f69._590f69(builder)` @1–3 |
| `TIER_TAGGER` | Deny 1.7. | `L._88f3cf._bb4487._569ad9._1e73d7._1e73d7(builder)` @1–11 |
| `TOTEM_ANIMATION_OVERLAY_CHILD` | Allow 1.12 through latest. | `L._88f3cf._bb4487._f8005d._d4ca6c._cfe983(builder)` @1–4 |
| `TOTEM_COUNTER` | Allow 1.11 through latest. | `L._88f3cf._bb4487._5a1b50._21aca6._cfe983(builder)` @1–4 |
| `TURBO_RENDERING_DEBUG_MOD` | Allow ordinal 8 through latest (1.17.0+); separate registry gate requires non-production and ordinal >=8. | `L._88f3cf._bb4487._a1dd3a._cfe983._cfe983._cfe983(builder)` @1–3; FeatureManager `_de9126()` @1549–1565 |

**Confirmed — top-level versus other declarations.** `INVENTORY_SEARCH`, `SERVER_COMMAND_CONFIG` and `TOTEM_ANIMATION_OVERLAY_CHILD` are not rows of the 119-entry top-level `feature-registry.tsv`; the constraint inventory includes more than top-level candidates. Source: bounded comparison with `feature-registry.tsv`, offset N/A. **Unknown — exhaustive nested registration.** This pass does not establish that the top-level `removeIf` is recursively applied to every child/container; the inspected `_535838()` operates on its supplied set. Sources: lunar / generic manager `_535838()` @0–35; saved constraint inventory, offset N/A.

**Tentative — one uncorroborated saved row.** `feature-support-constraints.txt` additionally attributes a `versionsAllowed(enum)` declaration to `SKYBLOCK_STORAGE_HOVER_PREVIEW`, class `L._88f3cf._bb4487._23f752._cfe983._2f4182._ba7d98`. The saved summary supplies neither a method identity nor javap offsets for that alleged declaration, so its offset is **N/A (secondary summary only)** and no allowed-version set is asserted here. **Confirmed — discrepancy boundary:** the inspected cached class body contains no `L._88f3cf._ba7d98` support-builder reference. Its `_bb4487(L._d4ca6c._cfe983._590f69._e62626$_cfe983)` @145 instead calls a nested object's `_d6c61c():L._ec7e36._429bf0`, a different method/return type from support building. Source: lunar / retained class body and `lunar_moonsworth.javap`, corresponding class block; summary resource offset N/A. **Unknown:** why the secondary summary differs, and whether another uninspected implementation declares such a constraint. This row is excluded from the 17 corroborated declarations rather than assigned an invented offset.

## 7. Server support controls enablement, not registration

**Confirmed — JV-41.** The support implementation stores the optional server independently of its final static-supported Boolean:

- `_951ef4()` returns supported @0–4.
- `_7aa5f3()` returns whether the stored server is non-null @0–12.
- `_cfe983(server)` compares the supplied server object with the stored server by reference equality @0–13.

Source for all three: lunar / `L._88f3cf._1e73d7._ba7d98`.

**Confirmed — active-state gate.** `L._88f3cf._cfe983.updateEnabled()` reads the optional support trait @39–49. If it has a server @54–60, it obtains the current server from `L._dd3308._1e73d7._657fd1()` @63–66. A null current server or failed comparison sets `enabled=false`, invokes `_688792()` and returns @67–90. This code does not remove the feature from the manager's set. Source: lunar / feature base `updateEnabled()` @39–90, compared with generic manager `_535838()` @5–16.

**Strong inference — Hypixel example.** The HYPIXEL_MOD and QUICKPLAY consumers combine a version allowance used for static support with a HYPIXEL server used during `updateEnabled`. Thus joining another server is not, by itself, the registration-time removal criterion traced here. Sources: their consumers @1–10 in section 6; support builder `_2b01f6()` @103–111; feature base `updateEnabled()` @39–90; removal predicate `_81676d()` @0–30. **Unknown:** observed server transitions, current-server identity and event timing were not collected.

## 8. Structural corroboration and validation

**Confirmed — FS-07, retained observation rather than a new settings read.** The task handoff reports that the previously inspected **Default mods key order matches a registry subsequence**, with `REPLAYMOD` absent. Its source is `C:\Users\Admin\.lunarclient\settings\game\Default\mods.json`, key names/order only, **offset N/A**. Prior FS-03 independently records 90 root keys (`version` plus 89 feature objects), sparse objects and nested children; source: `evidence-index.md` and `java-internals.md`, offset N/A. This pass did **not** reopen the settings file or read any settings values, and does not present the handoff's order comparison as a freshly repeated test.

**Confirmed — sparse-save mechanism.** The generic manager serializer visits its registered set, serializes a fresh per-feature object and only adds it to the root when that object has a nonempty entry set. Source: lunar / `L._02d7ad._cfe983._590f69(JsonObject)` @12–80, especially @58–80. **Strong inference:** a persisted key-order subsequence is consistent with insertion-ordered registration plus sparse saving; it is not an exhaustive active-feature list. Sources: serializer @12–80; varargs helper @0–14; FS-07 retained structural observation, offset N/A.

**Strong inference — ReplayMod corroboration, not proof from absence.** The absence of the saved `REPLAYMOD` key is consistent with its declared module requirement and registration filtering. It does **not** prove that `replaymod` was absent or that removal caused the missing key: sparse serialization can also omit an empty feature object. Sources: lunar / ReplayMod support consumer @1–10, builder `_2b01f6()` @27–111, generic manager removal predicate @0–30, serializer @58–80; retained key observation FS-07, offset N/A. **Unknown:** the effective module set and the cause of this particular missing saved key.

### Validation actually performed in this pass

| Status | Check and result | Source / offset |
|---|---|---|
| Confirmed | TSV has 119 rows, 119 distinct IDs, and order exactly 0–118. | `feature-registry.tsv`, offset N/A |
| Confirmed | TSV condition counts are 95 initial, 16 `!PRODUCTION`, 1 `!PRODUCTION && MC_VERSION>=8`, 1 Radio, 6 unconditional tail. The first two development categories together mean Panorama +16 debug/specialized entries. | `feature-registry.tsv`, offset N/A |
| Confirmed | Saved registry disassembly has 119 feature `new` sites and 24 `Set.add` sites. | `de.txt`; lunar / FeatureManager `_de9126()` @9–1829 |
| Confirmed | Removal-predicate, mapped-support-function and survivor-consumer bindings verified with local JDK javap BootstrapMethods entries 0, 5 and 1. | lunar / generic manager `_535838()` @6, @19; `_81676d()` @9; classfile metadata offset N/A |
| Confirmed | Seventeen constraint declarations have matching named consumer bodies and actual offsets; the extra storage-preview summary was not promoted to Confirmed. | Section 6's lunar class/method offsets; summary resource offset N/A |
| Confirmed | Version helper endpoints and key constant bindings were checked against retained disassembly and version metadata. | Section 5's lunar/genesis method offsets; `versions.conf` and `verfields.json`, offset N/A |
| Unknown | Fresh revalidation of Default key order, effective flags/modules/server state and live registry counts. Not performed by design. | FS-07 source boundary and static branches cited above; runtime offset N/A |

## 9. Ledger cross-reference

The following analyst ledger IDs are appended in [evidence-index.md](evidence-index.md), not newly minted REA Evidence IDs. Existing JV-10/JV-11/JV-09/FS-03 remain preserved; these additions narrow their formerly unresolved points.

| ID | Classification | Finding / source anchors | Limit |
|---|---|---|---|
| **JV-39** | Confirmed | Constructor-time ordered registration; 95 varargs + non-production Panorama/16 debug + Radio +6 unconditional debug-named tail. lunar / FeatureManager `<init>` @0–15, generic `<init>` @0–3, set-backed `<init>` @23–28, FeatureManager `_de9126` @1–1836; TSV offset N/A. | Candidate construction sites, not a measured effective member count. |
| **JV-40** | Confirmed | `removeIf` means optional support present and `!_951ef4()`; no support defaults to keep. lunar / generic manager `_535838` @5–16, `_81676d` @0–30, `_cfe983(Support)` @0–17; BootstrapMethods #0/#5 metadata offset N/A. | Operates on supplied set; no claim of exhaustive child pruning. |
| **JV-41** | Confirmed | Support-builder version/module Boolean plus optional server; module-any-present/any-absent semantics; generation/JUnit branches; server affects enablement separately. lunar / builder methods in section 4, `_2b01f6` @0–111, implementation constructor @4–13, feature `updateEnabled` @39–90, util `hasModule` @0–21 and `_4d6574` @0–42. | Effective flags, properties, module membership and server state unobserved. |
| **JV-42** | Confirmed | Inclusive version helpers, resolved version constants and 17 corroborated support consumers. lunar / `L.util._c8175c` helper offsets in section 5; genesis / version `_601d9f` constant offsets in section 5; individual lunar consumers in section 6. | Storage-preview secondary row remains Tentative; declarations are not complete feature behavior. |
| **FS-07** | Confirmed retained observation; Strong inference interpretation | Prior Default key order is a registry subsequence; ReplayMod key absent; sparse serializer explains why absence is not proof. Default `mods.json` key-structure observation and prior FS-03, offset N/A; lunar / generic serializer @12–80. | Not freshly repeated; no settings values read. |

**Unknown — remaining questions.** Effective per-launch candidate/survivor counts, full recursive child-support handling, event-driven server re-enablement timing, the storage-preview summary discrepancy and complete per-feature behavior remain outside this pass. Sources bounding those unknowns: generic manager `_535838()` @0–35, builder `_2b01f6()` @0–111, feature `updateEnabled()` @39–90 and the saved inventories (offset N/A). None is filled with runtime assumptions.
