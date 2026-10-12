# Session 4 status, contradictions and next investigations

Date: 2026-10-11. Static-only investigation. This file supersedes the **named findings only**; parent reports/ledgers remain historical inputs, not overwritten. Confidence and location conventions follow [README](README.md). Evidence links and retained hashes are indexed in [evidence-ledger.md](evidence-ledger.md) and [finding-locations.tsv](finding-locations.tsv).

## Checklist closure

| Original topic | Outcome | Remaining boundary |
|---|---|---|
| U-07 event-bus threading | **Resolved for base/debug implementation and selected public paths** | Actual flag state, producer thread identities, runtime contention unknown |
| U-11 RpcChannel | **Resolved at channel level** | Transitive caller-specific deadlines/UI cleanup, exact maintenance timing not exhausted |
| Support `_83eb1a` / setFlipped | **Resolved for selected server/toggle/refresh recursion** | Producer ordering and exhaustive specialized support attachments remain partial |
| U-03/U-14 overrides | **Partial, materially advanced** | Boolean category priority/restoration and remote/criteria parser traced; all producers/broadcast/reset cases not exhausted |
| U-18 six additional modules | **Six bounded traces saved; partial** | Full custom layouts, selected bridges and producer/cancellation semantics remain open per report |
| U-07/U-08 native | **Partial** | Java contracts and export addresses/stub advanced; native threading/paint/marshalling not recovered |
| Evidence/cross-check/Git README | **Delivered** | Validation checks documents/provenance, not runtime correctness or publication rights |

## Corrections and confirmations against earlier work

| Earlier source / claim | Session-4 result | Evidence |
|---|---|---|
| [java-internals.md](../java-internals.md) §event bus: Strong inference that subclass enforces affinity; [class legend](../session2-class-legend.md) calls it thread-checked | **Correction:** base class performs gated predicate check, logging and stack dump. Debug subclass does not independently refuse wrong-thread dispatch. Flag names containing THROW are not behavior evidence. | S4-BUS-01; base `_a140a8 @0–47`; modern bridge `_3d8570 @0–17` |
| Java internals: additions queued during dispatch and flushed afterwards | **Clarification:** yes, backing arrays mutate at replay; additionally pending additions can be invoked in the **current** event. Pending removals leave captured arrays unchanged. | S4-BUS-03; pending helper `_cfe983(Class,event,Supplier) @21–165` |
| Java internals: per-handler exception isolation | **Qualification:** normal arrays have Throwable reporting, pending adds have a different exception policy, and dispatch depth is not universally protected by finally. | S4-BUS-04; supplier/internal wrapper/paired paths |
| Constructor lock prevents other threads dispatching while managers wire | **Confirmed with scope:** locked public dispatch region serialized; pre-lock thread diagnostics and externally exposed mutable map are not covered by that blanket statement. | S4-BUS-02 |
| [ipc-deep-dive.md](../ipc-deep-dive.md): unknown service produces no response; game relies on timeouts or ignores result (inference) | **Resolved:** cache has expireAfterWrite(10 MINUTES), but expiration logs only and disconnect explicitly invalidates silently. No channel-owned Future/controller failure completion. | S4-RPC-01/02/04 |
| IPC deep dive: RPC_RESPONSE completes pending call | **Qualification:** ID must match, pending entry is invalidated before parse, decode can fail without callback; successful callback is submitted through bridge, not completed in every response branch. | S4-RPC-03 |
| [feature-registration-deep-dive.md](../feature-registration-deep-dive.md): static supported filtering differs from server enablement | **Confirmed and extended:** parent/server/dynamic gates precede overrides; flip intent, ordinary toggle and effective flag differ. No need to repeat candidate catalog. | S4-SUPPORT-01/02 |
| [settings-persistence.md](../settings-persistence.md): effective reads differ from stored sparse saves | **Compatible:** override categories and restoration extend the effective-state model; six modules attach existing typed settings/HUD traits. No personal values re-read. | S4-SUPPORT-05/06; S4-MOD-01–06 |
| [native-analysis-preparation.md](../native-analysis-preparation.md): owner queue condition then unconditional native iteration | **Confirmed and extended:** static shared 4096 queue, inline async=true/queued async=false, no per-task catch in drain. Native threading remains unknown. | S4-NATIVE-03/04 |
| Session-3 JNI 56 declarations/58 exports and potential skew | **Confirmed discrepancy, interpretation not upgraded:** DLL-only symbols have executable entry RVAs; absence of Session.name/JNI_OnLoad in named exports is bounded. No observed lookup failure or universal absence of alternate registration. | S4-NATIVE-01 |
| CPU-backed rendering/texture callback inference | **Corroborated Java boundary, not native architecture:** logical texture IDs and bridge$uploadBgra traced; string/RVA evidence not a native callback call graph. | S4-NATIVE-02/06 |

