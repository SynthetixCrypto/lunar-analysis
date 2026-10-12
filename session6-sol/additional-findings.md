# Session 6 — Additional implementation findings

Date: 2026-10-11. These extend the open Session 5 gaps; they do not repeat its verified Session 4 headline findings. Confidence and alias conventions are defined in [java-gap-resolution.md](java-gap-resolution.md). Offsets below are method-local JVM offsets. Exact artifact/class identities and evidence are in [evidence-index.md](evidence-index.md).

## G-01: armor geometry and protection estimate recovered

**Confirmed retained bytecode; details and bounded limits in [armor-followup.md](armor-followup.md), S6-AR-01..05.** Group HUD `L._88f3cf._bb4487._21aca6._1e73d7._590f69._cfe983 @8–217` lays out vertical elements with maximum width and summed heights, horizontal with summed widths and maximum height, normally adding two-unit inter-element gaps and four-unit outer dimensions. Degenerate zero-size elements affect gap accumulation. Individual equipment children have independent HUD settings/placement; their `_52e8ee @8–105` gate requires non-vanilla mode, moveArmorIndividually, typing permission and a present element.

Protection child `_590f69._cfe983._cc7511 @126–376` aggregates armor points and the first bridge-qualified protection enchantment per stack. Its term is literally `floor(((6+level) XOR 2)*0.75/3.0)`; bytecode `ixor @286` rules out silently interpreting this as exponentiation. It calculates `P=min(min(E,25)*.04f*.75f,.8f)` and `R=1-(1-A*.04f)*(1-P)`, displaying `R*100`. Toughness has a separate label and does not enter that expression. This is a displayed estimate, not proof of Minecraft damage equivalence; exact bridge protection-type qualification remains untraced.

Custom icon child `_cfe983._21aca6._8ca005 @0–329` allocates up to 20 point records in HEAD/CHEST/LEGS/FEET order, capped by totalArmorValue; ten icons pair records and may draw different halves. Alternate equipment renderer `_1e73d7._bb4487` uses 20-unit pitch, dimensions/scale/extraTop formulas documented in the supplement. Material color tables, complete version-specific hotbar anchoring, texture/glint internals, persistence and runtime visual parity remain open. [Focused methods and identities](evidence-armor/focused-excerpts.json) preserve the exact evidence.

## G-02: potion behavior recovered

**Confirmed, retained renderers and modern inventory families.** [potion-followup.md](potion-followup.md), S6-PE-01..04, resolves the named blink, ordering, outer spacing and inventory cancellation questions.

Shared renderer `L._88f3cf._bb4487._52e8ee._bb4487._d4ca6c(effect) @29–118` computes icon alpha, with duration `d=int(duration)` and threshold `T=blinkDuration*20`:

~~~text
alpha = clamp(clamp(2*d/T,0,0.5)
            + cos(d*pi/5)*clamp((1-d/T)*0.25,0,0.25),0,1)
~~~

The curve applies only when potionBlink and potionBlinkIcon are enabled, the effect is nonambient and `0<=d<=T`; otherwise icon alpha is 1. The math bridge annotation identifies cosine. Duration text uses a separate renderer counter, shows at <=10 and resets during draw after >20. Icon and text phases therefore have different sources; runtime cadence was not measured.

NORMAL and MINIMAL preserve the input bridge collection order. VANILLA sorts ambient first; its ordinary branch then orders negative duration first, duration descending and color descending. If both durations exceed 32147 or both are ambient, it omits the duration tests. `L._88f3cf._bb4487._52e8ee._d4ca6c._cfe983(a,b) @0–164` is the comparator authority.

The recovered outer geometry is mode-specific: NORMAL uses 22-unit rows and height `22*n+2`; MINIMAL uses tile side 41 with background/border, else 30, plus padding-dependent stride; VANILLA uses 24-unit tiles at 27-unit stride and group/short-line alignment. MINIMAL reverse wrapping uses `floor(n/k)*stride` when `n>k`, retaining an extra origin step at exact multiples. These exact quirks and complete dimension/alignment formulas are preserved in [potion-followup.md](potion-followup.md), not smoothed into approximate layouts.

