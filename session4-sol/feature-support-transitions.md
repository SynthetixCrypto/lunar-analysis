# Feature support and override transitions — session 4

Artifact: `lunar.jar`, static bytecode only. **Confirmed** = branch implementation; **Strong inference** = conditional consequence; **Unknown** = not recovered/observed. All aliases map to original JVM names in [mapping.json](evidence-support/mapping.json); full cache, fresh `javap -c/-v`, alias dumps and lambda bindings are retained in [evidence-support](evidence-support/). Personal settings, `lunar_option_overrides.json` and server traffic were **not** read. Prior registration filtering is already resolved and not repeated here.

## Four states must not be conflated

**Confirmed — S4-SUPPORT-01.** `L._88f3cf._cfe983.updateEnabled @0–191` computes its cached effective flag in this precedence:

1. Disabled parent → false and return (`@0–38`).
2. Server-qualified support with missing/wrong current server → false (`@39–90`).
3. Present dynamic allowance trait with false `_98d4d1()` → false (`@91–124`).
4. Present Boolean override → that value (`@125–178`).
5. Otherwise interface default enablement (`@179–191`).

Thus a forced true override cannot bypass the parent/server/dynamic allowance gates. Static `_951ef4()` support is registration-time filtering from session 3; it is not re-read here. `updateEnabled()` is not itself a generic user-toggle setter or a manager membership mutation. Its `_688792 @0–25` only handles a lifecycle/display trait when no handler trait exists. Universal “calling updateEnabled always registers/unregisters handlers” is unsupported.

Stored toggle (`L._88f3cf._2ce426.isEnabled`), cached effective `feature.enabled`, override Optional and handler-active flag are distinct. Named branches below establish which is changed; no report assumes they are interchangeable.

## `setFlipped` is server-specific remembered toggle intent

**Confirmed — S4-SUPPORT-02.** `L._88f3cf._1e73d7._ba7d98._83eb1a @0–4` returns mutable `_045710`, and `setFlipped @0–5` writes it. It is not the final supported boolean or the server-comparison result.

`L._88f3cf._2ce426._cfe983(feature,requested)` handles server-qualified **requested=true** first. No/wrong server: invert flipped and return `@30–71`, **without changing ordinary toggle or effective state through the later path**. Matching server: invert flipped and continue `@72–103`. Request=false bypasses that entire flipping gate. This makes flipped a deferred intent marker rather than a universal “feature currently active” indicator. The second comparison’s impossible-with-stable-server alternative `@106–118` is preserved in raw code; server concurrency was not observed.

