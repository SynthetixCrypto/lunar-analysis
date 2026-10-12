# Session 7 — Native threading, ownership and lifecycle

## Thread roles recovered statically

| Role | Verified code | Limits |
|---|---|---|
| Engine construction caller | `EngineImpl` constructor `0x180038ac0` registers actor 1 | Not a runtime OS-thread-name observation |
| Native renderer worker | `_beginthreadex` entry `0x1800383f0` → `0x180039990` → init `0x18003b020` / loop `0x18003b490`; registers actor 0 | Number of internal Ultralight rasterizer workers not determined |
| Java texture consumer | `getTexture` → supplier `0x18004bd60` → synchronous JNI create/resize/upload | Real Minecraft render-thread identity depends on caller |
| Other actor users | Actor registry and TLS pump support additional IDs; actor 3 has per-thread lookup | No complete actor-2/3 producer inventory |

Evidence: [constructor](evidence/engine-impl-ctor.json), [thread entry](evidence/engine-worker.json), [worker init](evidence/worker-init.json), [worker run](evidence/worker-run.json), [actor registry](evidence/actor-register.json), [lookup](evidence/actor-lookup.json).

**Verified / high confidence:** constructor waits for engine-ready byte `+0x18`, pumping caller actors and yielding while the worker initializes. Worker initialization installs platform adapters, calls `Renderer::Create`, then publishes ready. Complete failure delivery if worker setup throws or cannot establish a usable renderer remains **Unknown**.

## What `invokeIteration()` actually does

Java records the construction thread in `WebEngine.owner`. `invokeIteration()` drains FunctionBus's Java main-actor queue only when called by that owner, then calls native `invokeIteration0()` regardless of the equality result. The native handle/vtable chain resolves to `0x180036320`, which iterates actor IDs registered in the current thread's TLS and drains them via `0x180035ec0`.

Evidence: [fresh WebEngine bytecode](evidence/com.moonsworth.webosr.wrappers.WebEngine.javap.txt), [JNI stub](evidence/iterate.json), [native iteration target](evidence/engine-iteration.json), [TLS pump](evidence/actor-pump.json), [queue consumer](evidence/actor-consume.json).

**Corrected interpretation:** this is caller-side queue service, not a direct “paint one frame now” request. The owner conditional is not a Java rejection of all foreign-thread native calls. Conversely, absence of that rejection is not proof that arbitrary-thread iteration or every browser API is safe.

## Actor dispatch and synchronization

At `0x180036380`, dispatch looks up the actor queue and compares its registered `_Thrd_id` with the current thread. If equal, the callable executes inline. Otherwise it is put into a ring with 64-byte callable slots and indices modulo `0x1001`; a full ring yields until space is available. The empty-slot convention implies **4096 usable entries** for this particular ring path. Queue-consumption code also has a separate linked/batched route.

Actor registration `0x180035b40` records the actor in TLS and sets the queue's thread ID at `+0x40070`. Lookup `0x180035aa0` uses the fixed actor area at `DAT_180084460 + id*0x40078`, with a separate map for actor 3.

Evidence: [dispatch](evidence/actor-dispatch.json), [consume](evidence/actor-consume.json), [register](evidence/actor-register.json), [lookup](evidence/actor-lookup.json). Dispatch Evidence ID: `ev_7716d57acdb11661f11c0a53fbf41524f60d571747885265c5c6d1c62ab202a2`; the raw dossiers preserve instruction and reference details.

**Verified:** the browser registry in the worker uses atomic exchange/wait/notify around engine `+0x15c`. Registry entries use weak-to-strong reference promotion; expired entries are erased and live browser ownership is held while work is selected. Shared ownership increments/decrements use atomic operations in the inspected paths.

**Unknown:** formal memory-order guarantees of every queue, all producer counts, global multi-engine interaction, race freedom, practical saturation and deadlock frequency. There is no universal “everything is mutex protected” or “everything is lock free” conclusion. Inline dispatch also means reentrancy is possible as a structural consequence, not as an observed bug.

## Scheduling and worker rendering

The worker pumps actors, updates registered source work, compares high-resolution elapsed times, updates the renderer, locks/selects browser registry entries, submits view work and publishes their suppliers. Timer setter `0x18003afd0` multiplies input seconds by `1e9` into engine intervals:

- `+0xd8`: renderer update interval.
- `+0xd0`: browser render eligibility interval.
- `+0xe0`: idle interval.

`0x18003af30` uses `1.0/fps`, updates Ultralight configuration and the render interval. ThreadConfig's Java defaults are zero. Mapping reads `GetDoubleField`; the native constructor/setter determines units, which Java declarations alone did not prove.

Evidence: [timer conversion](evidence/engine-timers.json), [Java-to-native timer extraction](evidence/threadconfig.json), [FPS setter](evidence/fps-body.json), [worker](evidence/worker-run.json), [ThreadConfig bytecode](evidence/com.moonsworth.webosr.config.ThreadConfig.javap.txt).

Ultralight renderer slot `+0x38` updates timers/run-loop; `+0x50` submits a batch of adjusted view pointers to Painter. The per-view `+0x40` operation is followed to a dependency helper, but its exact source name is not asserted. See [dependency verification](ghidra-verification.md).