Modern inventory mixins under `ML._d4ca6c._590f69._21aca6._1e73d7._21aca6._590f69._590f69` directly cancel HEAD effect drawing/visibility hooks when the module is enabled and showInInventory is false. `_d4ca6c.lunar$renderEffects @0–38` and `_13ea87.lunar$checkEffectRendering @166–202` are representative confirmed hooks, with cancellable annotations in [focused-excerpts.json](evidence-potion/focused-excerpts.json). This is concrete injection evidence, not an inferred event-bus cancellation. All legacy parity, live input order and every inner scaling variant remain open.

## G-14/G-16/G-17: RPC edge cases narrowed

**Confirmed precursor; Derived failure.** Embedded `Draft_6455.processFrameContinuousAndNonFin @69–104` constructs int-only `InvalidDataException(1007)`, which delegates to Exception() without assigning a message. `WebSocketImpl.decodeFrames @106–132` forwards this exception before closing, and Lunar transport `onError @0–6` calls `getMessage().startsWith` without a null guard. If that shown branch occurs, the error handler throws NPE and skips that intended close on that pass. The outer receive-loop error path may run afterward; actual terminal ordering remains unknown. No malformed-input experiment was performed. [rpc-findings.md](rpc-findings.md), S6-RPC-02, cites library and JDK constructor bodies separately.

**Confirmed receive topology; Derived serialization.** `WebSocketClient.run @377–415` reads/decode/callbacks synchronously on one receive thread; the sole retained Lunar response-accept caller is transport onMessage @35–43. Duplicate frames on this path cannot overlap cache lookup/invalidate, even though the channel API itself is non-atomic. This closes G-16 for the shown normal transport path, not arbitrary concurrent API invocation. [rpc-findings.md](rpc-findings.md), S6-RPC-03.

**Partial G-17.** Transport constructor @40–49 owns a new channel/cache per instance; reconnect does not migrate pending entries. Main worker `_a61e7a @0–21` closes the old transport only when isOpen, so a replaced CONNECTING/CLOSING instance can retain active read/write threads and its cache. Clearing the main field is not a proof of prompt collection or leak. Thread termination/late responses/GC remain open. [rpc-findings.md](rpc-findings.md), S6-RPC-04.

**Confirmed shared field.** Tebex and PayNow capability callbacks both assign `_5e258b @55`; if their values differ, the last processed response wins. This does not establish differing deployed responses. [rpc-findings.md](rpc-findings.md), S6-RPC-05.

## G-21/G-22: dependencies and source arbitration

**Confirmed.** Dependency collector `L._ba7d98._bb4487._4cf8c3(Supplier) @0–150` captures actual observable reads in a temporary identity set, evaluates @15–21, removes obsolete callbacks @26–88 and then adds new ones @91–146. Setting/value setters update before listener notification. Allowance callback `L._88f3cf._1e73d7._a1dd3a._91843f @0–101` suppresses unchanged flags and lifecycle-before-COMPLETE work, then selects effective recompute or the full toggle path. This resolves successful local sequencing, not independent brand/world/Apollo/disconnect arrival order.

**Derived conditional risk.** That collector uses one static temporary slot with no finally around Supplier.get. A throwing supplier can leave it installed; nested collection can replace the outer slot. No live corrupted graph/race was reproduced. [support-findings.md](support-findings.md), S6-SUPPORT-07.

**Confirmed G-22.** Generic settings use one last-accepted override slot, not Boolean feature category priority. The only additional direct interceptor implementation found is a BooleanSupplier forcing decorator, which delegates writes/reset/predicates but can mask reads. Server refresh's unguarded SERVER/null request can clear a generic override of another category. Per-type parsing remains in settings. [support-findings.md](support-findings.md), S6-SUPPORT-03..06; the hierarchy scan is bounded to 8,095 retained classes.

