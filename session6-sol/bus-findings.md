# Session 6 — Event-bus caller and failure audit

Static only. JVM offsets are method-local decimal. `L`/`ML` aliases resolve to original JVM names and exact class hashes in [focused-manifest.json](evidence-bus/focused-manifest.json). Fresh verbose javap and retained readable code are beside that manifest. No target execution or synthetic reproduction was performed.

## G-11: exact caller audit

**Confirmed within the 8,095-class retained disassembly boundary.** The focused search uses exact bus owner and JVM descriptors, rather than common obfuscated method aliases. [focused-callers.json](evidence-bus/focused-callers.json) retains each enclosing body. An earlier broad `bus-api-callers.json` is preserved but contains alias collisions and is not a completeness source.

| API | Callers found | Classification |
|---|---|---|
| Mutable map `_ef97c4()` | One: `L._88f3cf._bb4487._a1dd3a._21aca6._21aca6._21aca6._f54c89 @26` | Diagnostic read. Explicitly acquires bus lock @17–18, snapshots entry set into ArrayList @21–35, sorts and formats listener counts/priorities/callback class names; unlocks normal @247–248 and exceptional @254–262. No map mutation. |
| Wrapper `_bb4487(Class,Consumer<Consumer<T>>)` | Six invocation instructions in five producer bodies | Chunk-unload batches and player-info batches, detailed below. |
| Paired `_cfe983(Class,Class,Function,Runnable)` | Eight invocation instructions | Two screen-render wrappers and six hotbar version variants. |
| Protected depth begin/end | Only debug subclass super-calls externally | No client caller managing its own begin/end pair was found. Bus-internal unqualified self-calls are separately audited, not counted as external producers. |

Wrapper producers:

- `ML._d4ca6c._590f69._21aca6._00e05b._590f69._21aca6._cfe983.lunar$onChunkReplaceUnLoadAllBlockEntities$v1_17_0 @56`; lambda `$0 @0–65` iterates the live block-entity map and constructs one unload event per entry @31–57.
- `ML._d4ca6c._590f69._21aca6._1e73d7._590f69._cfe983.lunar$onChunkUnloadAllBlockEntities @44`; lambda `$0 @0–65` performs the corresponding entry iteration/event construction.
- `ML._d4ca6c._590f69._21aca6._1e73d7._bb4487._21aca6.lunar$onPlayerInfo @21,48`, `lunar$handlePlayerInfoRemove @11`, `lunar$handlePlayerInfoUpdate @11`. Add/remove lambdas iterate profiles/UUIDs and construct new events. `lambda$lunar$handlePlayerInfoUpdate$0 @0–55` filters null extracted names; `lambda$lunar$handlePlayerInfoRemove$0 @29–80` selects null versus `"player"` profile names at MC_VERSION <=18 versus >18. Reflection profile helper catches four checked reflection exceptions and returns an empty list @133–137; it does not catch every runtime failure.

**Derived:** these are reusable event *batch producers*, not one-shot operations with a visible consumed flag. Re-invoking the outer Consumer repeats iteration and constructs fresh events. The bus wrapper's first invocation delivers captured-array listeners; the second invocation (when deferred mutations exist) delivers pending listeners. This is intentional fan-out structure; it does not prove every original listener receives each event twice. The producer itself and event constructors may run twice, and changed collection contents may produce different batches. No outer wrapper memoizes a batch or promises an exactly-once side effect. Live map iteration admits a conditional concurrent-modification failure; no such failure was observed.

Paired producers:

- `ML._d4ca6c._590f69._21aca6._1e73d7._13ea87._d4ca6c.lunar$drawScreenEvents @24` and `ML._d4ca6c._590f69._21aca6._1e73d7._21aca6._1e73d7.lunar$drawScreenEvents @24`: PRE/POST screen events `L._d4ca6c._cfe983._590f69._bb4487$_1e73d7/$_590f69`. They pass the supplied screen-render Runnable through. Catching Throwable outside the bus creates/rethrows a Minecraft ReportedException; neither catch repairs bus depth.
- In the latter GUI class, `lunar$onRenderHotbar$v1_16_1 @22`, `$v1_20_0`, `$v1_20_5`, `$v1_21_0`, `$v26_1 @21`; and `ML._d4ca6c._590f69._21aca6._1e73d7._21aca6._d4ca6c.lunar$onRenderHotbar$v26_2 @21`. PRE/POST classes are `L._d4ca6c._cfe983._d4ca6c._133367$_590f69/$_21aca6`. Their factories call `wrapEvents`; operation lambdas invoke the supplied MixinExtras Operation once when the bus selects the operation branch. No depth repair catch surrounds the paired invocation in these methods.