No contradiction was found requiring changes to the resolved session-3 global HUD scale/snapping, registration-filter or ordered migration algorithms. Those reports were reused, not independently re-executed. This is a scoped comparison, not a verification of every prior sentence.

## Newly exposed conditional risks—not reproduced bugs

- Bus exceptional paths can bypass depth decrement even though lock cleanup runs; pending-only PRE cancellation differs from ordinary PRE; wrapper/deferred paths can invoke user factories more than once.
- RPC close/send race can leave pending tracking; malformed response removes tracking before failure; separate lookup/invalidate operations do not establish concurrent exactly-once completion.
- FunctionBus queue add can fail when full, unknown routine can leave Java promise unresolved, and callback exceptions are not Java-side promise rejection.
- NativeHandle/PromiseJS check-call-zero does not establish atomic completion/destruction; native arbitration remains unknown.

These are conditional consequences of cited code and ordinary Java library semantics. No Lunar runtime was started to reproduce them.

## Recommended next work, priority order

1. **Static and already supported:** audit bus callers of mutable-map/wrapper/paired APIs for assumptions about current-event additions, cancellation and depth balance. Trace non-auth IPC caller pending-state cleanup after expiration/disconnect, rather than repeat service schemas.
2. **Static feature propagation:** enumerate remaining override producers/removal paths and specialized setting interceptors; check whether each calls normal toggle lifecycle or merely effective recompute. No server contact or personal override file reads.
3. **Static module finish:** identify reach distance producer and bridge counter field; confirm combo attacker bridge semantics; complete armor protection/bars/individual layout, potion mode spacing/blink/inventory hooks, toggle flight/reset formulas, and pack child/dimensions/texture replacement lifecycle.
4. **Needs explicit configuration approval:** configure a native analysis provider, then follow `WebOSR_createEngine RVA 0x10a30`, iteration helper `0x199c0`, texture callbacks, JNI descriptor lookup and teardown. Do not equate a forwarding stub/vtable slot with an identified Render method.
5. **Only with separate runtime approval:** actual queue/paint cadence, callback thread, close races and IPC sequence. No such approval exists. Actual launcher POST/launch response, Ichor ordering, other launcher handlers and dormant ChatService questions retain prior open statuses.

## Preservation and tooling limitations

- New findings are inside `session4-sol`; the only new root-level report is the requested [Git README](../README.md).
- An existing Git repository was found during finalization; no init/stage/commit/push/reset performed. Git baseline comparisons are against its current HEAD, **not an invented pre-session hash snapshot**.
- Historical ledger-prefix digests from session 3 can independently check that the older prefixes remain unchanged. Git's `text=auto` can make stored blob bytes differ from working-file line endings; byte and CRLF-normalized comparisons are reported separately. See [validation](session4-validation.json) for exact coverage.
- Parallel collectors reached a usage limit. Their saved evidence was reused; no worker completion or exhaustive coverage is inferred from retained files. Some bounded searches are empty/UTF-16 and require care.
- Ghidra remains unavailable/not_configured. No tooling installed/configured and no target code executed. REA's open native target is closed at finalization; its evidence export and [lifecycle result](rea-session-close.json) are preserved.