## G-30/G-32: Java-native boundary gains

**Confirmed Java contract, native lifetime unknown.** Modern `bridge$uploadBgra @54–104` uses `sourceY*stride + sourceX*4`, with per-row byte stride. Ordinal >=29 compacts and swaps B/R; older GL uses rowLength=stride/4 and restores state even on exceptional exit. A single reusable static staging ByteBuffer has no Java synchronization. This is not proof of native callback concurrency, premultiplication, source ownership or GPU-retention behavior. Reverse framebuffer readback swaps B/R in place before native TexturedImageSource.update; native copy versus borrow is unknown. [jni-and-webosr.md](jni-and-webosr.md), S6-WEB-02/03.

**Confirmed Java data flow; Derived codec consequence.** FunctionBus's captured reflection Class reaches PromiseJS.resolve through buildInvocationParameters @257–273. Base objectToString dispatches on that supplied Class; Lunar's subclass catches unsupported-type exceptions and uses Gson.toJson(value). A reflection implementation class rather than generic T can therefore select Gson fallback, including JSON quoting for strings. Exact runtime reflection classes and native parsing/null semantics were not observed. [jni-and-webosr.md](jni-and-webosr.md), S6-WEB-04. Native marshalling parity remains open.

## G-33: FunctionBus caller and queue recovery boundaries

**Confirmed Java paths; practical behavior still Unknown.** The only external direct Java invoke caller in the retained cache is `L._81676d._21aca6._cfe983._bb4487._cfe983(PromiseJS,Browser,String[]) @22`, annotated CallbackJS("invoke") with async default false. Its body takes args[0], forwards remaining arguments and returns without a queue guard, catch, retry or promise rejection. An empty argument array has a separate conditional bounds-exception path. Child delegation is an additional same-class invocation, not another external caller.

FunctionBus's queue field accesses are allocation, poll and add; capacity is 4096 and invoke @172–189 directly adds outside its local exception handlers. The queue's standard add failure is corroborated with local JDK bytecode. Unknown selected routines return @98; because the annotated router accepts PromiseJS, automatic completion is suppressed and the router adds no completion. `consumeMainActorQueue @0–23` does not catch task failure; WebEngine.invokeIteration drains before native iteration, and its three direct Java callers have no local catch covering the iteration call. **Derived:** an escaping task failure can skip that native iteration and leave later tasks queued. Actual saturation, later recovery and native exception/promise translation remain unknown. [functionbus-followup.md](functionbus-followup.md), S6-FBUS-01..04, records exact callers, registration and exception-table bounds.

## Independent-client design implications

These are analyst recommendations, not additional claims about Lunar:

- Specify raw settings, effective settings, selected feature overrides, allowance and active handlers as distinct state. Choose and document whether to reproduce generic last-write arbitration and category-blind clears.
- Use entity-tick correlation and outgoing-target identity if reproducing the documented reach/combo behavior; specify same-tick deduplication and stale timestamp consumption explicitly.
- Make event dispatch scopes and deferred replay exception-safe, and document whether batch factories may run more than once.
- Make transport loss release checkout UI independently of a normal close push. Keep command acknowledgement separate from periodic radio state synchronization.
- Define buffer ownership, copy/borrow duration, pixel format, stride, thread affinity and destruction order before implementing browser rendering. Java evidence alone cannot supply the missing native contract.
- Give callback queues explicit backpressure and promise completion/error rules, including unknown routines and task failure during draining.
- Use the recovered potion formulas as specification inputs; explicitly decide whether quirks such as exact-multiple reverse padding are compatibility requirements.

The complete unfinished-gap ledger is [remaining-unknowns.md](remaining-unknowns.md). Native questions and exact provider-dependent next actions are in [native-rendering-analysis.md](native-rendering-analysis.md).
