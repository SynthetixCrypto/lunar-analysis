# Settings migration, defaults and effective overrides

Study date: 2026-10-11, session 3. Static bytecode; no settings values, credentials or runtime state were read in this continuation. **Confirmed / Strong inference / Tentative / Unknown** distinguish direct evidence, interpretation, provisional attribution and missing evidence. All JVM citations below are in `lunar.jar`; offsets are decimal, method-relative. Non-code file observations have bytecode offset N/A.

## 1. Migration version and loop (JV-50)

**Confirmed.** Migrator `L._2b0ee0._cfe983._bb4487` initializes `CURRENT` (`_631465`) to the supplier-list size, not a literal: `<clinit> @0–18`. Its `$1.<init>` supplies 31 ordered steps, independently recorded in [settings-migration-steps.tsv](settings-migration-steps.tsv), rows 2–32. `_ad8b9c(i) @0–26` lazily constructs/caches a step via `Int2ObjectMap.computeIfAbsent`; `_93f583(i) @0–28` resolves the supplier.

**Confirmed.** `_cfe983(Object target,JsonObject json) @0–83` does:

```text
fileVersion = json.has("version") ? json["version"].getAsInt() : 0
if fileVersion == CURRENT: return false
for i = fileVersion; i < CURRENT; i++:
    step = _ad8b9c(i)
    if step != null:
        context.setVersion(i+1)
        step.apply(context, target, json)
return true
```

The order is **set context version first, then apply** (`@55–71`). **Confirmed:** the helper does not itself update the JSON root's `version` at each iteration; the save path writes CURRENT. **Unknown:** malformed, negative or future file-version policy is not fully established here; the exact-version early return is not a general `>= CURRENT` check (`@23–38`).

**Tentative (retained handoff observation, not re-read).** The handoff records Default `mods.json` version 31 and `settings/game/version` 31, and older Arena PvP/UHC/Hypixel Skyblock profiles with missing or version-12 metadata. Those scalar observations are not independently reproduced because the continuation's rule permits reading only settings key names/types. The **Confirmed** implementation version remains 31 from the migration list; the existing file-shape evidence is FS-02/03. Personal setting values are neither needed nor recorded here.

## 2. What the steps do

**Confirmed.** Steps are target-specific JSON rewrites before typed settings load, not a blanket transformation of every feature. For example, v3→4 and v4→5 first test `instanceof L._88f3cf._bb4487._1253fc._cfe983` (BOSSBAR), then change y only if its old value matches exactly. The step ledger preserves the full class names and key strings for all 31 transitions. Strings alone do not establish each transition's complete algorithm.

| Transition | Confirmed rewrite | Step class / method / offsets |
|---|---|---|
| 3→4 | BOSSBAR y=40 becomes 12 | `L._2b0ee0._cfe983._cfe983._1253fc._cfe983(ctx,target,json) @0–48` |
| 4→5 | BOSSBAR y=12 becomes 1 | `…_d4ca6c._cfe983(ctx,target,json) @0–46` |
| 5→6 | UHC_OVERLAY item-scale restructuring (`skullScale`/`playerHeadScale`, gold-item scales, `selectedItems`, `options`) | `…_cb9292._cfe983`; detailed method citations in the transition appendix below |
| 9→10 | General-settings `useMinecraftScale` removed if `_2683bc` is true **or** `_22e64f(false)>1` | `…_ec7e36._cfe983(ctx,target,json) @0–29` |
| 10→11 | Ping's nametag/HUD settings separated into `PING_NAMETAG` and `PING_HUD` | `…_1eb51c._cfe983`; transition appendix |
| 29→30 | HEIGHT_LIMIT/HYPIXEL_BEDWARS height-limit child restructuring | `…_88f3cf._cfe983`; transition appendix |
| 30→31 | HEIGHT_LIMIT split into BEDWARS/BRIDGE/VANILLA/SERVER configuration | `…_2ce426._cfe983`; transition appendix |

For rows using `…`, the shared prefix is `L._2b0ee0._cfe983._cfe983`. [settings-migration-bytecode-locations.tsv](settings-migration-bytecode-locations.tsv) supplies exact method signatures and Code ranges for **every** step; [settings-migration-steps.tsv](settings-migration-steps.tsv) supplies the original JVM class names. Both are static citations, not personal profile contents.