Server-manager `L._dd3308._1e73d7` constructor binds events `_00e05b`, `_c8175c`, `_1e73d7` (`<init> @4–37`; verbose BootstrapMethods #0–2). Brand-event handler `_590f69(_c8175c) @0–51` iterates server enum and sets current server on first recognized non-null brand. If resulting current server is null, it returns `@60–76`; this handler does not first unconditionally clear a previous match. Real producer sequence remains Unknown.

On matching server arrival, recursive `_cfe983(server,feature) @0–77` samples the ordinary toggle; if true, calls toggle handling with true, then writes flipped back to the sampled true/false. It recursively traverses children `@82–143`. On disconnect handler `_cfe983(_1e73d7) @0–21` captures old server, clears current, then applies `_21aca6(oldServer,feature)` to all roots and finally refreshes `@26–73`.

Disconnect recursion `_21aca6(server,feature) @0–103` applies only to matching server-qualified features with an ordinary enabled toggle: save flipped, set ordinary false, and if saved flipped was true set ordinary true again and keep flipped true. Children recurse `@103–164`. **Strong inference:** user intent can remain stored true outside the supported server while the effective server gate makes the feature inactive; this is not registration removal.

## Refresh clears server override slots, then recomputes descendants

**Confirmed — S4-SUPPORT-03.** `L._dd3308._1e73d7._12d046 @0–60` first invokes a clear pass (`_f636dc`, BootstrapMethods #3) over roots, then `_6c713e(feature)` over roots. Clear helpers remove **SERVER** override values by passing null (`_590f69(feature,interceptor) @0–12`, `_21aca6(setting,interceptor) @0–12`), visit setting interceptors and recurse children (`_f636dc @0–63`; `_dcf582(setting) @0–19`). Client override categories are not universally cleared by this server pass.

Recompute `_6c713e @0–34` calls feature.updateEnabled then traverses descendants via child trait. World-event `_21aca6(_00e05b) @0–11` refreshes only when payload `_cc2398()` is true. These are event-triggered code paths; no live order between brand arrival, world readiness, Apollo updates and disconnect was collected.

## Ordinary toggle changes synchronize subscriptions and children

**Confirmed — S4-SUPPORT-04.** Toggle method `L._88f3cf._2ce426._cfe983(feature,requested) @123–162` refuses a true request if dynamic allowance is false, calling only updateEnabled. On the normal changing-state path it updates transition flag (`@364–366`), invokes handler trait (`@371–412`), recalculates effective state (`@417–418`), calls feature transition hook `_41ba55 @423–425`, propagates child toggles (`@430–539`) and posts feature-change event `_d4ca6c._cfe983._1253fc._bb4487 @547–560`. A child is re-enabled only if its own ordinary toggle was enabled; disabling cascades. Lifecycle COMPLETE and parent-state checks gate whether a transition is deemed necessary (`@235–359`). Input-associated key bindings are explicitly released `@177–232` before this decision.

Handler trait `L._88f3cf._1e73d7._429bf0._cfe983(feature,boolean,boolean) @0–107` changes its desired flag only if different. Its internal `_cfe983(lifecycle,logging,children,parent) @0–165` computes actual subscribed = desired AND lifecycle-allowed AND ancestor-handler-active (`@0–50`), invokes subscribe `_6e84a9` or unsubscribe `_4ee67b` when that changes (`@52–83`), then propagates handler state to descendants (`@83–165`, `_dcf582 @0–124`). Bus changes during dispatch follow the session-4 deferred-mutation behavior, so an unsubscribed Consumer may still exist in the current captured event array.

**Unknown / important limit:** effective-state recompute alone is not equivalent to this toggle lifecycle. Individual override/setting listeners can trigger additional propagation; whether every forced-enabled or forced-disabled source invokes the same transition hook/event requires source-by-source confirmation. Do not claim one universal atomic transaction across settings, effective flags, children and subscriptions.

## Apollo/metadata overrides have category priority and restoration

**Confirmed — S4-SUPPORT-05.** Feature Boolean interceptor is `L._88f3cf._1e73d7._a140a8`, **not** dynamic condition class `_a1dd3a`. It stores an EnumMap of override entries. `_2a1335 @19–85` returns the first entry whose Optional value is non-null. Enum order (`L._c8175c._cfe983._21aca6.<clinit> @0–67`, `$values @0–34`) is:

`SERVER → CLIENT_INTERNAL → CLIENT_REMOTE → CLIENT_CRITERIA → CLIENT_OVERRIDE`.

Under EnumMap’s enum-order iteration semantics, earlier non-null categories win. Do **not** infer from the name CLIENT_OVERRIDE that it always has greatest priority. This order is confirmed for this Boolean interceptor; not a universal policy for all setting types.

`_a140a8._cfe983(feature,category,Boolean) @0–388` rejects cases without toggle, remembers the original ordinary toggle on first non-null override (`@176–189`), inserts/clears the category (`@114–210`), optionally broadcasts (`@213–270`), and compares old/new selected overrides (`@273–290`). Changed selection propagates to enabled-setting interceptor (`@316–348`); if all selected overrides disappear, restores the remembered ordinary value and clears that saved value (`@349–377`). It then updates feature/descendants via `_6c713e @0–34` (`@380–382`). Restore is conditional on selected-value change and available enabled setting; this is not unconditional reset-to-default.

Per-category holder `L._c8175c._cfe983._590f69._0ee36d @0–22` clears active value/category but retains criteria predicate. Predicate update `_cfe983(Predicate,T) @0–45` OR-combines non-null predicates, replaces criteria value, and null predicate resets its predicate. Predicate slots and direct active override slots differ. Feature criteria setter `_a140a8._cfe983(Predicate,Boolean) @0–45` creates CLIENT_CRITERIA entry; it does not itself perform updateEnabled.

**Confirmed — S4-SUPPORT-06.** Remote metadata handler `L._02d7ad._d4ca6c._cfe983._13ea87._21aca6(JsonObject,Predicate) @0–422` resolves migrated/actual feature IDs (`@64–117`), reads `enabled` schema, installs CLIENT_REMOTE override when predicate is null (`@125–165`), or criteria override with explicit recompute when predicate exists (`@168–191`). `properties` contains recursive child and setting overrides (`@196–413`). Setting entries are skipped when lacking interceptor or carrying exclusion trait `_5c48a8 @330–360`; migrated property identifiers are resolved as needed `@372–393`. These are source-declared key names/algorithms, not user values.

Dynamic allowance `L._88f3cf._1e73d7._a1dd3a` tracks dependencies through `_ba7d98._bb4487`; `_91843f @0–101` recomputes condition, returns if unchanged, waits for COMPLETE, then updates effective state directly when no toggle, otherwise calls toggle logic with `ordinaryEnabled && allowed`. This proves dependency-driven transitions exist, not their live trigger ordering.

## Status and next questions

Server flipping, remembered intent, refresh clearing, override precedence/restoration, enabled-gate order and normal toggle/subscription propagation are **resolved within the cited classes**. Actual override payload provenance and file content remain Unknown by design. Remaining useful static work: enumerate every override producer and verify which invokes normal toggle lifecycle versus effective recompute, including exclusions/criteria; inspect metadata removal/reset paths and specialized setting interceptors. No personal overrides or runtime transitions are needed to make those next static checks.
