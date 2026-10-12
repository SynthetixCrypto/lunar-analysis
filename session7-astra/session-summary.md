# Session 7 — Native WebOSR investigation summary

Date: 2026-10-12. **Result:** meaningful native Ghidra analysis is now complete for this pass, with explicit residual gaps. The principal model is a native renderer worker producing three-buffer CPU surfaces, with Java `getTexture()` synchronously pulling completed data into graphics textures.

## What was actually done

- Reviewed the latest corrections and Session 6's sixteen native questions; concentrated on G-28–G-33 instead of repeating resolved feature inventories.
- Recovered Ghidra access using an existing installation and a workspace-scoped REA process with corrected environment. No installation or global configuration change was needed.
- Analyzed the five binding exports, engine/helper/vtable chain, native actor transport, worker setup/run/shutdown, browser construction/destruction, swapchain allocation/stride/dirty regions, JNI callback/reference/exception helpers and reverse image-source copying.
- Opened `Ultralight.dll` separately to corroborate RendererImpl vtable dispatch and actual update/Painter-submission work, then reopened the binding for final targeted checks.
- Independently parsed PE exports and WebOSR native class declarations, reproduced the **55 shared / 1 Java-only / 3 DLL-only** reconciliation, freshly disassembled selected Java contracts/lifecycle bodies and verified matching class hashes.
- Enumerated JNI table offsets from the installed JDK header and performed a bounded registration search with disassembly of raw-byte candidates.
- Saved complete available Evidence records, raw MCP responses, readable projections, bundles, snapshots, request receipts and reproduction scripts. Closed both native analysis targets and terminated the helper normally.

## Major verified findings

| Finding | Evidence and location | Confidence / limit |
|---|---|---|
| `invokeIteration0` pumps caller actors | Binding `0x18001c3b0` → wrapper → EngineImpl vtable `+8` → `0x180036320`; [evidence](evidence/engine-iteration.json) | High static confidence; not a direct render call |
| Native renderer worker exists | Constructor `0x180038ac0`, `_beginthreadex`, worker init/run; [evidence](evidence/engine-impl-ctor.json) | High; internal rasterizer worker count/runtime IDs unknown |
| Dependency update/render work is real | Ultralight `0x1800532c0` cycles timer/run-loop; `0x1800535d0` submits views to Painter; [update](evidence/renderer-update.json) / [render](evidence/renderer-render.json) | High for bodies; exact per-view helper name unresolved |
| Custom surface has three CPU buffers | Binding ctor `0x18004b130`, three records initialized by `0x18004bc00`; [evidence](evidence/pixel-buffer-init.json) | High; not three GPU swapchain images |
| Java pull causes texture callbacks | `getTexture` → supplier `0x18004bd60`; create/resize/dirty upload and recycle; [evidence](evidence/swapchain-get-texture.json) | High for normal chain; actual caller thread name unobserved |
| Dirty history is native-selected | `0x18004b740`: clip/dedup/merge current and two prior rectangles; [evidence](evidence/dirty-regions.json) | High; all-interleaving correctness unproved |
| JNI upload borrows native storage | `0x18002d910`: direct view, CallVoidMethodA, local-ref delete; [evidence](evidence/upload-call-assembly.json) | High; synchronous-use requirement derived from recycling |
| Reverse update copies input | `0x18004a530`: copy before actor-0 dispatch; worker exact BGRA8 size check; [copy](evidence/image-update-copy.json) / [check](evidence/image-upload-work.json) | High; destination object's queued lifetime separate |
| Explicit shutdown join | `0x1800396e0` → stop/ack → `0x18003aec0`; [evidence](evidence/engine-dtor-body.json) | High normal-path confidence; total cleanup not proven |
| JNI mismatch independently reproduced | 56 declarations, 58 JNI exports, intersection 55; [evidence](evidence/jni-reconciliation-fresh.json) | High; dynamic registration still unknown |

## Assumptions corrected or narrowed

1. Ghidra was usable in this environment once the child process pointed to its actual directory. Prior “provider unavailable” findings describe their earlier observations, not a continuing block.
2. Native iteration is an actor-queue pump; assigning it renderer Update/Render semantics from the forwarding stub was unjustified.
3. Browser texture delivery combines worker-side generation with caller-side upload callbacks. “Push callback” versus “Java pull” is not an exclusive choice here.
4. Swapchain is a three-record CPU allocation with logical texture-ID upload, not evidence of native GPU triple buffering.
5. Row stride is configuration-aligned byte width. A separate 16-byte-rounded cached field is not sufficient to define the callback stride.
6. A direct JNI ByteBuffer does not imply ownership transfer. Browser upload borrows backing storage; reverse image update copies it before enqueueing.
7. DLL-only exports have meaningful implementations. Their missing Java declarations do not establish deadness or legacy registration.
8. The inspected callback exception checker clears pending Java exceptions. Universal propagation, recovery or safe cleanup cannot be assumed.
9. The `attachShared` cleanup invoke slot is a no-op; an automatically inferred detach operation would be incorrect. Overall attachment lifetime remains open.

Exploratory mislabels and provider prototype/flow limitations are recorded in [Ghidra verification](ghidra-verification.md).

## What remains unresolved

The most important gaps are the **complete GPU texture-delete chain**, **native source-object lifetime across queued updates**, **queue memory-order correctness**, **failed initialization/unwind**, **full JNI Environment/detach lifecycle**, **alpha/color-space semantics**, **Session.name dynamic linkage**, and **native JS codec/promise ownership**. Runtime FPS, thread contention and real failure frequency were not observed.

The surface destructor demonstrably frees CPU buffers and releases handler ownership, but it does not by itself prove deletion of the cached Java graphics texture. No leak is claimed. The engine join proves worker shutdown sequencing, not universal callback/resource retirement.

## Deliverables and next use

All nine requested reports:

1. [Research onboarding](research-onboarding.md)
2. [Ghidra verification](ghidra-verification.md)
3. [Native/JNI mapping](native-jni-mapping.md)
4. [WebOSR rendering](webosr-rendering.md)
5. [Native threading/lifecycle](native-threading-lifecycle.md)
6. [Cross-language contracts](cross-language-contracts.md)
7. [Evidence index](evidence-index.md)
8. [Remaining gaps and all 16 acceptance answers](remaining-gaps.md)
9. This summary

The contracts support an original architecture with explicit worker/graphics ownership, frame memory leases, format/stride metadata, bounded queue policy and acknowledged shutdown. These are design recommendations, not a reconstruction of proprietary implementation code.

Next static priorities: trace texture destruction and queued source lifetime, then initialization/JNI ownership failure paths, renderer dependency tails and JS/promise contracts. [Remaining gaps](remaining-gaps.md) supplies exact seeds and evidence requirements.

The retained set contains **155 unique REA Evidence IDs**, with 154 inline envelopes and one additional record recovered through the exported Ultralight bundle. Provider errors and unsuccessful instruction-boundary guesses are retained and labeled instead of counted as positive findings.

Prior research and installed artifacts were preserved; all new workspace artifacts remain uncommitted. No target execution, private service access, personal-state inspection, installation, commit or push occurred. [Validation](validation.json) records final file/link, selected-class and binary-hash checks.
