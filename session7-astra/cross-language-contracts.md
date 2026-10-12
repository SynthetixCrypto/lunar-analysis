# Session 7 — Cross-language contracts and independent design implications

These contracts are derived from the exact artifact versions identified in [onboarding](research-onboarding.md). “Verified” describes static behavior; the design choices at the end are recommendations for a new implementation, not claims about Lunar internals.

## Java → native ownership and scheduling

| Boundary | Verified contract | Confidence / unresolved edge |
|---|---|---|
| `WebOSR.createEngine` | Creates native configuration/callback wrappers and EngineImpl, then exposes a Java handle | High for normal construction chain; full failure unwind unknown |
| `NativeHandle` | Stores a private `long`; `close()` skips zero, invokes destroy, then sets zero | High; no universal concurrent-close guarantee |
| `WebEngine.invokeIteration` | Java owner condition controls FunctionBus queue consumption; native iteration always follows | High; foreign-thread safety not established |
| Native iteration | Drains actors registered to current thread's TLS | High; not direct render submission |
| `Browser.getTexture` | May synchronously create/resize/upload a texture before returning the logical ID | High for inspected supplier chain; runtime caller identity unknown |
| `TexturedImageSource.update` | Direct address and positive capacity; immediate native copy followed by actor-0 validation/update | High; queued object's own lifetime remains open |

Evidence: [create](evidence/create-engine.json), [handle bytecode](evidence/com.moonsworth.webosr.NativeHandle.javap.txt), [iteration bytecode](evidence/com.moonsworth.webosr.wrappers.WebEngine.javap.txt), [actor pump](evidence/actor-pump.json), [texture consumer](evidence/swapchain-get-texture.json), [image update JNI](evidence/image-update-jni.json), [copy](evidence/image-update-copy.json).

## Native → Java texture contract

The Java callback interface has these source-level interpretations, established by native call arguments plus Java consumers:

```text
createTexture(width, height, byteStride) -> logicalTextureId
resizeTexture(id, width, height, byteStride)
uploadTexture(id, sourceBuffer, x, y, width, height, byteStride)
readTexture(id, destinationBuffer, intArg1, intArg2, intArg3)
deleteTexture(id)
```

The interface/descriptors are verified. Native create/resize/upload callers were followed in detail. Read/delete method identity does not imply their complete normal caller chains were recovered; the read callback's three integer meanings are deliberately left unnamed here.

### Upload layout

- Four bytes per pixel; Java interprets incoming pixels as BGRA.
- `x/y/width/height` are pixels; stride is **bytes**, and need not equal `width*4`.
- The ByteBuffer spans the native full-frame backing store; a region is described by separate arguments.
- Source row start is `base + y*stride + x*4`.
- The synchronous Java call does not transfer ownership of native memory.
- The inspected modern conversion path produces compact RGBA staging; it is a channel permutation, not demonstrated alpha/color-space conversion.

Evidence: [native callsite](evidence/swapchain-upload-assembly.json), [JNI assembly](evidence/upload-call-assembly.json), [Java handler](evidence/L._81676d._21aca6._590f69._cfe983._cfe983.javap.txt), [Java bridge](evidence/ML._d4ca6c._1e73d7._590f69._88f3cf._2f4182._cfe983.javap.txt).

**Inferred usage requirement:** finish reading or make an owned copy before returning from the callback. A retained direct ByteBuffer can still reference storage that native code has recycled or freed.

### Reverse layout

Native worker accepts a **tightly packed** `width*height*4` BGRA8 array for the selected image-source update path. Java's direct-buffer **capacity** is passed to native copying, so merely setting a smaller `limit()` does not narrow the input in this implementation. Non-direct buffers/invalid addresses and nonpositive capacities do not reach the native copy on the inspected JNI branch.

Fresh source-owner bytecode corroborates the separate framebuffer→image-source path; native copy/validation now closes its previous borrow-versus-copy gap. [Owner bytecode](evidence/L._81676d._21aca6._13ea87._cfe983.javap.txt), [worker validation](evidence/image-upload-work.json).

**Unknown:** alpha premultiplication and all image-source resize/unbind/close races. A successful byte copy is not an ownership lease on the destination object.

## Errors and completion

| Boundary | Established behavior | Do not infer |
|---|---|---|
| Texture JNI callback | Call followed by exception check/describe/clear/log | Universal propagation to Java or all native exception translation |
| Reverse size mismatch | Worker logs expected vs received BGRA8 bytes; does not install mismatching vector on that branch | A Java exception/result or completion acknowledgment |
| Actor dispatch | Inline if already on registered actor thread; otherwise queued with yield on full ring | Guaranteed asynchronous execution or unlimited queue capacity |
| Browser construction/destruction | Wait loops pump caller actors and yield | A timeout, cancellation protocol or reentrancy barrier |
| Engine destruction | Stop request, acknowledgment and worker join | Total cleanup of every external/GPU resource |
| Java close sequence | Destroy followed by handle clear; manager closes sources → browser → engine | Exception-safe completion of all subsequent steps |

Evidence: [exception checker](evidence/jni-invoke-check.json), [size mismatch](evidence/image-upload-work.json), [dispatch](evidence/actor-dispatch.json), [browser destructor](evidence/browser-dtor-body.json), [engine destructor](evidence/engine-dtor-body.json), [NativeHandle](evidence/com.moonsworth.webosr.NativeHandle.javap.txt).

The Java FunctionBus queue and native actor queues are separate mechanisms. This session's native queue findings do not prove native JS promise resolution, codec/null semantics, timeout or retry behavior. G-32 and the promise-specific portion of G-33 remain open.

## Original independent architecture — recommended choices

The following are **design proposals**, not recovered proprietary implementation:

1. **Explicit render-thread ownership.** Put browser work on a designated worker and GPU commands on the application's graphics owner. Make the ownership rule enforceable at each public entry point.
2. **Owned frame messages.** Represent a frame as dimensions, byte stride, pixel format, alpha convention, dirty regions and a memory lease. Publish immutable completed frames and release the lease only after upload completes. A latest-frame policy is optional and should be specified rather than accidental.
3. **Separate CPU and GPU lifetime.** Give CPU buffers and graphics textures distinct owners and explicit release operations. A browser close should acknowledge both worker teardown and graphics resource release.
4. **Explicit copy/borrow APIs.** A borrowed callback buffer must have a documented scope; an asynchronous update accepts owned bytes or copies them. Specify capacity versus remaining/slice semantics at the Java boundary.
5. **Bounded queues with a failure policy.** Define capacity, producer model, memory ordering, saturation behavior and cancellation. Use structured shutdown work with acknowledgments; specify whether dispatch can execute inline and permit reentrancy.
6. **Deterministic shutdown.** Stop new work, retire pending source updates, release views/surfaces and graphics resources on their owners, join workers, then release callback/global references. Aggregate cleanup errors so one failure does not silently skip all later steps.
7. **Typed JNI boundary.** Generate/check descriptors, wrap local/global references, document attachment ownership, and convert failures into explicit Java results/exceptions. Treat callback failure and fatal worker failure separately.
8. **Pixel-format tests in the independent client.** Use synthetic asymmetric color/alpha patterns, padded rows, disjoint dirty regions, resizing, skipped frames and close-during-pending-work to verify the new contracts. No proprietary target execution is necessary to test one's own design.

These choices use generic lessons from the observed boundaries. Exact proprietary layout, symbol names, queue dimensions and algorithms need not be reproduced to build an independent client.
