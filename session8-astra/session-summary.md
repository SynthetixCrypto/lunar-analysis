# Session 8 — final native investigation and development readiness

Date: 2026-10-12. **Decision: begin the original Fabric MVP now.** The investigation materially narrowed native ownership/JS gaps and produced concrete implementation contracts. Some proprietary native questions remain open; none is a prerequisite for the proposed client-only HUD/settings MVP. No client implementation or runtime validation was performed in this research pass.

## Deliverables

| Area | Report |
|---|---|
| GPU ownership and deletion | [GPU resource lifecycle](gpu-resource-lifecycle.md) |
| Copied payload versus destination lifetime | [Queued update lifetime](queued-update-lifetime.md) |
| Actors, memory visibility and shutdown | [Queue synchronization](queue-synchronization.md) |
| Attachment, references and exceptions | [JNI lifecycle](jni-lifecycle.md) |
| Pixels, JS/promise transport and JNI mismatches | [Remaining native contracts](remaining-native-contracts.md) |
| All sixteen inherited questions | [Native question status](native-question-status.md) |
| Original subsystem contracts | [Independent client architecture](independent-client-architecture.md) |
| Build order and first tasks | [MVP development plan](mvp-development-plan.md) |
| Go/no-go and future test gates | [Development readiness](development-readiness.md) |
| Exact record identities and limitations | [Evidence index](evidence-index.md) |
| Public repository cleanup | [Repository audit](repository-audit.md) |

## What was actually investigated

Reviewed Session 7's reports, evidence ledger and specific native/Java records. Verified active REA using `binary_session`: its configured Ghidra location was stale. Reused the installed tools through a workspace-scoped MCP helper with a corrected environment. Opened the matching binding artifact with its retained analysis snapshot and collected targeted Ghidra decompilation, assembly, reference and vtable evidence. No global tool configuration or installed target was modified.

Traced image-source destruction from JNI handle ownership through the refcount vtable and actor-0 acknowledgment. Inspected actor/surface ring publication, engine stop/ready, JNI attachment/reference helpers, Java deletion bridges and JS argument/promise construction/completion. Freshly disassembled 25 selected Java classes from the client/modern bridge JARs without initialization. Consulted versioned official Fabric guidance and public metadata for the proposed stack.

Retained **69 current-call native Evidence envelopes**, exact class/disassembly hashes and an exported bundle containing **209 records including inherited evidence**. Raw records are local-only; the public index is sanitized. Native session closed successfully and helper exited normally.

## Newly verified findings

- **Source destructor barrier:** `0x180049400` dispatches actor-0 provider cleanup and waits for acknowledgment before releasing members. `0x1800499e0` identity-checks provider removal; `0x180049a41` atomically acknowledges. This adds a normal-shutdown safeguard beyond input-byte copying.
- **Queue instruction detail:** the actor ring publishes its producer/consumer indices with ordinary stores; the alternate batch route and shutdown acknowledgments contain memory `XCHG`. That is evidence about the Windows x64 implementation, not proof of arbitrary multi-producer safety.
- **Java graphics release mechanisms:** TextureHandler removes logical IDs and invokes a bridge release method. Shipped bridge implementations route to superclass close/release-ID and owner callbacks, with version/render-thread branches. The complete browser-close trigger for each supplier ID remains missing.
- **JNI allocation/ABI:** daemon attachment, allocated Environment storage and `JNIEnv*` field access are corroborated in assembly; global-reference deletion has a concrete JNI-slot path. Complete Environment destruction/detachment remains unproved.
- **JS transport:** argument values pass through string coercion and owned UTF-16 copies. Promise creation protects promise/resolve/reject values; queued completion acquires strong ownership. String/null and undefined completions are distinct; successful valid-context completion unprotects and clears retained values.
- **Premultiplication limit:** the inspected DeferredBitmap conversion method throws a not-implemented exception if called. Neither normal invocation nor the end-to-end alpha convention is established.

These facts are high-confidence within the cited bodies. Conditional serialized-lifetime and selected-Java-bridge interpretations remain inferences. See individual reports for exact address/record mappings and residual bounds.

## Corrections and unresolved questions

The Session 7 model of worker rendering, three CPU buffers, Java pull/upload and actor pumping remains supported. Destination lifetime is no longer wholly unexplained, but the destructor barrier does not make racing update/close safe. An absent GPU-delete call in the CPU destructor does not prove a GPU leak. A missing x64 fence does not prove missing source-language atomic ordering. Native stringification is not generic JSON decoding. Decompiler-lost promise out-parameters were corrected with assembly, rather than interpreting apparent null protection arguments literally.

All sixteen inherited questions are classified: **7 Resolved within bounds, 8 Partially resolved, 1 Unresolved, 0 Blocked**. Remaining questions include full browser-to-GPU deletion and failure unwind, concurrent source/queue shutdown, worker failure-before-ready, complete JNI detach/Environment ownership, alpha/color-space, promise abandonment/double completion/error behavior, and `Session.name()` alternate linkage. Real thread identities, frame cadence, contention and failure frequency remain unobserved.

## Development decision and first tasks

Use **Fabric Loader/API + Java 21 + Gradle/Loom + Mojang official mappings**, provisionally targeting **Minecraft 1.21.11**. This is a version-pinned initial target, not a latest-release claim. Verify and lock the exact dependency tuple through the official generator and build/launch checks before relying on it.

1. Bootstrap a new original implementation repository and validate title-screen startup.
2. Spike one HUD element, a screen-opening key and accurate physical click observation.
3. Implement stable IDs, module/resource lifecycle, typed event dispatch and validated settings.
4. Add revisioned persistence and a restart-persistent FPS vertical slice.
5. Add CPS, coordinates, remappable keystrokes, movable editor, settings and profiles.
6. Test the packaged mod in a clean instance before beginning launcher development.

The architecture specifies ownership, interfaces, failure handling, deterministic tests and acceptance criteria for each subsystem. Minecraft screens and rendering support the MVP; no native browser, custom JNI or proprietary service dependency is proposed. Native follow-up is non-blocking or optional; exact toolchain and adapter verification are the immediate development gates.

## Repository result and verification

Updated root README through Session 8 and added `.gitignore` for raw research/build/cache/secret/proprietary artifacts. The audit found **15 tracked extracted Minecraft classes**, **589 path-bearing files**, **1,108 code-evidence heuristic matches** and **12 oversized reachable history blobs**. Ignore rules leave existing tracked/history content intact. A precise local review/untracking manifest and authorized follow-up commands are documented; no untracking or history changes were made.

[Validation](validation.json) confirms all 25 selected class hashes, five prior installed-artifact identities, native-envelope bundle membership, valid local JSON, and preservation of all 1,945 prior tracked files; README is their only changed file. The separate documentation check validates local links/fragments and indexed Evidence IDs. The initial inline-code false-positive link was corrected in the scanner. All twelve reports are present; new raw data remains ignored. No commit, push, target execution, private-service request, credential access or protection bypass was performed.
