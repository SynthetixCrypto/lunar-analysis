# Session 7 — Remaining gaps and acceptance checklist

Date: 2026-10-12. This updates investigated statuses, preserving [Session 6's G-01–G-33 definitions](../session6-sol/remaining-unknowns.md). Static verification is not runtime verification.

## G-28–G-33 disposition

| Gap | Session 7 status | Remaining question |
|---|---|---|
| G-28 native threads/paint | **Substantially advanced, partial** | Worker creation, actors, scheduling and join resolved. Runtime thread identities/cadence, full rasterizer internals, queue memory-order proof and failure-before-ready remain unknown. |
| G-29 native helper/vtable semantics | **Bounded resolved** for five seeds and iteration chain | JNI handle helper, wrapper `+0xe8`, EngineImpl vtable and actor pump resolved. Broader native API coverage is not implied. |
| G-30 texture path/lifetime | **Substantially advanced, partial** | Three CPU records, dirty rectangles, pull-triggered upload, stride, immediate reverse copy and CPU destruction resolved. GPU delete chain, premultiplication, source-object queue lifetime and complete unwind remain open. |
| G-31 Session.name linkage | **Partial; negative search bounded** | Fresh 55/1/3 mismatch and actual `getName` body resolved. No alternate registration proved. Other-module/computed registration and actual use remain unknown. |
| G-32 JS generic codec | **Not resolved in this pass** | Native JS type/null handling, text parsing, promise/value ownership and Java codec parity require dedicated tracing. |
| G-33 queue/promise behavior | **Partial** | Native actor inline/queue/full-yield behavior and callback exception clear observed. JS promise lifetime, retry/timeout and practical saturation remain unobserved. |

G-01–G-27 were not reopened as feature investigations. Existing bounded Java conclusions stand only within their earlier evidence. No runtime/private-service/personal-state boundaries were widened.

## All 16 inherited native questions

| # | Question | Status and evidence-backed answer | Residual uncertainty |
|---|---|---|---|
| 1 | Helper `0x199c0` and `+0xe8` object | **Answered:** handle field lookup; wrapper holds shared EngineImpl at `+0xe8/+0xf0`. [Evidence](evidence/engine-handle.json) / [wrapper](evidence/engine-wrapper-ctor.json) | All stale-handle/failure paths |
| 2 | Vtable `+8` action | **Answered:** EngineImpl `0x18003aeb0` → TLS actor pump `0x180036320`. [Evidence](evidence/engine-iteration.json) | Broader iteration guarantees |
| 3 | Frame via callbacks or Java pull | **Answered for normal chain:** worker publishes CPU frame; Java `getTexture` causes callbacks. [Evidence](evidence/swapchain-get-texture.json) | Other API/caller routes |
| 4 | Distinct paint callback | **Partial:** traced worker/Painter/surface path; upload is TextureHandler callback, not established Browser.Listener paint. [Evidence](evidence/worker-run.json) | Complete internal paint callbacks |
| 5 | Bitmap/surface allocator/owner | **Answered for custom path:** factory allocates Swapchain, three CPU records, owned destruction; default delegates bitmap factory. [Evidence](evidence/surface-create.json) / [records](evidence/pixel-buffer-init.json) | Default bitmap implementation internals |
| 6 | Surface vs engine/texture lifetime | **Partial:** shared handler ownership, surface-owned CPU storage, engine join established. [Evidence](evidence/swapchain-dtor.json) | GPU texture delete and all cross-object failure lifetimes |
| 7 | Format and stride | **Partial, strong contract:** 4-byte pixels, configured byte-row alignment, BGRA Java consumer; reverse size explicitly BGRA8. [Evidence](evidence/swapchain-stride.json) / [validation](evidence/image-upload-work.json) | Alpha/color space and full rasterizer format path |
| 8 | Iteration thread/workers | **Answered statically:** native worker + actor-0; construction caller actor-1; native iteration pumps caller TLS. [Evidence](evidence/engine-impl-ctor.json) | Actual runtime thread IDs/cadence |
| 9 | Native synchronization | **Partial:** atomic registry guard, refcounts, actor queue and swapchain ring mechanisms identified. [Evidence](evidence/worker-run.json) / [dispatch](evidence/actor-dispatch.json) | Memory-order proof and contention |
| 10 | Native affinity | **Partial:** registered actor thread determines inline vs queue; texture callback follows getTexture caller. [Evidence](evidence/actor-dispatch.json) | Universal enforcement across every API |
| 11 | JNI TextureHandler | **Answered for upload:** GetMethodID/signature, jvalue array, CallVoidMethodA, local-ref delete verified. [Evidence](evidence/upload-call-assembly.json) | All callback failure/lookup edge cases |
| 12 | Create/resize/upload/delete | **Partial:** create/resize/upload caller order resolved; delete method identified. [Evidence](evidence/swapchain-get-texture.json) / [delete](evidence/jni-delete-texture.json) | Complete normal-shutdown delete caller |
| 13 | Dirty-region uploads | **Answered statically for custom surface:** clipped current + two previous damage rectangles, merge/dedup, per-region upload. [Evidence](evidence/dirty-regions.json) | Runtime cadence / all-interleaving correctness |
| 14 | Engine destruction | **Partial, major advance:** stop closure → ack → join → resource release. [Evidence](evidence/engine-dtor-body.json) | Callback unregistration, failures and GPU release |
| 15 | Session.name registration | **Unresolved linkage:** getName body established; bounded scans found no proof of alternate registration. [Evidence](evidence/registration-bounded-scan.json) | Computed/other-module registration or runtime linkage |
| 16 | swapBuffers/setTimers legacy/dead/registered | **Partial:** real bodies and absent Java declarations verified. [Evidence](evidence/jni-reconciliation-fresh.json) | External/native/dynamic callers; deadness not established |

## Highest-value next static work

### P1 — Complete graphics-resource destruction

Start from binding `JniTextureHandler::delete` implementation `0x18002d630`, handler vtable `+0x28`, supplier cached ID, Java handler `deleteTexture` and browser/source close chains. Existing `procedure_references` evidence includes indirect/data-reference limitations; no direct caller list can settle a virtual call by itself. Inspect implementing virtual callsites and Java owner cleanup paths. Goal: one complete ownership chain from allocation to graphics destruction, including failed create/resize and close with queued work.

### P2 — Source-object lifetime and queue correctness

Reverse update closure owns copied bytes but captures a native source pointer. Trace size/update/unbind/destroy ordering, weak/strong captures, actor draining at close, and synchronous same-actor dispatch. For swapchain publication, inspect listing and memory barriers around queue read/write indices and derive the actual producer/consumer assumptions. Do not label it race-free from x86 stores alone.

### P3 — Failed construction and JNI attachment ownership

Inspect worker exception boundaries and the ready/stop acknowledgment protocol. Trace Environment allocations and destruction; `attachShared` cleanup invoke is a no-op, but other thread-exit/detach mechanisms remain possible. Follow reference wrappers rather than treating names as ownership proof.

### P4 — Resolve renderer and surface dependency tails

In `Ultralight.dll`, continue per-view helper `0x1800030b0`, Painter virtual `+0x20`, and view `+0xe8` → nested virtual `+0x40`. If needed open `UltralightCore.dll` with its already recorded digest. Correct provider prototypes/no-return flow only as analysis metadata, keeping original bytes immutable. Goal: name exact operations and establish alpha/surface layout from shipped code, not assumed public SDK parity.

### P5 — Dedicated native JS/promise trace

Use retained Java FunctionBus evidence to select native entry points. Trace conversion, exceptions, completion, cancellation and retained JS values/promises separately from actor transport. Current queue findings do not close G-32.

### P6 — Broader registration proof

Extend a typed instruction/value-flow search beyond the conventional `0x6b8` displacement pattern and beyond the binding module only if required to explain the shipped API. Prioritize concrete registration/caller evidence over another string inventory. `Session.name` actual linkage remains unknown until such an edge is found or separately authorized execution observes it.

## Runtime-only and scope boundaries

Actual paint rate, latency, queue saturation, thread contention, selected backend/version and cleanup failures were not measured. Personal profiles, credentials, private service behavior, launch selection, anti-cheat and integrity mechanisms were outside this pass. Any future runtime investigation requires a separately specified objective and authorization; none was performed here.

## Completion state

Nine requested reports are present. Binding and Ultralight evidence/snapshots are retained; targets were closed and helper exited. [Validation](validation.json) checks report links, evidence JSON and target digests. These deliverables complete this research pass while explicitly preserving the unresolved questions above.
