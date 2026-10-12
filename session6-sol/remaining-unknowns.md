# Session 6 — Remaining unknowns and gap ledger

Date: 2026-10-11. This supersedes only the *status* of investigated entries in [Session 5 remaining-gaps.md](../session5-deepseek/remaining-gaps.md); it preserves that report and its original definitions. “Bounded resolved” means the specified static implementation scope, not runtime verification or all-version parity. No target launch, private service or personal-state inspection was authorized/performed.

## Priority conclusions and genuine blockers

G-04/G-05, the specified G-13 callers and direct-call G-11 audit are bounded resolved. G-18/G-19 have substantially complete retained producer/interceptor/reset models, with external/dynamic callers and broader metadata-deletion behavior still open. G-10 now has concrete exception chains, but no observed failing workload. See [java-gap-resolution.md](java-gap-resolution.md).

The current REA environment already accepts the intended full JDK 21. No Java repair is outstanding. Ghidra remains unconfigured and a bounded installation search found no usable installation. The user's explicit approval requirement prevents installing it autonomously. No native decompiler/database was opened. Therefore native ownership, paint callbacks, threading, synchronization, registration and failure unwinding remain blocked on provider availability. [native-rendering-analysis.md](native-rendering-analysis.md) records N-0..N-8, all 16 questions and exact next actions.

## Original G-01 through G-33

| Gap | Session 6 disposition | What still needs evidence / next useful work |
|---|---|---|
| G-01 armor | **Bounded resolved named layout/aggregation formulas** | Material color/UV/glint internals, full version hotbar anchoring, exact protection bridge qualification/map order and persistence remain open; [armor follow-up](armor-followup.md) |
| G-02 potion | **Bounded resolved** for named remaining formulas/hooks | NORMAL/MINIMAL live bridge collection order, all legacy hooks, selected version and every internal icon/text scale variant remain unknown; [follow-up](potion-followup.md) |
| G-03 toggle sneak | Not investigated anew | Exact flight/motion formula and special-version sync/reset/cancellation paths remain open |
| G-04 reach | **Bounded resolved**, modern retained producer/counter/periodic timing/range source | Selected cache/version, legacy parity, runtime packets and cadence remain unknown; [reach/combo](reach-combo-findings.md) |
| G-05 combo | **Bounded resolved**, modern bridge plus inspected Minecraft writers | Actual packet/order/selected-cache behavior; same-tick dedup is a derived consequence, not measured hit registration |
| G-06 pack display | Not investigated anew | Full custom geometry, child HUD/color propagation, reload sequence and texture release |
| G-07 other features | Not investigated anew | Choose feature algorithms by intended independent-client scope, not a fresh catalog inventory |
| G-08 bus diagnostic selection | Not investigated anew | Runtime diagnostic flag remains unknown; further static subclass/initializer selection could be useful without reading personal values |
| G-09 producer threads/contention | Runtime-gated, unobserved | Real thread identity, contention and deadlock behavior require separately authorized observation; static thread bounds remain possible |
| G-10 bus failure/depth | **Partial: concrete static paths** | Identify a legitimate shipped workload that actually triggers leaking depth/stale replay; no reproduction or frequency claim; [bus report](bus-findings.md) |
| G-11 exposed map/wrapper callers | **Bounded resolved**, 8,095-class direct-reference scope | Reflection/external/future callers excluded; exact map reader is locked diagnostic only; batch production may repeat |
| G-12 pending-only PRE | Open reachability | Find a concrete nested listener-add/cancellation sequence in hotbar/screen callers; branch existence alone was previously resolved |
| G-13 caller abandonment | **Bounded resolved**, specified 16 methods and traced UI/callback state | No demonstrated pre-send request-pending latch; separate checkout close-push cleanup and stale radio state remain limited findings, not universal UI recovery; [RPC](rpc-findings.md) |
| G-14 null onError message/order | **Partial: artifact-contained null-message path** | Actual arrival/terminal error-close order and launch-JVM NPE message behavior remain unobserved |
| G-15 Guava maintenance | Not investigated anew | Exact retained-version logical expiry/physical removal/notification timing remains open |
| G-16 simultaneous accept | **Bounded resolved for normal receive path** | Serialized receive excludes overlapping duplicate-frame acceptance; concurrent external/manual/reflection API invocation remains outside proof |
| G-17 discarded transport | **Partial: per-instance ownership and retention paths** | Old active thread termination, late activity, queued callbacks and GC timing are not established; no leak claim |
| G-18 every override producer | **Substantially resolved within direct retained calls** | 46 override/criteria/removal instructions and 32 setter instructions classified; reflection/plugins/native/absent artifacts and live order excluded; [support](support-findings.md) |
| G-19 reset/removal/interceptors | **Bounded resolved reset/hierarchy; partial remote deletion** | Criteria definitions persist; omitted metadata does not clear in inspected loaders. Other refresh/removal producers or live service semantics remain unknown |
| G-20 independent producer order | Open | Actual brand/world-ready/Apollo/disconnect interleaving; successful local callback sequencing does not impose an external total order |
| G-21 allowance dependency order | **Partial: successful local sequencing resolved** | Static read capture, update-before-notify and remove-before-add proven; live trigger order, nested/throwing supplier occurrence remain open |
| G-22 non-Boolean precedence | **Bounded resolved retained interceptor hierarchy** | Generic single-slot last accepted write, category-blind clear and forcing decorator proven; external implementations/per-instance supplier state excluded |
| G-23 personal profile outcomes | Out of scope | No personal/inactive profiles inspected; migration ledger was already resolved and not repeated |
| G-24 coordinates grouped formatting | Not investigated anew | Grouped-format parity remains open |
| G-25 all-version branch matrix | Partial incidental gates only | Reach, potion and GPU gates documented locally; no full matrix across all feature branches |
| G-26 ordinal mapping | Not investigated anew | No complete ordinal→Minecraft-version mapping; suffixes/annotations are exact local evidence, not a universal mapping |
| G-27 selected owned launch | Out of scope without authorization | No selected launch/profile/cache/JRE inferred from retained artifacts |
| G-28 native threads/paint | **Blocked on deep native provider** | Actual paint scheduler/callback cadence, worker construction/join, lock/atomic model |
| G-29 native helper/vtable semantics | **Blocked on deep native provider** | Resolve createEngine, helper RVA199c0, pointee+e8, virtual slot+8 with actual callee bodies |
| G-30 native texture path/lifetime | **Partial Java contract; native blocked** | Byte stride, source/dest region, swap and Java cleanup proven; actual callback path, native allocator/owner, copy/borrow, cleanup/joins and premultiplication unknown; [JNI/WebOSR](jni-and-webosr.md) |
| G-31 Session.name linkage/callers | **Partial reconciliation; native registration blocked** | 55 shared + Java-only name + 3 DLL-only symbols; no Session symbolic refs in four JARs. RegisterNatives/reflection/other-library/native callers and actual linkage behavior unknown |
| G-32 JS generic codec | **Partial Java completion flow; native parity blocked** | Captured reflection Class→Gson fallback path traced; native text parsing, JS type/null semantics and promise ownership remain unknown |
| G-33 queue/promise behavior | **Partial caller/guard/recovery audit** | Identified Java route has no guard/recovery; no practical saturation, native exception translation, JS timeout/retry or promise-lifetime measurement; [FunctionBus follow-up](functionbus-followup.md) |