**Confirmed.** `L._02d7ad._cfe983.load(JsonObject) @0–20` combines the migrator's return value with `_cbc1da()`. When true it re-saves with `_1f5a0f(true)` after loading (`@174–183`). Root version is written by `_590f69(JsonObject) @0–9`.

**Strong inference.** Old keys in an older profile do not establish that migration is broken or that those features remain active; that profile may not have been loaded/re-saved, and read-merge-write can retain unknown keys. Sources: the above load/save path and file-I/O behavior in [java-internals.md §5](java-internals.md#5-feature-registration-settings-and-persistence) (JV-14).

## 3. Load-state and the missing-file gap (JV-51)

**Confirmed.** `L._02d7ad._cfe983._5d96a0 @0–49` first marks top-level features `LOADING_CONFIG`, then invokes config-file load. Inside `load(JsonObject) @44–170`, the manager visits every registered feature, supplies its object or a new empty object, calls `feature.load`, catches per-feature exceptions, and sets `LOADED_CONFIG` after the attempt. A missing **feature key inside an existing file** is therefore different from a missing whole file.

**Confirmed.** The missing-file branch in `L._02d7ad._d4ca6c._5d96a0()` returns without calling `load(JsonObject)` (see its bytecode citation appendix). Thus `LOADED_CONFIG` is skipped if the file does not exist. **Strong inference:** on initial startup the feature's constructor defaults remain, because no JSON has been supplied to its loader. This does not imply the final load-state remains `CONSTRUCTOR`.

**Confirmed.** After the file-load attempt, the manager still performs `_55938e(feature)` and walks the `children` trait (`_5d96a0 @50–100`; `_13ea87(children) @0–11`). `_55938e @0–161` installs or invokes the enable listener, calls `updateEnabled` on its fallback path (`@135–143`), and writes `load_state=COMPLETE` (`@148–160`). Missing `LOADED_CONFIG` is an intermediate lifecycle gap, not proof that features never finish initialization. See [module-lifecycle.md](module-lifecycle.md).

## 4. Constructor default versus stored value versus effective value (JV-52)

**Confirmed.** Defaults are built in constructors using typed factory `L._ec7e36._81676d`, not supplied by the user's config. Representative exact citations are in [additional-module-traces.md](additional-module-traces.md), [hud-math.md](hud-math.md), and the FPS/CPS/ZOOM traces in [module-lifecycle.md](module-lifecycle.md). This is a code claim, not a reading of current preferences.

**Confirmed.** `Setting.get()` is `L._ec7e36._13ea87.get @0–39`:

1. Register the read with dependency tracker `L._ba7d98._bb4487._cfe983` (`@0–1`).
2. Look up `intercept` trait `_2b6a6c` (`@4–14`).
3. Without the trait, return `_1f5b06()` (stored value); with it, use its Optional override and fall back to `_1f5b06()` (`@15–39`).

**Strong inference.** Server/Apollo/option-override machinery can therefore change the effective value without changing the stored preference. **Unknown:** all producers and precedence among the concrete intercept sources are not traced by this getter. In particular the sources and merge policy for `lunar_option_overrides.json` remain open (U-14/U-03). The getter's single-Optional fallback is **Confirmed**; full override attribution is not.

**Confirmed.** Save uses **stored**, not effective, values: `L._ec7e36._13ea87._590f69(JsonObject) @21–83` compares `_1f5b06()` with `getDefaultValue()` and encodes `_1f5b06()` only if different. Default primitive settings remove their key (`@86–98`); children can still make a nonempty settings object (`@99–157`). Thus “only non-default settings are saved” refers to the local stored value, not the server-effective value.

## 5. Existing file-I/O findings remain in force

**Confirmed by prior static trace (JV-11–15).** Feature objects are sparse, empty ones omitted, writes read/merge the existing JSON, saves run synchronously and directly through `FileWriter` rather than an observed atomic rename, and changes trigger immediate owning-file saves when profiles are ready. See [java-internals.md §5](java-internals.md#5-feature-registration-settings-and-persistence) for the full I/O and propagation trace. The sparse feature loop is independently visible in `L._02d7ad._cfe983._590f69 @12–96`; this continuation does not run a save.

**Unknown.** Crash consistency under an interrupted write, actual server override inputs, and migration outcomes for the user's inactive profiles were not observed. No dynamic or destructive test is authorized.
