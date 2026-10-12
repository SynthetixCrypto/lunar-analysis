# Remaining rendering and JavaScript contracts

**Result:** native JS transport and promise ownership advanced; alpha/color-space and alternate JNI linkage remain open. All results are static and version-bound. Evidence aliases resolve in the [index](evidence-index.md).

## Pixel format and alpha

**Verified / high:** custom CPU storage uses four bytes per pixel, a configured byte-row alignment and per-dirty-rectangle uploads. Java's inspected consumer uploads BGRA; reverse image updates validate tight `width * height * 4` BGRA8. Callback stride must come from the swapchain record, not the separate 16-byte-rounded surface field. See [Session 7 rendering](../session7-astra/webosr-rendering.md).

**New verified fact:** binding `DeferredBitmap` virtual `ConvertToPremultipliedAlpha` reaches `0x18004cdd0`, which throws an explicit not-implemented exception (`bitmap-premultiply`, `bitmap-vtable-correct`). This is a method-body finding, not proof that the method is called during normal updates. Its existence does not establish that the supplied bytes are already premultiplied or that the output uses straight alpha.

**Unknown:** end-to-end alpha convention, blend factors at every selected consumer, color-space tagging/transfer functions, sRGB versus linear compositing and selected rasterizer/backend. BGRA channel order alone answers none of those. A future image API needs an explicit `channel order + alpha mode + color space + row stride` contract; this is unnecessary for the MVP's Minecraft-native text/shape HUD.

## Native JS argument transport

Binding callback dispatcher `0x180047920` walks argument values through `0x1800475f0`. Fresh `js-argument-text` shows `JSValueToStringCopy`, length/UTF-16 character access, an owned native text copy and `JSStringRelease`.

**Verified / high:** this layer converts arguments to strings. It is not an observed generic native object/JSON decoder. Any JSON encoding/decoding required by a Java API must occur elsewhere. JavaScript coercion details, conversion-exception handling and every Java codec branch are not thereby resolved. A literal text result such as `"null"` must not be confused with the nullable completion path below.

## Promise creation, capture and completion

| Stage | Verified observation | Evidence |
|---|---|---|
| Creation | Dispatcher calls `JSObjectMakeDeferredPromise`, receiving resolve/reject outputs, then protects promise and both callbacks | `promise-create-body`, `promise-create-assembly`, `0x180047920` |
| Ownership | Refcounted PromiseImpl is created; completion obtains a strong reference from an existing weak control block using an atomic nonzero-count increment loop | `promise-value-resolve`, `0x180048570`; `promise-dtor`, `0x180043930` |
| Dispatch | Completion closure holds strong ownership and optional copied/moved UTF-16 text; dispatches actor 0 | `promise-value-resolve`, `promise-resolve-native` |
| String/null completion | Worker uses `JSValueMakeString` for present text and `JSValueMakeNull` for absent optional text, then invokes resolver | `promise-json-complete`, `promise-string-assembly`, `0x1800436b0` |
| No-value completion | Separate overload uses `JSValueMakeUndefined` | `promise-empty-worker`, `0x1800464b0` |
| Success cleanup | On the inspected valid-context branch, unprotect retained promise/resolve/reject values and zero their stored fields | Both worker completion bodies |

The alias `promise-json-complete` was an exploratory label; the body constructs a **JS string**, not a parsed JSON value. Also, the creation decompiler misleadingly displays zero arguments for some protection calls. Assembly at `0x180047c2e–0x180047c85` shows resolve/reject output pointers and subsequent loads of those outputs. Do not infer `JSValueProtect(null)` from the pseudocode.

**Confidence: high** for observed ownership operations and value kinds. The completion worker checks browser/view/context availability before doing JS work. **Unknown:** duplicate completion behavior, cleanup when the context is no longer usable, abandoned/rejected promise teardown in every route, cancellation, retry/timeouts and JS exception delivery. The inspected resolver call supplies no JS exception-out destination, but this is not a universal error-handling specification. G-32/G-33 remain partial, rather than closed by queue analysis.

## Session.name and other JNI mismatches

Fresh Session/Promise Java disassembly was collected; the earlier independent reconciliation remains **56 Java native declarations, 58 JNI exports, 55 shared symbols, one Java-only and three DLL-only**. `Session.name()` does not match the exported `Session_getName`; the latter contains a working string-returning body. DLL-only `Browser_swapBuffers` and `WebEngine_setTimers` also contain real implementations.

Session 7's bounded four-module registration search did not prove alternate registration. This session did not broaden it to every computed call in every dependency. Thus `Session.name()` runtime linkage remains **Unresolved**, while compatibility/deadness of the extra exports remains **Partially resolved**. Neither absence of a direct symbol match nor lack of a discovered caller proves dead code. Evidence: [prior JNI report](../session7-astra/native-jni-mapping.md), S8 `java-22`.

## Research stop decision

These unknowns matter to reproducing a native browser integration, not to creating an original Fabric-based client. Continue them only for a specific later feature or independently authorized diagnostic question. The [MVP plan](mvp-development-plan.md) has no dependency on Lunar's JavaScript, JNI or native renderer contracts.