## Native questions that Java cannot close

Even with both transfer directions now documented, native evidence is still required for:

- TextureHandler GetMethodID/Call*Method sites, callback thread and retained JNI references.
- Native surface/frame-buffer allocation, resize, pointer validity, copying/borrowing and destruction.
- Paint generation, dirty-region selection and scheduling, workers, synchronization and affinity.
- Browser/engine initialization failure unwind, destruction order, worker joins and callback unregistration.
- Session.name alternate registration and actual users of getName/swapBuffers/setTimers.
- Native promise/value conversion, exception translation, resolution and cleanup.

Do not promote a Java signature, native string/RTTI hit, DLL export or forwarding stub into a native implementation conclusion. The [16-question table](native-rendering-analysis.md) remains the next native pass's acceptance checklist.

## Original B-01 through B-05 boundaries

| Boundary | Session 6 action |
|---|---|
| B-01 launch service response/artifacts | No service request; remains outside current scope |
| B-02 live stdout/IPC handshake | No launch/observation; remains outside current scope |
| B-03 performance/startup/FPS | No measurement; remains outside current scope |
| B-04 Replay/Reverse and remote/social internals | No deeper feature/service investigation. Existing iteration/pre-tick caller bodies appear only to bound ordinary API behavior |
| B-05 anti-cheat/integrity | Not investigated; no bypass or protection modification |

## Session 7 priority

First choice is **further native static analysis once Ghidra installation is approved and the provider passes its live probe**. The exact binary digest, five address seeds, JNI mismatches, both pixel-transfer directions and 16 unanswered questions give that pass a concrete target. Installing/configuring the provider is the only installation approval dependency; no system-wide Java change is needed.

If that prerequisite remains unavailable, prioritize **implementation-ready technical specifications** for the now-resolved settings/support, event dispatch, RPC caller and reach/combo/potion behavior. The reports are detailed enough to define states, contracts and edge-case decisions without more inventories. Additional feature algorithms such as G-03/G-06 or a chosen G-07 module should follow the independent client's requirements. Runtime observation and private services are not implicit next steps.
