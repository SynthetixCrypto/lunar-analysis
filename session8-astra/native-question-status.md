# Sixteen inherited native questions — Session 8 disposition

Date: 2026-10-12. **7 Resolved within stated bounds, 8 Partially resolved, 1 Unresolved, 0 Blocked.** These classifications answer the inherited questions, not whole-program correctness. Ghidra's active-connection configuration issue was bypassed locally; none of these questions remains blocked by provider availability.

The baseline is [Session 7's exact sixteen-question checklist](../session7-astra/remaining-gaps.md#all-16-inherited-native-questions). All native addresses below are binding addresses unless explicitly qualified. [Evidence index](evidence-index.md) maps S8 record aliases to exact IDs; Session 7 aliases resolve through its [index](../session7-astra/evidence-index.md).

| # | Inherited question | Status | Supporting evidence and answer | Remaining boundary / implementation relevance |
|---|---|---|---|---|
| 1 | Handle helper `0x199c0` and `+0xe8` object | **Resolved** | S7 `engine-handle`, `engine-wrapper-ctor`: wrapper holds shared EngineImpl at `+0xe8/+0xf0` | Normal handle layout only; stale handles/failure edges remain outside this answer |
| 2 | Engine vtable `+8` action | **Resolved** | S7 `engine-iteration`: `0x18003aeb0` reaches TLS actor pump `0x180036320` | It is not direct render submission |
| 3 | Callback frame or Java pull? | **Resolved** | S7 worker and `swapchain-get-texture`: worker publishes CPU frames; Java pull triggers synchronous texture callbacks | Verified normal custom-surface path; other paths not implied |
| 4 | Distinct paint callback | **Partially resolved** | S7 worker/Painter path; S8 [GPU lifecycle](gpu-resource-lifecycle.md): upload is TextureHandler callback | Complete internal paint-callback/rasterizer inventory remains unknown |
| 5 | Bitmap/surface allocation and owner | **Resolved** | S7 `surface-create`, `pixel-buffer-init`, `swapchain-dtor`: custom factory owns three CPU records | Default Ultralight bitmap internals not included; these records are not GPU images |
| 6 | Surface versus engine/texture lifetime | **Partially resolved** | S7 browser/engine/surface destructors; S8 source destruction barrier and fresh Java release bridges | Full browser → logical-ID delete trigger and failure unwind unproved; original MVP does not use these resources |
| 7 | Format and stride | **Partially resolved** | S7 aligned four-byte/BGRA contract; S8 `bitmap-premultiply` throws if invoked | Alpha/color-space remain unknown; do not infer them from BGRA |
| 8 | Iteration thread and workers | **Resolved** | S7 actor registration/worker; S8 `worker-entry`, `engine-constructor-assembly` | Static roles resolved, not live OS thread identities or cadence |
| 9 | Native synchronization | **Partially resolved** | S8 `actor-send-assembly`, `actor-consume-assembly`, `swapchain-publish-asm`, acknowledgment `XCHG` | Producer cardinality, source-language memory order and all races unproved |
| 10 | Native affinity | **Partially resolved** | Inline-on-registered-thread dispatch; `getTexture` caller performs callbacks | No universal foreign-thread enforcement across all APIs |
| 11 | JNI TextureHandler mechanics | **Resolved** | S7 descriptor/jvalue/direct-buffer/local-ref evidence; S8 create/delete assembly | Normal inspected callback ABI only; lookup/allocation exceptions remain bounded |
| 12 | Create/resize/upload/delete lifecycle | **Partially resolved** | S7 supplier order; S8 handler vtable, delete callback, `java-10`, `cleanup-0/1` | Java deletion mechanism advanced; mandatory normal-shutdown trigger still missing |
| 13 | Dirty-region uploads | **Resolved** | S7 `dirty-regions`: clip/dedup/merge current plus historical damage and upload per region | Static custom path only; no runtime cadence or all-interleaving test |
| 14 | Engine destruction | **Partially resolved** | S7 stop/ack/join; S8 `shutdown-assembly`, constructor-ready and worker-entry checks | Failure-before-ready, concurrent admissions and full callback/GPU shutdown unproved |
| 15 | `Session.name()` alternate registration | **Unresolved** | Fresh Java declaration confirms mismatch; S7 bounded registration scan and real `getName` body | No dynamic/computed linkage edge proved; no runtime call performed |
| 16 | Extra `swapBuffers` / `setTimers` exports | **Partially resolved** | S7 independent export/declaration reconciliation and real native bodies | No proof of deadness, legacy-only use or every external caller |

## Cross-session corrections and additions

1. Preserve the Session 7 correction: native iteration pumps queues, while a worker performs rendering.
2. Source payload copying was verified earlier; **source destruction now has a separately verified worker acknowledgment**. This narrows the ownership gap without proving concurrent safety.
3. Java cleanup mechanisms exist beyond CPU-buffer destruction. An absent delete call in one native destructor is not evidence of a GPU leak.
4. Ordinary x64 stores do not establish absent acquire/release semantics; locked refcounts do not establish multi-producer queue safety.
5. The inspected JS argument bridge stringifies; optional completion distinguishes null/string from the separate undefined overload. This advances G-32 without claiming generic codec parity.
6. A `ConvertToPremultipliedAlpha` method that throws does not prove that conversion is needed or that input pixels are already premultiplied.
7. The root README's old “Ghidra not configured” conclusion is obsolete: meaningful native analysis succeeded in Sessions 7–8 via corrected local provider environments.

## G-28–G-33 and readiness

G-29 remains resolved for the selected helper/vtable seeds. G-28, G-30, G-32 and G-33 remain **partial**, with new queue/source/promise evidence; G-31's runtime linkage remains **unresolved**. None blocks the original Fabric MVP. The blocking development work is now verifying the selected toolchain/input/render adapters, then implementing and testing original code. See [readiness](development-readiness.md).
