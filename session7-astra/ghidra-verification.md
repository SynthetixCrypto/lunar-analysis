# Session 7 — Ghidra verification

## Provider recovery and actual analysis

**Verified:** native dossiers identify Ghidra **12.1.4**, x86-64 PE, default auto-analysis complete, ephemeral source-immutable import, and the expected artifact SHA-256. The workspace helper used the already installed REA **6.4.0**, Ghidra `C:\tools\ghidra_12.1.4_PUBLIC`, and Microsoft full JDK **21.0.10.7**. It changed the child process environment only. See [helper](rea-local.mjs), [initial requests](initial-requests.json), [binding opening evidence](evidence/binding-open.json), and the provider/profile metadata in [worker dossier](evidence/worker-run.json).

The original connected MCP server's stale Ghidra directory did not become valid merely because the installation existed elsewhere. Analysis proceeded through a persistent second MCP connection. There was no installation, global environment edit, binary patch, or launch of a target DLL/JAR.

## Seed verification

Binding image base: `0x180000000`. Independent PE parsing and Ghidra agree on these entry points:

| Export suffix (`Java_com_moonsworth_webosr_wrappers_`) | VA | RVA | File offset | Recovered behavior |
|---|---|---|---|---|
| `WebOSR_createEngine` | `0x180010a30` | `0x10a30` | `0xfe30` | Builds JNI/config wrappers, calls native engine factory and wraps ownership |
| `WebEngine_invokeIteration0` | `0x18001c3b0` | `0x1c3b0` | `0x1b7b0` | Reads engine handle and dispatches vtable `+8`, an actor pump |
| `WebEngine_setTimers` | `0x18001c400` | `0x1c400` | `0x1b800` | Reads timer configuration and dispatches timer setter |
| `Browser_swapBuffers` | `0x18001fc10` | `0x1fc10` | `0x1f010` | Obtains texture supplier and calls supplier `+0x10` |
| `Session_getName` | `0x180029690` | `0x29690` | `0x28a90` | Reads native session name and creates a Java UTF string |

Evidence: [PE tables](evidence/pe-identities.json), [createEngine](evidence/create-engine.json), [iteration](evidence/iterate.json), [timers](evidence/timers.json), [swap](evidence/swap.json), [session name](evidence/session-name.json).

## Indirect calls resolved with actual objects

**Verified:** binding helper `0x1800199c0` looks up/caches Java `handle:J`, then uses `GetLongField`. Engine wrapper constructor `0x180018be0` stores the native shared-pointer pair at `+0xe8/+0xf0`. The native factory constructs `EngineImpl`, whose primary vtable is at `0x180060d88`.

| Engine vtable offset | Target VA in binding | Static role |
|---|---|---|
| `+0x08` | `0x18003aeb0` → `0x180036320` | Drain actors registered in caller TLS |
| `+0x20` | `0x18003a900` | Create browser and enqueue worker registration |
| `+0x28` | `0x18003aa60` | Create image source |
| `+0x30` | `0x18003afd0` | Convert timer seconds to nanoseconds |
| `+0x38` | `0x18003af30` | FPS setter using reciprocal seconds |

Evidence: [handle](evidence/engine-handle.json), [wrapper](evidence/engine-wrapper-ctor.json), [factory](evidence/engine-factory.json), [constructor](evidence/engine-impl-ctor.json), [vtable bytes](evidence/engine-vtable-bytes.json), [iteration target](evidence/engine-iteration.json).

For rendering, `Ultralight.dll!Renderer::Create` at `0x180050190` leads to constructor `0x180051020`, which installs `RendererImpl` vtable `0x18006c7e8`. This independently ties the worker's renderer calls to dependency implementations:

| Renderer slot | Ultralight target | What is established |
|---|---|---|
| `+0x38` | `0x1800532c0` | Updates WebCore shared timer, cycles WTF run loop, enters JS locking context |
| `+0x40` | `0x180053550` | Forwards a per-view operation to `0x1800030b0`; exact source API name remains unresolved |
| `+0x50` | `0x1800535d0` | Accepts view array/count, adjusts view pointers and submits to Painter virtual `+0x20` |

Evidence: [factory](evidence/ultralight-create.json), [constructor](evidence/renderer-ctor.json), [vtable](evidence/renderer-vtable.json), [update](evidence/renderer-update.json), [per-view operation](evidence/renderer-select.json), [render submission](evidence/renderer-render.json). “Update” and “render submission” describe verified work; complete rasterizer internals remain outside the analyzed bodies.

## Corrections and decompiler limitations

The following exploratory evidence filenames are retained for traceability, but must not be used as semantic labels:

| Exploratory file | Actual bounded result / replacement |
|---|---|
| `engine-fps.json` (`0x18003aa60`) | Image-source creation; actual FPS setter is `fps-body.json` (`0x18003af30`) |
| `upload-callback.json` (`0x18002ce90`) | Resize method-ID lookup; upload callback body is `jni-upload.json` (`0x18002d910`) |
| `texture-update-body.json` (`0x18004ccb0`) | Clears a flag; actual image copy body is `image-update-copy.json` (`0x18004a530`) |
| `browser-ctor.json` (`0x180047920`) | JavaScript-facing property/function work, not BrowserImpl construction; use `browser-ctor-correct.json` (`0x180041fe0`) |
| `swapchain-resize.json` (`0x18004bd50`) | Dirty-rectangle accessor; resize body is `surface-resize-correct.json` (`0x18004b550`) |
| `jni-detach-task.json` (`0x180001cf0`) | Shared-attachment cleanup slot resolves to a no-op/guard stub, not an established detach call |
| `registration-candidate-1.json` | Incorrect instruction boundary; corrected instruction is `registration-candidate-1-correct.json` at `0x18002fd08` |

The image source uses virtual inheritance. Its texture-update interface is selected via `0x180061e68`; `0x18004a51c` is an adjustment thunk into `0x18004a530`. Selecting the neighboring vtable produces the wrong method.

Ghidra sometimes drops register/stack arguments at indirect calls. The upload assembly explicitly shows `R8=methodID`, `RDX=handler object`, `R9=jvalue[]` before `CallVoidMethodA`; the shorter pseudocode must not be read as a two-argument JNI call. See [upload assembly](evidence/upload-call-assembly.json) and [GetMethodID assembly](evidence/jni-upload-method-assembly.json).

Some dependency pseudocode marks `free` as non-returning; that is a provider flow-model limitation, not evidence that deallocation aborts execution. Reports use the observed pre-call work and leave affected tail/unwind behavior open. No unsupported claim of complete C++ exception unwinding, lock-freedom, race-freedom or all indirect callers is made.

## Preservation and closure

- [Binding initial evidence bundle](binding-evidence-bundle.json) and [initial snapshot](binding-analysis-snapshot.json), saved before switching DLLs.
- [Ultralight final bundle](ultralight-evidence-bundle.json) and [snapshot](ultralight-analysis-snapshot.json).
- [Binding final bundle](binding-final-evidence-bundle.json) and [final snapshot](binding-final-analysis-snapshot.json), after focused reopen.
- [Final close receipt](evidence/binding-final-close.json): 141 evidence records and 98 primitive snapshot entries. These are receipt counts, not 141 independently proven conclusions.

The helper then exited normally. [Evidence index](evidence-index.md) and [validation](validation.json) describe file/link checks and fresh target hash comparison.
