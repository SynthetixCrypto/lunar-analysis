# Event bus threading, dispatch and mutation — session 4

Static bytecode findings, not runtime observations. **Confirmed** = implemented branch; **Strong inference** = conditional consequence; **Unknown** = not established. Artifact throughout: `lunar.jar`. Aliases resolve to actual JVM identities in [class-mapping.json](evidence-bus/class-mapping.json); fresh `javap -p -c/-v` and readable alias dumps are retained in [evidence-bus](evidence-bus/). This closes the missing debug-subclass/thread-check question, without redoing the event catalog or Mixin cancellation audit.

## Thread check is in the base class and only diagnoses

**Confirmed — S4-BUS-01.** `L._d4ca6c._590f69._a140a8(Class) @0–47` returns if its static check flag is false or the event implements the external-thread marker `L._ba7d98._1e73d7._590f69` (`@7–16`). Otherwise it queries render-thread bridge `_3d8570 @17–25`. On failure it logs and calls `Thread.dumpStack @28–44`: **no throw, queue, dispatch rejection or early return from the public posting path**. The feature flag names `THROW_ON_WRONG_THREAD_*` do not describe the actual action in this method.

The modern bridge `ML._d4ca6c._d4ca6c._21aca6._21aca6._21aca6._3d8570 @0–17` uses `RenderSystem.isOnRenderThread()` for `MC_VERSION>=29`, otherwise `isOnRenderThreadOrInit$v1_16_1`. This is a bridge predicate, not an observed thread identity. Static check-flag selection is in base `<clinit> @14–61`; its enabled state at runtime is **Unknown**. No settings values were read.

**Confirmed.** `L._d4ca6c._cfe983` is the debug subclass, selected by base `<clinit> @93–116` when the production flag is false. Its constructor `@9–24` rejects construction in production. It overrides queue append, depth begin/end and replay with equivalent operations (`_cfe983(Deferred) @0–11`, `_13ea87 @0–5`, `_57e17e @0–4`, `_455ac7 @0–92`); it does **not** contain a separate thread-enforcement algorithm. Its event deque is initialized null (`<init> @4–6`). Extra counters/diagnostic declarations alone are not evidence of enforcement.

## Synchronization and reentrancy

**Confirmed — S4-BUS-02.** Constructor `L._d4ca6c._590f69.<init> @4–45` allocates a default (non-fair) ReentrantLock, ArrayList of deferred mutations, AtomicInteger depth and ordinary HashMap of listener arrays. Registration `_21aca6(Class,Consumer,int) @0–54`, removal `_590f69(Class,Consumer) @0–50`, supplier posting `_cfe983(Class,Supplier) @5–56`, wrapper posting `_bb4487 @5–57` and paired posting `_cfe983(PRE,POST,Function,Runnable) @10–70` check `isHeldByCurrentThread`: same-thread nesting calls the internal implementation directly; another thread blocks on the same lock. The externally acquired lock is released through exception-table cleanup on public entry paths.

Handlers run **synchronously on the posting thread while that lock is held**; the bus has no executor in these posting methods. Nested event posting is allowed, not deferred. Constructor-held client lock (`L._cfe983.<init> @38–44`, unlock `@1734–1740`, retained full dump) therefore prevents another thread entering the locked dispatch region while managers are wired. The thread-check diagnostic itself precedes lock acquisition and is not prevented by that lock.

**Confirmed, limitation.** `_ef97c4 @0–4` returns the backing mutable HashMap, not a copy/locked view; `_9e2624 @0–4` exposes the lock. Protected helper calls and external mutation of that map are outside the public locking guarantee. “All bus data are thread-safe” is too broad. Client calls using public wrappers are serialized; runtime lock contention/deadlocks were not measured.

## Exact class dispatch, priorities, deferred mutations

**Confirmed — S4-BUS-03.** Listener lookup is exact `HashMap.get(eventClass)`, not assignable-supertype traversal (`_21aca6(Class,Supplier) @0–11`). Existing listener array is captured once. Registration makes a new array, appends and sorts by **negative priority** (`_cfe983(int,Consumer,Class,array) @0–71`; comparator helper `_cfe983(Listener) @0–5` uses `ineg`). Default priority is 100. **Strong inference:** normal priorities execute descending with stable equal-priority insertion order under Java object-array sort semantics; `Integer.MIN_VALUE` negation overflow is an exception to an unrestricted descending-order claim. Removal matches **Consumer reference identity** (`_cfe983(Consumer,Class,array) @33–39`) and removes all identical occurrences; an empty result removes the key.

Private register/remove implementations test depth `@0–25` and append add/remove records if nonzero. `_13ea87 @0–8` increments depth. `_57e17e @0–14` decrements and replays only if it reaches zero. `_455ac7 @13–92` applies records in append order and clears them after successful replay. Subscription hook notification on first listener/last removal is separate (`_88f3cf`, `_429bf0`, `_2f4182`); registration filtering is not server feature enablement.

