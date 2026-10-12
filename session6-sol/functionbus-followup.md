# G-33 FunctionBus caller, guard, and recovery follow-up

2026-10-11. Static only. G-33 asks whether queue-full and unknown-routine unresolved-promise behavior occur in practice; its authorized static follow-up is to audit invoke callers and queue-depth guards. This report resolves those Java-side boundaries, not observed saturation or native promise behavior. Session 4 wrapper findings are prerequisites and are not re-investigated as new discoveries.

Evidence is in evidence-functionbus/manifest.json: exact original class names, fresh JDK 21 javap verbose files and SHA-256 hashes. Aliases follow existing reports. Offsets are JVM instruction offsets. The direct-reference scan covers 8,095 retained cache classes; reflection, JNI dispatch, runtime-generated/external classes and absent version artifacts are excluded. Fresh javap corroborates all reported method bodies.

## The actual Java caller adds no guard or recovery

**Confirmed — S6-FBUS-01.** The only external direct Java call to FunctionBus.invoke in the full retained-cache scan is L._81676d._21aca6._cfe983._bb4487._cfe983(PromiseJS<String>,Browser,String[]) @22. The complete body @0–25 obtains the current bus @0–4, takes args[0] as routine name @9–11, copies args[1..length] @12–19, invokes @22, and returns. There is no queue size/remainingCapacity check, retry, catch, timeout registration, reject, or fallback in that body. There is also no empty-argument guard before args[0]. An empty array therefore has a separate conditional ArrayIndexOutOfBoundsException path before bus invocation.

The method has @CallbackJS(value="invoke") with no async element. CallbackJS.async has AnnotationDefault false. L._81676d._21aca6._21aca6 constructor registers this callback object with its root bus at @239–249; when configured, it also registers child buses @336–362. Browser factory L._81676d._21aca6._21aca6._cfe983._cfe983(int,int,double,Listener) binds lunarInternalInvoke to the root FunctionBus @56–64. This establishes the Java registration route, not native callback timing or caller-thread identity.

FunctionBus itself makes a recursive child invoke at @73. The qualified-call cache scan misses that unqualified same-class javap comment, so the final call set is external callback @22 plus child delegation @73. FunctionBus's Lunar subclass L._81676d._21aca6._590f69._cfe983 overrides only stringToObject/objectToString; it adds no invoke, enqueue, drain or recovery guard.

## Queue capacity is unchecked at the enqueue site

**Confirmed — S6-FBUS-02.** Exact MAIN_ACTOR_QUEUE field accesses across the cache are FunctionBus.consumeMainActorQueue @0, FunctionBus.invoke @172, and FunctionBus.<clinit> @10. No subclass or caller directly reads size(), remainingCapacity(), isEmpty(), or performs offer/put on this field. The constructor allocates ArrayBlockingQueue(4096); the non-async branch directly calls add @186. Its exception table covers parameter conversion @99–113 and immediate callback execution @136–157, but not enqueue @172–189. No Java retry/drop policy, queue-depth guard, backpressure, or explicit promise rejection protects this add in the inspected route.

**Derived — conditional, not reproduced.** When the queue is full at add, standard ArrayBlockingQueue/AbstractQueue add semantics throw IllegalStateException. The local JDK 21 AbstractQueue.add bytecode, retained in jdk21-AbstractQueue.txt, calls offer @2 and throws IllegalStateException("Queue full") @10–19 when offer is false. This substantiates the Java library consequence; it does not show which JRE an owned Lunar launch selects or show actual saturation.

The annotated invoke router itself defaults to non-async. Therefore, if dispatched through the registered root bus, it is eligible for that root bus's queue before it routes to a selected child/routine. The routed target can enqueue another task if its own async flag is false. These are possible Java branches, not a claim about measured queue growth, callback rate, or native schedule.

## Unknown routines do not acquire a Java recovery path in the caller

**Confirmed — S6-FBUS-03.** FunctionBus.invoke returns directly at @98 for absent selected routine after child delegation. The external annotated router simply returns after its invoke call @25. Because the router takes PromiseJS, its MethodInstancePair has hasPromiseJS; completePromiseIfNeeded @0–7 leaves completion to the callback. The router does not resolve/reject in its body. No finally or completion-on-return logic appears around its nested invoke. Thus unknown nested routines have no Java promise completion in this route, including the annotated router wrapper. This closes the caller-side recovery audit; it does not prove the native promise remains unresolved forever.

Parameter failures become RuntimeException @116–127; immediate callback failures become RuntimeException @160–171; queued callback failures become RuntimeException in lambda$invoke$0 @21–32. These Java bodies do not reject the promise on those failure branches. Native JNI exception-to-JS rejection conversion remains unknown and requires native implementation evidence.

## Java drain callers do not catch queued callback failures locally

**Confirmed — S6-FBUS-04.** consumeMainActorQueue @0–23 polls then runs each task @14–15 without a catch. WebEngine.invokeIteration drains @13 only when currentThread equals its recorded owner, then calls native invokeIteration0 @17. It does not catch drain failure.

The full retained-cache scan finds three direct callers of WebEngine.invokeIteration:

| Java caller | Call offset | Local boundary |
|---|---:|---|
| L._81676d._21aca6._590f69._02d7ad(render-context) | @31 | Engine-non-null and elapsed-time >=5 ms gate @7–25; timestamp write @34–38 only follows successful return. No exception table. |
| L._88f3cf._bb4487._00f454._d4ca6c._bb4487._590f69._cb9292(render-context) | @169 | Repeats while relevant effect/profile condition holds and Browser.getTexture() == -1 @140–175; calls Thread.yield after iteration. No exception table or queue-depth guard. |
| L._88f3cf._bb4487._00f454._d4ca6c._21aca6._0ee944() | @40 | Rewind loop calls iteration every twentieth loop count @26–40. Its only Exception handler protects @48–56 processRewindTick, not @40 iteration. |

**Derived:** a queued task failure aborts that drain call after the task has been polled, leaves later tasks queued, skips invokeIteration0 for that wrapper call, and escapes each of these immediate Java callers. Wider Minecraft/event-bus caller policies and native callback entry exception handling are separate boundaries; this audit does not claim the application stops or never drains again. The elapsed-time gate and texture/rewind loops are iteration conditions, not queue-capacity control.

## Disposition

G-33 is **statically bounded / partially resolved**: the identified Java caller and drain paths add no queue-depth guard or promise recovery, and annotated nesting does not complete unknown calls. Actual queue saturation, native exception translation, native promise cleanup, JS timeout/retry policy, scheduling rate and practical unresolved-promise duration remain unknown. Do not mark the original in-practice question fully resolved without authorized runtime or concrete native code evidence.