**Inferred:** actual frame availability depends on timer thresholds, available surface buffers and caller consumption. **Unknown:** measured FPS, paint frequency, starvation or time spent in callbacks. The earlier Java ≥5 ms opportunity gate is not a scheduled 200 Hz guarantee and does not define native rendering frequency.

## Browser initialization and destruction

BrowserImpl constructor `0x180041fe0` sets up native listener interfaces and dispatches actor-0 initialization. The closure reaches `0x180042c00`, which creates the view and establishes the texture supplier. `0x180047760` waits for supplier availability while pumping/yielding. Browser wrapper constructor `0x18001ddc0` stores shared native browser ownership and retains a Java wrapper reference.

BrowserImpl destructor `0x180042860` moves its view reference into an actor-0 closure and waits while servicing caller actors. Closure `0x180046090` checks the view reference-count-like method, logs `Leaked Handle (~BrowserImpl)` if the returned value exceeds one, invokes view `+0xe8`, releases via view `+8`, and sets completion. The dependency's `+0xe8` implementation is followed to another indirect call, so its precise higher-level “close/unregister” semantics are **Unknown**.

Evidence: [constructor](evidence/browser-ctor-correct.json), [worker create](evidence/browser-create-worker.json), [wrapper constructor](evidence/browser-wrapper-ctor.json), [destructor](evidence/browser-dtor-body.json), [closure](evidence/browser-destroy-task.json), [dependency view slot](evidence/view-close.json).

The diagnostic is evidence of a check, not proof of a live leaked browser. Complete callback unregistration and exceptional destruction are not established by this path alone.

## Engine shutdown and join

**Verified normal-path sequence, high confidence:**

1. EngineImpl destructor `0x1800396e0` dispatches actor-0 closure at `0x18003a160`.
2. The closure sets engine stop byte `+0xe8` and acknowledges via a completion flag.
3. Caller pumps its actors/yields until acknowledgment.
4. If a worker thread ID exists, join helper `0x18003aec0` is invoked. It rejects zero ID/self-join and checks `_Thrd_join` results.
5. Shared handler/host ownership and renderer/platform resources are released on the inspected continuation. A still-joinable thread at the later guard leads to `terminate` in the recovered body.

Evidence: [engine destructor](evidence/engine-dtor-body.json), [shutdown closure](evidence/shutdown-task.json), [join](evidence/thread-join.json). Destructor Evidence ID: `ev_ee6eef617010f429934f1e5a655827a523a578df29338b83d76ac4a1177c9bc9`; stop closure: `ev_dcabe5d409d0d576112b606c466ccd6c80682463bfea796796f4a2d38c169476`.

This verifies an explicit worker join; it does not prove all queues are globally empty, all callbacks unregistered, every GPU texture deleted, or every failure branch nonblocking. Calls from the worker itself require separate reasoning because the join rejects self-join.

## Ownership ledger

| Resource | Established owner/lifetime | Remaining uncertainty |
|---|---|---|
| Engine wrapper handle | Java `long handle` addresses native wrapper; wrapper holds shared EngineImpl | All invalid/stale-handle checks and failed-construction unwind |
| Browser wrapper | Holds shared BrowserImpl and retained Java object | Complete callback-detach and exceptional teardown |
| CPU surface buffers | Three owned native records; destructor destroys each | Race-free publication and all failed allocation paths |
| Java upload ByteBuffer | Direct view over native record; callback-local JNI object reference cleaned | Consumer must not assume retaining Java object pins backing memory |
| Reverse update input | Copied immediately to native owned vector | Raw native object lifetime across queued work |
| Java texture handler | Global reference wrapper retained; global deleter helper present | All wrapper paths and detach/Environment lifecycle |
| Java/GPU texture | Logical ID cached by supplier, Java handler maintains texture map | Complete native or Java delete chain at browser close |
| Renderer worker | Native thread created by engine, explicitly stopped/joined | Failure before ready acknowledgment and worker-side exceptions |

CPU buffer release evidence: [surface destructor](evidence/swapchain-dtor.json), [pixel record release](evidence/pixel-buffer-release.json). JNI reference and attachment details: [JNI report](native-jni-mapping.md).

## Fresh Java lifecycle corroboration

Fresh disassemblies/hashes reproduce the higher-level order: delete registered image sources, close Browser, then close engine. The selected manager's shutdown method has no catch/finally covering those steps. `NativeHandle.close()` invokes `destroy()` then clears `handle`; a thrown failure before the clear leaves that assignment unexecuted.

Evidence: [manager](evidence/L._81676d._21aca6._21aca6.javap.txt), [image-source owner](evidence/L._81676d._21aca6._13ea87._cfe983.javap.txt), [NativeHandle](evidence/com.moonsworth.webosr.NativeHandle.javap.txt), [fresh lifecycle hashes](evidence/lifecycle-fresh-hashes.json).

**Inferred:** escaping cleanup failures can interrupt this Java sequence. Native callback exceptions on the inspected upload-check path are cleared, so one must not equate every Java callback throw with an escaping shutdown failure. No failing workload was run.