**Confirmed — crucial correction to “mutations only affect the next event.”** `_cfe983(Class,event,Supplier) @21–165` additionally walks **pending additions for that same class**, invoking their Consumers against the current event. It scans newly appended tail entries until list size stops growing (`@27–46`, `@138–153`). Pending removals are skipped. These additions run in queued insertion order, **not sorted priority order**, before final replay; nested dispatch can also see them. Old listeners scheduled for removal still remain in captured arrays until depth-zero replay.

**Strong inference:** registering a listener from a handler can deliver the current event immediately in the deferred-add pass, not only later events. A self-registering callback can repeatedly extend that pass; no finite limit/deduplication appears here. An add followed by remove can still receive the current event through the addition record before replay removes it. This is branch-based analysis, not a reproduced runtime loop.

If no ordinary array exists, the pending helper may invoke the supplied event factory, but its produced event is local: the outer supplier implementation’s return remains null (`_21aca6(Class,Supplier) @12–13`, `@116–134`). Do not equate a null returned event with no listener work in every nested case.

## Failure paths do not have universal finally-balanced dispatch depth

**Confirmed — S4-BUS-04.** In ordinary supplier dispatch, factory `Supplier.get @19–28` precedes depth increment `@35–37` and lies outside the handler catch. Handler invocation `@65–81` catches Throwable and invokes the logging/reporting helper `_cfe983(Class,Throwable)`. Normal handler failures therefore do not terminate the loop if reporting returns. They are not all rethrown in development. Pending-add invocation catches Exception/Error and calls the **different** `_cfe983(Throwable,Class)` policy helper (`pending @82–129`): nonproduction rethrows; production rethrows AbstractMethodError/IllegalAccessError, otherwise logs/prints (`policy @0–77`).

**Confirmed.** Depth exit is an ordinary call, not a `finally`: supplier dispatch `@128–129`; wrapper dispatch `_1253fc @76–77`; paired PRE `@185–186` and POST `@326–327`. Exceptions in diagnostic/reporting, deferred-add invocation, wrapper production of events or replay can bypass it. Public wrappers release the lock, but **lock release does not repair depth or flush the deferred list**.

**Strong inference:** an exceptional path after `_13ea87` but before `_57e17e` can leave positive depth and keep later mutations queued. A failed replay can leave an uncleared list. Scope this as conditional correctness risk, not an observed failure. Supplier construction failure before begin does not create that specific depth leak. The wrapper’s first user Consumer invocation is caught (`_1253fc @21–44`), but its pending-add second invocation `@59–67` lies outside that catch and can run user code twice. Its synthesized array Consumer catches individual handler Throwables (`_cfe983(array,Class,event) @29–53`).

## Cancellation: ordinary broadcast versus paired operation

**Confirmed — S4-BUS-05.** Ordinary supplier/wrapper dispatch does not inspect `isCancelled` in its handler loop and does not short-circuit remaining listeners. `L._d4ca6c._1e73d7` stores a boolean cancellation flag (retained alias dump). Most producer cancellation semantics remain those already documented by the session-3 bounded Mixin audit.

The paired overload is different: internal `_21aca6(PRE,POST,Function,Runnable)` captures both arrays `@0–24`, selects PRE/POST/BOTH for the event factory `@36–85`, dispatches PRE and pending additions, exits PRE depth, then **checks PRE cancellation `@189–212`**. If cancelled it returns without operation or POST. Otherwise Runnable runs `@232–234` and POST dispatch follows `@239–346`.

**Confirmed branch limitation.** That cancellation check occurs only on the path where a PRE listener array exists. If only pending PRE additions exist, `_cfe983` may deliver them `@216–229` (or both pending-only `@455–505`) but the cancellation flag is **not** checked before Runnable. If no listeners/pending mutations exist, the event factory is not called and Runnable runs `@511–513`. POST with an existing array does not call the pending-add helper on that phase before depth exit (`@244–327`); POST with no array does (`@333–346`). Thus neither “every PRE cancellation skips the operation” nor “every newly added POST handler sees the current POST” is universally true.

## Status / next work

- Thread-check location/action, debug-subclass role, public lock scope, normal reentrancy, priority, deferred add/remove and paired cancellation are **resolved statically** within these overloads.
- Error-policy/depth imbalance and mutable-map exposure are **conditional Strong inference risks**, not tested defects.
- Actual check-flag state, runtime producer thread identities and contention remain **Unknown**. No runtime work is authorized.
- Next useful static follow-up: audit callers of the mutable map and wrapper/paired APIs for assumptions about duplicate production, pending-only cancellation or exception-balanced depth, rather than repeating all event constructors.