This closes the bounded mutable-map caller question: **the found caller reads under the exposed lock**. It does not establish that reflective code, external mods, uncached classes or future builds cannot mutate the exposed map.

## G-10: which exceptions escape, and what they leave

The Session 4 structural risk is narrowed to concrete call chains rather than upgraded to an observed defect.

1. **Confirmed control flow:** base `_1253fc(Class,Consumer) @16–18` increments depth when an existing listener array exists. Its first outer Consumer invocation @21–35 is caught; handler @38–44 invokes the `(Throwable,Class)` policy. That policy explicitly `athrow`s in nonproduction @22–23 and for AbstractMethodError/IllegalAccessError in production @24–39. These paths leave before depth-end @76–77. The second outer producer invocation @59–67 is outside that catch, so any escaping failure there likewise bypasses depth-end. Caller batch loops above supply real iteration and constructor work to those locations.
2. **Confirmed reporting boundary:** base `_cfe983(Class,Throwable) @0–38` calls `Throwable.getMessage @5`, logging @17 and `L._767dc1._590f69._cfe983(Throwable,String,boolean,Hint) @35` without a protective catch. That reporter calls `printStackTrace @5` when selected, then its Sentry helper @16 and logging @33, also without a catch. The helper calls `L._767dc1._1e73d7._1253fc(Throwable) @1`, then Sentry capture @15. Throwable normalization calls a stack/cause helper @7 and virtual `getMessage @11` outside its reflective reconstruction catch (only @62–155 is caught). Thus reporting is not guaranteed to return for arbitrary Throwable implementations or downstream failures. No telemetry was executed.
3. **Confirmed replay boundary:** `_57e17e @0–14` decrements depth before invoking `_455ac7`. Replay @13–80 iterates records and re-enters normal register/remove; `List.clear @83–87` is after the loop and there is no finally. First/last-listener hook `_2f4182(Class) @19–39,44–64` explicitly throws RuntimeException for annotation/marker inconsistencies. Valid hook lookup invokes producer lookup `_1eb51c @71`; it can initialize a producer class (`Class.forName(...,true,...)`) or instantiate/init it. These are real throwing operations, not a proven malformed shipped event. A failed replay therefore leaves **depth already zero** and deferred list uncleared; this differs from the positive-depth failure in cases 1–2. No rollback of earlier applied records is present.

**Strong inference, conditional:** with an array present, an escaping failure in case 1 or reporting during active dispatch leaves the depth elevated. Subsequent mutations take the deferred branch, and another balanced dispatch cannot remove the leaked baseline depth. Replay failure can leave stale records for later replay. Public entry-point finally blocks unlock the ReentrantLock; none resets depth or clears the deferred list. A surrounding Minecraft crash-report catch changes exception presentation, not these fields.

**Unknown:** an actually occurring shipped workload that triggers this, production frequency, effect after fatal Minecraft termination, and whether a later external recovery resets/recreates the bus. This audit establishes paths and caller behavior; it does not reproduce a live stuck bus. G-10 is partially resolved at static path level, not a runtime-confirmed bug.

## G-12 boundary

The paired callers identify hotbar and screen events susceptible to the already documented pending-only PRE branch. Static code alone does not establish a real nested invocation where PRE has only deferred listeners and cancellation actually occurs. That reachability remains open; the existing branch result is not reinvestigated here.

## Development implications (analyst recommendations)

For an independent client, expose an immutable diagnostic listener snapshot; use exception-safe dispatch scopes; specify batch producer repeatability; and distinguish a failed depth scope from a failed replay. These are design recommendations, not assertions that Lunar implements those safeguards.
