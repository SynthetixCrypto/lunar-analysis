# Event bus: threading, nested dispatch, deferred mutations, and failure branches

Study date: 2026-10-11. Session 4 continuation; **static evidence only**. This report addresses the bus-specific part of U-07 and the previously compressed JV-05 algorithm. It does **not** regenerate the event catalog, cancellation audit, or producer map. Parent reports were read without modification.

**Confidence convention:** **Confirmed** means directly present in the shipped bytecode/metadata; **Strong inference** means a consequence derived from that bytecode plus ordinary JVM/library semantics, not an observed execution; **Tentative** means provisional interpretation; **Unknown** means not established. Decimal offsets are method-local javap `Code` offsets. Metadata/BootstrapMethods references have no Code offset. Symbolic branch examples below were reasoned about, **not run**.

## 1. Outcome and corrections

| Prior claim / question | Result | Confidence and locator |
|---|---|---|
| `L._d4ca6c._cfe983` enforces thread affinity | **Contradicted.** It is the debugging bus, adds a count/name diagnostic, and inherits dispatch/checking. Its overrides delegate depth operations or reproduce queue operations. | **Confirmed:** `lunar.jar`, subclass `<init> @0–25`, `_13ea87 @0–5`, `_57e17e @0–4`, `_455ac7 @0–92`; complete fresh subclass disassembly. |
| Wrong-thread flags select that subclass | **Contradicted.** Subclass choice is solely `_63fe11 = !P`, where `P = L._1e73d7._cfe983._c1461e`; flags affect a base-class warning predicate, not subclass selection. | **Confirmed:** base `<clinit> @0–119`, especially `@93–116`; subclass constructor guard `@9–24`. |
| Wrong-thread events are thrown, ignored, or scheduled onto the render thread | **Contradicted as a description of this bus implementation.** The base check logs and calls `Thread.dumpStack`, then continues. Marker types skip it. No bus scheduling or rejection branch follows a false thread predicate. | **Confirmed:** base `_a140a8(Class) @0–47`, string recipe BootstrapMethods #15; modern predicate implementation `_3d8570() @0–17`. |
| Priority is descending | **Qualified.** Committed arrays sort on the signed int key `-priority`; ordinary values descend, but `Integer.MIN_VALUE` overflows and sorts first. Pending additions run separately in list order, without priority sorting. | **Confirmed:** add-array lambda `_cfe983(int,Consumer,Class,Record[]) @0–71`; key `_cfe983(Record) @0–5`; pending helper `@49–115`. |
| All handlers are isolated | **Qualified.** Committed handlers have `catch(Throwable)`; pending handlers use the broader-path `Exception`/`Error` policy instead. Reporters can themselves throw, and depth cleanup is not in a finally block. | **Confirmed:** ordinary core `_21aca6(Class,Supplier) @65–108`; pending helper exception table; error-policy methods `@0–38` / `@0–77`. |
| Constructor lock prevents other threads dispatching during wiring | **Supported with boundaries.** Same-bus public dispatch and mutation cores block on the lock; the checker runs before acquisition. Constructor releases at `1740`, before its last initialization calls, and has no general finally-unlock. | **Confirmed:** client `L._cfe983.<init> @38–44`, `@1734–1758`, exception table; public bus post `@0–56`. Blocking consequence **Strong inference**. |
| Deferred mutations apply at outermost exit | **Qualified.** Committed-map updates drain only when decrement reaches zero on balanced normal paths. But pending **additions can receive events before commit**, including the current event; removals do not suppress the captured snapshot. PRE and POST are separate depth intervals, and exceptional exits can strand depth/queue state. | **Confirmed:** depth `_13ea87 @0–8`, `_57e17e @0–14`, drain `_455ac7 @0–92`, pending helper `@0–165`; wrapper `@112–232`, `@261–346`. |
| No committed handlers means no event construction | **Qualified.** True only if there is also no matching pending addition. Pending-only posting can call the supplier and dispatch its event, yet still return null to the caller. | **Confirmed:** ordinary core `@0–19`, `@116–134`; pending helper `@65–107`. |

**Unknown:** actual runtime flag values, live thread ownership, whether a particular application path encounters the adverse branches, and native/GameUI threading. None was sampled or inferred from private settings.

## 2. Artifact identity, reproducibility, and exact symbols

**Confirmed provenance.** Fresh JDK `javap -p -c` and `javap -p -v` were run as static disassembly tools against only selected archive classes; no Lunar class, JAR, native, or JS was loaded/executed as target code. `q.py` was inspected before use; it reads the retained analyst `classes.pkl` and prints query results. Fresh selected Code output matches cached output for every captured class/method, modulo outer whitespace. No installation/configuration, credential/settings-value reading, or anti-cheat/integrity analysis occurred.

| Artifact | Path | Fresh SHA-256 |
|---|---|---|
| Core | `C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar` | `bf36e10e21154263ac16363f8c83bb08cff3a077cb788120954d3625b94a02e9` |
| Version adapter | `C:\Users\Admin\.lunarclient\offline\multiver\modern-0.1.0-SNAPSHOT-all-nomappings.jar` | `99df64c5913e9a32111135bfde140343d4baa954fe5ba08069962670566db02e` |

**Confirmed exact identity:** the principal classes are:

| Report shorthand | Exact JVM class in `lunar.jar` |
|---|---|
| **B** / `L._d4ca6c._590f69` | `com.moonsworth.lunar.client.RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.RORCICOHRIOIIIOIOHIIIICRCIHRII` |
| **D** / `L._d4ca6c._cfe983` | `com.moonsworth.lunar.client.RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.COOCHIRORIICRCIIRIROHIIRIRICCH` |
| **R** / handler record `L._d4ca6c._bb4487` | `com.moonsworth.lunar.client.RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.IRCROOHIIOOHIRCRRHOHIORHCOHIOR` |
| **Q** / pending operation `B$_cfe983` | `com.moonsworth.lunar.client.RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.RORCICOHRIOIIIOIOHIIIICRCIHRII$COOCHIRORIICRCIIRIROHIIRIRICCH` |
| **Mode** / `B$_21aca6` | `com.moonsworth.lunar.client.RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.RORCICOHRIOIIIOIOHIIIICRCIHRII$RROHOCRCCHCIORHICIHCOHRIRCIHCI` |

**Confirmed retained evidence:** [evidence-bus/class-mapping.json](evidence-bus/class-mapping.json) maps **all 13 cited captured classes**, original JVM names, archive members, class hashes, archive hashes, output filenames, and cached/fresh comparison results. Full original-name raw disassembly is in `*.javap-c.txt` and `*.javap-v.txt`; `*.aliases.txt` is a readable rendering of the same selected output. Principal files: [base Code](evidence-bus/L-_d4ca6c-_590f69.javap-c.txt), [base verbose/BootstrapMethods](evidence-bus/L-_d4ca6c-_590f69.javap-v.txt), [subclass Code](evidence-bus/L-_d4ca6c-_cfe983.javap-c.txt), [constructor lock/tail slice](evidence-bus/L-_cfe983.javap-c.txt), [render-thread bridge slice](evidence-bus/ML-_d4ca6c-_d4ca6c-_21aca6-_21aca6-_21aca6.javap-c.txt), [bounded reference search](evidence-bus/bounded-reference-search.json).

**Confirmed analyst procedure:** [capture.py](evidence-bus/capture.py) writes only into its own `evidence-bus/` directory. It hashes supplied archives, reads selected ZIP members, runs the installed Microsoft JDK 21.0.10.7 `javap.exe`, retains complete bus/subclass/record/base output, and slices unrelated methods from the client, adapter, and two diagnostic consumers. Reproduction: `python "C:\Users\Admin\Downloads\New folder\lunar-analysis\session4-sol\evidence-bus\capture.py"`. Archive-classpath disassembly avoids Windows long extracted-member paths. All new reports/scripts are patch-created; generated raw evidence is confined to the authorized output directory.

### Method key (all B methods below are in `lunar.jar`)

**Confirmed** names/descriptors, from complete base disassembly:

| Meaning used here | Actual alias signature |
|---|---|
| Register | `_21aca6(Class,Consumer,int)` public; `_590f69(Class,Consumer,int)` private |
| Unregister | `_590f69(Class,Consumer)` public; `_1e73d7(Class,Consumer)` private |
| Ordinary post | `_cfe983(Class,Supplier)` public; `_21aca6(Class,Supplier)` private |
| Pending-event dispatch | `_cfe983(Class,Event,Supplier)` protected |
| Producer/callback post | `_bb4487(Class,Consumer<Consumer<T>>)` public; `_1253fc(Class,Consumer<Consumer<T>>)` private |
| PRE/POST wrapper | `_cfe983(Class,Class,Function<Mode,Pair>,Runnable)` public; `_21aca6(Class,Class,Function<Mode,Pair>,Runnable)` private |
| Enter / leave / commit | `_13ea87(Class)` / `_57e17e()` / `_455ac7()` protected |
| Committed-handler reporter | `_cfe983(Class,Throwable)` private |
| Broader-path failure policy | `_cfe983(Throwable,Class)` private |
| Lock accessor / live map accessor | `_9e2624()` / `_ef97c4()` public |

## 3. Subclass and wrong-thread branch, resolved

### 3.1 Variant selection is not thread enforcement

**Confirmed.** B's constructor creates a default `ReentrantLock`, `ArrayList<Q>`, `AtomicInteger(0)`, and `HashMap<Class,R[]>` (`<init> @4–45`). Its static getter `_20bc5b @0–3` returns a shared default instance. Both constructors are public, so this is not a prohibition on additional bus instances. The instance selected by `<clinit> @93–116` is D iff `_63fe11` is true; `_63fe11 = !P` at `@0–11`.

**Confirmed polarity / bounded interpretation.** D's `<init> @9–24` throws `IllegalAccessError("DebuggingEventBus is being used in production environment!")` if `P` is true. This directly establishes the shipped guard's production interpretation; it does **not** establish the current runtime value of P. D's three private static booleans have `ConstantValue: int 0`; its final deque is initialized null at `@4–6`, with no subsequent use in its complete body. Its enter/leave overrides only invoke `super`; enqueue and drain do the same list work as B (using Q getters). There is no thread-owner field, thread comparison, overridden public posting method, or additional check in D's complete fresh class output.

**Confirmed.** D's `_ef6f38 @0–84` creates an `Object2IntOpenHashMap`, iterates the live bus map, and includes only classes whose handler array length is **greater than one** (`@52–55`). Name helper `_2ce426 @0–73` chooses a simple/qualified name according to length and whether it contains `Event`. This is a diagnostic count map, not the handler snapshot and not an affinity mechanism. The method itself does not acquire the bus lock.

### 3.2 Actual check is a warning before taking the lock

**Confirmed.** B's `_a140a8(Class) @0–47` is called before acquisition in ordinary post `@0–4`, callback post `@0–4`, and wrapper `@0–9` (PRE class and POST class both checked). Registration/unregistration and generic lock helpers do not call it.

**Confirmed** branch order:

1. If static `_529826` is false, return (`@0–6`).
2. If `L._ba7d98._1e73d7._590f69.class.isAssignableFrom(eventClass)`, return (`@7–16`). That is the marker referred to as `ThreadedEvent` by the shipped warning string, not a request to move work to another thread.
3. Invoke render bridge `_e3e382()._3d8570()` (`@17–25`). If true, return.
4. If false, log `Event [<simpleName>] was fired on the wrong thread! If this is intentional, make it implement ThreadedEvent` (`@28–41`, BootstrapMethods #15), call `Thread.dumpStack()` (`@44`), then return (`@47`). There is no explicit throw, drop, queue, or early exit from the posting operation.

**Confirmed predicate route.** In `modern-0.1.0-SNAPSHOT-all-nomappings.jar`, `ML._d4ca6c._d4ca6c._21aca6._21aca6._21aca6._3d8570() @0–17` chooses `RenderSystem.isOnRenderThread()` when `MC_VERSION >= 29`, else `RenderSystem.isOnRenderThreadOrInit$v1_16_1()`. This proves the named bridge predicate route, not the running version or live render-thread result. Raw selected output and exact mapping are retained.

**Confirmed static expressions**, abbreviating only fields already touched by B's initializer (no flag-provider implementations or private flag values inspected):

```text
P = L._1e73d7._cfe983._c1461e
beta = L.util._cb9292._198f02
dev = L.util._cb9292._7772b4
disableCheck = L.util._e93d3c._2683bc
_63fe11 = !P
_529826 = !disableCheck && (!P || (beta && THROW_ON_WRONG_THREAD_BETA.isEnabled())
                                           || (dev && THROW_ON_WRONG_THREAD_DEV.isEnabled()))
_09429d = P && (!beta || IGNORE_EXTERNAL_THREAD_BETA.isEnabled())
```

Locators: B `<clinit> @0–11`, `@14–61`, `@64–90`. **Confirmed bounded negative:** `_09429d` is declared and assigned but never read in B's complete Code output; see retained search. Its name/initializer is not evidence that this implementation ignores external threads. **Unknown:** reflective access, external non-cached classes, or behavior of those flag providers. No claim that the flag is globally unused is made.

**Strong inference.** Under normal predicate/logging success, a wrong-thread caller still synchronously dispatches on its own thread after obtaining the lock. Exceptions from bridge resolution/predicate/logging could abort before acquisition; those are not a deliberate wrong-thread rejection branch in this method.

## 4. Lock, snapshots, registration, and synchronization boundary

### 4.1 What is actually serialized

**Confirmed.** Public register `_21aca6(Class,Consumer,int) @0–54`, unregister `_590f69(Class,Consumer) @0–50`, ordinary post `_cfe983(Class,Supplier) @5–56`, callback post `_bb4487 @5–57`, and wrapper `_cfe983(Class,Class,Function,Runnable) @10–70` use the **same** `_1c2403` lock. They first test `isHeldByCurrentThread`; the owner calls the core directly without another lock/unlock. A non-owner acquires it, executes the core, then unlocks on success or in an `any` exception-table cleanup. Thus handlers/suppliers/producers/runnables invoked by a normal public operation run inside the critical section; no callback is intentionally moved off-thread by these methods.

**Confirmed.** Generic helpers `_1e73d7(Runnable) @0–50` and `_590f69(Supplier) @0–49` similarly acquire/release or reuse ownership, but **do not increment dispatch depth**. `_0a8e8a @0–7` reports current-thread ownership. `_9e2624 @0–4` exposes the actual lock. There are no monitor-based/synchronized wrappers replacing this protocol in the inspected classes.

**Strong inference, conditional on compliant callers.** Concurrent callers of these public APIs serialize; AtomicInteger is not what makes the HashMap/List safe. Reentrant same-thread dispatch is allowed, with depth tracked separately. Cross-thread registration arriving during a handler blocks rather than concurrently appending to the queue: only after acquiring the lock does it test depth. A handler that waits for another thread which needs this bus lock can produce an application-level wait cycle; no timeout, `tryLock`, or scheduling branch exists here. This is a structural risk, **not an observed deadlock**.

### 4.2 Exact-key snapshots and exposed storage

**Confirmed.** Ordinary post captures `map.get(eventClass)` once (`_21aca6(Class,Supplier) @0–11`), then iterates that array reference. Wrapper captures **both** PRE and POST arrays before calling its factory (`_21aca6(wrapper) @0–24`); callback post captures one array (`_1253fc @0–11`). There is no superclass/interface subscriber lookup. Arrays are replaced, not edited, by normal add/remove helpers. Therefore this is **copy-on-write array storage under an external lock**, not a concurrent map and not a cloned dispatch snapshot.

**Confirmed boundary.** `_ef97c4 @0–4` returns the mutable HashMap itself, not an immutable copy; its arrays can be reached through it. D's count helper also reads live storage without taking the lock. Thus the lock guarantee is limited to callers respecting the protocol, not all possible accesses to these public/protected objects.

**Confirmed checked consumers, bounded.** The retained exact-owner reference search across cached classes finds one `_ef97c4` call: diagnostic `L._88f3cf._bb4487._a1dd3a._21aca6._21aca6._21aca6._f54c89()`. It obtains the bus lock at `@12–18`, copies `entrySet()` into an ArrayList at `@21–35`, reads/prints entries while still holding the lock, and unlocks at `@247–260` with exception cleanup. This copy is not a deep immutable snapshot, but the observed consumer uses the lock correctly. One `_ef6f38` caller is `EVENT_DEBUG_MOD` helper `L._88f3cf._bb4487._a1dd3a._d4ca6c._3c6778 @44–57`; its caller `_1253fc(Event) @8–9` is the event handler. **Strong inference:** normal bus invocation supplies lock ownership for this path; the count helper does not guarantee it when called independently. **Unknown:** callers outside the retained index or reflective access.

### 4.3 Add/remove are deferred by depth, not merely lock ownership

**Confirmed.** Private register `_590f69(Class,Consumer,int) @0–25` queues Q(add=true,class,consumer,priority) whenever the AtomicInteger is **nonzero**, not just positive. At zero it invokes the first-listener hook when the old array is null/empty (`@26–52`) and uses `HashMap.compute` (`@55–70`) to build a new array. Default `Consumer` registration priority is 100 (`_21aca6(Class,Consumer) @0–8`); Runnable adapters delegate to this path (`@0–11` / `@0–12`, BootstrapMethods #0/#1).

**Confirmed.** Add-array lambda `_cfe983(int,Consumer,Class,R[]) @0–71` allocates `oldLength+1`, appends a new record, copies old elements, and sorts when length >1. No duplicate or null-consumer check appears. Comparator key `_cfe983(R) @0–5` uses `ineg`; BootstrapMethods #2/#16 bind the actual add and key lambdas. **Strong inference:** Java's stable object-array sort preserves prior registration order at equal priority. **Strong inference:** signed overflow makes `Integer.MIN_VALUE` map to itself, ahead of all other priority keys; the normal descending-priority claim needs that edge qualification.

**Confirmed.** Private unregister `_1e73d7(Class,Consumer) @0–25` queues Q(add=false,class,consumer,0) at nonzero depth. At zero it uses `computeIfPresent @26–40`; the remove lambda `_cfe983(Consumer,Class,R[]) @0–81` keeps records whose `Consumer` reference is **not identical** (`if_acmpeq @39`). It removes **all** identical-reference occurrences, not one and not `.equals` matches. Empty results return null (`@57–67`), removing the class key. If `computeIfPresent` returns null—including an already-absent key—the last-listener hook runs (`unregister @41–47`).

**Confirmed lifecycle boundary.** First/last hooks `_88f3cf(Class) @0–13` / `_429bf0(Class) @0–13` resolve a dynamic-listener association via `_2f4182(Class) @0–77`. A `@TriggeredBy` annotation on a non-`DynamicListenerEvent` or a missing annotation on such an event throws; valid annotations resolve a listener and invoke BootstrapMethods #4/#5 targets. These hooks run under the caller's lock, before first insert / after removal. **Unknown:** the complete downstream listener lifecycle effects; they are not necessary to establish the bus's snapshot/queue algorithm and were not expanded into unrelated code.

## 5. Ordinary posting: every significant branch

### 5.1 Committed-snapshot path

**Confirmed**, B private `_21aca6(Class,Supplier) @0–134`:

| Condition / step | Actual branch |
|---|---|
| Snapshot array is null | Skip committed construction/handlers and call pending helper with `(class,null,supplier)` at `116–121`. |
| Snapshot is nonnull | Call supplier exactly at `19–28`, **before depth increment** and outside this core's handler catch regions. |
| Supplier returns null | Return null at `30–32`, `114–115`; do not scan pending operations or decrement, because no increment occurred. |
| Supplier returns event E | Increment via `_13ea87(class)` at `35–37`; iterate the initially captured array at `40–96`. |
| A committed handler fails | Catch any Throwable from record-consumer retrieval/invocation (`65–81 →84`), call committed reporter at `86–90`, then continue at `93` **if reporter returns**. |
| Loop-level Exception/Error escapes | Outer region `40–99 →102` calls broader failure policy at `104–108`; continue only if that policy returns. |
| Normal committed completion | Scan pending additions with the same E at `116–121`; decrement at `124–129` iff original snapshot was nonnull; return E at `132–134`. |

**Strong inference.** On a top-level post, registration/unregistration performed by the supplier occurs immediately at depth zero even though the lock is held. Those changes do **not** replace the already captured snapshot. Nested supplier posting is permitted, but the outer event has not yet entered its depth interval. Thus depth is not synonymous with lock nesting or the full lifetime of a public post call.

**Confirmed cancellation boundary.** Ordinary posting contains no `isCancelled` branch. Cancelling E does not stop subsequent bus listeners; the returned object may be examined by its producer. Cancellation is mutable (`L._d4ca6c._1e73d7.cancel @0–5`, `isCancelled @0–4`, `setCancelled @0–5`), so later listeners can clear it. This does not revisit the parent Mixin audit.

### 5.2 Pending additions can receive the event before registration commits

**Confirmed**, B protected `_cfe983(Class,Event,Supplier) @0–165`:

1. Return if both event and supplier are null, or list is empty (`@0–20`).
2. Read the pending list's current size and iterate by index (`@21–60`); consider only Q entries with add=true and **identical Class reference** (`@65–79`). Remove entries are ignored for delivery.
3. If no event was passed, obtain one from supplier (`@82–95`); null returns immediately (`@96–100`). A newly obtained nonnull event increments depth once, and sets a local ownership flag (`@101–107`).
4. Invoke Q's Consumer directly (`@109–115`). There is no priority sort, no cancellation test, and no deduplication.
5. Supplier/queued-consumer Exception or Error goes to the **broader** failure policy (`@123–129`, catch ranges `82–100` and `101–120`), not the committed-handler reporter.
6. At normal end, decrement only if this helper itself created the event and incremented (`@156–162`). An already supplied event relies on its caller's depth interval, if any.

**Strong inference, precise effects.** A committed handler A registering handler B for this same event queues the add; B is nevertheless invoked by this helper on the current E before the map update. A queued unregister of an existing handler does not remove it from the current array. A queued add followed by queued remove of that same Consumer still delivers the add when scanned; only the later drain applies both to storage. Pending adds can also receive same-type nested posts while still uncommitted. These consequences follow directly from list scanning and snapshot retention, not a guessed cross-thread race.

**Confirmed loop-cursor anomaly.** The initial cursor (`local 6`) is zero (`@24–25`), the pass limit is saved in local 5 (`@27–36`), and local 7 starts from local 6 (`@38–40`). After a pass, the **new current list size** replaces local 6 (`@138–147`). If it differs from old limit 5, control returns to `@27`, where the new limit is read and the cursor starts at that same new size. **Strong inference:** additions appended by a queued handler during an otherwise normal pass are skipped by that pass's follow-up iteration, not recursively delivered until a fixed point. They remain eligible for commit/later events. For example, pass limit 1, Q0 appends Q1, then new size 2 becomes both next cursor and next limit, so Q1 is not called. This is a bytecode-derived branch consequence, **not** a tested runtime bug frequency.

**Confirmed pending-only return asymmetry.** When the ordinary core's committed snapshot is null, its local event remains null; the protected helper returns void. It can create an event, call pending consumers, and balance its own increment, but ordinary post still returns null (`ordinary @12–13`, `@116–134`). Thus a caller's null result is not proof that no handler received an event. On ordinary successful paths there is at most one successful nonnull construction, but the helper can retry a throwing supplier at later matching entries if the production failure policy swallows that failure before an event was retained (`helper @82–100 →123–132`).

### 5.3 Map commit and nesting

**Confirmed.** `_13ea87 @0–8` increments the shared AtomicInteger. `_57e17e @0–14` decrements it and invokes `_455ac7` only on result **exactly zero**. The drain iterates Q in list order (`@13–41`), routes adds through public register (`@49–62`) and removes through public unregister (`@68–77`), then clears the list **only after full success** (`@83–92`). Under normal public posting it retains lock ownership, so those public calls reuse the lock. At zero depth they update the map, including associated hooks. D's drain has the same order and clear-after-success behavior (`D._455ac7 @0–92`).

**Strong inference.** Balanced nested committed dispatch leaves outer depth nonzero, so it does not commit queued changes at inner return. Pending additions can still be delivered at inner/outer helper stages before eventual commit. On the ordinary balanced outermost exit, the map's pending operations apply in queue order. A failed operation/hook can leave earlier commits applied, remaining operations uncommitted, and the list uncleared; there is no transactional rollback or clear-in-finally in the drain.

## 6. Producer/callback posting: another dispatch contract

**Confirmed**, B `_bb4487(Class,Consumer<Consumer<T>>) @0–57` and core `_1253fc @0–80`:

- With a nonnull snapshot, increment once (`core @16–18`), pass a snapshot-dispatch closure to the producer (`@21–30`, BootstrapMethods #8), and catch producer Exception/Error via the broader policy (`@38–44`). The closure `_cfe983(R[],Class,Event) @0–62` ignores a null event and loops committed handlers with `catch(Throwable) @29–44 →47`, but it **does not** acquire the lock, increment depth, check affinity, or scan pending operations itself.
- After that, if the pending list is nonempty, invoke the **producer again**, now with a pending-dispatch closure (`core @47–67`, BootstrapMethods #9). That closure `_cfe983(Class,Event) @0–7` calls the protected pending helper with a null supplier. This second producer invocation is **outside** the producer catch region.
- Decrement at `core @72–77` only if the original snapshot was nonnull. With neither snapshot nor queued operations, the producer is not called. With only queued operations, it is called once with the pending closure and the core itself never increments.

**Strong inference.** A producer may call its supplied callback zero, one, or multiple times; this API does not promise one event object or one producer invocation. Side effects in the producer can occur twice if pending operations are present/created. If the second invocation throws, the final decrement is skipped. A producer could retain a callback and invoke it after return: the captured closure has no lock/lifetime guard, so the bus's public-entry synchronization would no longer protect that invocation. **Unknown:** whether inspected application callers actually retain callbacks; this is an API boundary, not evidence of a live race.

## 7. PRE/POST wrapper: factory, snapshot, cancellation, and exceptions

All locators in this section refer to B private `_21aca6(Class,Class,Function<Mode,Pair>,Runnable) @0–518`, except explicitly named Mode methods. Its public wrapper holds/reuses the lock and checks both event class keys before locking (`public @0–70`).

### 7.1 Factory selection and construction time

**Confirmed.** Both arrays are captured at `@0–24`, before factory or PRE handlers. Mode selection at `@36–80` is:

| Captured PRE array | Captured POST array | Pending list | Factory mode / branch |
|---|---|---|---|
| present | present | any | BOTH |
| present | null | empty | PRE |
| null | present | empty | POST |
| either array present | other any | nonempty | BOTH, even if pending entries concern unrelated types |
| null | null | nonempty | BOTH in separate branch `@443–467` |
| null | null | empty | **No factory**, run Runnable directly `@511–513` |

**Confirmed.** Mode's `wrapEvents(Supplier<PRE>,Supplier<POST>) @0–65` calls PRE then POST suppliers for BOTH (`@7–25`), PRE only for PRE (`@36–46`), or POST only for POST (`@52–62`). It constructs a Pair immediately; it does not defer POST construction until after the Runnable. Factory `Function.apply @80` is otherwise arbitrary: the bus does not force callers to use `wrapEvents`, enforce nonnull Pair, or verify pair element membership against the Class keys.

### 7.2 PRE and cancellation are branch-dependent

**Confirmed**, when a PRE snapshot exists:

- Read `Pair.first` (`@95–105`); if null, skip PRE increment/delivery/cancellation (`@107–109 →213`).
- For nonnull PRE, increment (`@112–114`), run all captured PRE handlers with committed-handler Throwable catches (`@117–174`, `143–159 →162`), then call pending helper on the same PRE (`@177–182`) and decrement/possibly commit (`@185–186`).
- **Only then**, test whether PRE is the cancellable base and `isCancelled()` is true (`@189–209`). If true, return at `@212`, skipping Runnable **and all POST dispatch**. It does not stop the PRE listener loop early; the final flag after all committed/pending PRE callbacks determines this result. PRE mutations have already been committed at outermost depth before that cancellation decision.

**Confirmed cancellation hole in other branches.** With **no captured PRE array**, the wrapper calls the pending helper on `Pair.first` (`@216–229`) and proceeds to Runnable (`@232–234`) **without a cancellation test**. Likewise when both snapshots are null but the queue is nonempty, pending PRE delivery (`@469–482`) is followed by Runnable (`@485–487`) with no `isCancelled`. Thus pending-only PRE handlers can set cancellation and it is not honored by those wrapper branches. A null Pair/factory/accessor failure follows the relevant exception behavior instead; it is not normalized to an empty pair.

### 7.3 Runnable and POST use already captured objects/arrays

**Confirmed.** Runnable executes once on a normally proceeding branch (`@232–234`, or `@485–487`, or `@511–513`). There is no encompassing dispatch-depth increment for the whole wrapper. A successful top-level PRE decrement can reach zero before Runnable, and POST increments later; in-between registration can therefore update the live map immediately. Same-thread nested wrapper calls retain any depth belonging to an outer event.

**Confirmed.** If captured POST array is nonnull, read `Pair.second`, skip if null (`@244–258`), else increment (`@261–263`), run only the originally captured POST handlers with Throwable catches (`@266–323`, `292–308 →311`), then decrement (`@326–327`). **Unlike committed PRE and ordinary post, this committed-POST branch does not call the pending helper.** If captured POST array is null, call pending helper on the POST object at `@333–346` instead. The both-arrays-null branch also does so at `@492–505`. There is no POST cancellation test anywhere in the wrapper.

**Strong inference, precise snapshot consequence.** A PRE handler can queue removal of a POST subscriber; top-level PRE commit removes it from the live map, but the old POST array was already captured, so that subscriber still receives this wrapper's POST. A new POST subscriber committed after PRE likewise is absent from that captured array. A registration performed by Runnable at depth zero updates the map immediately, but also cannot alter this wrapper's captured arrays/mode/pair. This is not a cross-thread effect; it follows from snapshot acquisition at entry.

**Strong inference.** A POST handler that registers another POST handler queues it and the normal POST decrement commits it, but that pending addition is not separately delivered this same POST by the committed-POST branch. By contrast a PRE handler's same-type pending add can receive the current PRE before cancellation checking. Wrapper PRE and POST behavior is therefore intentionally described separately rather than treated as two identical ordinary posts.

### 7.4 Catch coverage is different for fast and pending-only paths

**Confirmed.** If either snapshot exists, one broad handler catches **Exception/Error** from `@36–212` and `@213–349`, targeting `@352`. This includes factory, pair access, PRE/POST entry/delivery/decrement, cancellation getter, and Runnable, but not snapshot lookup before `@36`. The broad handler follows the same policy shape as `_cfe983(Throwable,Class)`: non-production P=false logs then rethrows (`@354–382`); P=true rethrows `AbstractMethodError`/`IllegalAccessError` (`@383–401`), otherwise logs and prints, then returns (`@402–440`). Its own logging is not protected by another cleanup region.

**Confirmed.** Both-snapshots-null/pending-present `@443–508` and no-handlers/no-pending direct Runnable `@511–513` are **outside** those broad catch ranges. Factory/Runnable/accessor exceptions in these branches propagate, although pending helper callbacks still have their own Exception/Error policy. POST is not in a finally block: factory/PRE failure or Runnable failure prevents subsequent POST work. Conversely a committed-handler failure swallowed by its reporter need not stop Runnable or POST.

## 8. Throwable paths and non-finally depth cleanup

### 8.1 Two different failure policies

**Confirmed**, B `_cfe983(Class,Throwable) @0–38`: formats/logs event class plus message (`@0–17`), then calls `L._767dc1._590f69._cfe983(Throwable,"EventBus",!P,null)` (`@20–35`). There is no explicit rethrow of the original handler failure. It is used by each committed array loop (ordinary, PRE, POST, and callback closure), whose catch type is **Throwable**. **Unknown:** the downstream reporting implementation's complete behavior; it was not expanded. Reporting can itself fail, so universal isolation is not proven by a catch around only Consumer invocation.

**Confirmed**, B `_cfe983(Throwable,Class) @0–77`: if P=false, log and `athrow` (`@0–23`); if P=true, rethrow `AbstractMethodError` or `IllegalAccessError` (`@24–39`), otherwise log class/type/message and `printStackTrace` (`@40–68`). The extra `catch(Throwable) @0–71 →74` simply rethrows, not isolates. Pending supplier/handler and producer failure regions catch **Exception and Error**, not a direct Throwable outside those two families. The wrapper implements the same broad policy inline, but committed individual-handler exceptions first take the committed reporter path.

### 8.2 Branch table: lock cleanup is not depth cleanup

**Confirmed.** Public entry methods protect their own acquired **lock** with exception cleanup. There is **no finally decrement** around the private dispatch intervals. Normal outermost drain is therefore not a universal guarantee after abnormal return. The following failure positions are directly located; effects listed are **Strong inference**, conditional on such an exception escaping the indicated catch/policy:

| Failure position | Branch-level consequence |
|---|---|
| Ordinary committed-path supplier, `core @19–28` | Propagates before this post increments; this post adds no depth leak. An outer dispatch may still own depth/lock. |
| Ordinary committed reporter, `core @86–90`, followed by broader rethrow `@104–108` | The increment at `@35–37` is not undone; skip pending helper/decrement/commit. If outer code swallows it, stale positive depth can survive while public wrapper releases its lock. |
| Ordinary pending helper after committed delivery, `core @116–121` | If helper's failure policy rethrows, the ordinary decrement at `@128–129` is skipped. |
| Pending helper creates event/increments `@101–107`, then queued Consumer/policy escapes `@109–129` | Its local decrement at `@161–162` is skipped; with an outer committed interval, both decrements may be skipped. |
| Callback producer's second invocation `core @59–67` | Outside producer catch region; any escape bypasses final decrement `@76–77` if a snapshot had incremented. |
| PRE pending helper or committed reporter escapes before wrapper `@185–186` | PRE increment can remain outstanding even if wrapper's broad production policy swallows the escaping error at `@352–440`. |
| POST reporter escapes before wrapper `@326–327` | POST increment can remain outstanding; the wrapper broad policy decides propagation/swallowing, not depth repair. |
| Drain operation/hook fails, `_455ac7 @49–77` | Count may already be zero; prior commits can remain applied and pending list uncleared. No rollback/transactional retry guarantee. |

**Strong inference.** Inherited APIs then use `depth != 0` to keep queuing registrations, and a later balanced post adds/subtracts one without repairing a pre-existing positive count. No depth-reset/recovery branch is present in the complete B/D classes. This establishes a potential state-corruption path, not that the shipped client has encountered it. Failures swallowed by the committed reporter or production broad policy **before normal cleanup is reached** can still leave normal balance intact; not every thrown Consumer failure leaks depth.

## 9. Client construction lock: what the old claim can and cannot mean

**Confirmed.** In `lunar.jar`, `L._cfe983.<init>` obtains the shared bus and lock (`@38–41`) and calls `lock()` (`@44`). Normal-path release is `@1734–1740`. Its remaining calls at `@1743–1755` occur **after** release, before constructor return `@1758`. Its exception table contains only `194–1295 →1298 Throwable` and `1650–1680 →1683 InterruptedException`; there is no general `any` handler covering the whole locked construction interval or final unlock. The raw lock/tail/exception-table slice is retained without unrelated initialization internals.

**Strong inference.** Other threads' public same-instance post/register/unregister cores cannot enter while this lock is held. Same-thread posts and mutations are allowed, and the lock alone does not create nonzero event depth, so initialization registration can occur immediately. A wrong-thread warning may execute **before** the other thread blocks. Direct live-map access or an escaped callback lies outside this public-entry guarantee. If an uncaught exception leaves the constructor before its normal unlock, the acquisition is not automatically released by Java; no constructor-wide finally repair is present. Actual failure occurrence and downstream effects are **Unknown**.

## 10. Adversarial symbolic branch checks (not executed)

Each example is a **Strong inference**, assumes only normal public APIs on one bus, and identifies the exact bytecode controlling the result. They are not target executions or reconstructed tests.

| Hypothetical sequence | Deduced result | Bytecode basis |
|---|---|---|
| Committed A(E) registers B(E, very high priority) | B can receive current E, but **after all captured handlers**, independent of its priority; map insertion waits until zero depth. | register private `@0–25`; ordinary `@40–96`, `@116–129`; helper `@65–115`. |
| A(E) queues unregister of committed C(E) before C's slot | C still runs from the retained array; commit removes C later. | ordinary captured array `@0–11`, loop `@40–96`; unregister `@0–25`. |
| A queues add B then remove B; pending helper starts | Add B is delivered despite later pending remove; normal drain adds then removes storage entry. | helper add-only filter `@65–79`; drain `@42–80`. |
| Outer event queues add B(F), then nested ordinary post(F,supplier), no committed F array | Supplier can construct F and B can receive it; nested post returns null; outer depth prevents storage commit yet. | ordinary `@12–19`, `@116–134`; helper `@82–107`, `@156–162`; leave `@0–14`. |
| One pending B(E) adds C(E) during its invocation | C is appended but skipped by the helper's changed-size follow-up cursor; normal zero-depth drain can still register C. | helper `@24–46`, `@138–153`; drain `@13–92`. |
| Wrapper captured PRE A and POST C; A removes C | Removal can commit after PRE, but captured POST C still runs if PRE not cancelled. | wrapper snapshots `@0–24`; PRE leave `@185–186`; POST loop `@266–323`. |
| Wrapper has only queued PRE B, no PRE snapshot; B cancels PRE | Runnable still executes, and POST branch proceeds if otherwise successful. | wrapper `@216–234` or `@469–487`; cancellation test exists only `@189–212`. |
| Callback producer has committed snapshot and queues an add during first call | Producer is invoked a second time with a different closure, so producer side effects may repeat. | callback core `@21–30`, pending check `@47–67`. |
| A committed handler throws, committed reporter returns normally | Later committed handlers still run; ordinary normal decrement/commit remain reachable. | ordinary Throwable catch `65–81 →84`, continuation `@93–129`. |
| A queued handler throws `AbstractMethodError` after helper increment | Broader policy rethrows even for P=true; helper lacks finally-decrement. | helper `@101–129`, `@161–162`; broader policy `@24–39`. |

## 11. Candidate ledger entries for parent integration

These are **candidate local ledger IDs**, not fabricated REA `ev_*` references. All claims use the retained raw disassembly and mappings in this output directory; parent indexes were not changed.

| Candidate ID | Finding | Classification / primary locator |
|---|---|---|
| **S4-BUS-01** | Subclass is debugging/count variant, not extra affinity enforcement; selection solely `!P`. | **Confirmed**; B `<clinit> @0–11,93–116`; D complete body, guard `@9–24`. Contradicts JV-05/§3 variant inference. |
| **S4-BUS-02** | Base affinity check is warning/dump only; ThreadedEvent exemption; modern render predicate route. | **Confirmed**; B `_a140a8 @0–47`, BootstrapMethods #15; modern `_3d8570 @0–17`. Runtime state **Unknown**. |
| **S4-BUS-03** | Common ReentrantLock serializes public operations, with same-thread nesting and no automatic scheduling. | **Confirmed** lock control; blocking/thread consequence **Strong inference**. Public register `@0–54`, post `@5–56`, wrapper `@10–70`; generic helpers `@0–50/@0–49`. |
| **S4-BUS-04** | Exact Class-key array snapshots; exposed mutable map; observed diagnostic consumer locks correctly. | **Confirmed**; ordinary core `@0–11`, wrapper `@0–24`, getter `@0–4`; diagnostic `_f54c89 @12–35,247–260`; bounded search. |
| **S4-BUS-05** | Nonzero-depth add/remove queue; duplicates allowed; identity-all removal and dynamic-listener hook branches. | **Confirmed**; private register/unregister `@0–71/@0–50`; removal lambda `@33–81`; hook resolution `@0–77`, BootstrapMethods #4/#5. |
| **S4-BUS-06** | Committed sort uses int negation; equal priorities stable by library contract; MIN_VALUE edge; pending deliveries unsorted. | **Confirmed** key/calls, consequences **Strong inference**; add lambda `@29–66`, key `@0–5`, helper `@49–115`, BootstrapMethods #16. |
| **S4-BUS-07** | Lazy ordinary branches: null supplier result aborts helper; pending-only event delivery can still return null; supplier precedes depth. | **Confirmed**; ordinary core `@0–37,114–134`; helper `@82–107`. Corrects lazy/no-handler and constructed-once blanket claims. |
| **S4-BUS-08** | Pending add delivery before commit, remove ignored for delivery; cursor skips additions appended during pass. | **Confirmed** algorithm; symbolic effects **Strong inference**; helper `@65–115,138–162`. |
| **S4-BUS-09** | Normal commit only at depth decrement to exactly zero; ordered drain clears only after success; exceptions can strand state. | **Confirmed** control, effects **Strong inference**; enter/leave `@0–8/@0–14`, drain `@13–92`; dispatch catch/cleanup locations in §8. |
| **S4-BUS-10** | Callback producer can be called twice; callback closures lack lock/depth/lifetime guards; second call unprotected. | **Confirmed** body; escaped-callback possibility **Strong inference**, actual use **Unknown**. Core `_1253fc @16–80`; closures `@0–62/@0–7`; BootstrapMethods #8/#9. |
| **S4-BUS-11** | Wrapper captures PRE+POST first, constructs pair before Runnable; mode follows captured arrays/pending presence. | **Confirmed**; wrapper `@0–88,443–513`; Mode `wrapEvents @0–65`. |
| **S4-BUS-12** | PRE cancellation honored only with nonnull committed PRE snapshot/event, after all PRE handlers/helper/leave; queued-only PRE branches omit check. | **Confirmed**; wrapper `@107–234,469–487`. Ordinary/POST dispatch does not stop on cancellation. |
| **S4-BUS-13** | PRE/POST separate depth intervals; stale captured POST after PRE commits; committed POST omits pending helper. | **Confirmed** control; stale-snapshot consequences **Strong inference**. Wrapper `@0–24,177–186,232–346`. |
| **S4-BUS-14** | Committed Throwable reporter versus pending/producer Exception/Error policy; no finally-depth repair; wrapper catch range differs for pending-only/fast paths. | **Confirmed**; reporter methods `@0–38/@0–77`; ordinary/helper exception tables; wrapper `@352–440`, catch ranges `36–212/213–349` exclude `443–513`. |
| **S4-BUS-15** | Constructor lock supports same-bus blocking only through normal release; not entire constructor and no overall finally-unlock. | **Confirmed** control; blocking/leak effects **Strong inference**; client `<init> @38–44,1734–1758`, exception table. Qualifies §2/JV-03 lock claim. |

## 12. Coverage and residual unknowns

**Confirmed coverage:** complete B/D Code and verbose metadata; handler/pending records; mode factory; event/cancellation bases; ThreadedEvent marker; modern thread-predicate bridge; selected client lock boundary; both cached exact-owner diagnostic-access consumers; fresh hashes and cached/fresh comparisons. All requested bus subquestions are answered at branch level or explicitly bounded above.

**Unknown / not claimed:** actual runtime flag values, selected live bus/version, live interleavings, reporter/downstream dynamic-listener effects, non-cached or reflective accesses, actual callback escape by producers, incidence/recovery of stranded depth, and native/GameUI thread/paint behavior. U-07 is resolved **for the shipped Java bus implementation**, not for native UI affinity. Static code cannot certify that every client consumer obeys the exposed-map/callback lifetime contracts, and the adverse symbolic branches are not runtime-observed failures.

**Confirmed scope discipline:** no parent index/README/report edits; no catalog/audit redo; all new writes stay in `C:\Users\Admin\Downloads\New folder\lunar-analysis\session4-sol` and its `evidence-bus/` subdirectory.
